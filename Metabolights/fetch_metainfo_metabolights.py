import xml.etree.ElementTree as ET

tree = ET.parse('/Users/yliao13/Desktop/metabolights_studies/meta information/eb-eye_metabolights_studies.xml')

root = tree.getroot()

for child in root:
    print(child.tag, child.attrib)