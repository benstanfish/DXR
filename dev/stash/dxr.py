from typing import Optional, Union, List, Tuple
from xml.etree.ElementTree import Element
from defusedxml import ElementTree as ET

def get_root(path: str) -> Union[Element, None]:
    try:
        root = ET.parse(path).getroot()
        if root.tag.lower() == 'projnet':
            return root
    except Exception as e:
        print(e)

def get_project_info_element(root: Element) -> Element:
    try:
        return root[0]
    except Exception as e:
        print(e)

def get_comments_element(root: Element) -> Element:
    try:
        return root[1]
    except Exception as e:
        print(e)

def comment_count(comments_element: Element) -> int:
    return len(comments_element)

def get_review_elements(root: Element) -> List[Element]:
    return [root[0], root[1]]