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
from PyQt6.QtCore import Qt, QEvent


from dxcore.dxcolor import WebColor
from dxgui.spacers import VSpacer, HSpacer
from dxgui.panel import Panel
from digest_reports import batch_create_reports


_TYPICAL_SPACING = 12
_OUTER_MARGINS = (0, 0, 0, 0)
_INNER_MARGINS = (6, 6, 6, 6)
_SPACING = 12


class HoverButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def enterEvent(self, event: QEvent):
        """Called when the mouse cursor enters the widget."""
        print(f"Mouse entered {self.text()} button!")
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent):
        """Called when the mouse cursor leaves the widget."""
        print(f"Mouse left {self.text()} button!")
        super().leaveEvent(event)


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

        left_panel = QWidget()
        left_panel.setProperty('class', 'left-panel')
        left_panel.setContentsMargins(0, 0, 0, 0)
        left_panel.setMinimumWidth(200)
        left_panel.setMaximumWidth(200)
    
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setProperty('class', 'left-panel-layout')
        left_panel_layout.setContentsMargins(0, 0, 0, 0)
        left_panel_layout.setSpacing(12)

        left_panel_header = QWidget()
        left_panel_header.setProperty('class', 'left-panel-header')
        left_panel_header_label = QLabel('Left Panel Header')
        left_panel_header_label.setProperty('class', 'header')
        left_panel_header.setLayout(QHBoxLayout())
        left_panel_header.layout().addWidget(left_panel_header_label)

        left_panel_body = QWidget()
        left_panel_body.setProperty('class', 'left-panel-body')
        left_panel_body.setContentsMargins(0, 0, 0, 0)
        left_panel_body_layout = QGridLayout()
        left_panel_body_layout.setSpacing(12)  
        left_panel_body.setLayout(left_panel_body_layout)

        left_panel_buttons = {
            'Review Tools': lambda: print('Hello World'),
            'Library': lambda: print('test two'),
            'Resources': ''
        }

        for i, (button_name, button_action) in enumerate(left_panel_buttons.items()):
            btn = QPushButton(button_name)
            if button_action:
                btn.clicked.connect(button_action)
            else:
                btn.setDisabled(True)
            left_panel_body_layout.addWidget(btn, i, 0)

        left_panel_layout.addWidget(left_panel_header)
        left_panel_layout.addWidget(left_panel_body)
        left_panel_layout.addSpacerItem(VSpacer())
        left_panel.setLayout(left_panel_layout)
            


        # The stage is the stacked layout widget that will host all the content layouts ('scenes')
        stage = QWidget()
        stage.setProperty('class', 'stage')
        stage.setContentsMargins(0, 0, 0, 0)
        stage_layout = QStackedLayout()
        stage.setLayout(stage_layout)
        stage.setMinimumWidth(600)


        # Create a right panel bar

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

        right_panel_image_placeholder = QLabel()
        right_panel_image_placeholder.setMaximumHeight(150)
        right_panel_image_placeholder.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        right_panel_image = QPixmap('./assets/yagura sunrays.png')
        right_panel_image_scaled = right_panel_image.scaled(150, 150,
                                Qt.AspectRatioMode.KeepAspectRatio, 
                                Qt.TransformationMode.SmoothTransformation)
        right_panel_image_placeholder.setPixmap(right_panel_image_scaled)
        right_panel_description = QLabel(r"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum")
        right_panel_description.setWordWrap(True)

        right_panel_body_layout.addWidget(right_panel_image_placeholder)
        right_panel_body_layout.addWidget(right_panel_description)

        right_panel_layout.addWidget(right_panel_header)
        right_panel_layout.addWidget(right_panel_body)
        right_panel_layout.addSpacerItem(VSpacer())
        right_panel.setLayout(right_panel_layout)






        scene0 = QWidget()
        scene0.setProperty('class', 'scene')
        scene0.setContentsMargins(0, 0, 0, 0)

        scene0_layout = QVBoxLayout()
        scene0_layout.setProperty('class', 'scene-layout')
        scene0_layout.setContentsMargins(0, 0, 0, 0)
        scene0_layout.setSpacing(12)

        scene0_header = QWidget()
        scene0_header.setProperty('class', 'scene-header')
        scene0_header_label = QLabel('Scene Header')
        scene0_header_label.setProperty('class', 'header')
        scene0_header.setLayout(QHBoxLayout())
        scene0_header.layout().addWidget(scene0_header_label)

        scene0_body = QWidget()
        scene0_body.setProperty('class', 'scene-body')
        scene0_body.setContentsMargins(0, 0, 0, 0)
        scene0_body_layout = QGridLayout()
        scene0_body_layout.setSpacing(12)  
        scene0_body.setLayout(scene0_body_layout)

        scene0_layout.addWidget(scene0_header)
        scene0_layout.addWidget(scene0_body)
        scene0_layout.addSpacerItem(VSpacer())
        scene0.setLayout(scene0_layout)

        for i in range(8):
            btn = HoverButton(f'Button {i + 1}')
            btn.setProperty('class', 'scene-button')
            btn.setMouseTracking(True)
            btn.clicked.connect(lambda: print(f'Button {i + 1} clicked'))
            btn.enterEvent(print(f'Button {i + 1} mouse over'))
            btn.leaveEvent(print(f'Button {i + 1} mouse over'))
            scene0_body_layout.addWidget(btn, i // 3, i % 3)

        stage_layout.addWidget(scene0)


    
        # Finish layout creation
        main_layout.addWidget(left_panel)
        main_layout.addWidget(stage)
        main_layout.addWidget(right_panel)

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