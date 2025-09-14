# Copyright (c) 2018-2025 Ben Fisher

"""This module contains non-user settings for Dr Checks Review summaries"""

from enum import IntEnum

class Widths(IntEnum):
    XX_SMALL = 5
    X_SMALL = 8
    SMALL = 10
    MEDIUM = 20
    LARGE = 50
    X_LARGE = 70

COMMENT_COLUMN_WIDTHS = [Widths.SMALL, Widths.SMALL, Widths.MEDIUM, Widths.MEDIUM, 
                         Widths.SMALL, Widths.SMALL, Widths.MEDIUM, Widths.MEDIUM, 
                         Widths.SMALL, Widths.MEDIUM, Widths.MEDIUM, Widths.X_LARGE, 
                         Widths.SMALL, Widths.SMALL, Widths.XX_SMALL, Widths.X_SMALL, Widths.SMALL]

RESPONSE_COLUMN_WIDTHS = [Widths.SMALL, Widths.MEDIUM, Widths.SMALL, Widths.SMALL,  
                          Widths.X_LARGE, Widths.X_SMALL]