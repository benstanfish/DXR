import os
from defusedxml import ElementTree as ET
from xml.etree.ElementTree import Element

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

dir_path = './dev/test/xml'
file_names = os.listdir(dir_path)
file_paths = [dir_path + '/' + file_name for file_name in file_names]


for file in file_paths:
    try:
        root = ET.parse(file).getroot()
        print(file, root)
    except Exception as e:
        print(file, e.args, e.with_traceback)