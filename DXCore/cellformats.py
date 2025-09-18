# Copyright (c) 2018-2025 Ben Fisher

from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from .dxcolor import DXColor
from dxbuild.constants import FALLBACKS

_FONT_NAME = FALLBACKS['font_name']
_FONT_SIZE = FALLBACKS['font_size']



x_border_style = Border(left=Side(border_style='thin', color=DXColor.LIGHT_GRAY_TEXT),
                        bottom=Side(border_style='thin', color=DXColor.LIGHT_GRAY_TEXT),
                        diagonal=Side(border_style='thin', color=DXColor.LIGHT_GRAY_TEXT),
                        diagonalDown=True,
                        diagonalUp=True)



comment_table_style = {
    'font': Font(name=_FONT_NAME, size=9, bold=True),
    'fill': None,
    'border': Border(bottom=Side(border_style='medium', color=DXColor.BLUE)),
    'alignment': Alignment(horizontal='left', vertical='bottom', wrap_text=False) 
}

