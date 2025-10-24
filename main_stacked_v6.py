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
from PyQt6.QtGui import QPixmap, QIcon, QGuiApplication
from PyQt6.QtCore import Qt, QEvent, pyqtSignal

from dxgui.spacers import VSpacer, HSpacer
from digest_reports import batch_create_reports
from dxmail import open_default_email

_VERSION = '0.0.3a'

def get_rsx_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception as e:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)    


_ICON = get_rsx_path('./assets/Yagura Sunrays.png')
_DEFAULT_PANEL_PANEL_TITLE = 'Tool Explorer'
_DEFAULT_RIGHT_PANEL_IMAGE = './assets/Yagura Starfield.png'
_DEFAULT_RIGHT_PANEL_DESCRIPTION = r"Hover the mouse over a tool button to display an explanation of it's functionality."


class HoverButton(QPushButton):
    hovered = pyqtSignal()
    unhovered = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)

    def enterEvent(self, event: QEvent):
        self.hovered.emit()
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent):
        self.unhovered.emit()
        super().leaveEvent(event)


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"DXR Tools {_VERSION}")
        self.setWindowIcon(QIcon(_ICON))
        
        self.status_bar = self.statusBar()
        self.status_bar.showMessage(f'Welcome to DXR Tools v{_VERSION}')

        window_left = 300
        window_top = 300
        window_width = 1000
        window_height = 600

        self.setGeometry(window_left, window_top, window_width, window_height)
        self.setWindowIcon(QIcon(_ICON))

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
        left_panel_header_label = QLabel('Menu')
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
            'Tools': lambda: stage_layout.setCurrentIndex(0),
            'Links': lambda: stage_layout.setCurrentIndex(1),
            'How Tos': '',
            'About': '',
            'Suggestions?': lambda: open_default_email(to_list=['benstanfish@gmail.com', 'benjamin.s.fisher@usace.army.mil'], 
                                                       cc_list=None, 
                                                       subject=f'DXR App v{_VERSION} Suggestion/Issue', 
                                                       body=f'Hi Ben\n\nI have a suggestion or issue regarding the DXR App v{_VERSION}:\n\n'),
        }

        left_panel_body_layout.addWidget(QLabel(' '))
        for i, (button_name, button_action) in enumerate(left_panel_buttons.items()):
            btn = QPushButton(button_name)
            if button_action:
                btn.clicked.connect(button_action)
            else:
                btn.setDisabled(True)
            left_panel_body_layout.addWidget(btn, i + 1, 0)

        left_panel_layout.addWidget(left_panel_header)
        left_panel_layout.addWidget(left_panel_body)
        left_panel_layout.addSpacerItem(VSpacer())
        exit_button = QPushButton('Quit')
        exit_button.setProperty('class', 'panel-button')
        exit_button.setObjectName('exit_button')
        exit_button.clicked.connect(lambda: self.close())

        left_panel_layout.addWidget(exit_button)
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
        right_panel.setMinimumWidth(300)
    
        right_panel_layout = QVBoxLayout()
        right_panel_layout.setProperty('class', 'right-panel-layout')
        right_panel_layout.setContentsMargins(0, 0, 0, 0)
        right_panel_layout.setSpacing(12)

        right_panel_header = QWidget()
        right_panel_header.setProperty('class', 'right-panel-header')
        self.right_panel_header_label = QLabel(_DEFAULT_PANEL_PANEL_TITLE)
        self.right_panel_header_label.setProperty('class', 'header')
        self.right_panel_header_label.setText('Tool Description')
        right_panel_header.setLayout(QHBoxLayout())
        right_panel_header.layout().addWidget(self.right_panel_header_label)

        right_panel_body = QWidget()
        right_panel_body.setProperty('class', 'right-panel-body')
        right_panel_body.setContentsMargins(0, 0, 0, 0)
        right_panel_body_layout = QGridLayout()
        right_panel_body_layout.setSpacing(12)  
        right_panel_body.setLayout(right_panel_body_layout)


        self.right_panel_image_placeholder = QLabel()
        self.right_panel_image_placeholder.setMaximumHeight(150)
        self.right_panel_image_placeholder.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # self.right_panel_image = QPixmap(_DEFAULT_RIGHT_PANEL_IMAGE)
        # right_panel_image_scaled = self.right_panel_image.scaled(150, 150,
        #                         Qt.AspectRatioMode.KeepAspectRatio, 
        #                         Qt.TransformationMode.SmoothTransformation)
        # self.right_panel_image_placeholder.setPixmap(right_panel_image_scaled)
        self.right_panel_image_placeholder.hide()
        self.right_panel_description = QLabel(_DEFAULT_RIGHT_PANEL_DESCRIPTION)
        self.right_panel_description.setWordWrap(True)

        right_panel_body_layout.addWidget(self.right_panel_image_placeholder)
        right_panel_body_layout.addWidget(self.right_panel_description)

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
        scene0_header_label = QLabel(list(left_panel_buttons.keys())[0])
        scene0_header_label.setProperty('class', 'header')
        scene0_header.setLayout(QHBoxLayout())
        scene0_header.layout().addWidget(scene0_header_label)

        scene0_body = QWidget()
        scene0_body.setProperty('class', 'scene-body')
        scene0_body.setContentsMargins(0, 0, 0, 0)
        scene0_body_layout = QGridLayout()
        # for i in range(3):
        #     scene0_body_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, i)
        scene0_body_layout.setSpacing(12)  
        scene0_body.setLayout(scene0_body_layout)

        scene0_layout.addWidget(scene0_header)
        scene0_layout.addWidget(scene0_body)
        scene0_layout.addSpacerItem(VSpacer())
        scene0.setLayout(scene0_layout)

        scene0_tools = {
            'DrX Review': {
                'action': lambda: batch_create_reports(),
                'image': './assets/drx_review.png',
                'description': r"Process batch process XML reports, exported from ProjNet Dr Checks reviews, into a colorized Excel report. Summary reports also include reviewer statistics for following up on comments.",
                'position': (0, 0, 1, 1)
            },
            'Bidder RFI': {
                'action': '',
                'image': './assets/bidder_rfi.png',
                'description': r"Process Bidder RFIs, exported as HTML files from ProjNet Bidder Module, into an RFI log used by JED and it's A/E consultants for planning bid rfi reponses and track amendments.",
                'position': (0, 1, 1, 1)
            },
            'JDG/JES Tracker': {
                'action': '',
                'image': './assets/jdg_tracker.png',
                'description': r"Tool used by JED TS to summarize the Japan Design Guide (JDG) and Japan Edited Specifications (JES) suggested revisions. Similar to DrX Review, this tool processes XML reports, exporeted from ProjNet Dr Checks reviews, into a summary log.",
                'position': (0, 2, 1, 1)
            },
            'ProjNet Login': {
                'action': lambda: self.open_webpage(url=r'https://projnet.org/projnet/binKornHome/index.cfm'),
                'image': './assets/projnet.png',
                'description': 'Link to the main login page for ProjNet, home to Dr Checks, Bidder Inquiry and other tools. New users can register a new account, or use a Quick-Access Key (provided by their ProjNet review manager) to access the tools from this page.',
                'position': (1, 0, 1, 1)
            },
            'Industry Database': {
                'action': '',
                'image': '',
                'description': r"A database of commonly know Japanese manufacturers, companies, organzations, etc., relating to the design and construction industry. This database is not intended to endorse any particular organization, but is merely a reference tool, intended to help users find a starting point for their own research into the Japanese market.",
                'position': (3, 0, 1, 1)
            },
            'Common Terms Database' : {
                'action': '',
                'image': '',
                'description': 'A small English-Japanese database of terms commonly encountered in design and construction.'
            }
        }

        scene0_buttons = self.create_scene_buttons(scene_body_layout=scene0_body_layout, scene_tools=scene0_tools, are_buttons_automatically_added=False)
        projnet_section = QLabel('ProjNet Related Tools')
        projnet_section.setProperty('class', 'section-header')
        scene0_body_layout.addWidget(projnet_section, 0, 0, 1, 2)
        scene0_body_layout.addWidget(scene0_buttons['ProjNet Login'], 1, 0)
        scene0_body_layout.addWidget(scene0_buttons['DrX Review'], 2, 0)
        scene0_body_layout.addWidget(scene0_buttons['Bidder RFI'], 2, 1)
        scene0_body_layout.addWidget(scene0_buttons['JDG/JES Tracker'], 2, 2)

        industry_section = QLabel('Japanese Industry Resources')
        industry_section.setProperty('class', 'section-header')
        scene0_body_layout.addWidget(industry_section, 3, 0, 1, 2)
        scene0_body_layout.addWidget(scene0_buttons['Industry Database'], 4, 0)
        scene0_body_layout.addWidget(scene0_buttons['Common Terms Database'], 4, 1)




        scene1 = QWidget()
        scene1.setProperty('class', 'scene')
        scene1.setContentsMargins(0, 0, 0, 0)

        scene1_layout = QVBoxLayout()
        scene1_layout.setProperty('class', 'scene-layout')
        scene1_layout.setContentsMargins(0, 0, 0, 0)
        scene1_layout.setSpacing(12)

        scene1_header = QWidget()
        scene1_header.setProperty('class', 'scene-header')
        scene1_header_label = QLabel(list(left_panel_buttons.keys())[1])
        scene1_header_label.setProperty('class', 'header')
        scene1_header.setLayout(QHBoxLayout())
        scene1_header.layout().addWidget(scene1_header_label)

        scene1_body = QWidget()
        scene1_body.setProperty('class', 'scene-body')
        scene1_body.setContentsMargins(0, 0, 0, 0)
        scene1_body_layout = QGridLayout()
        for i in range(3):
            scene1_body_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, i)
        scene1_body_layout.setSpacing(12)  
        scene1_body.setLayout(scene1_body_layout)

        scene1_layout.addWidget(scene1_header)
        scene1_layout.addWidget(scene1_body)
        scene1_layout.addSpacerItem(VSpacer())
        scene1.setLayout(scene1_layout)

        scene1_tools = {
            'JED Resources': {
                'action': lambda: self.open_webpage(url=r'https://www.poj.usace.army.mil/Business-With-Us/References/'),
                'image': './assets/jed_webpage.png',
                'description': r"A link to the USACE Japan Engineer District resources webpage. Use this link to access the most current versions of the Japan Edited Specifications, Japan District Design Guide, Japan District Cost Estimating Guide, etc.",
                'position': (0, 0, 1, 1)
            },
            'ProjNet Login': {
                'action': lambda: self.open_webpage(url=r'https://projnet.org/projnet/binKornHome/index.cfm'),
                'image': './assets/projnet.png',
                'description': 'Link to the main login page for ProjNet, home to Dr Checks, Bidder Inquiry and other tools. New users can register a new account, or use a Quick-Access Key (provided by their ProjNet review manager) to access the tools from this page.',
                'position': (1, 0, 1, 1)
            },
            'UFC/UFGS' : {
                'action': lambda: self.open_webpage(url=r'https://www.wbdg.org/dod'),
                'image': './assets/wbdg.png',
                'description': 'Link to the DoD Unified Facilities Criteria Program resources on Whole Building Design Guide (WBDG), which includes current and past UFCs as well as UFGS specifications and other facilities criteria documents.',
                'position': (2, 0, 1, 1)
            },
            'ERDC Library' : {
                'action': lambda: self.open_webpage(url=r'https://erdc-library.erdc.dren.mil/home'),
                'image': './assets/erdc.png',
                'description': 'Link to the USACE Engineering Research & Development Center (ERDC) knowledge core center (online library of resources).'
            },
            'ICC Codes' : {
                'action': lambda: self.open_webpage(url=r'https://codes.iccsafe.org/'),
                'image': './assets/icc.png',
                'description': 'Link Internation Code Council (ICC) website of online i-code documents, included the IBC, IEBC, IFC, IMC, IPC, IgCC, etc.',
                'position': (2, 1, 1, 1)
            },
            'MLIT (EN)' : {
                'action': lambda: self.open_webpage(url=r'https://www.mlit.go.jp/en/'),
                'image': './assets/mlit_en.png',
                'description': 'Link the the English language version of the Ministry if Land, Infrastructure, Transport and Tourism (MLIT).',
                'position': (3, 0, 1, 1)
            },
            'MLIT (JP)' : {
                'action': lambda: self.open_webpage(url=r'https://www.mlit.go.jp/en/'),
                'image': './assets/mlit_jp.png',
                'description': 'Link the the Japanese language version of the Ministry if Land, Infrastructure, Transport and Tourism (MLIT).',
                'position': (3, 1, 1, 1)
            },
            '' : {
                'action': '',
                'image': '',
                'description': ''
            }
        }


        scene1_buttons = self.create_scene_buttons(scene_body_layout=scene1_body_layout, scene_tools=scene1_tools, are_buttons_automatically_added=False)
        usg_link_section = QLabel('JED/USACE Links')
        usg_link_section.setProperty('class', 'section-header')
        scene1_body_layout.addWidget(usg_link_section, 0, 0, 1, 2)
        scene1_body_layout.addWidget(scene1_buttons['JED Resources'], 1, 0)
        scene1_body_layout.addWidget(scene1_buttons['ERDC Library'], 1, 1)
        scene1_body_layout.addWidget(scene1_buttons['ProjNet Login'], 1, 2)

        us_design_header = QLabel('US Design Links')
        us_design_header.setProperty('class', 'section-header')
        scene1_body_layout.addWidget(us_design_header, 2, 0, 1, 2)
        scene1_body_layout.addWidget(scene1_buttons['UFC/UFGS'], 3, 0)
        scene1_body_layout.addWidget(scene1_buttons['ICC Codes'], 3, 1)

        goj_header = QLabel('GOJ Links')
        goj_header.setProperty('class', 'section-header')
        scene1_body_layout.addWidget(goj_header, 4, 0, 1, 2)
        scene1_body_layout.addWidget(scene1_buttons['MLIT (EN)'], 5, 0)
        scene1_body_layout.addWidget(scene1_buttons['MLIT (JP)'], 5, 1)





        stage_layout.addWidget(scene0)
        stage_layout.addWidget(scene1)
    
        # Finish layout creation
        main_layout.addWidget(left_panel)
        main_layout.addWidget(stage)
        main_layout.addWidget(right_panel)

        main.setLayout(main_layout)
        self.setCentralWidget(main)

    def create_scene_buttons(self, scene_body_layout: QGridLayout, scene_tools: dict, are_buttons_automatically_added: bool=False) -> dict:
        scene_buttons = {}
        for i, (button_name, button_data) in enumerate(scene_tools.items()):
            if button_name:
                scene_buttons[button_name] = HoverButton(button_name)
                scene_buttons[button_name].setProperty('class', 'scene-button')
                if button_data['action']:
                    scene_buttons[button_name].clicked.connect(button_data['action'])
                else:                
                    scene_buttons[button_name].setDisabled(True)
                scene_buttons[button_name].hovered.connect(lambda button_name=button_name, 
                                                image_path=button_data['image'], 
                                                description=button_data['description']: 
                                                self.update_right_panel(header=button_name, 
                                                                            image_path=image_path, 
                                                                            description=description))
                scene_buttons[button_name].unhovered.connect(lambda: self.update_right_panel())
            if are_buttons_automatically_added:
                if button_data['position']:
                    (row, column, row_span, column_span) = button_data['position']
                    scene_body_layout.addWidget(scene_buttons[i], row, column, row_span, column_span) 
                else:
                    scene_body_layout.addWidget(scene_buttons[i], i // 3, i % 3) 
        return scene_buttons


    def update_right_panel(self,
                           header:str=_DEFAULT_PANEL_PANEL_TITLE,
                           image_path:str='',
                           description:str=_DEFAULT_RIGHT_PANEL_DESCRIPTION):
        # Default settings will clear the right panel
        self.right_panel_header_label.setText(header)
        if image_path:
            try:
                temp_image = QPixmap(get_rsx_path(image_path))
                temp_scaled = temp_image.scaled(150, 150,
                                    Qt.AspectRatioMode.KeepAspectRatio, 
                                    Qt.TransformationMode.SmoothTransformation)
                self.right_panel_image_placeholder.show()
                self.right_panel_image_placeholder.setPixmap(temp_scaled)
            except Exception as e:
                print(e)
        else:
            self.right_panel_image_placeholder.setPixmap(QPixmap())
            self.right_panel_image_placeholder.hide()
        self.right_panel_description.setText(description)


    def open_webpage(self, url=r'https://www.poj.usace.army.mil/Business-With-Us/References/'):
        """
        Function to open the specified URL in the default web browser.
        """
        webbrowser.open(url)
        # self.status_bar.showMessage(f'Opening url: {url}')




if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_hints = QGuiApplication.styleHints()
    color_scheme = style_hints.colorScheme()
    if color_scheme == Qt.ColorScheme.Dark:
        with open('./dxgui/dark_theme.css') as file:
            styles = file.read()
    else:
        with open('./dxgui/light_theme.css') as file:
            styles = file.read()
    app.setStyleSheet(styles)

    window = AppWindow()
    window.show()
    app.exec()