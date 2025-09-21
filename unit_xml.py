# Copyright (c) 2018-2025 Ben Fisher

import xml.etree.ElementTree as ET
import random
from faker import Faker
from dxbuild.buildtools import timestamp
from typing import Literal

root = ET.Element('ProjNet')

proj_info = ET.SubElement(root, 'DrChecks')
review_comments = ET.SubElement(root, 'Comments')

fake = Faker()
date_format_string = '%b %d %Y %I:%M %p'

proj_info_dict = {'ProjectID': fake.numerify('######'),
                  'ProjectControlNbr': fake.numerify('######'),
                  'ProjectName': fake.text(75),
                  'ReviewID': fake.numerify('####'),
                  'ReviewName': fake.text(50)}

for item in proj_info_dict:
    ET.SubElement(proj_info, item).text = proj_info_dict[item]







def make_backcheck(parent_element):
    backcheck_statuses = ['Closed', 'Closed without comment.', 'Non-Concur']
    backcheck_dict = {'id': fake.numerify('######'),
                    'comment': '1',
                    'evaluation': '1',
                    'status': random.choice(backcheck_statuses),
                    'backcheckText': fake.text(100),
                    'attachment': random.choice(['True', '']),
                    'createdBy': fake.name(),
                    'createdOn': fake.date(date_format_string)}
    for item in backcheck_dict:
        ET.SubElement(parent_element, item).text = backcheck_dict[item]

for i in range(1, 10):
    bc = ET.SubElement(review_comments, f'backcheck{i}')
    make_backcheck(bc)


file_name = f'./dev/test/xml/test_xml_{timestamp()}.xml'
tree = ET.ElementTree(root)
tree.write(file_name, encoding='utf-8', xml_declaration=True)