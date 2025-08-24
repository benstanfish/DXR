""" 
This module defines the abstract and concrete class used for deserializing
conversation building blocks (Comements, Evaluations and Backchecks) from 
ProjNet DrChecks XML reports.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from heapq import merge


def parse_single_tag(tag, xml_element_node):
    """Helper method to extract XML data for first child element node with tag of tag."""
    return xml_element_node.find(tag).text if xml_element_node.find(tag) is not None else None

def clean_text(text):
    return text.replace('<br />', '\n')


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

    @abstractmethod
    def dump_values(self):
        pass


class Comment(Remark):
    
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
        date_created = datetime.strptime(element.find('createdOn').text, 
                                        '%b %d %Y %I:%M %p').isoformat() if \
                                            element.find('createdOn') is not None else None,
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

    def dump_values(self):
        raise NotImplementedError

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
        self._parent_id = parent_id
        self._impact_scope = impact_scope
        self._impact_cost = impact_cost
        self._impact_time = impact_time

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
        date_created = datetime.strptime(element.find('createdOn').text, 
                                        '%b %d %Y %I:%M %p').isoformat() if \
                                            element.find('createdOn') is not None else None
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

    def dump_values(self):
        raise NotImplementedError


class Backcheck(Remark):

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
        self._parent_id = parent_id
        self._evaulation_id = evaluation_id

    @classmethod
    def from_tree(cls, element):
        id_ = parse_single_tag('id', element)
        parent_id = parse_single_tag('comment', element)
        evaluation_id = parse_single_tag('evaluation', element)
        status = parse_single_tag('status', element)
        text = clean_text(parse_single_tag('backcheckText', element))
        has_attachment = True if element.find('attachment').text is not None else False
        author = parse_single_tag('createdBy', element)
        date_created = datetime.strptime(element.find('createdOn').text, 
                                        '%b %d %Y %I:%M %p').isoformat() if \
                                            element.find('createdOn') is not None else None
        return Backcheck(id_=id_, 
                        parent_id=parent_id, 
                        status=status, 
                        evaluation_id=evaluation_id,
                        text=text,
                        has_attachment=has_attachment,
                        author=author,
                        date_created=date_created)
    
    def dump_values(self):
        raise NotImplementedError