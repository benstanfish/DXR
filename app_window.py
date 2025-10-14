import sys
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QMenuBar,
                             QStatusBar,
                             QWidget, 
                             QLabel, 
                             QLineEdit, 
                             QPushButton, 
                             QGridLayout,
                             QHBoxLayout,
                             QVBoxLayout,
                             QSizePolicy)
from PyQt6.QtGui import (QAction, QIcon, QKeySequence)
from PyQt6.QtCore import Qt
from digest_reports import batch_create_reports


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DXR Suite v1.0")
        self.setGeometry(300, 300, 600, 400)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        about_menu = menubar.addMenu('&About')
        
        docs_action = QAction('Documentation', self)
        docs_action.setShortcut('Ctrl+D')

        license_action = QAction('License', self)
        contact_action = QAction('Contact', self)
        
        about_menu.addAction(docs_action)
        about_menu.addSeparator()
        about_menu.addAction(license_action)
        about_menu.addAction(contact_action)


        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Welcome to DXR!')

        vbox_container = QVBoxLayout() 
        
        head_bannder = QHBoxLayout()
        head_bannder.addWidget(QLabel('Header Area'))
        
    
        foot_banner = QHBoxLayout()
        foot_banner.addWidget(QLabel('Footer Area'))


        body = QHBoxLayout()
        


        run_dxr = QPushButton("Dr Checks Review")
        run_bid = QPushButton("Bidder RFI Log")
        body.addWidget(run_dxr)
        body.addWidget(run_bid)

        vbox_container.addLayout(head_bannder)
        vbox_container.addLayout(body)
        vbox_container.addLayout(foot_banner)

        central_widget = QWidget()
        central_widget.setLayout(vbox_container)
        self.setCentralWidget(central_widget)




        # permanent_label = QLabel('Status Bar Permanent Label')
        # self.status_bar.addPermanentWidget(permanent_label)


        


        
        # layout = QVBoxLayout()
        # layout.addWidget(run_dxr, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(run_bid, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(
            """ 
            QHBoxLayout {border: 1px solid tomato;}
            QPushButton {background: transparent; 
                         padding: 24px; 
                         border: 2px solid dodgerblue; 
                         border-radius: 12px;}
            QPushButton::hover {background: dodgerblue;}
            """
        )

        # run_dxr.clicked.connect(self.run_dxr_report)
        # run_bid.clicked.connect(self.run_bid_report)


    def run_dxr_report(self):
        batch_create_reports()
        print('Batch completed')


    def run_bid_report(self):
        print('Running bidder report.')







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())