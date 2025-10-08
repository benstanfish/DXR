# Copyright (c) 2018-2025 Ben Fisher

from openpyxl import Workbook
from openpyxl.styles import DEFAULT_FONT

from dxbuild.reviews import Review
from dxbuild.constants import FALLBACKS
from dxbuild.buildtools import timestamp, is_valid_root
from dxreport import singlereport

from PyQt6.QtWidgets import QApplication, QFileDialog
import sys

# Debug information
_WRITE_FILE = False
xml_path = './dev/test/data.xml'

app = QApplication(sys.argv)
xml_paths, _ = QFileDialog.getOpenFileNames(
    parent=None, 
    caption='Select Files Dialog',
    filter='XML Files (*.xml);;HTML Files (*.html);;All Files (*)'
)

for xml_path in xml_paths:
    # if is_valid_root(xml_path):
    #     print(xml_path, is_valid_root(xml_path))
    # else:
    #     print(xml_path, 'passed')
    if is_valid_root(xml_path=xml_path):
        try:
            review = Review.from_file(xml_path)
            print(xml_path, review.is_valid)
            
            #TODO: this is where the ws needs to be created and review added
            

        except Exception as e:
            print(xml_path, f'Error: {e}')


# Create workbook object with initial settings
DEFAULT_FONT.__init__(name=FALLBACKS['font_name'], size=FALLBACKS['font_size'])
wb = Workbook()
ws = wb.active

# review = Review.from_file(xml_path)
# print(review.is_valid)
# if review:
#     singlereport.create_report(review, ws)

if _WRITE_FILE:
    save_name = f'./dev/test/out/test_{timestamp()}.xlsx'
    wb.save(save_name)
    print(f'{save_name} has been saved.')

wb.close()
