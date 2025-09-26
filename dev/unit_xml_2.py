# Copyright (c) 2018-2025 Ben Fisher

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from typing import Literal

def get_root(path: str) -> Element | None:
    try:
        root = ET.parse(path).getroot()
        if root.tag.lower() == 'projnet': # type: ignore
            return root
        else:
            return None
    except Exception as e:
        print(e)
        return None

def has_children(element: Element) -> bool:
    if element is not None and len(element) > 0:
        return True
    return False

def has_project_info(element: Element) -> bool:
    return has_children(element.find('DrChecks'))

def has_comments(element: Element) -> bool:
    return has_children(element.find('Comments'))

responses_types = Literal['evaluations', 'backchecks']
def has_responses(element: Element, response_type:responses_types = 'evaluations') -> bool:
    items = element.iter(response_type)
    for item in items:
        if has_children(item):
            return True
    return False


# file_name = 'test.xml'

# root = ET.Element('ProjNet')
# project_info = ET.SubElement(root, 'DrChecks')
# comments = ET.SubElement(root, 'Comments')

# ET.SubElement(project_info, 'title').text = 'Project Title'
# ET.SubElement(project_info, 'project_number').text = '103242'

# comment = ET.SubElement(comments, 'comment')
# ET.SubElement(comment, 'ID').text = '01234u234'

# tree = ET.ElementTree(root)
# tree.write(file_name, encoding='utf-8', xml_declaration=True)

file_name = './dev/test/xml/no_evals.xml'

parsed_root = get_root(file_name)
# print(has_children(parsed_root))
# print(has_project_info(parsed_root))
# print(has_comments(parsed_root))
# print(has_children(parsed_root.find('Comments')[0]))
print(has_responses(parsed_root, 'backchecks'))