
import os
from .specsinspec import create_html_reports

from PyQt6.QtWidgets import QApplication, QFileDialog


def batch_create_html() -> str | bool:

    sec_paths, _ = QFileDialog.getOpenFileNames(
        parent=None, 
        caption='Select Files Dialog',
        filter='SEC Files (*.sec);;All Files (*)'
    )

    if len(sec_paths) > 0:
        folder_path = os.path.dirname(sec_paths[0])
        create_html_reports(folder_path)