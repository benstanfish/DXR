# Copyright (c) 2018-2025 Ben Fisher

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element


file_name = 'test.xml'

# root = ET.Element('ProjNet')
# shorthand_empty = ET.SubElement(root, 'shorthandempty')
# whitespace_empty = ET.SubElement(root, 'whitespaceempty')
# whitespace_empty.text = '   '
# hastext = ET.SubElement(root, 'hastext').text = 'hello world'
# haschild = ET.SubElement(root, 'haschild')
# child = ET.SubElement(haschild, 'child').text = 'hello world'

# tree = ET.ElementTree(root)
# tree.write(file_name, encoding='utf-8', xml_declaration=True)




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
    

new_root = get_root(file_name)
try:
    print(new_root.find('shorthandempty') is None) 
except:
    pass




# new_root.find('DrChecks').text.strip() == '' --> Empty
# 