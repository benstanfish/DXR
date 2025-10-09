# Copyright (c) 2018-2025 Ben Fisher

from defusedxml import ElementTree as ET
from xml.etree.ElementTree import Element
from typing import Literal
from datetime import datetime

from dxbuild.constants import _LOG_DIR

import logging
from dxcore.logconstants import log_format_string
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
log_formatter = logging.Formatter(log_format_string)
log_file_handler = logging.FileHandler(f'{_LOG_DIR}/{__name__}.log')
log_file_handler.setFormatter(log_formatter)
logger.addHandler(log_file_handler)


responses_types = Literal['evaluations', 'backchecks']

class Parseable():
    def __init__(self):
        pass

    def get_root(path: str) -> Element | None:
        try:
            root = ET.parse(path).getroot()
            if root.tag.lower() == 'projnet':
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

    def has_project_info(cls, element: Element) -> bool:
        return cls.has_children(element.find('DrChecks'))

    def has_comments(cls, element: Element) -> bool:
        return cls.has_children(element.find('Comments'))

    def has_responses(cls, element: Element, response_type:responses_types = 'evaluations') -> bool:
        items = element.iter(response_type)
        for item in items:
            if cls.has_children(item):
                return True
        return False
    
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
            self,
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