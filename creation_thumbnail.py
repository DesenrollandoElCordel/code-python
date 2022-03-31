import xml.etree.ElementTree as eT
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--xml', default='../Encodage/Moreno-TEI-files', type=str, help="Le chemin du dossier des fichiers xml à charger.")
args = parser.parse_args()

for filename in os.listdir(args.xml):
    if filename.endswith('.xml'):
        xml_path = os.path.join(args.xml, filename)
        label, ext = os.path.splitext(filename)

        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = eT.parse(xml_path)
        root = tree.getroot()

        for pb in root.findall(".//tei:pb", ns):
            pageNumber = pb.get("n")
            if pageNumber == "1":
                iiif_uri = pb.get("facs")
                iiif_thumbnail_uri = iiif_uri[:22] + "200," + iiif_uri[26:]
                # print(iiif_thumbnail_uri)
                graphic = root.find(".//tei:facsimile/tei:graphic", ns)
                if graphic is not None:
                    graphic.set("url", iiif_thumbnail_uri)
                print(label + ": done")

        tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
