from datetime import datetime
from openpyxl import Workbook
from dxgui import dxdialogs
import dxbuild.buildtools as buildtools
from dxbuild.buildtools import autoincrement_name

# Debug information
_WRITE_FILE = False
_SHEET_BASE_NAME = 'Comments'

# Create Workbook and add auto-incremented sheet names
wb = Workbook()

if len(wb.sheetnames) == 1:
    ws1 = wb.active
    ws1.title = _SHEET_BASE_NAME

for i in range(4):
    new_sheet_name = autoincrement_name(_SHEET_BASE_NAME, wb.sheetnames)
    wb.create_sheet(new_sheet_name)

print(wb.sheetnames)

if _WRITE_FILE:
    save_name = f'./dev/test/out/test_{buildtools.timestamp()}.xlsx'
    wb.save(save_name)
    print(f'{save_name} has been saved.')
wb.close()