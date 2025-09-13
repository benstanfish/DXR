# Copyright (c) 2018-2025 Ben Fisher

from datetime import datetime
from typing import List, Tuple, Dict, Literal

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import Rule
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


def start_end_cells_from_range(
        range_string: str | CellRange
    ) -> List:
    """Returns a list of the first and last cells in a range as strings."""
    if isinstance(range_string, CellRange):
        return [f'{get_column_letter(range_string.min_col)}{range_string.min_row}',
                f'{get_column_letter(range_string.max_col)}{range_string.max_row}']
    elif isinstance(range_string, str):
        # Test to see if the passed string is 'range-like'
        import re
        range_pattern = r'\b([a-zA-Z]{1,3}\d{1,7})(:[a-zA-Z]{1,3}\d{1,7}){0,1}\b'
        matches = re.findall(pattern=range_pattern, string=range_string)
        if matches:
            # This is the case where the string appears to be 'range-like'
            # convert to a CellRange and extract the bounds
            temp = CellRange(range_string)
            return [f'{get_column_letter(temp.min_col)}{temp.min_row}',
                    f'{get_column_letter(temp.max_col)}{temp.max_row}']
    # If code continues to this point, the input was invalid and an empty tuple is returned.
    return []


abs_rel_type = Literal['column', 'row', 'both', 'none']
def abs_rel_address(
        range_string: str, 
        type:abs_rel_type='none'
    ) -> str:
    """Returns range-like string with absolute or relative """
    temp = range_string.replace('$','')

    import re
    range_like = r'\b([a-zA-Z]{1,3})(\d{1,7})\b'
    match = re.match(pattern=range_like, string=temp)
    if match:
        whole_match = match.group(0)    # The whole match
        letters = match.group(1)        # Group 1 of the match
        numbers = match.group(2)        # Group 2 of the match
        if type == 'both':
            return '$' + letters + '$' + numbers
        elif type == 'column':
            return '$' + letters + numbers
        elif type == 'row':
            return letters + '$' + numbers
        else:
            return whole_match
    return ''
    

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


def table_header_list(
        worksheet: Worksheet, 
        cell_range: CellRange
    ) -> List:
    """Returns a list of the values in the provide cell range of the worksheet."""
    return [cell.value for cell in [cell for cell in worksheet[cell_range.coord]][0]]


def table_header_dict(
        worksheet: Worksheet, 
        cell_range: CellRange
    ) -> Dict:
    """
    Returns a dictionary of the range values as keys and the order as an index.
    
    Note: the purpose of this function is to work towards the python equivalent of
    ListObject.ListColumn(columnValue).Index -> which gives the index, i.e. column number
    of the list column by the name = columnValue. Note, the index is not the absolute
    column number, but the number starting from the first column. To get the absolute
    number, you would need to add the distance from the table first column to the 
    worksheet first column.
    """
    temp = table_header_list(worksheet, cell_range)
    temp_dict = {}
    for i, value in enumerate(temp):
        if value.lower() not in temp_dict:
            temp_dict[value.lower()] = i + 1
    return temp_dict


def conditionally_format_column(
        range_string: str, 
        check_for_string: str, 
        ws: Worksheet, 
        dxf: DifferentialStyle
    ) -> None:
    """Function that creates conditional format rule and applies it to a table column.

    Args:
        range_string (str): "A1:B10" representation of a range.
        check_for_string (str): _description_
        ws (Worksheet): Openpyxl Worksheet object
        dxf (DifferentialStyle): Openpyxl DifferentialStyle object
    """
    start_cell, end_cell = start_end_cells_from_range(range_string)
    if start_cell:
        formula_string = [f'=LOWER({abs_rel_address(range_string=start_cell, type='column')})="{check_for_string}"']
        cf_rule = Rule(type='expression', 
                        dxf=dxf, 
                        formula=formula_string)
        ws.conditional_formatting.add(range_string=range_string, cfRule=cf_rule)