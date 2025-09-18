# Copyright (c) 2018-2025 Ben Fisher

from os.path import getctime
from datetime import datetime
from typing import List, Dict, Tuple
from openpyxl.worksheet.cell_range import CellRange

from .constants import (COMMENT_COLUMNS, 
                        RESPONSE_COLUMNS, 
                        USER_NOTES_COLUMNS,
                        _PROJECT_INFO_INDEX,
                        _COMMENTS_INDEX,
                        _RESPONSE_EXPANSION_TYPES)
from .parsetools import (get_root, parse_single_tag, date_to_excel)
from .remarks import Comment


class ProjectInfo:

    def __init__(self, 
                 project_id=None,
                 control_number=None,
                 project_name=None,
                 review_id=None,
                 review_name=None,
                 xml_date=None,
                 run_date=None):
        self.project_id = project_id
        self.control_number = control_number
        self.project_name = project_name
        self.review_id = review_id
        self.review_name = review_name
        self.xml_date = xml_date
        self.run_date = run_date
        self.vertical_offset = 2
        self.frames = {}
        self.set_frames()
        
    @classmethod
    def from_tree(cls, element, file_path=None):
        project_id = parse_single_tag('ProjectID', element)
        control_number = parse_single_tag('ProjectControlNbr', element)
        project_name = parse_single_tag('ProjectName', element)
        review_id = parse_single_tag('ReviewID', element)
        review_name = parse_single_tag('ReviewName', element)
        if file_path is not None:
            file_date = getctime(file_path)
            xml_date = datetime.fromtimestamp(file_date).strftime('%Y-%m-%d %H:%M:%S')
        else:
            xml_date = None
        run_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return ProjectInfo(project_id=project_id,
                           control_number=control_number,
                           project_name=project_name,
                           review_id=review_id,
                           review_name=review_name,
                           xml_date=xml_date,
                           run_date=run_date)
   
    @property
    def all_data_dict(self) -> Dict:
        return {
            'Project Name': self.project_name,
            'Project ID': self.project_id,
            'Control Number': self.control_number,
            'Review Name': self.review_name,
            'Review ID': self.review_id,
            'XML Date': date_to_excel(self.xml_date),
            'Run Date': date_to_excel(self.run_date)
        }
    
    def to_list(self) -> List:
        """Returns a 2D list intended to be exported to Excel."""
        info = []
        for key in self.all_data_dict.keys():
            info.append([key, self.all_data_dict[key]])
        return info

    @property
    def count(self) -> int:
        return len(self.to_list())

    @property
    def size(self) -> Tuple[int, int]:
        return (self.count, 2)
    
    def set_frames(self) -> None:
        self.frames['outline'] = CellRange(min_col=1, max_col=2, min_row=1, max_row=self.count + self.vertical_offset)
        self.frames['keys'] = CellRange(min_col=1, max_col=1, min_row=1, max_row=self.count)
        self.frames['values'] = CellRange(min_col=2, max_col=2, min_row=1, max_row=self.count)

    def shift_frames(self, col_shift: int = 0, row_shift: int = 0) -> None:
        for region in self.frames:
            self.frames[region].shift(col_shift=col_shift, row_shift=row_shift)
            

