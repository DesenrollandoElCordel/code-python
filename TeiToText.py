import xml.etree.ElementTree as ET
import os

folder = 'transcriptions'

for f in os.listdir(folder):
    if not f.endswith('.DS_Store'):
        xml_path = os.path.join(folder, f)
        label, ext = os.path.splitext(f)
        label = str(label)

        print(xml_path)
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        tree = ET.parse(xml_path)
        root = tree.getroot()
        body = root.find('.//tei:body', ns)

        text = ET.tostring(body, encoding='utf-8', method='text')
        new_text = text.decode()

        with open('test.txt', 'at') as x:
            x.write(label)
            x.write(new_text)
