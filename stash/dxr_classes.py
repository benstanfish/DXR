from typing import List, Dict
from xml.etree.ElementTree import Element
from datetime import datetime
import json

class Evaluation():
    def __init__(self, element: Element):
        self.id = element.find('id').text
        self.parent_id = element.find('comment').text if element.find('comment') is not None else None
        self.status = element.find('status').text if element.find('status') is not None else None
        self.impact_scope = element.find('impactScope').text if element.find('impactScope') is not None else None
        self.impact_cost = element.find('impactCost').text if element.find('impactCost') is not None else None
        self.impact_time = element.find('impactTime').text if element.find('impactTime') is not None else None
        self.text = element.find('evaluationText').text.replace('<br />', '\n') if element.find('evaluationText') is not None else None
        self.attachment = element.find('attachment').text if element.find('attachment') is not None else None
        self.author = element.find('createdBy').text if element.find('createdBy') is not None else None # type: ignore
        self.date = datetime.strptime(element.find('createdOn').text, '%b %d %Y %I:%M %p').isoformat() if element.find('createdOn') is not None else None

    @classmethod
    def from_element(cls, element: Element):
        return Evaluation(element)

    def dump(self) -> Dict:
        return {
            'id': self.id,
            'parent comment id': self.parent_id,
            'status': self.status,
            'impact scope': self.impact_scope,
            'impact cost': self.impact_cost,
            'impact time': self.impact_time,
            'text': self.text,
            'attachment': self.attachment,
            'author': self.author,
            'date': self.date,
        }


class Evaluations():
    def __init__(self, evaluations: List[Evaluation]):
        self.evaulations_list = evaluations

    @classmethod
    def from_list(evaluations: List[Evaluation]):
        return Evaluations(evaluations)

    @property
    def count(self) -> int:
        return len(self.evaulations_list)

    def dump(self):
        return [evaluation.dump() for evaluation in self.evaulations_list]

class Backcheck():
    def __init__(self, element: Element):
        self.id = element.find('id').text
        self.parent_id = element.find('comment').text if element.find('comment') is not None else None
        self.evaluation_id = element.find('evaluation').text if element.find('evaluation') is not None else None
        self.status = element.find('status').text if element.find('status') is not None else None
        self.text = element.find('backcheckText').text.replace('<br />', '\n') if element.find('backcheckText') is not None else None
        self.attachment = element.find('attachment').text if element.find('attachment') is not None else None
        self.author = element.find('createdBy').text if element.find('createdBy') is not None else None
        self.date = datetime.strptime(element.find('createdOn').text, '%b %d %Y %I:%M %p').isoformat() if element.find('createdOn') is not None else None

    @classmethod
    def from_element(self, element: Element):
        return Backcheck(element)

    def dump(self) -> Dict:
        return {
            'id': self.id,
            'parent comemnt id': self.parent_id,
            'evaluation id': self.evaluation_id,
            'status': self.status,
            'text': self.text,
            'attachment': self.attachment,
            'author': self.author,
            'date': self.date,
        }


class Backchecks():
    def __init__(self, backchecks: List[Backcheck]):
        self.backchecks_list = backchecks

    @classmethod
    def from_list(backchecks: List[Backcheck]):
        return Backchecks(backchecks)

    @property
    def count(self) -> int:
        return len(self.backchecks_list)

    def dump(self):
        return [backcheck.dump() for backcheck in self.backchecks_list]


