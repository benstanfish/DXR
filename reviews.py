"""Module that provides top-level ProjNet Dr Checks reviews XML parsing functionality"""

from typing import List, Dict, Tuple
from defusedxml import ElementTree as ET
# from utils import parse_single_tag
# from remarks import Comment

from blocks import Comment, parse_single_tag

_PROJECT_INFO_INDEX = 0
_COMMENTS_INDEX = 1
_COMMENT_COLUMNS = ['id', 
                    'status', 
                    'discipline',
                    'author',
                    '',
                    'date_created',
                    'text',
                    'is_critical',
                    '',
                    'has_attachment']

_COMMENTS_COLUMNS = {
    'ID': 'id',
    'Status': 'status',
    'Discipline': 'discipline',
    'Author': 'author',
    'Email': 'email',
    'Date': 'date_created',
    'Comment': 'text',
    'Critical': 'is_critical',
    'Class': '',
    'Att.': ''
}







def get_root(path):
    try:
        root = ET.parse(path).getroot()
        if root.tag.lower() == 'projnet': # type: ignore
            return root
    except Exception as e:
        print(e)

def get_review(root):
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


class ProjectInfo():
    
    def __init__(self, 
                 project_id,
                 control_number,
                 project_name,
                 review_id,
                 review_name):
        self._project_id = project_id
        self._control_number = control_number
        self._project_name = project_name
        self._review_id = review_id
        self._review_name = review_name

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
    def project_id(self):
        return self._project_id
    
    @property
    def control_number(self):
        return self._control_number
    
    @property
    def project_name(self):
        return self._project_name
    
    @property
    def review_id(self):
        return self._review_id
    
    @property
    def review_name(self):
        return self._review_name
    
    @property
    def all_data(self):
        return {
            'Project Name': self._project_name,
            'Project ID': self._project_id,
            'Control Number': self._control_number,
            'Review Name': self._review_name,
            'Review ID': self._review_id
        }


class ReviewComments():

    def __init__(self,
                 comments: List=[]):
        self._comments = comments

    @classmethod
    def from_tree(cls, element):
        comments = []
        for comment in element.findall('comment'):
            comments.append(Comment.from_tree(comment))
        return ReviewComments(comments=comments)
    
    @property
    def comments(self):
        return self._comments

    @property
    def comment_count(self):
        return len(self._comments)

    @property
    def max_evaulations_count(self):
        temp_count = 0
        for comment in self.comments:
            if comment.evaluations_count > temp_count:
                temp_count = comment.evaluations_count 
        return temp_count

    @property
    def max_backchecks_count(self):
        temp_count = 0
        for comment in self.comments:
            if comment.backchecks_count > temp_count:
                temp_count = comment.backchecks_count 
        return temp_count    

    @property
    def max_response_counts(self):
        return (self.max_evaulations_count, 
                self.max_backchecks_count)

    @property
    def total_evaulations_count(self):
        temp_count = 0
        for comment in self.comments:
            temp_count += comment.evaluations_count
        return temp_count

    @property
    def total_backchecks_count(self):
        temp_count = 0
        for comment in self.comments:
            temp_count += comment.backchecks_count
        return temp_count
    
    @property
    def total_responses_count(self):
        return self.total_evaulations_count + self.total_backchecks_count
    
