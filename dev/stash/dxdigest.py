#Copyright (c) 2018-2025 Ben Fisher


from typing import List, Tuple

from dxbuild.reviews import Review
from dxbuild.buildtools import timestamp, list_dimensions, copy_to_range
from dxconfig.settings import *
from dxcore.dxcolor import WebColor

from openpyxl import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.utils.cell import coordinate_to_tuple
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import DEFAULT_FONT, Font


xml_path = './dev/test/data.xml'
review = Review.from_file(xml_path)
project_info = review.project_info
review_comments = review.review_comments
user_notes = review.user_notes

for i, column_name in enumerate(review_comments.column_names):
    print(i + 1, column_name)

print(review_comments.comment_columns_count)


print(project_info.get_range('H1').coord)
print(project_info.get_key_range('H1').coord)
print(project_info.get_value_range('H1').coord)


xlsx_path = f'./dev/test/out/export_test_{timestamp()}.xlsx'


expansion_type = 'chronological'
all_list, comment_region_rows = review_comments.to_list(expansion_type=expansion_type)
header_list, comment_region_columns = review_comments._get_all_headers(expansion_type=expansion_type)


print(len(all_list))
TABLE_ANCHOR = 'H11'

print(review_comments.get_comment_header_range(TABLE_ANCHOR).coord)
print(review_comments.get_comment_body_range(TABLE_ANCHOR).coord)
print(review_comments.get_response_header_range(TABLE_ANCHOR).coord)
print(review_comments.get_response_body_range(TABLE_ANCHOR).coord)



print(comment_region_rows, comment_region_columns)

for i, header in enumerate(header_list):
    print(i + 1, header)



# DEFAULT_FONT.__init__(name='Aptos', size=10)
# wb = Workbook()
# sht = wb.active
# test_range = CellRange(min_row=1, max_row=1, min_col=1, max_col=3)
# test_cell = Cell(sht, row=1, column=1)
# print(test_cell.coordinate)
# print(test_range.coord, test_range.bounds[0])


project_info_end_row = project_info.get_count
user_note_region_end_column = user_notes.count
header_row = project_info_end_row + PROJECT_INFO_VERTICAL_OFFSET
USER_NOTE_CELL = Cell(worksheet=sht,  row=header_row, column=1)
PROJECT_INFO_CELL = Cell(worksheet=sht, row=1, column=user_note_region_end_column + 1)
COMMENTS_HEADER_CELL = Cell(worksheet=sht, row=header_row, column=user_note_region_end_column + 1)
COMMENTS_BODY_CELL = COMMENTS_HEADER_CELL.offset(1, 0)
USER_NOTE_HEADER_RANGE = CellRange(min_col=1, 
                                   max_col=user_note_region_end_column,
                                   min_row=header_row, 
                                   max_row=header_row)
PROJECT_INFO_RANGE = CellRange(min_col=user_note_region_end_column + 1, 
                               max_col=user_note_region_end_column + 2,
                               min_row=1, 
                               max_row=project_info_end_row)
print(review_comments.comment_column_count)
print(review_comments.evaluations_count + review_comments.backchecks_count)
comment_table_header_end_column = user_note_region_end_column + 1 + comment_region_columns
COMMENTS_HEADER_RANGE = CellRange(min_col=user_note_region_end_column + 1,
                                  max_col=comment_table_header_end_column,
                                  min_row=header_row,
                                  max_row=header_row)

print(f'USER_NOTE_HEADER_RANGE: {USER_NOTE_HEADER_RANGE.coord}')
print(f'PROJECT_INFO_RANGE: {PROJECT_INFO_RANGE.coord}')
print(f'COMMENTS_HEADER_RANGE: {COMMENTS_HEADER_RANGE.coord}')

anchor_row, anchor_column = coordinate_to_tuple(COMMENTS_HEADER_CELL.coordinate)
rows, columns = list_dimensions(all_list)

copy_to_range(user_notes.get_info, worksheet=sht, anchor_cell=USER_NOTE_CELL.coordinate)
# copy_to_range(project_info.get_info, worksheet=sht, anchor_cell=PROJECT_INFO_CELL.coordinate)
# copy_to_range(header_list, worksheet=sht, anchor_cell=COMMENTS_HEADER_CELL.coordinate)
# copy_to_range(all_list, worksheet=sht, anchor_cell=COMMENTS_BODY_CELL.coordinate)


# a_range = sht[str(project_info.get_key_range('H1'))]
# for row in a_range:
#     for cell in row:
#         cell.font = Font('Aptos', size=11, color=WebColor.DARKSLATEBLUE.replace('#',''), bold=True)

# dxf_info_keys = DifferentialStyle(font=Font(name='Courier New', size=12, color=WebColor.tomato.replace('#','')))
# for cell in sht[PROJECT_INFO_RANGE.coord]:
#     cell.font = Font('Courier New', size=12, color=WebColor.tomato.replace('#',''))

# table_range = CellRange(min_row=11,
#                         min_col=1,
#                         max_row=11+125,
#                         max_col=47)

# print(table_range.coord)

# table_style = TableStyleInfo(name="TableStyleMedium9", 
#                              showRowStripes=False, 
#                              showFirstColumn=False, 
#                              showLastColumn=False,
#                              showColumnStripes=False)

# table = Table(displayName='Comments',
#               ref=table_range.coord)

# table.tableStyleInfo = table_style
# if sht is not None:
#     sht.add_table(table)

# wb.close()
# wb.save(xlsx_path)