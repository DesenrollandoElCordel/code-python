import csv
import xml.etree.ElementTree as eT
import os
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--xml', default='../Encodage/TEI_tests/', type=str, help="Le chemin du dossier des fichiers xml à charger.")
parser.add_argument('--csv', default='../pliegos_iiif.csv', type=str, help="Le chemin du fichier CSV contenant les URI IIIF")
args = parser.parse_args()

# Conversion cvs > list
with open(args.csv) as csvFile:
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
            for pb in root.findall(".//tei:pb", ns):
                imgName = pb.get('source')
                if imgName == list_rows[i][7]:
                    pb.set('facs', list_rows[i][8][29:])

                    # Linking IIIF Manifest URI to TEI <facsimile>
                    facsimile = root.find(".//tei:facsimile", ns)
                    facsimile.set('facs', list_rows[i][9])

        tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
