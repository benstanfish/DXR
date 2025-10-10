import sys, os
from PyQt6.QtWidgets import (
    QApplication, 
    QFileDialog, 
    QWidget
)


class GetFilesDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Select File(s) Dialog')
        self.setGeometry(300, 300, 600, 400)

        file_names, _ = QFileDialog.getOpenFileNames(
            parent=self, 
            caption='Select Files Dialog',
            filter='XML Files (*.xml);;HTML Files (*.html);;All Files (*)')
        
        for file_name in file_names:
            print(file_name)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GetFilesDialog()
    window.show()
    sys.exit(app.exec())