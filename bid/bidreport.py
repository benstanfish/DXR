# Copyright (c) 2018-2025 Ben Fisher

import os, sys

from openpyxl import Workbook
from openpyxl.styles import DEFAULT_FONT
from openpyxl.worksheet.worksheet import Worksheet

from PyQt6.QtWidgets import QApplication, QFileDialog
from bidconstants import FALLBACKS, timestamp
from bidhtml import read_bid_html_to_list


def batch_create_reports() -> str | bool:

    _WRITE_FILE = True

    DEFAULT_FONT.__init__(name=FALLBACKS['font_name'], size=FALLBACKS['font_size'])
    wb = Workbook()
    
    html_path, _ = QFileDialog.getOpenFileName(
        parent=None, 
        caption='Select File Dialog',
        filter='HTML Files (*.html);;All Files (*)'
    )

    # Check to see if the user selected any files or cancelled the file select dialog.
    if len(html_path) > 0:
        bidder_rfis = read_bid_html_to_list(html_path=html_path)
        if bidder_rfis:
            if len(wb.sheetnames) == 1: 
                ws = wb.active
                ws.title = 'Bidder RFIs'

                

            else:
                pass  
        if _WRITE_FILE:
            save_name = os.path.join(os.path.dirname(html_path[0]), f'Bidder RFI Log {timestamp('%Y-%m-%d %H-%M-%S')}.xlsx')
            wb.save(save_name)
        wb.close()
        print(f'{save_name} written to disk.')
        os.startfile(os.path.dirname(save_name))
        os.startfile(save_name)
        return save_name
    else:
        return False
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    batch_create_reports()
    sys.exit(app.exec())