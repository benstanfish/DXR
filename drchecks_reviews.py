""" 
This module defines the abstract and concrete class used for deserializing
conversation building blocks (Comements, Evaluations and Backchecks) from 
ProjNet DrChecks XML reports.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from heapq import merge
from typing import (
    List,
    Dict,
    Tuple,
    Literal
)
from defusedxml import ElementTree as ET


_PROJECT_INFO_INDEX = 0
_COMMENTS_INDEX = 1
_COMMENT_COLUMNS = {
    'ID': 'id',
    'Status': 'status',
    'Discipline': 'discipline',
    'Author': 'author',
    'Email': 'email',
    'Date': 'date_created',
    'Comment': 'text',
    'Critical': 'is_critical',
    'Class': 'classification',
    'Att': 'has_attachment',
    'Days Open': 'days_open',
    'Highest Resp.': ''
}
_RESPONSE_EXPANSION_TYPES = Literal['chronological', 'type']
_RESPONSE_COLUMNS = {
    'Status': 'status',
    'Author': 'author',
    'Email': 'email',
    'Date': 'date_created',
    'Text': 'text',
    'Att': 'has_attachment'
}
_RESPONSE_VALUES = {
    'concur': 1,
    'for information only': 2,
    'non-concur': 3,
    'check and resolve': 4
}

#region Module level helper methods
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


def date_to_excel(iso_date):
    return datetime.fromisoformat(iso_date)


def clean_text(text):
    """Method to strip new-line entities from XML string."""
    return text.replace('<br />', '\n')

#endregion

#region Classes for reconstructing whole Dr Checks XML reviews

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
    def max_evaluations(self):
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
        return (self.max_evaluations, 
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

    @property
    def to_list(self, attrs=_COMMENT_COLUMNS):
        my_data = []
        for comment in self.comments:
            my_data.append(comment.to_list(attrs))
        return my_data

    @property
    def column_names(self, attrs=_COMMENT_COLUMNS):
        return [key for key in attrs.keys()]


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


def get_all_comments_and_responses(review_comments: ReviewComments, 
                                   expansion_type: _RESPONSE_EXPANSION_TYPES='chronological',
                                   comment_attrs=_COMMENT_COLUMNS,
                                   response_attrs=_RESPONSE_COLUMNS):
    """Returns the full List of comments and corresponding responses."""
    all_responses = []
    max_eval_count, max_bc_count = review_comments.max_responses

    for comment in review_comments.comments:
        temp = []
        temp += comment.to_list(comment_attrs)

        if expansion_type == 'chronological':
            resp_list = comment.list_responses_chronological
            resp_count = comment.total_response_count
            diff_eval = (max_eval_count + max_bc_count) - resp_count
            for resp in resp_list:
                temp += resp.to_list(response_attrs)
            for i in range(diff_eval):
                temp += ['']*len(response_attrs)
            all_responses.append(temp)
        else:
            for evaluation in comment.evaluations:
                temp += evaluation.to_list(response_attrs)
            diff_eval = max_eval_count - comment.evaluations_count
            for i in range(diff_eval):
                temp += ['']*len(response_attrs)
            for backcheck in comment.backchecks:
                temp += backcheck.to_list(response_attrs)
            diff_bc = max_bc_count - comment.backchecks_count
            for j in range(diff_bc):
                temp += ['']*len(response_attrs)
            all_responses.append(temp)
    return all_responses


def expand_response_headers(review_comments: ReviewComments, 
                            expansion_type: _RESPONSE_EXPANSION_TYPES ='chronological',
                            attrs=_RESPONSE_COLUMNS):
    max_evals, max_bcs = review_comments.max_responses
    header = []
    if expansion_type.lower() != 'chronological':
        for i in range(max_evals):
            for key in attrs.keys():
                header.append(f'Eval {i + 1} {key}')
        for j in range(max_bcs):
            for key in attrs.keys():
                header.append(f'BCheck {j + 1} {key}')
    else:
        for k in range(max_evals + max_bcs):
            for key in attrs.keys():
                header.append(f'Resp {k + 1} {key}')
    return (header, expansion_type)


def get_all_comments_and_response_headers(review_comments: ReviewComments,
                                          comment_attrs=_COMMENT_COLUMNS,
                                          expansion_type: _RESPONSE_EXPANSION_TYPES ='chronological',
                                          attrs=_RESPONSE_COLUMNS):
    header_names = []
    header_names += review_comments.column_names
    max_evals, max_bcs = review_comments.max_responses
    if expansion_type.lower() != 'chronological':
        for i in range(max_evals):
            for key in attrs.keys():
                header_names.append(f'Eval {i + 1} {key}')
        for j in range(max_bcs):
            for key in attrs.keys():
                header_names.append(f'BCheck {j + 1} {key}')
    else:
        for k in range(max_evals + max_bcs):
            for key in attrs.keys():
                header_names.append(f'Resp {k + 1} {key}')
    return header_names

#endregion

#region Classes for reconstructing Dr Checks XML elements

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

    def to_list(self, attrs=_COMMENT_COLUMNS):
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
        # TODO: Need to add the logic to determine of the comment is closed or not
        # and to calculate when it was closed.
        current_date = datetime.now()
        time_diff = current_date - datetime.fromisoformat(str(self.date_created))
        return time_diff.days
    
    @property
    def is_reopened(self):
        # TODO: Add a function to determine if the Comment was closed at one point,
        # determine by looking at Backchecks, but then reopened by a reviewer.
        # Make sure overarching test to see if the comment is closed.
        if str(self.status).lower() == 'closed':
            return False
        else:
            pass
        

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
        has_attachment = '〇' if parse_single_tag('attachment', element) is not None else None
        author = parse_single_tag('createdBy', element)
        date_created = parse_date_node('createdOn', element)
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
            'has_attachment': self.has_attachment,
            'author': self.author,
            'date_created': date_to_excel(self.date_created),
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
    def total_response_count(self):
        """Returns sum total of all Evaluations and Backchecks"""
        return len(self.evaluations) + len(self.backchecks)
    
    @property
    def total_responses(self):
        """Returns tuple with Evaluation totals and Backchecks totals"""
        return (len(self.evaluations), len(self.backchecks))

    @property
    def list_reponses(self):
        """Returns list of Responses in type order: first Evaluations then Backchecks."""
        return self.evaluations + self.backchecks

    @property
    def list_responses_chronological(self):
        """Returns list of Responses in chronological order, regardless of Evaluation or Backcheck type."""
        sort_key = lambda Remark: Remark.date_created
        return list(merge(self.evaluations, self.backchecks, key=sort_key))

    @property
    def highest_response(self, resp_values=_RESPONSE_VALUES):
        all_responses = self.list_reponses
        resp_value = 0
        for resp in all_responses:
            if resp_values[resp.status.lower()] > resp_value:
                resp_value = resp_values[resp.status.lower()]
        resp_dict = {}
        for key, value in resp_values.items():
            resp_dict.update({value: key}) 
        return resp_dict[resp_value].title()

    @property
    def highest_evaluation_response(self, resp_values=_RESPONSE_VALUES):
        all_responses = self.evaluations
        resp_value = 0
        for resp in all_responses:
            if resp_values[resp.status.lower()] > resp_value:
                resp_value = resp_values[resp.status.lower()]
        resp_dict = {}
        for key, value in resp_values.items():
            resp_dict.update({value: key}) 
        return resp_dict[resp_value].title()

    @property
    def highest_backcheck_response(self, resp_values=_RESPONSE_VALUES):
        all_responses = self.backchecks
        resp_value = 0
        for resp in all_responses:
            if resp_values[resp.status.lower()] > resp_value:
                resp_value = resp_values[resp.status.lower()]
        resp_dict = {}
        for key, value in resp_values.items():
            resp_dict.update({value: key}) 
        return resp_dict[resp_value].title()


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
        has_attachment = '〇' if parse_single_tag('attachment', element) is not None else None
        author = parse_single_tag('createdBy', element)
        date_created = parse_date_node('createdOn', element)
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
            'has_attachment': self.has_attachment,
            'author': self.author,
            'date_created': str(self.date_created).replace('T', ' '),
            'remark_type': self.remark_type,
            'parent_id': self.parent_id,
            'impact_scope': self.impact_scope,
            'impact_cost': self.impact_cost,
            'impact_time': self.impact_time,
            'days_open': self.days_open
        }

    def to_list(self, attrs=_RESPONSE_COLUMNS):
        return super().to_list(attrs)


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
        has_attachment = '〇' if parse_single_tag('attachment', element) is not None else None
        author = parse_single_tag('createdBy', element)
        date_created = parse_date_node('createdOn', element)
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
            'has_attachment': self.has_attachment,
            'author': self.author,
            'date_created': str(self.date_created).replace('T', ' '),
            'remark_type': self.remark_type,
            'parent_id': self.parent_id,
            'evaluation_id': self.evaulation_id,
            'days_open': self.days_open
        }

    def to_list(self, attrs=_RESPONSE_COLUMNS):
        return super().to_list(attrs)

#endregion