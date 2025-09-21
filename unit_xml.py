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
    evaluation_statuses = ['Closed', 'Closed without comment.', 'Non-Concur']    
    comment_dict = {'id': fake.numerify('#'*7),
                    'spec': random.choice([fake.text(),'']),
                    'sheet': random.choice([fake.text(),'']),
                    'detail': random.choice([fake.text(),'']),
                    'critical': random.choice(['Yes','']),
                    'commentText': fake.text(100),
                    'status': random.choice(evaluation_statuses),
                    'DocRef': random.choice([fake.text(),'']),
                    'Discipline': random.choice([fake.text(),'']),
                    'DocType': random.choice([fake.text(),'']),
                    'CoordinatingDiscipline': random.choice([fake.text(),'']),
                    'attachment': random.choice(['True', '']),
                    'createdBy': fake.name(),
                    'createdOn': fake.date(date_format_string)}
    for item in comment_dict:
        ET.SubElement(a_comment, item).text = comment_dict[item]

    evals = ET.SubElement(a_comment, 'evaluations')
    bcs = ET.SubElement(a_comment, 'backchecks')
    
    has_evals = random.choice([True, False])
    if has_evals:
        for i in range(1, random.randint(1,10)):
            bc = ET.SubElement(evals, f'evaluation{i}')
            make_evaluaton(bc, a_comment.find('id').text)

    has_bcs = random.choice([True, False])
    if has_bcs:
        for i in range(1, random.randint(1,10)):
            bc = ET.SubElement(bcs, f'backcheck{i}')
            make_backcheck(bc, a_comment.find('id').text)

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
                    'evaluation': fake.numerify('#'*7),
                    'status': random.choice(backcheck_statuses),
                    'backcheckText': fake.text(100),
                    'attachment': random.choice(['True', '']),
                    'createdBy': fake.name(),
                    'createdOn': fake.date(date_format_string)}
    for item in backcheck_dict:
        ET.SubElement(parent_element, item).text = backcheck_dict[item]


for i in range(1, random.randint(1,20)):
    make_comment(review_comments)




file_name = f'./dev/test/xml/test_xml_{timestamp()}.xml'
tree = ET.ElementTree(root)
tree.write(file_name, encoding='utf-8', xml_declaration=True)