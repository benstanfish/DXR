"""
This module provides the functions for communicating Dr Checks data to Excel
including the styling elements.
"""

from openpyxl import Workbook
from DXBuild.DXTools import timestamp

file_path = f'excel_test_{timestamp}.xlsx'

wb = Workbook()
ws = wb.active

ANCHOR_CELL = 'H11'




wb.save(file_path)