class ReviewComments:

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
    def count(self) -> int:
        return len(self.comments)

    @property
    def max_evaluations(self) -> int:
        temp_count = 0
        for comment in self.comments:
            if comment.evaluations_count > temp_count:
                temp_count = comment.evaluations_count 
        return temp_count

    @property
    def max_backchecks(self) -> int:
        temp_count = 0
        for comment in self.comments:
            if comment.backchecks_count > temp_count:
                temp_count = comment.backchecks_count 
        return temp_count    

    @property
    def max_responses(self) -> Tuple[int, int]:
        return (self.max_evaluations, 
                self.max_backchecks)

    @property
    def evaluations_count(self) -> int:
        temp_count = 0
        for comment in self.comments:
            temp_count += comment.evaluations_count
        return temp_count

    @property
    def backchecks_count(self) -> int:
        temp_count = 0
        for comment in self.comments:
            temp_count += comment.backchecks_count
        return temp_count
    
    @property
    def responses_count(self) -> int:
        return self.evaluations_count + self.backchecks_count

    @property
    def comments_to_list(self, attrs: Dict=COMMENT_COLUMNS) -> List:
        my_data = []
        for comment in self.comments:
            my_data.append(comment.to_list(attrs))
        return my_data

    @property
    def column_names(self, attrs: Dict=COMMENT_COLUMNS) -> List:
        return [key for key in attrs.keys()]

    @property
    def comment_columns_count(self, attrs: Dict=COMMENT_COLUMNS) -> int:
        return len([key for key in attrs.keys()])   

    @property
    def response_columns_count(self, attrs: Dict=RESPONSE_COLUMNS) -> int:
        return len([key for key in attrs.keys()] * (self.max_evaluations + self.max_backchecks))
    
    @property
    def all_column_count(self):
        return self.comment_columns_count + self.response_columns_count

    def _get_all_headers(self,
                        comment_attrs: Dict=COMMENT_COLUMNS,
                        response_attrs: Dict=RESPONSE_COLUMNS,
                        expansion_type: _RESPONSE_EXPANSION_TYPES ='chronological') -> List:
        """Returns a list of all the column names (for use in Excel) and the column count."""
        header_names = [key for key in comment_attrs.keys()]
        max_evals, max_bcs = self.max_responses
        if expansion_type.lower() != 'chronological':
            for i in range(max_evals):
                for key in response_attrs.keys():
                    header_names.append(f'Eval {i + 1} {key}')
            for j in range(max_bcs):
                for key in response_attrs.keys():
                    header_names.append(f'BCheck {j + 1} {key}')
        else:
            for k in range(max_evals + max_bcs):
                for key in response_attrs.keys():
                    header_names.append(f'Resp {k + 1} {key}')
        return header_names

    def to_list(self, 
                comment_attrs: Dict=COMMENT_COLUMNS,
                response_attrs: Dict=RESPONSE_COLUMNS,
                expansion_type: _RESPONSE_EXPANSION_TYPES='chronological') -> List:
        """Returns the full List of comments and corresponding responses and the number of rows."""

        full_list = [self._get_all_headers(comment_attrs=comment_attrs, 
                                          response_attrs=response_attrs, 
                                          expansion_type=expansion_type)]
        max_eval_count, max_bc_count = self.max_responses
        for comment in self.comments:
            temp = []
            temp += comment.to_list(comment_attrs)
            if expansion_type == 'chronological':
                resp_list = comment.list_responses_chronological
                resp_count = comment.total_response_count
                diff_eval = (max_eval_count + max_bc_count) - resp_count
                for resp in resp_list:
                    temp += resp.to_list(response_attrs)
                for i in range(diff_eval):
                    temp += [''] * len(response_attrs)
                full_list.append(temp)
            else:
                for evaluation in comment.evaluations:
                    temp += evaluation.to_list(response_attrs)
                diff_eval = max_eval_count - comment.evaluations_count
                for _ in range(diff_eval):
                    temp += [''] * len(response_attrs)
                for backcheck in comment.backchecks:
                    temp += backcheck.to_list(response_attrs)
                diff_bc = max_bc_count - comment.backchecks_count
                for _ in range(diff_bc):
                    temp += [''] * len(response_attrs)
                full_list.append(temp)
        return full_list

    @property
    def size(self) -> Tuple[int, int]:
        return (self.count, self.all_column_count)


class UserNotes:
    def __init__(self):
        self.headers = [header for header in USER_NOTES_COLUMNS]
        self.frames = {}

    def to_list(self) -> List[str]:
        return self.headers
    
    @property
    def size(self) -> Tuple[int, int]:
        return (1, self.count)

    @property
    def count(self) -> int:
        return len(self.headers)
    
    def set_frames(self, cell_range: CellRange) -> None:
        if cell_range:
            self.frames['outline'] = cell_range
            min_col, min_row, max_col, max_row = cell_range.min_col, cell_range.min_row, cell_range.max_col, cell_range.max_row            
            self.frames['header']  = CellRange(min_col=min_col, max_col=max_col, min_row=min_row, max_row=min_row)
            self.frames['body']  = CellRange(min_col=min_col, max_col=max_col, min_row=min_row + 1, max_row=max_row)
    
    def shift_frames(self, col_shift: int = 0, row_shift: int = 0) -> None:
        for region in self.frames:
            self.frames[region].shift(col_shift=col_shift, row_shift=row_shift)  
        


class Review:
    """Returns a Review object containing project info and review comments objects."""

    def __init__(self,
                 project_info: ProjectInfo,
                 review_comments: ReviewComments,
                 root=None,
                 file_path=None):
        self.project_info = project_info
        self.review_comments = review_comments
        self.root = root
        self.file_path = file_path
        self.user_notes = UserNotes()
        self.frames = {}

    @classmethod
    def from_file(cls, path):
        root = get_root(path) if not None else None
        if root:
            project_info = ProjectInfo.from_tree(root[_PROJECT_INFO_INDEX], file_path=path) if not None else None
            review_comments = ReviewComments.from_tree(root[_COMMENTS_INDEX]) if not None else None
        return Review(project_info=project_info,
                      review_comments=review_comments,
                      root=root,
                      file_path=path)

    def build_frames(self) -> Dict:
        return {}