class Comment:
    def __init__(self, element: Element):
        self.id = element.find('id').text
        self.spec = element.find('spec').text if element.find('spec') is not None else None
        self.sheet = element.find('sheet').text if element.find('sheet') is not None else None
        self.detail = element.find('detail').text if element.find('detail') is not None else None
        self.critical = element.find('critical').text if element.find('critical') is not None else None
        self.text = element.find('commentText').text.replace('<br />', '\n') if element.find('commentText') is not None else None
        self.attachment = element.find('attachment').text if element.find('attachment') is not None else None
        self.docref = element.find('DocRef').text if element.find('DocRef') is not None else None
        self.author = element.find('createdBy').text if element.find('createdBy') is not None else None
        self.date = datetime.strptime(element.find('createdOn').text, '%b %d %Y %I:%M %p').isoformat() if element.find('createdOn') is not None else None
        self.status = element.find('status').text if element.find('status') is not None else None
        self.discipline = element.find('Discipline').text if element.find('Discipline') is not None else None
        self.coordinatingdiscipline = element.find('CoordinatingDiscipline').text if element.find('CoordinatingDiscipline') is not None else None
        self.doctype = element.find('DocType').text if element.find('DocType') is not None else None
        self.evaluations = Evaluations([Evaluation(eval) for eval in element.find('evaluations')]) if element.find('evaluations') is not None else Evaluations([])
        self.backchecks = Backchecks([Backcheck(bs) for bs in element.find('backchecks')]) if element.find('backchecks') is not None else Backchecks([])

    @classmethod
    def from_element(self, element: Element):
        return Comment(element)

    @property
    def evaluations_list(self):
        return self.evaluations_list
    
    @property
    def backchecks_list(self):
        return self.backchecks_list

    def evaluations_count(self) -> int:
        return len(self.evaluations)

    def backchecks_count(self) -> int:
        return len(self.backchecks)

    def dump(self) -> Dict:
        return {
            'id': self.id,
            'spec': self.spec,
            'sheet': self.sheet,
            'detail': self.detail,
            'critical': self.critical,
            'text': self.text,
            'attachment': self.attachment,
            'docref': self.docref,
            'author': self.author,
            'date': self.date,
            'status': self.status,
            'discipline': self.discipline,
            'coordinating discipline': self.coordinatingdiscipline,
            'doctype': self.doctype,
            'evaluations': self.evaluations.dump(),
            'backchecks': self.backchecks.dump()
        }

class Comments():
    def __init__(self, comments: List[Comment]):
        self.comments_list = comments

    @classmethod
    def from_list(self, comments: List[Comment]):
        return Comments(comments)

    @classmethod
    def from_element(self, comments: Element):
        comments_list = []
        for comment in comments:
            comments_list.append(Comment.from_element(comment))
        return Comments(comments=comments_list)

    @property
    def count(self) -> int:
        return len(self.comments_list)

    @property
    def max_evaluations(self):
        return max(item.evaluations.count for item in self.comments_list)

    @property
    def max_backchecks(self) -> int:
        return max(item.backchecks.count for item in self.comments_list)

    def dump(self) -> dict:
        return [comment.dump() for comment in self.comments_list]
    
class ProjectInfo():
    def __init__(self, element:Element):
        self.project_id = element.find('ProjectID').text if element.find('ProjectID') is not None else None
        self.project_control_number = element.find('ProjectControlNbr').text if element.find('ProjectControlNbr') is not None else None
        self.project_name = element.find('ProjectName').text if element.find('ProjectName') is not None else None
        self.review_id = element.find('ReviewID').text if element.find('ReviewID') is not None else None
        self.review_name = element.find('ReviewName').text if element.find('ReviewName') is not None else None
        self.run_date = datetime.now().isoformat()

    @classmethod
    def from_element(self, element: Element):
        return ProjectInfo(element)
    
    def dump(self) -> Dict:
        return {
            'project id': self.project_id,
            'project control number': self.project_control_number,
            'project name': self.project_name,
            'review id': self.review_id,
            'review name': self.review_name,
            'run date': self.run_date
        }

class Review():
    def __init__(self, project_info: ProjectInfo, all_comments: Comments):
        self.project_info = project_info
        self.comments = all_comments

    @classmethod
    def from_root(self, root: Element):
        info = ProjectInfo.from_element(root[0])
        comments_element = root[1]
        comments_list = []
        for comment in comments_element:
            comments_list.append(Comment(comment))
        comments = Comments.from_list(comments_list)
        return Review(project_info=info, all_comments=comments)
    
    def dump(self) -> dict:
        return {
            'project info': self.project_info.dump(),
            'comments': self.comments.dump()
        }
    
    def to_json(self):
        with open('review_data.json', 'w') as json_file:
            data = self.dump()
            json.dump(data, json_file, indent=4)

    @property
    def list_all_authors(self) -> List:
        return list(set([comment.author for comment in self.comments.comments_list]))
    