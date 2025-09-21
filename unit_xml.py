# Copyright (c) 2018-2025 Ben Fisher

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import random
from faker import Faker
from dxbuild.buildtools import timestamp
from typing import Dict

date_format_string = '%b %d %Y %I:%M %p'

root = ET.Element('ProjNet')

proj_info = ET.SubElement(root, 'DrChecks')
review_comments = ET.SubElement(root, 'Comments')

fake = Faker()
proj_info_dict = {'ProjectID': fake.numerify('######'),
                  'ProjectControlNbr': fake.numerify('######'),
                  'ProjectName': fake.text(75),
                  'ReviewID': fake.numerify('####'),
                  'ReviewName': fake.text(50)}

for item in proj_info_dict:
    ET.SubElement(proj_info, item).text = proj_info_dict[item]

def make_comment(parent_element: Element) -> None:
    a_comment = ET.SubElement(parent_element, 'comment')
    a_comment_id = ET.SubElement(a_comment, 'id')
    a_comment_id.text = fake.numerify('######')
    evals = ET.SubElement(a_comment, 'evaluations')
    bcs = ET.SubElement(a_comment, 'backchecks')
    
    for i in range(1, 5):
        bc = ET.SubElement(evals, f'evaluation{i}')
        make_evaluaton(bc, a_comment_id.text)

    for i in range(1, 10):
        bc = ET.SubElement(bcs, f'backcheck{i}')
        make_backcheck(bc, a_comment_id.text)

def make_evaluaton(parent_element: Element, comment_id: str) -> None:
    evaluation_statuses = ['Closed', 'Closed without comment.', 'Non-Concur']
    evaluation_dict = {'id': fake.numerify('######'),
                        'comment': comment_id,
                        'status': random.choice(evaluation_statuses),
                        'impactScope': random.choice(['Yes', 'No']),
                        'impactCost': random.choice(['Yes', 'No']),
                        'impactTime': random.choice(['Yes', 'No']),
                        'evaluationText': fake.text(100),
                        'attachment': random.choice(['True', '']),
                        'createdBy': fake.name(),
                        'createdOn': fake.date(date_format_string)}
    for item in evaluation_dict:
        ET.SubElement(parent_element, item).text = evaluation_dict[item]


def make_backcheck(parent_element, comment_id: str) -> None:
    backcheck_statuses = ['Closed', 'Closed without comment.', 'Non-Concur']
    backcheck_dict = {'id': fake.numerify('######'),
                    'comment': comment_id,
                    'evaluation': '1',
                    'status': random.choice(backcheck_statuses),
                    'backcheckText': fake.text(100),
                    'attachment': random.choice(['True', '']),
                    'createdBy': fake.name(),
                    'createdOn': fake.date(date_format_string)}
    for item in backcheck_dict:
        ET.SubElement(parent_element, item).text = backcheck_dict[item]


for i in range(1, 10):
    make_comment(review_comments)




file_name = f'./dev/test/xml/test_xml_{timestamp()}.xml'
tree = ET.ElementTree(root)
tree.write(file_name, encoding='utf-8', xml_declaration=True)