import os
import xml.etree.ElementTree as ET

folder = "transcriptions"
# print(folder)

for f in os.listdir(folder):
    if not f.endswith('.DS_Store'):
        xml_path = os.path.join(folder, f)

        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = ET.parse(xml_path)
        root = tree.getroot()

        cc = root.find(".//tei:availability", ns)
        cc.remove(cc[0])

        ET.SubElement(cc, "p")
        for x in cc.iter('p'):
            new_cc = 'CC-BY-NC-SA'
            x.text = str(new_cc)

        msId = root.find(".//tei:msIdentifier", ns)
        collection = ET.Element('collection')
        msId.insert(3, collection)
        for c in msId.iter('collection'):
            new_text = 'Colleción Moreno'
            c.text = str(new_text)

        new_folder = "encodage_updated/"
        if not os.path.isdir(new_folder):
            os.mkdir(new_folder)

        new_path = os.path.join(new_folder, f)
        # print(new_path)

        tree.write(new_path, encoding="UTF-8", xml_declaration=True)
