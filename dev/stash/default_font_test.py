# from openpyxl.styles import DEFAULT_FONT
import openpyxl
# openpyxl.styles.DEFAULT_FONT.name = 'Aptos'

# print(openpyxl.styles.DEFAULT_FONT.name)

openpyxl.styles.DEFAULT_FONT.__init__(name='Aptos', size=10)


wb = openpyxl.Workbook()

file_path = './output2.xlsx'
wb.save(file_path)
wb.close()