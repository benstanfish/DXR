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
from dxgui.spacers import VSpacer, HSpacer
from dxgui.panel import Panel
from digest_reports import batch_create_reports


_TYPICAL_SPACING = 12
_OUTER_MARGINS = (0, 0, 0, 0)
_INNER_MARGINS = (6, 6, 6, 6)
_SPACING = 12


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"DXR Tools {constants.__version__}")
        self.setWindowIcon(QIcon('./assets/Yagura Sunrays.png'))

        window_left = 300
        window_top = 300
        window_width = 1000
        window_height = 600

        self.setGeometry(window_left, window_top, window_width, window_height)
        self.setWindowIcon(QIcon('./assets/Yagura Sunrays.png'))

        # Create Central Widget to serve as the main widget for the application.
        main = QWidget()
        main.setProperty("class", "main-widget")
        main.setContentsMargins(0, 0, 0, 0)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)


        # Create the subregions to house all the controls for tools and modules.

        right_panel = QWidget()
        right_panel.setProperty('class', 'right-panel')
        right_panel.setContentsMargins(0, 0, 0, 0)
        right_panel.setMinimumWidth(200)
        right_panel.setMaximumWidth(200)
    
        right_panel_layout = QVBoxLayout()
        right_panel_layout.setProperty('class', 'right-panel-layout')
        right_panel_layout.setContentsMargins(0, 0, 0, 0)
        right_panel_layout.setSpacing(12)

        right_panel_header = QWidget()
        right_panel_header.setProperty('class', 'right-panel-header')
        right_panel_header_label = QLabel('Right Panel Header')
        right_panel_header_label.setProperty('class', 'header')
        right_panel_header.setLayout(QHBoxLayout())
        right_panel_header.layout().addWidget(right_panel_header_label)

        right_panel_body = QWidget()
        right_panel_body.setProperty('class', 'right-panel-body')
        right_panel_body.setContentsMargins(0, 0, 0, 0)
        right_panel_body_layout = QGridLayout()
        right_panel_body_layout.setSpacing(12)  
        right_panel_body.setLayout(right_panel_body_layout)

        for i in range(5):
            right_panel_body_layout.addWidget(QPushButton(f'Button {i + 1}'), i, 0)



        right_panel_layout.addWidget(right_panel_header)
        right_panel_layout.addWidget(right_panel_body)
        right_panel_layout.addSpacerItem(VSpacer())
        right_panel.setLayout(right_panel_layout)
            










        stage = QWidget()
        stage.setProperty('class', 'stage')
        stage.setContentsMargins(0, 0, 0, 0)
        stage_layout = QStackedLayout()
        stage.setLayout(stage_layout)
        stage.setMinimumWidth(600)

        profile = QWidget()
        profile.setProperty('class', 'profile')
        profile.setContentsMargins(0, 0, 0, 0)   
        profile.setMinimumWidth(200)
        profile.setMaximumWidth(200)
        profile_layout = QVBoxLayout()
        profile_layout.setSpacing(12)

        profile.setLayout(profile_layout)

        profile_header = QLabel('Profile Region')
        profile_header.setProperty('class', 'header')
        profile_image_placeholder = QLabel()
        profile_image_placeholder.setMaximumHeight(150)
        profile_image = QPixmap('./assets/yagura sunrays.png')
        profile_image_scaled = profile_image.scaled(150, 
                                150,
                                Qt.AspectRatioMode.KeepAspectRatio, 
                                Qt.TransformationMode.SmoothTransformation)
        profile_image_placeholder.setPixmap(profile_image_scaled)
        profile_description = QLabel(r"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum")
        profile_description.setWordWrap(True)

        profile_layout.addWidget(profile_header)
        profile_layout.addWidget(profile_image_placeholder)
        profile_layout.addWidget(profile_description)
        profile_layout.addSpacerItem(VSpacer())


        scene = QWidget()
        scene.setProperty('class', 'scene')
        scene.setContentsMargins(0, 0, 0, 0)
        scene_layout = QVBoxLayout()
        scene_layout.setSpacing(12)
        scene.setLayout(scene_layout)

        scene_header = QLabel('Scene Banner')
        scene_header.setProperty('class', 'header')
        scene_body = QWidget()
        scene_body.setProperty('class', 'scene-body')
        scene_body.setContentsMargins(0, 0, 0, 0)
        scene_body_layout = QGridLayout()
        scene_body_layout.setSpacing(12)
        scene_body_layout.setContentsMargins(0, 0, 0, 0)
        scene_body.setLayout(scene_body_layout)

        # for i in range(9):
        #     scene_body_layout.addWidget(QPushButton(f'Button {i + 1}'), i // 3, i % 3)


        scene_layout.addWidget(scene_header)
        scene_layout.addWidget(scene_body)
        scene_layout.addSpacerItem(VSpacer())

        stage_layout.addWidget(scene)


    
        # Finish layout creation
        main_layout.addWidget(right_panel)
        main_layout.addWidget(stage)
        main_layout.addWidget(profile)

        main.setLayout(main_layout)
        self.setCentralWidget(main)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('./dxgui/styles.css') as file:
        styles = file.read()
    app.setStyleSheet(styles)


    window = AppWindow()
    window.show()
    app.exec()