# Copyright (c) 2018-2025 Ben Fisher

import xml.etree.ElementTree as ET
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

statuses = Literal['Closed', 'Closed without comment.', 'Non-Concur']
backcheck_dict = {'id': fake.numerify('######'),
                  'comment': '1',
                  'evaluation': '1',
                  'status': 'Concur',
                  'backcheckText': fake.text(100),
                  'attachment': fake.boolean(),
                  'createdBy': fake.name(),
                  'createdOn': fake.date(date_format_string)}

for item in backcheck_dict:
    ET.SubElement(review_comments, item).text = backcheck_dict[item]

file_name = f'./dev/test/xml/test_xml_{timestamp()}.xml'
tree = ET.ElementTree(root)
tree.write(file_name, encoding='utf-8', xml_declaration=True)