import sys
from PyQt6.QtWidgets import (QApplication, 
                             QWidget, 
                             QLabel, 
                             QLineEdit, 
                             QPushButton, 
                             QGridLayout,
                             QVBoxLayout,
                             QHBoxLayout)
from PyQt6.QtCore import Qt


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DXR Suite v1.0")
        self.setGeometry(300, 300, 400, 300)

        layout = QGridLayout()
        self.setLayout(layout)

        run_dxr = QPushButton("Dr Checks Review")
        run_bid = QPushButton("Bidder RFI Log")

        layout.addWidget(run_dxr, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(run_bid, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(
            """ 
            QPushButton {background: transparent; 
                         padding: 24px; 
                         border: 2px solid dodgerblue; 
                         border-radius: 12px;}
            QPushButton::hover {background: dodgerblue;}
            """
        )

        run_dxr.clicked.connect(self.run_dxr_report)
        run_bid.clicked.connect(self.run_bid_report)


    def run_dxr_report(self):
        print('Running DXR report.')


    def run_bid_report(self):
        print('Running bidder report.')







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())