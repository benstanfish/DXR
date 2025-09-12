# Copyright (c) 2018-2025 Ben Fisher

from datetime import datetime
from typing import List, Tuple

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils.cell import coordinate_to_tuple

def timestamp(format_string: str=r'%Y%m%d_%H%M%S') -> str:
    """Returns a timestamp, default format: YYYYMMDD_HHMMSS"""
    return datetime.now().strftime(format_string)

def list_dimensions(input_list: List) -> Tuple[int, int]:
    """Returns a Tuple of (Row, Column) count, assuming 1D or 2D Lists."""
    if isinstance(input_list[0], list):
        rows = len(input_list)
        cols = len(input_list[0]) if isinstance(input_list[0], list) else 1
    else:
        rows = 1
        cols = len(input_list)
    return (rows, cols)
    
def copy_to_range(data_list: List, 
                  worksheet: Worksheet | None, 
                  anchor_cell: str='A1'):
    if worksheet is not None:
        anchor_row, anchor_column = coordinate_to_tuple(anchor_cell)
        rows, columns = list_dimensions(data_list)
        if rows == 1:
            for j in range(columns):
                worksheet.cell(row=anchor_row, column=anchor_column + j).value = data_list[j]
        else:
            for i in range(rows):
                for j in range(columns):
                    worksheet.cell(row=anchor_row + i, column=anchor_column + j).value = data_list[i][j]
