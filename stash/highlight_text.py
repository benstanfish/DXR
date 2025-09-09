
import os
import pymupdf as pdf

path = "C:\\Users\\j2ee9bsf\\Documents\\00 Projects\\FY26 NAVY P530 AIMD Facility KAB\\08 Intermediate\\P530 Comments w Responses.pdf"

reviewers = {
    'Erika Nakasone, NAVFAC, FAC Planner, PM': 'yellow',
    'Yukiya Uezato, NAVFAC, PWD': 'pink',
    'Toshiya Inokuchi, NAVFAC, NCTS FE NIED': 'green'
}

doc = pdf.open(os.path.abspath(path))
for page in doc.pages():
    for key in reviewers.keys():
        for rect in page.search_for(key):
            highlight = page.add_highlight_annot(rect)
            highlight.set_colors(stroke=pdf.pdfcolor[reviewers[key]])
            highlight.update()
    
doc.save(os.path.join(os.path.dirname(path), 'highlighted.pdf'))
