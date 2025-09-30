# Copyright (c) 2018-2025 Ben Fisher

from openpyxl import Workbook
from openpyxl.styles import DEFAULT_FONT

from dxbuild.constants import FALLBACKS
from dxbuild.buildtools import timestamp
from dxreport import singlereport

# Debug information
_WRITE_FILE = True
xml_path = './dev/test/data.xml'

# Create workbook object with initial settings
DEFAULT_FONT.__init__(name=FALLBACKS['font_name'], size=FALLBACKS['font_size'])
wb = Workbook()
ws = wb.active

singlereport.create_report(ws, xml_path)

if _WRITE_FILE:
    save_name = f'./dev/test/out/test_{timestamp()}.xlsx'
    wb.save(save_name)
    print(f'{save_name} has been saved.')

wb.close()