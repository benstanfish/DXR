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
                             QVBoxLayout)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt

from dxcore.dxcolor import WebColor
from digest_reports import batch_create_reports


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"DXR Tools {constants.__version__}")
        self.setGeometry(300, 300, 650, 450)
        self.setWindowIcon(QIcon('./assets/Yagura Sunrays.png'))


        central_widget = QWidget()
        layout = QVBoxLayout()

        header = QHBoxLayout()
        body = QGridLayout()
        footer = QHBoxLayout()

        header_banner_height = 50

        banner = QLabel('DXR Tools')
        banner.setProperty('class', 'header')
        banner.setMaximumHeight(header_banner_height)
        
        

        yagura = QLabel()
        yagura_image = QPixmap('./assets/Yagura Starfield.png')
        yagura_image = yagura_image.scaled(header_banner_height, header_banner_height,
                               Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        yagura.setMaximumHeight(header_banner_height)
        yagura.setPixmap(yagura_image)
        yagura.setProperty('class', 'last-logo')


        jed = QLabel()
        jed_image = QPixmap('./assets/icon.ico')
        jed_image = jed_image.scaled(header_banner_height - 4, header_banner_height - 4,
                               Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        jed.setMaximumHeight(header_banner_height)
        jed.setPixmap(jed_image)        


        header.addWidget(banner)
        
        h_spacer = QSpacerItem(20, header_banner_height, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        header.addSpacerItem(h_spacer)


        header.addWidget(jed)
        header.addWidget(yagura)
        
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(0)

        footer_banner = QLabel('Footer')
        footer_banner.setMaximumHeight(75)
        footer.addWidget(footer_banner)
        footer.setContentsMargins(0, 0, 0, 0)
        footer.setSpacing(0)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Welcome to DXR!')

        
        review_button = QPushButton('Dr Checks Review')
        bid_button = QPushButton('Bidder RFI Log')
        jes_tracker_button = QPushButton('JED Guide Tracker')
        manufacturers_button = QPushButton('Manufacturer Database')
        
        proj_net_button = QPushButton('ProjNet')
        jed_button = QPushButton('Working with JED')

        instructions_button = QPushButton('How to Guides')
        about_button = QPushButton('About')

        tools_section = QLabel('Tools')
        tools_section.setProperty('class', 'section-header')
        body.addWidget(tools_section, 0, 0, 1, 3)
        body.addWidget(review_button, 1, 0)
        body.addWidget(bid_button, 1, 1)
        body.addWidget(jes_tracker_button, 1, 2)       
        body.addWidget(manufacturers_button, 2, 0)

        resources_section = QLabel('Resources')
        resources_section.setProperty('class', 'section-header')  
        body.addWidget(resources_section, 3, 0, 1, 3)
        body.addWidget(proj_net_button, 4, 0)   
        body.addWidget(jed_button, 4, 1)
        
        help_section = QLabel('Help')
        help_section.setProperty('class', 'section-header')
        body.addWidget(help_section, 5, 0, 1, 3)
        body.addWidget(instructions_button, 6, 0)
        body.addWidget(about_button, 6, 1)

        disabled_buttons = [bid_button, 
                            jes_tracker_button, 
                            manufacturers_button, 
                            instructions_button, 
                            about_button]
        for button in disabled_buttons:
            button.setEnabled(False)


        body.setContentsMargins(0, 12, 0, 12)
        body.setSpacing(12)


        layout.addItem(header)
        layout.addItem(body)
        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        # layout.addItem(footer)

        central_widget.setLayout(layout)
        central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_widget)


        review_button.clicked.connect(self.run_dxr_report)
        proj_net_button.clicked.connect(lambda: self.open_webpage(url=r'https://projnet.org/projnet/binKornHome/index.cfm'))
        jed_button.clicked.connect(lambda: self.open_webpage(url=r'https://www.poj.usace.army.mil/Business-With-Us/References/'))

    def run_dxr_report(self):
        self.status_bar.showMessage('Running DXR reports...')
        result = batch_create_reports()
        if result:
            self.status_bar.showMessage(f'Report created: {result}.')
        else:
            self.status_bar.showMessage('There was an error in writing the report.')


    def run_bid_report(self):
        print('Running bidder report.')

    def open_webpage(self, url=r'https://www.poj.usace.army.mil/Business-With-Us/References/'):
        """
        Function to open the specified URL in the default web browser.
        """
        webbrowser.open(url)
        self.status_bar.showMessage(f'Opening url: {url}')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('./dxgui/styles.css') as file:
        styles = file.read()
    app.setStyleSheet(styles)

    window = AppWindow()
    window.show()
    app.exec()