
from dxbuild.dxreview import Review
from dxbuild.dxtools import copy_to_range, timestamp, bounds_from_range_string
from dxcore.dxcondition import *

from openpyxl import Workbook
from openpyxl.cell.cell import Cell
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.worksheet.table import Table
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import Rule
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
    # print(status_vector in status_dv)

    high_cnr_rule = Rule(type='expression', dxf=red_dx, formula=['=LOWER($X12)="check and resolve"'])
    high_nc_rule = Rule(type='expression', dxf=yellow_dx, formula=['=LOWER($X12)="non-concur"'])
    high_fio_rule = Rule(type='expression', dxf=green_dx, formula=['=LOWER($X12)="for information only"'])
    high_con_rule = Rule(type='expression', dxf=blue_dx, formula=['=LOWER($X12)="concur"'])
    
    ws.conditional_formatting.add(range_string='X12:X125', cfRule=high_cnr_rule)
    ws.conditional_formatting.add(range_string='X12:X125', cfRule=high_nc_rule)
    ws.conditional_formatting.add(range_string='X12:X125', cfRule=high_fio_rule)
    ws.conditional_formatting.add(range_string='X12:X125', cfRule=high_con_rule)

    cnr_rule = Rule(type='expression', dxf=light_red_dx, formula=['=LOWER($Y12)="check and resolve"'])
    nc_rule = Rule(type='expression', dxf=light_yellow_dx, formula=['=LOWER($Y12)="non-concur"'])
    fio_rule = Rule(type='expression', dxf=light_green_dx, formula=['=LOWER($Y12)="for information only"'])
    con_rule = Rule(type='expression', dxf=light_blue_dx, formula=['=LOWER($Y12)="concur"'])
    
    ws.conditional_formatting.add(range_string='Y12:Y125', cfRule=cnr_rule)
    ws.conditional_formatting.add(range_string='Y12:Y125', cfRule=nc_rule)
    ws.conditional_formatting.add(range_string='Y12:Y125', cfRule=fio_rule)
    ws.conditional_formatting.add(range_string='Y12:Y125', cfRule=con_rule)

    for row in ws.iter_rows(min_row=12, max_row=125, min_col=13, max_col=13):
            for cell in row:
                cell.number_format = 'm/d/yy'


    tables = ws.tables
    table_data = tables.items()
    rng = table_data[0][1]
    # print(f'Table range is {rng}')
    cell_rng = CellRange(rng)
    # print(cell_rng.min_col, cell_rng.max_col,
    #       cell_rng.min_row, cell_rng.max_row)

    table_range = table.ref
    _, max_col, header_row, max_row = bounds_from_range_string(table_range)
    min_row = header_row + 1
    print(min_row, max_row)
    print(max_col)



wb.close()
# wb.save(f'./dev/test/out/test_{timestamp()}.xlsx')




