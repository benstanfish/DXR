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
        layout = QHBoxLayout()



     




        central_widget.setLayout(layout)
        central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('./assets/styles.css') as file:
        styles = file.read()
    app.setStyleSheet(styles)

    window = AppWindow()
    window.show()
    app.exec()