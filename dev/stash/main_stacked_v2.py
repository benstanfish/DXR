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

from dxgui.scene import Scene   
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

        tool_buttons = {
            "Dr Checks Review": lambda: batch_create_reports(),  
            "RFI Bidder Log": lambda: print("Button 2 clicked"),
            "JDDG/JES Change Tracker": lambda: print("Button 3 clicked")
        }

        resc_buttons = {
            "Resource 1": lambda: print("Resource 1 clicked"),  
            "Resource 2": lambda: print("Resource 2 clicked"),
            "Resource 3": lambda: print("Resource 3 clicked"),
            "Resource 4": lambda: print("Resource 4 clicked")
        }

        tool_scene = Scene(scene_name='Tools', button_dict=tool_buttons)
        resc_scene = Scene(scene_name='Resources', button_dict=resc_buttons)
        help_scene = Scene(scene_name='Help')
        scenes = [tool_scene, 
                  resc_scene, 
                  help_scene]

        scene_container = QStackedLayout()
        for scene in scenes:
            scene_container.addWidget(scene)
        scene_container.setProperty("class", "scene-container")

        stage = QWidget()
        stage.setProperty("class", "stage")
        stage.setLayout(scene_container)


        # Create a "Panel" with buttons on the left to control the stage contents
        
        panel_buttons = {
            "Tools": lambda: scene_container.setCurrentIndex(0),  
            "Resources": lambda: scene_container.setCurrentIndex(1),
            "Info": lambda: scene_container.setCurrentIndex(2)  
        }
        panel = Scene(scene_name='Modules', scene_id='panel', button_dict=panel_buttons, col_count=1)
        panel.setMaximumWidth(200)

    
        # Finish layout creation
        layout.addWidget(panel, 1)
        layout.addWidget(stage, 2)

        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('./assets/styles.css') as file:
        styles = file.read()
    app.setStyleSheet(styles)

    window = AppWindow()
    window.show()
    app.exec()