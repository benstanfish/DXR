# Copyright (c) 2018-2025 Ben Fisher

from datetime import datetime
from defusedxml import ElementTree as ET
from xml.etree.ElementTree import Element

def get_root(
        path: str
    ) -> Element | None:
    """Returns 'ProjNet' element as root for Dr Checks XML report files. Other XML files return None."""
    try:
        root = ET.parse(path).getroot()
        if root.tag.lower() == 'projnet': # type: ignore
            return root
        else:
            return None
    except Exception as e:
        print(e)
        return None

def parse_single_tag(
        tag: str, 
        element: Element
    ) -> str | None:
    """Helper method to extract XML data for first child element node with tag of tag."""
    node = element.find(tag)
    return node.text if node is not None else None

def parse_date_node(
        tag: str, 
        element: Element
    ) -> str | None:
    """Parses a date-like XML node and returns an isoformatted datetime string."""
    node = element.find(tag)
    if node is not None and node.text is not None:
        return datetime.strptime(node.text, '%b %d %Y %I:%M %p').isoformat()
    return None

def date_to_excel(
        iso_date: str | None
    ) -> datetime | None:
    """Deformats a datetime date to an ISO formatted date time string."""
    if iso_date is not None:
        return datetime.fromisoformat(iso_date)
    return None

def clean_text(
        text: str | None
    ) -> str | None:
    """Method to strip new-line entities from XML string."""
    if text is not None:
        return text.replace('<br />', '\n')
    return None