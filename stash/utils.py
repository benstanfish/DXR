"""Library of basic helper functions"""

def parse_helper(tag, xml_element_node):
    return xml_element_node.find(tag).text if \
        xml_element_node.find(tag) is not None else None
