# Copyright (c) 2018-2025 Ben Fisher

from datetime import datetime
from typing import List, Tuple

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils.cell import coordinate_to_tuple, get_column_letter
from openpyxl.worksheet.cell_range import CellRange

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
    
def copy_to_range(
    data_list: List, 
    worksheet: Worksheet | None, 
    anchor_cell: str='A1'
) -> None:
    """Copy a 1D or 2D list to worksheet via Openpyxl."""
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

def range_string_from_bounds(
    min_row: int, 
    max_row: int, 
    min_col: int, 
    max_col: int,
    min_row_abs: bool=False,
    max_row_abs: bool=False,
    min_col_abs: bool=False,
    max_col_abs: bool=False
) -> str:
    """Return range string from row, column bounds. Allows for partwise absolute referencing."""
    start_col_letter = get_column_letter(min_col)
    end_col_letter = get_column_letter(max_col)
    
    return f'{"$" if min_row_abs else ""}{start_col_letter}{"$" if max_row_abs else ""}{min_row}' \
           f':{"$" if min_col_abs else ""}{end_col_letter}{"$" if max_col_abs else ""}{max_row}'

def bounds_from_range_string(
    range_string: str 
) -> tuple[int, int, int, int]:
    #split at ':'
    return (1, 1, 1, 1)



# def cell_range_from_tuple(
#         cell_bounds: Tuple[int, int, int, int]
#     ) -> CellRange:
#     """Return Openpyxl CellRange from tuple of the row, column bounds."""
#     return CellRange(min_row = cell_bounds[0],
#                      max_row = cell_bounds[1],
#                      min_col = cell_bounds[2],
#                      max_col = cell_bounds[3])