""" 
DEPRECATED!!!


This module defines the abstract and concrete class used for deserializing
conversation building blocks (Comements, Evaluations and Backchecks) from 
ProjNet DrChecks XML reports.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from heapq import merge
from DXutils import parse_helper
from stash.settings import COMMENT_PARAMS
from blocks import Remark, Comment

# class Remark(ABC):
#     """Abstraction of commonalities between Comment, Evaluation and Backcheck classes"""

#     def attributes_list(self):
#         """Return list of class attribute names, with prefix _ removed."""
#         return [item.replace('_', '', 1) for item in self.__dict__]

#     def values_list(self, attrs=[]):
#         """Return a list of values in supplied attrs list or all values if [].
        
#         The values in the supplied attrs must match the names of the Remark properties
#         except without the private '_' prefix. However, if an empty list (default) is
#         provided all attribute values are returned.
#         """
#         if len(attrs) > 0:
#             _attrs = []
#             for item in attrs:
#                 if item == '' or None:
#                     _attrs.append('')
#                 else:
#                     _attrs.append(self.__dict__[f'{'_' + item}'])
#             return _attrs
#         else:
#             # For comments, three .pop() will drop the last three items
#             return [self.__dict__[f'{'_' + item}'] for item in self.attributes_list]          

#     def values_from_dict(self, attrs={}):
#         return attrs == {}

#     @abstractmethod
#     def from_tree(self, xml_element_node):
#         pass

#     @property
#     @abstractmethod
#     def id(self):
#         pass

#     @property
#     @abstractmethod
#     def status(self):
#         pass

#     @property
#     @abstractmethod
#     def text(self):
#         pass

#     @property
#     @abstractmethod
#     def has_attachment(self):
#         pass

#     @property
#     @abstractmethod
#     def author(self):
#         pass

#     @property
#     @abstractmethod
#     def date_created(self):
#         pass

#     @property
#     @abstractmethod
#     def remark_type(self):
#         pass




# class Comment(Remark):
    
#     def __init__(self, 
#                 id_=None,
#                 spec=None,
#                 sheet=None,
#                 detail=None,
#                 is_critical=None,
#                 docref=None,
#                 doctype=None,
#                 discipline=None,
#                 coordinating_discipline=None,
#                 status=None,
#                 text=None,
#                 has_attachment=False,
#                 author=None,
#                 date_created=None,
#                 evaluations=[],
#                 backchecks=[]):
#         self._id = id_
#         self._spec = spec
#         self._sheet = sheet
#         self._detail = detail
#         self._is_critical = is_critical
#         self._docref = docref
#         self._doctype = doctype
#         self._discipline = discipline
#         self._coordinating_discipline = coordinating_discipline
#         self._status = status
#         self._text = text
#         self._has_attachment = has_attachment
#         self._author = author
#         self._date_created = date_created
#         self._remark_type = 'comment'
#         self._evaluations = evaluations
#         self._backchecks = backchecks

#     @classmethod
#     def from_tree(cls, element):
#         id_ = parse_helper('id', element)
#         spec = parse_helper('spec', element)
#         sheet = parse_helper('sheet', element)
#         detail = parse_helper('detail', element)
#         is_critical = parse_helper('critical', element)
#         docref = parse_helper('DocRef', element)
#         doctype = parse_helper('DocType', element)
#         discipline = parse_helper('Discipline', element)
#         coordinating_discipline = parse_helper('CoordinatingDiscipline', element)     
#         status = parse_helper('status', element)
#         text = parse_helper('commentText', element)
#         has_attachment = True if element.find('attachment') is not None else False
#         author = parse_helper('createdBy', element)
#         date_created = datetime.strptime(element.find('createdOn').text, 
#                                         '%b %d %Y %I:%M %p').isoformat() if \
#                                             element.find('createdOn') is not None else None
#         evaluations = [Evaluation.from_tree(eval) for eval in element.find('evaluations')] \
#             if element.find('evaluations') is not None else []
#         backchecks = [Backcheck.from_tree(bc) for bc in element.find('backchecks')] \
#                     if element.find('backchecks') is not None else []
#         return Comment(id_=id_,
#                     spec=spec,
#                     sheet=sheet,
#                     detail=detail,
#                     is_critical=is_critical,
#                     docref=docref,
#                     doctype=doctype,
#                     discipline=discipline,
#                     coordinating_discipline=coordinating_discipline,
#                     status=status,
#                     text=text,
#                     has_attachment=has_attachment,
#                     author=author,
#                     date_created=date_created,
#                     evaluations=evaluations,
#                     backchecks=backchecks)

#     @property
#     def id(self):
#         return self._id

#     @property
#     def status(self):
#         return self._status

#     @property
#     def text(self):
#         return self._text

#     @property
#     def has_attachment(self):
#         return self._has_attachment

#     @property
#     def author(self):
#         return self._author

#     @property
#     def date_created(self):
#         return self._date_created

#     @property
#     def remark_type(self):
#         return self._remark_type
    
#     @property
#     def evaluations(self):
#         return self._evaluations
    
#     @property
#     def backchecks(self):
#         return self._backchecks

#     @property
#     def spec(self):
#         return self._spec
    
#     @property
#     def sheet(self):
#         return self._sheet
    
#     @property
#     def detail(self):
#         return self._detail
    
#     @property
#     def is_critical(self):
#         return self._is_critical

#     @property
#     def docref(self):
#         return self._docref
    
#     @property
#     def doctype(self):
#         return self._doctype
    
