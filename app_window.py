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

        central_widget = QWidget()
        layout = QVBoxLayout()

        header = QHBoxLayout()
        body = QGridLayout()
        footer = QHBoxLayout()


        header.addWidget(QLabel('Header'))
        footer.addWidget(QLabel('Footer'))

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Welcome to DXR!')



        run_dxr = QPushButton("Dr Checks Review")
        
        run_bid = QPushButton("Bidder RFI Log")
        body.addWidget(run_dxr, 1, 0)
        body.addWidget(run_bid, 1, 1)


        layout.addItem(header)
        layout.addItem(body)
        layout.addItem(footer)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)




        # permanent_label = QLabel('Status Bar Permanent Label')
        # self.status_bar.addPermanentWidget(permanent_label)


        # layout = QVBoxLayout()
        # layout.addWidget(run_dxr, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(run_bid, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(
            """
            QPushButton {background: transparent;
                         padding: 12px;
                         border: 2px solid dodgerblue;
                         border-radius: 12px;}
            QPushButton::hover {background: dodgerblue;}
            """
        )

        # run_dxr.clicked.connect(self.run_dxr_report)
        # run_bid.clicked.connect(self.run_bid_report)

        run_dxr.clicked.connect(self.run_dxr_report)


    def run_dxr_report(self):
        self.status_bar.showMessage('Running DXR reports...')
        result = batch_create_reports()
        if result:
            self.status_bar.showMessage(f'Report created: {result}.')
        else:
            self.status_bar.showMessage('There was an error in writing the report.')


    def run_bid_report(self):
        print('Running bidder report.')







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    app.exec()