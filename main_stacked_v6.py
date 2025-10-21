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
from digest_reports import batch_create_reports



def get_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    
    hex_color = f"#{red:02x}{green:02x}{blue:02x}"
    return hex_color



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

        # Create Central Widget to serve as the main widget for the application.

        central_widget = QWidget()
        central_widget.setProperty("class", "central-widget")
        central_widget.setContentsMargins(0, 0, 0, 0)

        central_layout = QHBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)


        # Create the subregions to house all the controls for tools and modules.

        panel_widget = QWidget()
        panel_widget.setProperty('class', 'panel')
        panel_widget.setContentsMargins(0, 0, 0, 0)
        panel_widget.setMinimumWidth(200)
        panel_widget.setMaximumWidth(200)
    
        panel_layout = QVBoxLayout()
        panel_header = QLabel('Panel Region')
        panel_header.setProperty('class', 'header')
        panel_layout.addWidget(panel_header)
        
        panel_layout.setSpacing(12)
        for i in range(5):
            panel_layout.addWidget(QPushButton(f'Button {i + 1}'))
        
        panel_layout.addSpacerItem(VSpacer())
        panel_widget.setLayout(panel_layout)
        
        stage_widget = QWidget()
        stage_widget.setProperty('class', 'stage')
        stage_widget.setContentsMargins(0, 0, 0, 0)
        stage_layout = QStackedLayout()
        stage_widget.setLayout(stage_layout)
        stage_widget.setMinimumWidth(600)

        profile_widget = QWidget()
        profile_widget.setProperty('class', 'profile')
        profile_widget.setContentsMargins(0, 0, 0, 0)   
        profile_widget.setMinimumWidth(200)
        profile_widget.setMaximumWidth(200)
        profile_layout = QVBoxLayout()
        profile_layout.setSpacing(12)

        profile_widget.setLayout(profile_layout)

        profile_header = QLabel('Profile Region')
        profile_header.setProperty('class', 'header')
        profile_thumb = QLabel()
        profile_thumb.setMaximumHeight(150)
        img = QPixmap('./assets/yagura sunrays.png')
        img_scaled = img.scaled(150, 
                                150,
                                Qt.AspectRatioMode.KeepAspectRatio, 
                                Qt.TransformationMode.SmoothTransformation)
        profile_thumb.setPixmap(img_scaled)
        profile_text = QLabel(r"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum")
        profile_text.setWordWrap(True)

        profile_layout.addWidget(profile_header)
        profile_layout.addWidget(profile_thumb)
        profile_layout.addWidget(profile_text)
        profile_layout.addSpacerItem(VSpacer())


        scene_widget = QWidget()
        scene_widget.setProperty('class', 'scene')
        scene_widget.setContentsMargins(0, 0, 0, 0)
        scene_layout = QVBoxLayout()
        scene_layout.setSpacing(12)
        scene_widget.setLayout(scene_layout)

        scene_header = QLabel('Scene Banner')
        scene_header.setProperty('class', 'header')
        scene_body = QWidget()
        scene_body.setProperty('class', 'scene-body')
        scene_body.setContentsMargins(0, 0, 0, 0)
        scene_body_layout = QGridLayout()
        scene_body_layout.setSpacing(12)
        scene_body_layout.setContentsMargins(0, 0, 0, 0)
        scene_body.setLayout(scene_body_layout)

        for i in range(9):
            scene_body_layout.addWidget(QPushButton(f'Button {i + 1}'), i // 3, i % 3)


        scene_layout.addWidget(scene_header)
        scene_layout.addWidget(scene_body)
        scene_layout.addSpacerItem(VSpacer())

        stage_layout.addWidget(scene_widget)

        


        # Create a "Panel" with buttons on the left to control the stage contents

    
        # Finish layout creation
        central_layout.addWidget(panel_widget)
        central_layout.addWidget(stage_widget)
        central_layout.addWidget(profile_widget)

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