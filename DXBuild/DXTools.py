# Copyright (c) 2018-2025 Ben Fisher

from datetime import datetime
from typing import List, Tuple, Dict

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils.cell import coordinate_to_tuple, get_column_letter
from openpyxl.worksheet.cell_range import CellRange


def timestamp(
        format_string: str=r'%Y%m%d_%H%M%S'
    ) -> str:
    """Returns a timestamp, default format: YYYYMMDD_HHMMSS"""
    return datetime.now().strftime(format_string)


def list_dimensions(
        input_list: List
    ) -> Tuple[int, int]:
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
        min_col: int, 
        max_col: int,
        min_row: int, 
        max_row: int, 
        min_col_abs: bool=False,
        max_col_abs: bool=False,
        min_row_abs: bool=False,
        max_row_abs: bool=False
    ) -> str:
    """Return range string from row, column bounds. Allows for partwise absolute referencing."""
    start_col_letter = get_column_letter(min_col)
    end_col_letter = get_column_letter(max_col)
    
    return f'{"$" if min_col_abs else ""}{start_col_letter}' \
           f'{"$" if min_row_abs else ""}{min_row}' \
           f':{"$" if max_col_abs else ""}{end_col_letter}' \
           f'{"$" if max_row_abs else ""}{max_row}'


def bounds_from_range_string(
        range: str | CellRange
    ) -> tuple:
    """Returns the tuple of row, column min, max bounds from a CellRange or range-like string."""
    if isinstance(range, CellRange):
        return (range.min_col, range.max_col, range.min_row, range.max_row)
    elif isinstance(range, str):
        # Test to see if the passed string is 'range-like'
        import re
        range_like = r'\b[a-zA-Z]{1,3}\d{1,7}\b'
        matches = re.findall(pattern=range_like, string=range)
        if matches:
            # This is the case where the string appears to be 'range-like'
            # convert to a CellRange and extract the bounds
            temp = CellRange(range)
            return (temp.min_col, temp.max_col, temp.min_row, temp.max_row)
    # If code continues to this point, the input was invalid and an empty tuple is returned.
    return ()


def autoincrement_name(
        base_name: str, 
        search_list: List
    ) -> str:
    """Returns the base_name with next largest integer suffixed if name already exists in search_list."""
    base_name_length = len(base_name)
    temp = []
    for thing in search_list:
        if thing[:base_name_length] == base_name:
            temp.append(thing)
    if len(temp):
        # This block executes if there are potential collisions with the base name
        max_number = 0
        for thing in temp:
            if len(thing) > base_name_length:
                curr_num = int(thing[base_name_length:])
                if curr_num > max_number:
                    max_number = curr_num
        return base_name + str(max_number + 1)
    # If no collisions, the base name is returned.
    return base_name


def range_values_to_list(
        worksheet: Worksheet, 
        cell_range: CellRange
    ) -> List:
    """Returns a list of the values in the provide cell range of the worksheet."""
    return [cell.value for cell in [cell for cell in worksheet[cell_range.coord]][0]]

def range_values_to_dict(
        worksheet: Worksheet, 
        cell_range: CellRange
    ) -> Dict:
    """Returns a dictionary of the range values as keys and the order as an index."""
    temp = range_values_to_list(worksheet, cell_range)
    temp_dict = {}
    for i, value in enumerate(temp):
        if value.lower() not in temp_dict:
            temp_dict[value.lower()] = i + 1
    return temp_dict