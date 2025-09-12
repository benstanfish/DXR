
from dxbuild.dxreview import Review
from dxbuild.dxtools import copy_to_range, timestamp
from openpyxl import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.worksheet.table import Table
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import DEFAULT_FONT


xml_path = './dev/test/data.xml'

review = Review.from_file(xml_path)
project_info = review.project_info
all_comments = review.review_comments
user_notes = review.user_notes

DEFAULT_FONT.__init__(name='Aptos', size=11)
wb = Workbook()
ws = wb.active

# Determine Anchor Cell
user_notes_data = user_notes.to_list()
project_info_data = project_info.to_list()
all_comments_data = all_comments.to_list()

VERTICAL_OFFSET = 3
HEADER_ROW = VERTICAL_OFFSET + project_info.size[0]
if ws:
    USER_DATA_CELL = Cell(worksheet=ws, row=HEADER_ROW, column=1)
    PROJECT_INFO_CELL = Cell(worksheet=ws, row=1, column=user_notes.size[1] + 1)
    ALL_COMMENTS_CELL = Cell(worksheet=ws, row=HEADER_ROW, column=user_notes.size[1] + 1)

# Dump Data to Excel
copy_to_range(user_notes_data, worksheet=ws, anchor_cell=USER_DATA_CELL.coordinate)
copy_to_range(project_info_data, worksheet=ws, anchor_cell=PROJECT_INFO_CELL.coordinate)
copy_to_range(all_comments_data, worksheet=ws, anchor_cell=ALL_COMMENTS_CELL.coordinate)

# Create ListObject, but don't assign a TableStyle since we can only used native options
TABLE_REGION = CellRange(min_row=USER_DATA_CELL.row,
                             max_row=USER_DATA_CELL.row + all_comments.count,
                             min_col=USER_DATA_CELL.column,
                             max_col=user_notes.size[1] + all_comments.size[1],
                             title='comments')

table = Table(displayName='Comments', ref=TABLE_REGION.coord)

if ws is not None:
    ws.add_table(table)

    status_dv = DataValidation(type='list', 
                               formula1='"Concur, For Information Only, Non-Concur, Check and Resolve"', 
                               allow_blank=True)
    STATUS_CELL = Cell(worksheet=ws, row=HEADER_ROW +1, column=24)
    ws.add_data_validation(status_dv)
    status_vector = CellRange('G12:G125')
    status_dv.add(status_vector)
    print(status_vector in status_dv)

wb.save(f'./dev/test/out/test_{timestamp()}.xlsx')




