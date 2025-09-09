import os
import pymupdf as pdf
import pandas as pd


prefacing_pages = 46
# building_types_pages = [1, 3]
# checkists_pages = [232, 293]

# file_name = './data/ASCE 41-23.pdf'

# file_name = './building_types/building_type_names.pdf'
# output_path = os.path.join(os.path.abspath(os.path.dirname(file_name)), 'name_block_outlined.pdf')
# excel_path = os.path.join(os.path.abspath(os.path.dirname(file_name)), 'name_excel.xlsx')

file_name = './building_types/building_type_desc.pdf'
output_path = os.path.join(os.path.abspath(os.path.dirname(file_name)), 'desc_block_outlined.pdf')
excel_path = os.path.join(os.path.abspath(os.path.dirname(file_name)), 'desc_excel.xlsx')

new_pdf = pdf.open()


blocks = []
with pdf.open(os.path.abspath(file_name)) as doc:
    # start = building_types_pages[0] + prefacing_pages
    # stop = building_types_pages[-1] + prefacing_pages
    start = 0
    stop = doc.page_count
    for page_no, page in enumerate(doc.pages(start=start, stop=stop)):
        shape = page.new_shape()
        for block in page.get_text('blocks'):
            this_block = [page_no] + [thing for thing in block]
            this_block[5] = this_block[5].replace('\n', ' ').strip()
            blocks.append(this_block)
            rect = pdf.Rect(block[:4])
            shape.draw_rect(rect)
            shape.finish(width=1, color=(1, 0, 0), fill=None)
        shape.commit()
    
    df = pd.DataFrame(blocks, columns=['page',
                                       'x0', 
                                       'y0', 
                                       'x1', 
                                       'y1',
                                       'text',
                                       'block_no',
                                       'block_type'])
    df.to_excel(excel_path, index=False)
    new_pdf.insert_pdf(doc, from_page=start, to_page=stop)

    # start = checkists_pages[0] + prefacing_pages
    # stop = checkists_pages[-1] + prefacing_pages
    # for page in doc.pages(start=start, stop=stop):
    #     shape = page.new_shape()
    #     for block in page.get_text('blocks'):
    #         rect = pdf.Rect(block[:4])
    #         shape.draw_rect(rect)
    #         shape.finish(width=1, color=(1, 0, 0), fill=None)
    #     shape.commit()

    # new_pdf.insert_pdf(doc, from_page=start, to_page=stop)
    
    new_pdf.save(output_path)