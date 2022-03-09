import csv
import xml.etree.ElementTree as eT
import os
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--xml', default='../Encodage/Moreno-TEI-files/', type=str, help="Le chemin du dossier des fichiers xml à charger.")
args = parser.parse_args()

# Conversion cvs > list
with open('../pliegos_iiif.csv') as csvFile:
    csv_reader = csv.reader(csvFile)
    list_rows = list(csv_reader)

# Parsing TEI files
for xmlFile in os.listdir(args.xml):
    if xmlFile.endswith('.xml'):
        xml_path = os.path.join(args.xml, xmlFile)
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = eT.parse(xml_path)
        root = tree.getroot()

        for i in range(len(list_rows)):
            # Linking IIIF URI (Images) to TEI <pb>
            '''for pb in root.findall(".//tei:pb", ns):
                imgName = pb.get('source')
                if imgName == list_rows[i][7]:
                    pb.set('facs', list_rows[i][8][29:])
                    tree.write(xml_path, encoding="UTF-8", xml_declaration=True)'''

            '''# Linking IIIF Manifest URI to TEI <facsimile>
            if list_rows[i][7].endswith('_1.jpeg') | list_rows[i][7].endswith('_1.jpg'):
                facsimile = root.find(".//tei:sourceDesc", ns)
                print(facsimile)'''
