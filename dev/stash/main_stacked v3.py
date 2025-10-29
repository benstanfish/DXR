import random
import sys, os

import logging
import constants
if not os.path.exists(constants.LOG_DIR):
    os.makedirs(constants.LOG_DIR)

import webbrowser
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QStatusBar,
                             QWidget,
                             QLabel,
                             QPushButton,
                             QSpacerItem,
                             QSizePolicy,
                             QGridLayout,
                             QHBoxLayout,
                             QVBoxLayout,
                             QStackedLayout)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt

from dxgui.scene import Panel
from dxcore.dxcolor import WebColor
from dxreport.digest_reports import batch_create_reports



class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"DXR Tools {constants.__version__}")

        window_left = 300
        window_top = 300
        window_width = 1000
        window_height = 600

        self.setGeometry(window_left, window_top, window_width, window_height)
        self.setWindowIcon(QIcon('./assets/Yagura Sunrays.png'))

        central_widget = QWidget()
        central_widget.setProperty("class", "central-widget")
        central_widget.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create left side panel

        
        # panel_layout = QVBoxLayout()
        # panel_layout.setProperty('class', 'panel-layout')
        
        # for i in range(5):
        #     btn = QPushButton(f'Button {i + 1}')
        #     btn.setProperty('class', 'panel-button')
        #     panel_layout.addWidget(btn)
        
        # panel = QWidget()
        # panel.setProperty('class', 'panel')
        # panel.setLayout(panel_layout)

        panel_buttons = []
        for i in range(5):
            btn = QPushButton(f'Button {i + 1}')
            panel_buttons.append(btn)
            
        panel = Panel('panel')
        panel.addButtons(panel_buttons)
        
        




        # Finish layout creation
        layout.addWidget(panel, 1)
        # layout.addWidget(stage, 2)

        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('./dxgui/styles.css') as file:
        styles = file.read()
    app.setStyleSheet(styles)

    window = AppWindow()
    window.show()
    app.exec()