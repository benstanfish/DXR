from enum import IntEnum

class Horizontal(IntEnum):
    """Enum mask for XlHAlign"""
    Center = -4108
    Center_Distributed = 7
    Distributed = -4117
    Fill = 5
    General = 1
    Justify = -4130
    Left = -4131
    Right = -4152

class Vertical(IntEnum):
    """Enum mask for XlVAlign"""
    Bottom = -4107
    Center = -4108
    Middle = Center
    Distributed = -4117
    Justify = -4130
    Top = -4160