""" 
This module defines the abstract class used for deserializing Evaulations
and Backchecks from ProjNet DrChecks XML reports.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from utils import parse_helper


class Reply(ABC):
    """Abstraction of commonalities between Evaluation and Backcheck classes"""

    @abstractmethod
    def from_tree(self, xml_element_node):
        pass

    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def parent_id(self):
        pass

    @property
    @abstractmethod
    def status(self):
        pass

    @property
    @abstractmethod
    def text(self):
        pass

    @property
    @abstractmethod
    def has_attachment(self):
        pass

    @property
    @abstractmethod
    def author(self):
        pass

    @property
    @abstractmethod
    def date_created(self):
        pass

    @property
    @abstractmethod
    def reply_type(self):
        pass


class Evaluation(Reply):

    def __init__(self, 
                 id_=None, 
                 parent_id=None,
                 status=None,
                 impact_scope=None,
                 impact_cost=None,
                 impact_time=None,
                 text=None,
                 has_attachment=False,
                 author=None,
                 dated_created=None,
                 reply_type=None):
        self._id = id_
        self._parent_id = parent_id
        self._status = status
        self._impact_scope = impact_scope
        self._impact_cost = impact_cost
        self._impact_time = impact_time
        self._text = text
        self._has_attachment = has_attachment
        self._author = author,
        self._date_created = dated_created
        self._reply_type =reply_type

    @classmethod
    def from_tree(cls, element):
        id_ = parse_helper('id', element)
        parent_id = parse_helper('comment', element)
        status = parse_helper('status', element)
        impact_scope = parse_helper('impactScope', element)
        impact_cost = parse_helper('impactCost', element)
        impact_time = parse_helper('impactTime', element)
        text = parse_helper('evaluationText', element)
        has_attachment = True if element.find('attachment').text is not None else False
        author = parse_helper('createdBy', element)
        date_created = datetime.strptime(element.find('createdOn').text, 
                                        '%b %d %Y %I:%M %p').isoformat() if element.find('createdOn') is not None else None
        reply_type = 'evaulation'
        return Evaluation(id_=id_, 
                          parent_id=parent_id, 
                          status=status, 
                          impact_scope=impact_scope,
                          impact_cost=impact_cost,
                          impact_time=impact_time,
                          text=text,
                          has_attachment=has_attachment,
                          author=author,
                          dated_created=date_created,
                          reply_type=reply_type)

    @property
    def id(self):
        return self._id

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def status(self):
        return self._status

    @property
    def text(self):
        return self._text

    @property
    def has_attachment(self):
        return self._has_attachment

    @property
    def author(self):
        return self._author

    @property
    def date_created(self):
        return self._date_created

    @property
    def reply_type(self):
        return self._reply_type

    @property
    def impact_scope(self):
        return self._impact_scope
    
    @property
    def impact_cost(self):
        return self._impact_cost
    
    @property
    def impact_time(self):
        return self._impact_time


class Backcheck(Reply):

    def __init__(self, 
                 id_=None, 
                 parent_id=None,
                 evaluation_id=None,
                 status=None,
                 text=None,
                 has_attachment=False,
                 author=None,
                 dated_created=None,
                 reply_type=None):
        self._id = id_
        self._parent_id = parent_id
        self._evaulation_id = evaluation_id
        self._status = status
        self._text = text
        self._has_attachment = has_attachment
        self._author = author,
        self._date_created = dated_created
        self._reply_type =reply_type

    @classmethod
    def from_tree(cls, element):
        id_ = parse_helper('id', element)
        parent_id = parse_helper('comment', element)
        evaluation_id = parse_helper('evaluation', element)
        status = parse_helper('status', element)
        text = parse_helper('backcheckText', element)
        has_attachment = True if element.find('attachment').text is not None else False
        author = parse_helper('createdBy', element)
        date_created = datetime.strptime(element.find('createdOn').text, 
                                        '%b %d %Y %I:%M %p').isoformat() if element.find('createdOn') is not None else None
        reply_type = 'backcheck'
        return Backcheck(id_=id_, 
                         parent_id=parent_id, 
                         status=status, 
                         evaluation_id=evaluation_id,
                         text=text,
                         has_attachment=has_attachment,
                         author=author,
                         dated_created=date_created,
                         reply_type=reply_type)

    @property
    def id(self):
        return self._id

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def status(self):
        return self._status

    @property
    def text(self):
        return self._text

    @property
    def has_attachment(self):
        return self._has_attachment

    @property
    def author(self):
        return self._author

    @property
    def date_created(self):
        return self._date_created

    @property
    def reply_type(self):
        return self._reply_type

    @property
    def evaulation_id(self):
        return self._evaulation_id
    