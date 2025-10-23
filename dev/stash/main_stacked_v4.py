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

from dxcore.dxcolor import WebColor
from digest_reports import batch_create_reports
from dxgui.spacers import VSpacer, HSpacer


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
        central_widget.setProperty('class', 'central-container')

        central_layout = QHBoxLayout()
        central_layout.setProperty('class', 'central-layout')
        central_layout.setContentsMargins(0, 0, 0, 0)

        panel = QWidget()
        panel.setProperty('class', 'panel')

        panel_layout = QVBoxLayout()
        panel_layout.setProperty('class', 'panel-layout')
        panel.setLayout(panel_layout)       

        panel_header = QLabel('Panel')
        panel_header.setProperty('class', 'header')
        panel_layout.addWidget(panel_header)
        for i in range(6):
            btn = QPushButton(f'Module {i + 1}')
            btn.setProperty('class', 'panel-button')
            panel_layout.addWidget(btn)
        
        
        panel_layout.addSpacerItem(VSpacer())



        scene1 = QWidget()
        scene1.setProperty('class', 'scene')
        scene1_layout = QGridLayout()
        scene1.setLayout(scene1_layout)
        scene1_header = QLabel('Scene 1')
        scene1_header.setProperty('class', 'header')
        scene1_layout.addWidget(scene1_header, 0, 0)
        



        stage = QWidget()
        stage.setProperty('class', 'stage')

        stage_layout = QStackedLayout()
        stage_layout.setProperty('class', 'stage-layout')
        stage_layout.setContentsMargins(0, 0, 0, 0)
        stage.setLayout(stage_layout)

        stage_layout.addWidget(scene1)
        








        central_layout.addWidget(panel)
        central_layout.addWidget(stage)
        central_layout.addSpacerItem(HSpacer())



        # Finish layout creation
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('./dxgui/styles.css') as file:
        styles = file.read()
    app.setStyleSheet(styles)

    window = AppWindow()
    window.show()
    app.exec()