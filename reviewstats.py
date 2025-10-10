# Copyright (c) 2018-2025 Ben Fisher

import sys, os
# import win32com.client as COM

from openpyxl import Workbook
from openpyxl.styles import DEFAULT_FONT
from openpyxl.worksheet.cell_range import CellRange



from PyQt6.QtWidgets import QApplication, QFileDialog

from dxbuild.reviews import Review
from dxbuild.constants import FALLBACKS, _LOG_DIR
from dxbuild.buildtools import timestamp, clean_name, autoincrement_name
from dxreport import singlereport

if not os.path.exists(_LOG_DIR):
    os.makedirs(_LOG_DIR)

import logging
from dxcore.logconstants import log_format_string
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
log_formatter = logging.Formatter(log_format_string)
log_file_handler = logging.FileHandler(f'{_LOG_DIR}/{__name__}.log')
log_file_handler.setFormatter(log_formatter)
logger.addHandler(log_file_handler)



def main() -> None:

    _WRITE_FILE = True
    xml_path = './dev/test/data.xml'

    DEFAULT_FONT.__init__(name=FALLBACKS['font_name'], size=FALLBACKS['font_size'])
    wb = Workbook()


    review = Review.from_file(xml_path)
    comments = review.review_comments.comments

    ws = wb.active
    singlereport.create_report(review, ws)



    ws_table_name = ws.tables.items()[0][0]
    ws_stat_name = ws.title[:25] + '-STAT'
    ws_stats = wb.create_sheet(ws_stat_name)
    
    disciplines = list(set([comment.discipline for comment in comments]))
    reviewers = list(set([comment.author for comment in comments]))


    # for disc in disciplines:
    #     print(disc, len(disciplines))

    anchor = ws_stats[CellRange('A1').coord]

    anchor.value = 'Dr Checks Review Statistics'
    anchor.offset(row=2).value = 'Project Name'
    anchor.offset(row=3).value = 'Project ID'
    anchor.offset(row=4).value = 'Review Name'

    anchor.offset(row=2, column=1).value = review.project_info.project_name
    anchor.offset(row=3, column=1).value = review.project_info.project_id
    anchor.offset(row=4, column=1).value = review.project_info.review_name

    anchor.offset(row=6).value = 'Overall Comment Status'
    anchor.offset(row=7).value = 'By Discipline'
    anchor.offset(row=7, column=1).value = 'Open'
    anchor.offset(row=7, column=2).value = 'Closed'
    anchor.offset(row=7, column=3).value = 'Total'

    anchor.offset(row=8).value = f'=UNIQUE({ws_table_name}[Discipline])'
    for i in range(1, 3):
        anchor.offset(row=8, column=i).value = f'=COUNTIFS({ws_table_name}[Discipline],$A9,{ws_table_name}[Status],B$8)'
    
    # print(anchor.offset(row=8, column=1).coordinate)

    
    anchor.offset(row=8 + len(disciplines)).value = 'Grand Total'
    for i in range(1, 4):
        anchor.offset(row=8 + len(disciplines), column=i).value = \
            f'=SUM({anchor.offset(row=8 + len(disciplines) - 1, column=i).coordinate}:{anchor.offset(row=8, column=i).coordinate})'




    if _WRITE_FILE:
        save_name = f'./dev/test/out/test_{timestamp()}.xlsx'
        wb.save(save_name)
        print(f'File {save_name} written to disk.')
        logger.debug(f'_WRITE_FILE = {_WRITE_FILE} -> saved workbook to "{save_name}"')

    wb.close()
    
    # try:
    #     excel = COM.Dispatch('Excel.Application')
    #     excel.Visible = False

    #     workbook = excel.Workbooks.Open(os.path.abspath(save_name))
    #     sht = workbook.Worksheets(ws_stat_name)

    #     sht.Range('A8').value = 'Discipline'
    #     sht.Range('B8').value = 'Open'
    #     sht.Range('C8').value = 'Closed'
    #     sht.Range('D9').value = 'Total'
    #     sht.Range('A9').formula2 = f'=UNIQUE({ws_table_name}[Discipline])'
    #     sht.Range(f'B9:B{9 + len(disciplines) - 1}').formula2 = f'=COUNTIFS({ws_table_name}[Discipline],$A9,{ws_table_name}[Status],B$8)'
    #     sht.Range(f'C9:C{9 + len(disciplines) - 1}').formula2 = f'=COUNTIFS({ws_table_name}[Discipline],$A9,{ws_table_name}[Status],C$8)'
    #     sht.Range(f'D9:D{9 + len(disciplines) - 1}').formula2 = f'=AGGREGATE(9,4,B9:C9)'
    #     sht.Range(f'A{9 + len(disciplines)}').value = 'Grand Total'

    #     sht.Range('F9').formula2 = f'=UNIQUE({ws_table_name}[Author])'



    # except Exception as e:
    #     logger.exception(f'Error in trying to edit via COM. {e}')
    # finally:

    #     workbook.Save()
    #     workbook.Close()
    
    #     if 'excel' in locals() and excel:
    #         excel.Quit()
    #     print('Code Executed -> Returned 0')

if __name__ == '__main__':
    main()