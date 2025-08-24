""" 
This module defines the abstract and concrete class used for deserializing
conversation building blocks (Comements, Evaluations and Backchecks) from 
ProjNet DrChecks XML reports.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from heapq import merge
from defusedxml import ElementTree as ET


_PROJECT_INFO_INDEX = 0
_COMMENTS_INDEX = 1

def get_root(path):
    """Returns 'ProjNet' element as root for Dr Checks XML report files. Other XML files return None."""
    try:
        root = ET.parse(path).getroot()
        if root.tag.lower() == 'projnet': # type: ignore
            return root
        else:
            return None
    except Exception as e:
        print(e)

def get_review_elements(root):
    """Returns a tuple of the element nodes for project info and all comments"""
    return (root[_PROJECT_INFO_INDEX], root[_COMMENTS_INDEX])

def _get_project_info_element(root):
    # This is a fallback method incase get_review fails
    try:
        return root[_PROJECT_INFO_INDEX]
    except Exception as e:
        print(e)

def _get_review_comments_element(root):
    # This is a fallback method incase get_review fails
    try:
        return root[_COMMENTS_INDEX]
    except Exception as e:
        print(e)

def parse_single_tag(tag, element):
    """Helper method to extract XML data for first child element node with tag of tag."""
    return element.find(tag).text if element.find(tag) is not None else None

def parse_date_node(tag, element):
    return datetime.strptime(element.find('createdOn').text, '%b %d %Y %I:%M %p').isoformat() if element.find('createdOn') is not None else None

def clean_text(text):
    """Method to strip new-line entities from XML string."""
    return text.replace('<br />', '\n')


class ProjectInfo():
    """Returns a list of all project identification data in a Dr Checks review."""

    def __init__(self, 
                 project_id,
                 control_number,
                 project_name,
                 review_id,
                 review_name):
        self.project_id = project_id
        self.control_number = control_number
        self.project_name = project_name
        self.review_id = review_id
        self.review_name = review_name

    @classmethod
    def from_tree(cls, element):
        project_id = parse_single_tag('ProjectID', element)
        control_number = parse_single_tag('ProjectControlNbr', element)
        project_name = parse_single_tag('ProjectName', element)
        review_id = parse_single_tag('ReviewID', element)
        review_name = parse_single_tag('ReviewName', element)
        return ProjectInfo(project_id=project_id,
                           control_number=control_number,
                           project_name=project_name,
                           review_id=review_id,
                           review_name=review_name)
   
    @property
    def all_data(self):
        return {
            'Project Name': self.project_name,
            'Project ID': self.project_id,
            'Control Number': self.control_number,
            'Review Name': self.review_name,
            'Review ID': self.review_id
        }


class ReviewComments():
    """Returns list of all Comment objects in a Dr Checks review."""

    def __init__(self,
                 comments=[]):
        self.comments = comments

    @classmethod
    def from_tree(cls, element):
        comments = []
        for comment in element.findall('comment'):
            comments.append(Comment.from_tree(comment))
        return ReviewComments(comments=comments)
    
    @property
    def count(self):
        return len(self.comments)

    @property
    def max_evaulations(self):
        temp_count = 0
        for comment in self.comments:
            if comment.evaluations_count > temp_count:
                temp_count = comment.evaluations_count 
        return temp_count

    @property
    def max_backchecks(self):
        temp_count = 0
        for comment in self.comments:
            if comment.backchecks_count > temp_count:
                temp_count = comment.backchecks_count 
        return temp_count    

    @property
    def max_responses(self):
        return (self.max_evaulations, 
                self.max_backchecks)

    @property
    def evaluations_count(self):
        temp_count = 0
        for comment in self.comments:
            temp_count += comment.evaluations_count
        return temp_count

    @property
    def backchecks_count(self):
        temp_count = 0
        for comment in self.comments:
            temp_count += comment.backchecks_count
        return temp_count
    
    @property
    def total_responses_count(self):
        return self.evaluations_count + self.backchecks_count


class Review():
    """Returns a Review object containing project info and review comments objects."""

    def __init__(self,
                 project_info: ProjectInfo,
                 review_comments: ReviewComments,
                 root=None):
        self.project_info = project_info
        self.review_comments = review_comments
        self.root = root

    @classmethod
    def from_file(cls, path):
        root = get_root(path) if not None else None
        if root:
            project_info = ProjectInfo.from_tree(root[_PROJECT_INFO_INDEX]) if not None else None
            review_comments = ReviewComments.from_tree(root[_COMMENTS_INDEX]) if not None else None
        return Review(project_info=project_info,
                      review_comments=review_comments,
                      root=root)


class Remark(ABC):
    """Parent class for Comment, Evaluation and Backcheck classes"""
    def __init__(self,
                 id_=None,
                 status=None,
                 text=None,
                 has_attachment=None,
                 author=None,
                 date_created=None,
                 remark_type='remark'):
        self.id = id_
        self.status = status
        self.text = text
        self.has_attachment = has_attachment
        self.author = author
        self.date_created = date_created
        self.remark_type = remark_type

    @property
    def attributes_list(self):
        return [attr for attr in self.__dict__]

    @abstractmethod
    def from_tree(self):
        pass
    
    @property
    @abstractmethod
    def dump(self) -> dict:
        pass

    def to_list(self, attrs):
        props = self.dump
        if isinstance(attrs, list):
            return [props[item] if item in props else '' for item in attrs]
        if isinstance(attrs, dict):
            for key in attrs.keys():
                return [props[attrs[key]] if attrs[key] in props else '' for key in attrs]
        else:
            return None
        
    @property
    def days_open(self):
        current_date = datetime.now()
        time_diff = current_date - datetime.fromisoformat(str(self.date_created))
        return time_diff.days

class Comment(Remark):
    """Returns a Comment object containing all the data from a Dr Checks 'comment' element; 
    including children 'evaulation' and 'backcheck' elements."""

    def __init__(self, 
                 id_=None, 
                 status=None, 
                 text=None, 
                 has_attachment=None, 
                 author=None, 
                 date_created=None, 
                 remark_type='comment',
                 spec=None,
                 sheet=None,
                 detail=None,
                 is_critical=None,
                 docref=None,
                 doctype=None,
                 discipline=None,
                 coordinating_discipline=None,
                 evaluations=[],
                 backchecks=[]):
        super().__init__(id_, status, text, has_attachment, author, date_created, remark_type)
        self.spec = spec
        self.sheet = sheet
        self.detail = detail
        self.is_critical = is_critical
        self.docref = docref
        self.doctype = doctype
        self.discipline = discipline
        self.coordinating_discipline = coordinating_discipline
        self.evaluations = evaluations
        self.backchecks = backchecks

    @classmethod
    def from_tree(cls, element):
        id_ = parse_single_tag('id', element)
        spec = parse_single_tag('spec', element)
        sheet = parse_single_tag('sheet', element)
        detail = parse_single_tag('detail', element)
        is_critical = parse_single_tag('critical', element)
        docref = parse_single_tag('DocRef', element)
        doctype = parse_single_tag('DocType', element)
        discipline = parse_single_tag('Discipline', element)
        coordinating_discipline = parse_single_tag('CoordinatingDiscipline', element)     
        status = parse_single_tag('status', element)
        text = clean_text(parse_single_tag('commentText', element))
        has_attachment = True if element.find('attachment') is not None else False
        author = parse_single_tag('createdBy', element)
        date_created = parse_date_node('createdOn', element)
        # date_created = datetime.strptime(element.find('createdOn').text, 
        #                                 '%b %d %Y %I:%M %p').isoformat() if \
        #                                     element.find('createdOn') is not None else None
        evaluations = [Evaluation.from_tree(eval) for eval in element.find('evaluations')] \
            if element.find('evaluations') is not None else []
        backchecks = [Backcheck.from_tree(bc) for bc in element.find('backchecks')] \
                    if element.find('backchecks') is not None else []
        return Comment(id_=id_,
                    spec=spec,
                    sheet=sheet,
                    detail=detail,
                    is_critical=is_critical,
                    docref=docref,
                    doctype=doctype,
                    discipline=discipline,
                    coordinating_discipline=coordinating_discipline,
                    status=status,
                    text=text,
                    has_attachment=has_attachment,
                    author=author,
                    date_created=date_created,
                    evaluations=evaluations,
                    backchecks=backchecks)

    @property
    def dump(self):
        return {
            'id': self.id,
            'status': self.status,
            'text': self.text,
            'has_attachment': self.status,
            'author': self.author,
            'date_created': str(self.date_created).replace('T', ' '),
            'remark_type': self.remark_type,
            'spec': self.spec,
            'sheet': self.sheet,
            'detail': self.detail,
            'is_critical': self.is_critical,
            'docref': self.docref,
            'doctype': self.doctype,
            'discipline': self.discipline,
            'coordinating_discipline': self.coordinating_discipline,
            'days_open': self.days_open,
            'evaluations': self.evaluations,
            'backchecks': self.backchecks
        }
    
    @property
    def evaluations_count(self):
        return len(self.evaluations)

    @property
    def backchecks_count(self):
        return len(self.backchecks)
    
    @property
    def response_count(self):
        return len(self.evaluations) + len(self.backchecks)
    
    @property
    def list_reponses(self):
        """Returns list of Responses in type order: first Evaluations then Backchecks."""
        return self.evaluations + self.backchecks

    @property
    def list_responses_chronological(self):
        """Returns list of Responses in chronological order, regardless of Evaluation or Backcheck type."""
        sort_key = lambda Remark: Remark.date_created
        return list(merge(self.evaluations, self.backchecks, key=sort_key))


class Evaluation(Remark):
    """Returns an Evaulation object containing information from a Dr Checks 'evaluation' element."""

    def __init__(self, 
                 id_=None, 
                 status=None, 
                 text=None, 
                 has_attachment=None, 
                 author=None, 
                 date_created=None, 
                 remark_type='evaluation',
                 parent_id=None,
                 impact_scope=None,
                 impact_cost=None,
                 impact_time=None):
        super().__init__(id_, status, text, has_attachment, author, date_created, remark_type)
        self.parent_id = parent_id
        self.impact_scope = impact_scope
        self.impact_cost = impact_cost
        self.impact_time = impact_time

    @classmethod
    def from_tree(cls, element):
        id_ = parse_single_tag('id', element)
        parent_id = parse_single_tag('comment', element)
        status = parse_single_tag('status', element)
        impact_scope = parse_single_tag('impactScope', element)
        impact_cost = parse_single_tag('impactCost', element)
        impact_time = parse_single_tag('impactTime', element)
        text = clean_text(parse_single_tag('evaluationText', element))
        has_attachment = True if element.find('attachment').text is not None else False
        author = parse_single_tag('createdBy', element)
        date_created = parse_date_node('createdOn', element)
        # date_created = datetime.strptime(element.find('createdOn').text, 
        #                                 '%b %d %Y %I:%M %p').isoformat() if \
        #                                     element.find('createdOn') is not None else None
        return Evaluation(id_=id_, 
                        parent_id=parent_id, 
                        status=status, 
                        impact_scope=impact_scope,
                        impact_cost=impact_cost,
                        impact_time=impact_time,
                        text=text,
                        has_attachment=has_attachment,
                        author=author,
                        date_created=date_created)

    @property
    def dump(self):
        return {
            'id': self.id,
            'status': self.status,
            'text': self.text,
            'has_attachment': self.status,
            'author': self.author,
            'date_created': str(self.date_created).replace('T', ' '),
            'remark_type': self.remark_type,
            'parent_id': self.parent_id,
            'impact_scope': self.impact_scope,
            'impact_cost': self.impact_cost,
            'impact_time': self.impact_time,
            'days_open': self.days_open
        }


class Backcheck(Remark):
    """Returns a Backcheck object containing information from a Dr Checks 'backcheck' element."""

    def __init__(self, 
                 id_=None, 
                 status=None, 
                 text=None, 
                 has_attachment=None, 
                 author=None, 
                 date_created=None, 
                 remark_type='backcheck',
                 parent_id=None,
                 evaluation_id=None):
        super().__init__(id_, status, text, has_attachment, author, date_created, remark_type)
        self.parent_id = parent_id
        self.evaulation_id = evaluation_id

    @classmethod
    def from_tree(cls, element):
        id_ = parse_single_tag('id', element)
        parent_id = parse_single_tag('comment', element)
        evaluation_id = parse_single_tag('evaluation', element)
        status = parse_single_tag('status', element)
        text = clean_text(parse_single_tag('backcheckText', element))
        has_attachment = True if element.find('attachment').text is not None else False
        author = parse_single_tag('createdBy', element)
        date_created = parse_date_node('createdOn', element)
        # date_created = datetime.strptime(element.find('createdOn').text, 
        #                                 '%b %d %Y %I:%M %p').isoformat() if \
        #                                     element.find('createdOn') is not None else None
        return Backcheck(id_=id_, 
                        parent_id=parent_id, 
                        status=status, 
                        evaluation_id=evaluation_id,
                        text=text,
                        has_attachment=has_attachment,
                        author=author,
                        date_created=date_created)
    
    @property
    def dump(self):
        return {
            'id': self.id,
            'status': self.status,
            'text': self.text,
            'has_attachment': self.status,
            'author': self.author,
            'date_created': str(self.date_created).replace('T', ' '),
            'remark_type': self.remark_type,
            'parent_id': self.parent_id,
            'evaluation_id': self.evaulation_id,
            'days_open': self.days_open
        }
    
