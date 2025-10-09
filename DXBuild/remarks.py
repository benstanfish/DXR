# Copyright (c) 2018-2025 Ben Fisher

from abc import ABC, abstractmethod
from datetime import datetime
from heapq import merge
from typing import List, Dict, Tuple

from .constants import (_TRUE_SYMBOLIC, COMMENT_COLUMNS, RESPONSE_COLUMNS, RESPONSE_VALUES)
from .parseable import Parseable

import logging
from dxcore.logconstants import log_format_string
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter(log_format_string)
log_file_handler = logging.FileHandler(f'./logs/{__name__}.log')
log_file_handler.setFormatter(log_formatter)
logger.addHandler(log_file_handler)


class Remark(ABC, Parseable):
    """Parent class for Comment, Evaluation and Backcheck classes"""
    def __init__(self,
                 id_=None,
                 status=None,
                 text=None,
                 has_attachment=None,
                 author=None,
                 date_created=None,
                 remark_type='remark'):
        super().__init__()
        self.id = id_
        self.status = status
        self.text = text
        self.has_attachment = has_attachment
        self.author = author
        self.date_created = date_created
        self.remark_type = remark_type

    @property
    def attributes_list(self) -> List:
        return [attr for attr in self.__dict__]

    @abstractmethod
    def from_element(self):
        pass
    
    @property
    @abstractmethod
    def all_properties_to_dict(self) -> Dict:
        pass

    def to_list(self, attrs: Tuple | Dict=COMMENT_COLUMNS) -> List:
        props = self.all_properties_to_dict
        if isinstance(attrs, list):
            return [props[item] if item in props else '' for item in attrs]
        if isinstance(attrs, dict):
            for key in attrs.keys():
                return [props[attrs[key]] if attrs[key] in props else '' for key in attrs]
        return []


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
    def from_element(cls, element):
        id_ = cls.parse_single_tag('id', element)
        spec = cls.parse_single_tag('spec', element)
        sheet = cls.parse_single_tag('sheet', element)
        detail = cls.parse_single_tag('detail', element)
        is_critical = cls.parse_single_tag('critical', element)
        docref = cls.parse_single_tag('DocRef', element)
        doctype = cls.parse_single_tag('DocType', element)
        discipline = cls.parse_single_tag('Discipline', element)
        coordinating_discipline = cls.parse_single_tag('CoordinatingDiscipline', element)     
        status = cls.parse_single_tag('status', element)
        text = cls.clean_text(cls.parse_single_tag('commentText', element))
        has_attachment = _TRUE_SYMBOLIC if cls.parse_single_tag('attachment', element) is not None else None
        author = cls.parse_single_tag('createdBy', element)
        date_created = cls.parse_date_node('createdOn', element)
        evaluations = [Evaluation.from_element(eval) for eval in element.find('evaluations')] \
            if element.find('evaluations') is not None else []
        backchecks = [Backcheck.from_element(bc) for bc in element.find('backchecks')] \
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
    def all_properties_to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'text': self.text,
            'has_attachment': self.has_attachment,
            'author': self.author,
            'date_created': self.date_to_excel(self.date_created),
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
            'ball_in_court': self.ball_in_court,
            'highest_response': self.highest_response(RESPONSE_VALUES),
            'evaluations': self.evaluations,
            'backchecks': self.backchecks
        }
    
    @property
    def evaluations_count(self) -> int:
        return len(self.evaluations)

    @property
    def backchecks_count(self) -> int:
        return len(self.backchecks)
    
    @property
    def total_response_count(self) -> int:
        """Returns sum total of all Evaluations and Backchecks"""
        return len(self.evaluations) + len(self.backchecks)
    
    @property
    def total_responses(self) -> Tuple[int, int]:
        """Returns tuple with Evaluation totals and Backchecks totals"""
        return (len(self.evaluations), len(self.backchecks))

    @property
    def list_responses(self) -> List:
        """Returns list of Responses in type order: first Evaluations then Backchecks."""
        return self.evaluations + self.backchecks

    @property
    def list_responses_chronological(self) -> List:
        """Returns list of Responses in chronological order, regardless of Evaluation or Backcheck type."""
        sort_key = lambda Remark: Remark.date_created
        return list(merge(self.evaluations, self.backchecks, key=sort_key))

    def highest_response(self, resp_values: Dict=RESPONSE_VALUES) -> str:
        all_responses = self.list_responses
        resp_value = 0
        for resp in all_responses:
            if resp_values[resp.status.lower()] > resp_value:
                resp_value = resp_values[resp.status.lower()]
        resp_dict = {}
        for key, value in resp_values.items():
            resp_dict.update({value: key}) 
        if resp_value == 0:
            return ''
        return resp_dict[resp_value].title()

    def highest_evaluation_response(self, resp_values: Dict=RESPONSE_VALUES) -> str:
        all_responses = self.evaluations
        resp_value = 0
        for resp in all_responses:
            if resp_values[resp.status.lower()] > resp_value:
                resp_value = resp_values[resp.status.lower()]
        resp_dict = {}
        for key, value in resp_values.items():
            resp_dict.update({value: key}) 
        if resp_value == 0:
            return ''
        return resp_dict[resp_value].title()

    def highest_backcheck_response(self, resp_values: Dict=RESPONSE_VALUES) -> str:
        all_responses = self.backchecks
        resp_value = 0
        for resp in all_responses:
            if resp_values[resp.status.lower()] > resp_value:
                resp_value = resp_values[resp.status.lower()]
        resp_dict = {}
        for key, value in resp_values.items():
            resp_dict.update({value: key}) 
        if resp_value == 0:
            return ''
        return resp_dict[resp_value].title()

    @property
    def latest_response(self) -> Remark | None:
        sort_key = lambda Remark: Remark.date_created
        responses =  list(merge(self.evaluations, self.backchecks, key=sort_key))
        if len(responses) != 0:
            return responses[-1]
        return None

    @property
    def ball_in_court(self) -> str:
        """Returns the Commentor or Evaluator depending on whose turn it is to response."""
        if self.total_response_count > 0 and self.latest_response is not None:
            resp_type = self.latest_response.remark_type
            resp_text = self.latest_response.text
            if resp_text == 'Closed without comment.':
                return 'Closed'
            elif resp_type == 'backcheck':
                return 'Evaluator'
                # return self.evaluations[0].author or 'Evaluator'
            elif resp_type == 'evaluation':
                return 'Commentor'
                # return self.author or 'Commentor'
            else:
                return ''
        return 'Evaluator'

    @property
    def days_open(self) -> int:
        """Calculates the number of days a comment is (was) open (if already closed)."""
        current_date = datetime.now()
        if self.status and self.status.lower() == 'closed' and self.backchecks_count > 0:
            latest_backcheck = self.backchecks[-1]
            time_diff = current_date - datetime.fromisoformat(str(latest_backcheck.date_created))
        else:
            time_diff = current_date - datetime.fromisoformat(str(self.date_created))
        return time_diff.days


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
    def from_element(cls, element):
        id_ = cls.parse_single_tag('id', element)
        parent_id = cls.parse_single_tag('comment', element)
        status = cls.parse_single_tag('status', element)
        impact_scope = cls.parse_single_tag('impactScope', element)
        impact_cost = cls.parse_single_tag('impactCost', element)
        impact_time = cls.parse_single_tag('impactTime', element)
        text = cls.clean_text(cls.parse_single_tag('evaluationText', element))
        has_attachment = _TRUE_SYMBOLIC if cls.parse_single_tag('attachment', element) is not None else None
        author = cls.parse_single_tag('createdBy', element)
        date_created = cls.parse_date_node('createdOn', element)
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
    def all_properties_to_dict(self) -> Dict:
        return {
            'id': self.id,
            'status': self.status,
            'text': self.text,
            'has_attachment': self.has_attachment,
            'author': self.author,
            'date_created': self.date_to_excel(self.date_created),
            'remark_type': self.remark_type,
            'parent_id': self.parent_id,
            'impact_scope': self.impact_scope,
            'impact_cost': self.impact_cost,
            'impact_time': self.impact_time
        }

    def to_list(self, attrs: Dict=RESPONSE_COLUMNS) -> List:
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
    def from_element(cls, element):
        id_ = cls.parse_single_tag('id', element)
        parent_id = cls.parse_single_tag('comment', element)
        evaluation_id = cls.parse_single_tag('evaluation', element)
        status = cls.parse_single_tag('status', element)
        text = cls.clean_text(cls.parse_single_tag('backcheckText', element))
        has_attachment = _TRUE_SYMBOLIC if cls.parse_single_tag('attachment', element) is not None else None
        author = cls.parse_single_tag('createdBy', element)
        date_created = cls.parse_date_node('createdOn', element)
        return Backcheck(id_=id_, 
                        parent_id=parent_id, 
                        status=status, 
                        evaluation_id=evaluation_id,
                        text=text,
                        has_attachment=has_attachment,
                        author=author,
                        date_created=date_created)
    
    @property
    def all_properties_to_dict(self) -> Dict:
        return {
            'id': self.id,
            'status': self.status,
            'text': self.text,
            'has_attachment': self.has_attachment,
            'author': self.author,
            'date_created': self.date_to_excel(self.date_created),
            'remark_type': self.remark_type,
            'parent_id': self.parent_id,
            'evaluation_id': self.evaulation_id
        }

    def to_list(self, attrs: Dict=RESPONSE_COLUMNS) -> List:
        return super().to_list(attrs)




