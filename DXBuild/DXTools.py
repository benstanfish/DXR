from datetime import datetime
from typing import List, Tuple

def timestamp(format_string: str=r'%Y%m%d_%H%M%S') -> str:
    """Returns a timestamp, default format: YYYYMMDD_HHMMSS"""
    return datetime.now().strftime(format_string)

def list_dimensions(a_list: List) -> Tuple[int, int]:
    """Returns a Tuple of (Row, Column) count, assuming 1D or 2D Lists."""
    if isinstance(a_list[0], list):
        return (len(a_list), len(a_list[0]))
    else: 
        return (1, len(a_list))