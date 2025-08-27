from drchecks_reviews import Review
from utils import timestamp, list_dimensions
import pandas as pd
import numpy as np


from openpyxl import Workbook
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.utils.cell import coordinate_to_tuple
from openpyxl.worksheet.table import Table, TableStyleInfo

xml_path = 'test.xml'
review = Review.from_file(xml_path)
project_info = review.project_info
review_comments = review.review_comments

expansion_type = 'type'
all_list, rows = review_comments.get_all_comments_and_responses(expansion_type=expansion_type)
header_list, columns = review_comments.get_all_comments_and_response_headers(expansion_type=expansion_type)

# df = pd.DataFrame(all_list, columns=header_list)
# df.to_excel(f'all_output_{expansion_type}_{timestamp()}.xlsx', index=False)


# df2 = pd.DataFrame(project_info.get_info)
# print(df2)

# a_comment = review_comments.comments[1]
# print(a_comment.latest_response.remark_type)
# print(a_comment.ball_in_court)

# for comment in review_comments.comments:
#     print(comment.id, comment.ball_in_court)

# print(rows, columns)

# np_list = np.array(header_list)
# print(np_list.shape)




def copy_to_range(data_list, ws, anchor_cell = 'A1'):
    anchor_row, anchor_column = coordinate_to_tuple(anchor_cell)
    rows, columns = list_dimensions(data_list)
    if rows == 1:
        for j in range(columns):
            ws.cell(row=anchor_row, 
                    column=j + anchor_column).value = data_list[j]
    else:
        for i in range(rows):
            for j in range(columns):
                ws.cell(row=i + anchor_row, 
                        column=j + anchor_column).value = data_list[i][j]

xlsx_path = f'export_test_{timestamp()}.xlsx'

wb = Workbook()
ws = wb.active

ANCHOR_CELL = 'H11'
anchor_row, anchor_column = coordinate_to_tuple(ANCHOR_CELL)
rows, columns = list_dimensions(all_list)

copy_to_range(header_list, ws, anchor_cell=ANCHOR_CELL)
copy_to_range(all_list, ws, anchor_cell='H12')

table_range = CellRange(min_row=anchor_row,
                        min_col=anchor_column,
                        max_row=anchor_row+rows,
                        max_col=anchor_column+columns-1)

print(table_range.coord)

table_style = TableStyleInfo(name="TableStyleMedium9", 
                             showRowStripes=False, 
                             showFirstColumn=False, 
                             showLastColumn=False,
                             showColumnStripes=False)

table = Table(displayName='Comments',
              ref=table_range.coord)

table.tableStyleInfo = table_style
ws.add_table(table)

wb.save(xlsx_path)