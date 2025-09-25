import os
from defusedxml import ElementTree as ET
from xml.etree.ElementTree import Element
from dxcore.dxconsole import Escape

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


dir_path = './dev/test/xml/'
file_names = [
    'bad_root.xml',
    'empty_comments_element.xml',
    'empty_root.xml',
    'normal.xml',
    'no_bcs.xml',
    'no_comments_element.xml',
    'no_evals.xml',
    'no_project_info.xml',
    'no_responses.xml',
    'no_root.xml'
]

for file_name in file_names:
    file_path = dir_path + file_name
    try:
        root = ET.parse(file_path).getroot()
        
    except:
        pass
