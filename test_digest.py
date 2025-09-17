from datetime import datetime

from dxbuild.dxreview import Review
import dxbuild.dxtools as dxtools
from dxcore.dxcondition import *
import dxconfig.settings as dxsettings

from openpyxl import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.cell import get_column_letter
from openpyxl.worksheet.errors import IgnoredError
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.worksheet.table import Table
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import Rule
from openpyxl.styles.alignment import Alignment
from openpyxl.styles import DEFAULT_FONT

_WRITE_FILE = False

xml_path = './dev/test/data.xml'

review = Review.from_file(xml_path)
project_info = review.project_info
all_comments = review.review_comments
user_notes = review.user_notes

DEFAULT_FONT.__init__(name='Aptos', size=10)
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
dxtools.copy_to_range(user_notes_data, worksheet=ws, anchor_cell=USER_DATA_CELL.coordinate)
dxtools.copy_to_range(project_info_data, worksheet=ws, anchor_cell=PROJECT_INFO_CELL.coordinate)
dxtools.copy_to_range(all_comments_data, worksheet=ws, anchor_cell=ALL_COMMENTS_CELL.coordinate)

# Create ListObject, but don't assign a TableStyle since we can only used native options
TABLE_REGION = CellRange(min_row=USER_DATA_CELL.row,
                         max_row=USER_DATA_CELL.row + all_comments.count,
                         min_col=USER_DATA_CELL.column,
                         max_col=user_notes.size[1] + all_comments.size[1],
                         title='comments')

table = Table(displayName='Comments', ref=TABLE_REGION.coord)



if ws is not None:
    ws.add_table(table)
    ws.sheet_view.showGridLines = False
    table_info = dxtools.get_table_info(ws)

    print(review.project_info.regions['region'].coord)
    print(review.project_info.shift_regions(col_shift=review.user_notes.count))
    print(review.project_info.regions['region'].coord)



    top_left_alignment = Alignment(horizontal='left', vertical='top')
    used_range = ws.calculate_dimension()
    for row in ws[used_range]:
        for cell in row:
            if isinstance(cell.value, datetime):
                cell.number_format = 'm/d/yy'
            cell.alignment = top_left_alignment


    open_closed_options = 'Open, Closed'
    status_options = 'Concur, For Information Only, Non-Concur, Check and Resolve'
    
    status_column_letters = dxtools.get_columns_by_name('status', table_info)
    status_columns = dxtools.build_column_vectors(status_column_letters, table_info) # Treat the first occurance separately
    dxtools.add_data_validation_to_column(status_options, status_columns[1:], ws)
    
    first_status_column = dxtools.add_data_validation_to_column(open_closed_options, status_columns[:1], ws)
    dxtools.conditionally_format_range(status_columns[0], 'closed', ws, light_gray_dx, 'H12:BB125', stop_if_true=True)
        
    for column in status_columns[1:]:
        dxtools.conditionally_format_range(column, 'check and resolve', ws, light_red_dx)
        dxtools.conditionally_format_range(column, 'non-concur', ws, light_yellow_dx)
        dxtools.conditionally_format_range(column, 'for information only', ws, light_green_dx)
        dxtools.conditionally_format_range(column, 'concur', ws, light_blue_dx)  
    
    highest_reponse_letters = dxtools.get_columns_by_name('highest resp', table_info)
    highest_response_columns = dxtools.build_column_vectors(highest_reponse_letters, table_info)[0]
    dxtools.add_data_validation_to_column(status_options, [highest_response_columns], ws)
    dxtools.conditionally_format_range(highest_response_columns, 'check and resolve', ws, red_dx)
    dxtools.conditionally_format_range(highest_response_columns, 'non-concur', ws, yellow_dx)
    dxtools.conditionally_format_range(highest_response_columns, 'for information only', ws, green_dx)
    dxtools.conditionally_format_range(highest_response_columns, 'concur', ws, blue_dx)


    critical_options = 'Yes, No'
    critical_column_letters = dxtools.get_columns_by_name('critical', table_info)
    critical_column = dxtools.build_column_vectors(critical_column_letters, table_info)
    dxtools.add_data_validation_to_column(critical_options, critical_column, ws)
    dxtools.conditionally_format_range(critical_column[0], 'yes', ws, red_dx)    
    
    class_options = 'CUI, Unclassified, Public'
    class_column_letters = dxtools.get_columns_by_name('class', table_info)
    class_column = dxtools.build_column_vectors(class_column_letters, table_info)
    dxtools.add_data_validation_to_column(class_options, class_column, ws)
    dxtools.conditionally_format_range(class_column[0], 'cui', ws, red_dx)   
    dxtools.conditionally_format_range(class_column[0], 'unclassified', ws, yellow_dx)
    
    
    
    #TODO: Work through the logic of setting the user column widths.
    
    for i, col_width in enumerate(dxsettings.COMMENT_COLUMN_WIDTHS):
        ws.column_dimensions[get_column_letter(i + 8)].width = col_width
    
    #TODO: Work through the logic of setting widths for the Response columns
    # for i, col_width in enumerate(dxsettings.RESPONSE_COLUMN_WIDTHS):
    #     ws.column_dimensions[get_column_letter(i + 8)].width = col_width

    #TODO: Write function to change the number format for a given column vector
    # for row in ws.iter_rows(min_row=12, max_row=125, min_col=13, max_col=13):
    #         for cell in row:
    #             cell.number_format = 'm/d/yy'
                
    # ws.column_dimensions['S'].width = 70
    for cell in ws['S']:
        cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)

    # ignore_number_as_text = IgnoredError(numberStoredAsText=True)



if _WRITE_FILE:
    save_name = f'./dev/test/out/test_{dxtools.timestamp()}.xlsx'
    wb.save(save_name)
    print(f'{save_name} has been saved.')
wb.close()