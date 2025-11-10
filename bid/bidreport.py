# Copyright (c) 2018-2025 Ben Fisher

import os, sys, shutil

from openpyxl import load_workbook
from openpyxl.styles import DEFAULT_FONT

from PyQt6.QtWidgets import QApplication, QFileDialog
from .bidconstants import FALLBACKS, timestamp
from .bidhtml import read_bid_html_to_list

import dxbuild.buildtools as buildtools

template_path = './bid/template.xlsx'




def create_bid_log() -> str | bool:

    _WRITE_FILE = True

    DEFAULT_FONT.__init__(name=FALLBACKS['font_name'], size=FALLBACKS['font_size'])

    html_path, _ = QFileDialog.getOpenFileName(
        parent=None, 
        caption='Select File Dialog',
        filter='HTML Files (*.html);;All Files (*)'
    )

    copied_file_path = os.path.join(os.path.dirname(html_path), f'Bidder RFI Log {timestamp('%Y-%m-%d %H-%M-%S')}.xlsx')
    copied_file = shutil.copy(template_path, copied_file_path)

    try:
        wb = load_workbook(copied_file)
    except FileNotFoundError as e:
        print(f'Could not find the template file: {e}')
        exit()

    # Check to see if the user selected any files or cancelled the file select dialog.
    if len(html_path) > 0:
        bidder_rfis = read_bid_html_to_list(html_path=html_path)
        if bidder_rfis:

            print('Will create new sheet')
            ws = wb.create_sheet('Bidder RFIs', index=3)

            comments_list = read_bid_html_to_list(html_path)
            buildtools.copy_to_range(comments_list, worksheet=ws, anchor_cell='A10')


        if _WRITE_FILE:
            # copied_file_path = os.path.join(os.path.dirname(html_path[0]), f'Bidder RFI Log {timestamp('%Y-%m-%d %H-%M-%S')}.xlsx')
            wb.save(copied_file_path)
        wb.close()
        print(f'{copied_file_path} written to disk.')
        # os.startfile(os.path.dirname(copied_file_path))
        # os.startfile(copied_file_path)
        return copied_file_path
    else:
        return False
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    create_bid_log()
    exit()
    sys.exit(app.exec())