#     @property
#     def discipline(self):
#         return self._discipline
    
#     @property
#     def coordinating_discipline(self):
#         return self._coordinating_discipline

#     @property
#     def evaluations_count(self):
#         return len(self.evaluations)

#     @property
#     def backchecks_count(self):
#         return len(self.backchecks)
    
#     @property
#     def response_count(self):
#         return len(self.evaluations) + len(self.backchecks)
    
#     @property
#     def get_responses(self):
#         return self.evaluations + self.backchecks

#     @property
#     def get_chronological_responses(self):
#         sort_key = lambda Remark: Remark.date_created
#         return list(merge(self.evaluations, self.backchecks, key=sort_key))

#     def print_responses(self):
#         for reply in self.get_responses:
#             print(reply.remark_type) # TODO: need to complete this code

#     def print_chronological_responses(self):
#         for reply in self.get_chronological_responses:
#             print(reply.remark_type) # TODO: need to complete this code

#     def get_dict(self):
#         return {
#             'id': self._id,
#             'status': self._status,
#             'discipline': self._discipline,
#             'author': self._author,
#             'date': self._date_created,
#             'comment': self._text,
#             'critical': self._is_critical,
#             'att': self._has_attachment
#         }




# class Evaluation(Remark):

#     def __init__(self, 
#                 id_=None, 
#                 parent_id=None,
#                 status=None,
#                 impact_scope=None,
#                 impact_cost=None,
#                 impact_time=None,
#                 text=None,
#                 has_attachment=False,
#                 author=None,
#                 dated_created=None):
#         self._id = id_
#         self._parent_id = parent_id
#         self._status = status
#         self._impact_scope = impact_scope
#         self._impact_cost = impact_cost
#         self._impact_time = impact_time
#         self._text = text
#         self._has_attachment = has_attachment
#         self._author = author
#         self._date_created = dated_created
#         self._remark_type = 'evaluation'

#     @classmethod
#     def from_tree(cls, element):
#         id_ = parse_helper('id', element)
#         parent_id = parse_helper('comment', element)
#         status = parse_helper('status', element)
#         impact_scope = parse_helper('impactScope', element)
#         impact_cost = parse_helper('impactCost', element)
#         impact_time = parse_helper('impactTime', element)
#         text = parse_helper('evaluationText', element)
#         has_attachment = True if element.find('attachment').text is not None else False
#         author = parse_helper('createdBy', element)
#         date_created = datetime.strptime(element.find('createdOn').text, 
#                                         '%b %d %Y %I:%M %p').isoformat() if \
#                                             element.find('createdOn') is not None else None
#         return Evaluation(id_=id_, 
#                         parent_id=parent_id, 
#                         status=status, 
#                         impact_scope=impact_scope,
#                         impact_cost=impact_cost,
#                         impact_time=impact_time,
#                         text=text,
#                         has_attachment=has_attachment,
#                         author=author,
#                         dated_created=date_created)

#     @property
#     def id(self):
#         return self._id

#     @property
#     def parent_id(self):
#         return self._parent_id

#     @property
#     def status(self):
#         return self._status

#     @property
#     def text(self):
#         return self._text

#     @property
#     def has_attachment(self):
#         return self._has_attachment

#     @property
#     def author(self):
#         return self._author

#     @property
#     def date_created(self):
#         return self._date_created

#     @property
#     def remark_type(self):
#         return self._remark_type

#     @property
#     def impact_scope(self):
#         return self._impact_scope
    
#     @property
#     def impact_cost(self):
#         return self._impact_cost
    
#     @property
#     def impact_time(self):
#         return self._impact_time
       


# class Backcheck(Remark):

#     def __init__(self, 
#                 id_=None, 
#                 parent_id=None,
#                 evaluation_id=None,
#                 status=None,
#                 text=None,
#                 has_attachment=False,
#                 author=None,
#                 dated_created=None):
#         self._id = id_
#         self._parent_id = parent_id
#         self._evaulation_id = evaluation_id
#         self._status = status
#         self._text = text
#         self._has_attachment = has_attachment
#         self._author = author
#         self._date_created = dated_created
#         self._remark_type = 'backcheck'

#     @classmethod
#     def from_tree(cls, element):
#         id_ = parse_helper('id', element)
#         parent_id = parse_helper('comment', element)
#         evaluation_id = parse_helper('evaluation', element)
#         status = parse_helper('status', element)
#         text = parse_helper('backcheckText', element)
#         has_attachment = True if element.find('attachment').text is not None else False
#         author = parse_helper('createdBy', element)
#         date_created = datetime.strptime(element.find('createdOn').text, 
#                                         '%b %d %Y %I:%M %p').isoformat() if \
#                                             element.find('createdOn') is not None else None
#         return Backcheck(id_=id_, 
#                         parent_id=parent_id, 
#                         status=status, 
#                         evaluation_id=evaluation_id,
#                         text=text,
#                         has_attachment=has_attachment,
#                         author=author,
#                         dated_created=date_created)

#     @property
#     def id(self):
#         return self._id

#     @property
#     def parent_id(self):
#         return self._parent_id

#     @property
#     def status(self):
#         return self._status

#     @property
#     def text(self):
#         return self._text

#     @property
#     def has_attachment(self):
#         return self._has_attachment

#     @property
#     def author(self):
#         return self._author

#     @property
#     def date_created(self):
#         return self._date_created

#     @property
#     def remark_type(self):
#         return self._remark_type

#     @property
#     def evaulation_id(self):
#         return self._evaulation_id
    
