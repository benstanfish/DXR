
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


file_name = './dev/test/data.xml'

root = get_root(file_name)
print(root.tag)

print(root.find('DrChecks').tag)
print(root.find('Comments').tag)