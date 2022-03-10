import argparse
import csv
import os
import xml.etree.ElementTree as eT

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--xml', default='../Encodage/engravings-catalogue/xml-files', type=str, help="Le chemin du dossier des fichiers xml à charger.")
parser.add_argument('--csv', default='../pliegos_iiif.csv', type=str, help="Le chemin du fichier CSV contenant les URI IIIF")
args = parser.parse_args()

# Conversion cvs > list
with open(args.csv) as csvFile:
    csv_reader = csv.reader(csvFile)
    list_rows = list(csv_reader)

# Parsing XML files
for xmlFile in os.listdir(args.xml):
    if xmlFile.endswith('.xml'):
        xml_path = os.path.join(args.xml, xmlFile)
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = eT.parse(xml_path)
        root = tree.getroot()

        for i in range(len(list_rows)):
            for image in root.findall('.//tei:figure/tei:graphic', ns):
                imgName = image.get('source')
                coords = image.get('n')
                coords = coords.replace(" ", "")

                # Linking manifests with engravings' coordinates to TEI <graphic>
                if imgName == list_rows[i][7]:
                    imgURI = list_rows[i][8][:46] + coords + list_rows[i][8][50:]
                    image.set('url', imgURI[29:])

        tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
