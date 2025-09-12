from openpyxl.styles import Font, PatternFill, Border
from openpyxl.styles.differential import DifferentialStyle
from .dxcolor import DXColor



highest_red_dx = DifferentialStyle(
    font=Font(name='Aptos', size=11, bold=False, color=DXColor.WHITE), 
    fill=PatternFill(start_color=DXColor.RED.replace('#',''), end_color=DXColor.RED.replace('#',''))
)

highest_yellow_dx = DifferentialStyle(
    font=Font(name='Aptos', size=11, bold=False, color=DXColor.BLACK), 
    fill=PatternFill(start_color=DXColor.YELLOW.replace('#',''), end_color=DXColor.YELLOW.replace('#',''))
)

highest_green_dx = DifferentialStyle(
    font=Font(name='Aptos', size=11, bold=False, color=DXColor.WHITE), 
    fill=PatternFill(start_color=DXColor.GREEN.replace('#',''), end_color=DXColor.GREEN.replace('#',''))
)

highest_blue_dx = DifferentialStyle(
    font=Font(name='Aptos', size=11, bold=False, color=DXColor.WHITE), 
    fill=PatternFill(start_color=DXColor.BLUE.replace('#',''), end_color=DXColor.BLUE.replace('#',''))
)





