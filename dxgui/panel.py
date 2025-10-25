
from typing import Tuple
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel 
from .spacers import VSpacer

class Panel(QWidget):
    def __init__(self, 
                 panel_unique_name:str,
                 header_text:str,
                 margins:None,
                 layout_margins:None,
                 spacing:int=0):
        super().__init__()
        # self.setProperty('class', 'panel')
        # self.setObjectName(panel_unique_name)

        if margins is not None:
            super().setContentsMargins(*margins)
        self.panel_unique_name = panel_unique_name
        
        self.layout = QVBoxLayout()
        self.layout.setProperty('class', 'panel-layout')
        if layout_margins is not None:
            self.layout.setContentsMargins(*layout_margins) 
        self.layout.setSpacing(spacing)

        self.header = QLabel(header_text)
        self.header.setProperty('class', 'header')
        self.layout.addWidget(self.header)


        self.layout.addSpacerItem(VSpacer())  # Add spacer at the bottom
        self.setLayout(self.layout) 

    def setMargins(self, left:int, top:int, right:int, bottom:int):
        """Set the contents margins of the panel."""
        self.setContentsMargins(left, top, right, bottom)

    def setLayoutMargins(self, left:int, top:int, right:int, bottom:int):
        """Set the margins of the panel's layout."""
        self.layout.setContentsMargins(left, top, right, bottom)    

    def setMinimumWidth(self, minw):
        return super().setMinimumWidth(minw)
    
    def setMaximumWidth(self, maxw):
        return super().setMaximumWidth(maxw)
    
    def setStyleSheet(self, styleSheet):
        return super().setStyleSheet(styleSheet)
    
    def setClass(self, class_name:str):
        self.setProperty('class', class_name)