import sys, os
from typing import List, Tuple, Dict, Any, Literal
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon

_DIALOG_TYPES = Literal['critical', 'warning', 'info', 'question', 'no_icon']

class SelectFileDialog(QFileDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

    def get_files(self,
                  caption='Select Files Dialog',
                  filter='XML Files (*.xml);;HTML Files (*.html);;All Files (*)'):
        self.paths, _ = self.getOpenFileNames(None, caption=caption, filter=filter)
        return self.paths


class SelectFolderDialog():
    pass


class SaveAsDialog(QFileDialog):
    pass


class InfoDialog(QMessageBox):
    
    def __init__(self):
        super().__init__()

    def show(self, 
             type:_DIALOG_TYPES='info',
             title='Dialog Window',
             text='Success!',
             buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel):
        self.dialog = QMessageBox(self)
        self.setWindowIcon(QIcon('./rsx/img/icon.ico'))
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(buttons)
        if type=='critical':
            self.setIcon(QMessageBox.Icon.Critical)
        elif type=='warning':
            self.setIcon(QMessageBox.Icon.Warning)
        elif type=='info':
            self.setIcon(QMessageBox.Icon.Information)
        elif type=='question':
            self.setIcon(QMessageBox.Icon.Question)
        else:
            self.setIcon(QMessageBox.Icon.NoIcon)
        self.exec()


class AboutDialog:
    pass


class TroubleDialog:
    pass



class _TestApplication():
    from PyQt6.QtWidgets import QApplication
    test_app = QApplication([])

    dialog = InfoDialog()
    dialog.show(type='no_icon')

    test_app.quit()