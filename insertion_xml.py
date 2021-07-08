import os
import xml.etree.ElementTree as ET

folder = ""
# print(folder)

for f in os.listdir(folder):
    if f.endswith('.xml'):
        xml_path = os.path.join(folder, f)

        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = ET.parse(xml_path)
        root = tree.getroot()

        encodingDesc = root.find(".//tei:encodingDesc", ns)
        # print(encodingDesc)
        project = ET.Element('projectDesc')
        encodingDesc.insert(0, project)
        ET.SubElement(project, "p")
        for y in project.iter('p'):
            description = 'Este archivo fue creado en el marco del proyecto Desenrollando el Cordel/Démêler le cordel/Untangling the cordel, dirigido por la profesora Constance Carta de la Universidad de Ginebra, con el apoyo de la Fundación filantrópica Famille Sandoz-Monique de Meuron.'
            y.text = str(description)

        '''cc = root.find(".//tei:availability", ns)
        cc.remove(cc[0])'''

        '''ET.SubElement(cc, "p")
        for x in cc.iter('p'):
            new_cc = 'CC-BY-NC-SA'
            x.text = str(new_cc)'''

        '''msId = root.find(".//tei:msIdentifier", ns)
        collection = ET.Element('collection')
        msId.insert(3, collection)
        for c in msId.iter('collection'):
            new_text = 'Colleción Moreno'
            c.text = str(new_text)'''

        '''new_folder = "encodage_updated/"
        if not os.path.isdir(new_folder):
            os.mkdir(new_folder)

        new_path = os.path.join(new_folder, f)
        # print(new_path)'''

        tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
