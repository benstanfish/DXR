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


        # Create a "Stage" area on the right to display content
        scenes = [create_scene('Tools'),
                  create_scene('Resources'),
                  create_scene('Help')]

        scene_container = QStackedLayout()
        for scene in scenes:
            scene_container.addWidget(scene)
        scene_container.setProperty("class", "stage-stacked-layout")


        stage = QWidget()
        stage.setProperty("class", "stage")
        stage.setLayout(scene_container)


        # Create a "Panel" with buttons on the left to control the stage contents

        panel_title = QLabel("Modules")
        panel_title.setProperty("class", "panel-title")

        panel_content = QVBoxLayout()
        panel_content.setProperty("class", "panel-content")
        panel_content.setContentsMargins(0, 0, 0, 0)
        panel_content.setSpacing(12)

        btns = []
        for i in range(len(scenes)):
            btn = QPushButton(f'{scene.scene_title.text()}')
            btn.setProperty("class", "panel-button")
            panel_content.addWidget(btn)
            btns.append(btn)

        btns[0].clicked.connect(lambda: scene_container.setCurrentIndex(0))
        btns[1].clicked.connect(lambda: scene_container.setCurrentIndex(1))

        panel_container = QVBoxLayout()
        panel_container.setProperty("class", "panel-container")
        panel_container.addWidget(panel_title)
        panel_container.addLayout(panel_content)    
        panel_container.setContentsMargins(12, 12, 12, 12)

        panel_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        panel_content.addSpacerItem(panel_spacer)

        panel = QWidget()
        panel.setMaximumWidth(200)

        panel.setProperty("class", "panel")
        panel.setLayout(panel_container)




    
        # Finish layout creation
        layout.addWidget(panel, 1)
        layout.addWidget(stage, 2)

        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)


def create_scene(scene_name:str="Tools", button_dict:dict=None) -> QWidget:
    scene_title = QLabel(scene_name)
    scene_title.setProperty("class", "stage-title") 

    stage_grid = QGridLayout()
    stage_grid.setProperty("class", "stage-grid")
    stage_grid.setSpacing(12)

    for i in range(random.randint(4, 9)):
        btn = QPushButton(f"Button {i+1}")
        btn.setProperty("class", "stage-button")
        stage_grid.addWidget(btn, i // 3, i % 3)

    stage_container = QVBoxLayout()
    stage_container.setProperty("class", "stage-container")
    stage_container.addWidget(scene_title)
    stage_container.addLayout(stage_grid)
    stage_container.setContentsMargins(12, 12, 12, 12)

    stage_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    stage_container.addSpacerItem(stage_spacer)

    scene = QWidget()
    scene.setProperty("class", "stage-scene")
    scene.setLayout(stage_container)

    return scene


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('./assets/styles.css') as file:
        styles = file.read()
    app.setStyleSheet(styles)

    window = AppWindow()
    window.show()
    app.exec()