# Copyright (c) 2018-2025 Ben Fisher

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import random
from faker import Faker
from dxbuild.buildtools import timestamp

fake = Faker()

override_name = 'no_bcs'

write_good_root = True
write_drchecks_element = True
write_comments_element = True
write_comments = True
write_evaluations = True
write_backchecks = False

max_comment_count = 30
max_evaluation_count = 4
max_backcheck_count = 4

date_format_string = '%b %d %Y %I:%M %p'
disciplines = ['General',
               'Architecture',
               'Structural',
               'Civil',
               'Landscape',
               'Mechanical',
               'Electrical',
               'Plumbing',
               'Life Safety',
               'Fire Protection']


def make_comment(parent_element: Element) -> None:
    a_comment = ET.SubElement(parent_element, 'comment')
    a_comment_id = ET.SubElement(a_comment, 'id')
    a_comment_id.text = fake.numerify('#'*7)
    comment_open_status = ['Closed', 'Non-Concur']    
    comment_dict = {'spec': random.choice([fake.sentence(nb_words=3),'']),
                    'sheet': random.choice([fake.sentence(nb_words=3),'']),
                    'detail': random.choice([fake.sentence(nb_words=3),'']),
                    'critical': random.choice(['Yes','']),
                    'commentText': fake.text(max_nb_chars=100),
                    'status': random.choice(comment_open_status),
                    'DocRef': random.choice([fake.sentence(nb_words=3),'']),
                    'Discipline': random.choice(disciplines),
                    'DocType': random.choice([fake.sentence(nb_words=3),'']),
                    'CoordinatingDiscipline': random.choice(disciplines),
                    'attachment': random.choice(['True', '']),
                    'createdBy': fake.name(),
                    'createdOn': fake.date(date_format_string)}
    for item in comment_dict:
        ET.SubElement(a_comment, item).text = comment_dict[item]

    evals = ET.SubElement(a_comment, 'evaluations')
    bcs = ET.SubElement(a_comment, 'backchecks')
    
    if write_evaluations:
        has_evals = random.choice([True, False])
        if has_evals:
            for i in range(1, random.randint(1, 4)):
                eval = ET.SubElement(evals, f'evaluation{i}')
                make_evaluaton(eval, a_comment_id.text)
        else:
            evals.text = ' '    # ProjNet incorrectly exports empty elements with spaces

    if write_backchecks:
        has_bcs = random.choice([True, False])
        if has_bcs:
            for i in range(1, random.randint(1, 4)):
                bc = ET.SubElement(bcs, f'backcheck{i}')
                make_backcheck(bc, a_comment_id.text)
        else:
            bcs.text = ' '      # ProjNet incorrectly exports empty elements with spaces

def make_evaluaton(parent_element: Element, comment_id: str) -> None:
    evaluation_statuses = ['Concur', 'For Information Only', 'Non-Concur', 'Check and Resolve']
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
    backcheck_statuses = ['Concur', 'Non-Concur']
    # Note that if the comment is closed without comment, the backcheckText == 'Closed without comment.'
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



if write_good_root:
    root = ET.Element('ProjNet')
else:
    root = ET.Element(fake.sentence(nb_words=1))

if write_drchecks_element:
    proj_info = ET.SubElement(root, 'DrChecks')
    proj_info_dict = {'ProjectID': fake.numerify('######'),
                    'ProjectControlNbr': fake.numerify('######'),
                    'ProjectName': fake.text(75),
                    'ReviewID': fake.numerify('####'),
                    'ReviewName': fake.text(50)}
    for item in proj_info_dict:
        ET.SubElement(proj_info, item).text = proj_info_dict[item]

if write_comments_element and write_comments_element:
    review_comments = ET.SubElement(root, 'Comments')
    
if write_comments_element and write_comments:
    for i in range(1, random.randint(1, max_comment_count)):
        make_comment(review_comments)


if override_name:
    file_name = f'./dev/test/xml/{override_name}_{timestamp()}.xml'
else:
    file_name = f'./dev/test/xml/test_xml_{timestamp()}.xml'
    

tree = ET.ElementTree(root)
tree.write(file_name, encoding='utf-8', xml_declaration=True)