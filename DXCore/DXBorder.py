from enum import IntEnum

class Weight(IntEnum):
    """Enum mask for XlBorderWeight"""
    Hairline = 1
    Thin = 2
    Medium = -4138
    Thick = 4

class Border(IntEnum):
    """Enum mask for XlBordersIndex"""
    Diagonal_Down = 5
    Diagonal_Up = 6
    Left = 7
    Top = 8
    Right = 10
    Bottom = 9
    Horizontal = 12
    Vertical = 11