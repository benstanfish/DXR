from defusedxml import ElementTree as ET

path = './dxr/test.xml'
doc = ET.parse(path)
root = doc.getroot()

print(root.text)