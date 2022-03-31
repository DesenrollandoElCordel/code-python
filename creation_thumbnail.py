import xml.etree.ElementTree as eT
import os

path = '../Encodage/TEI_tests/'

for filename in os.listdir(path):
    if filename.endswith('.xml'):
        xml_path = os.path.join(path, filename)
        label, ext = os.path.splitext(filename)

        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = eT.parse(xml_path)
        root = tree.getroot()

        for pb in root.findall(".//tei:pb", ns):
            pageNumber = pb.get("n")
            if pageNumber == "1":
                iiif_uri = pb.get("facs")
                iiif_thumbnail_uri = iiif_uri[:22] + "150," + iiif_uri[26:]
                # print(iiif_thumbnail_uri)
                graphic = root.find(".//tei:facsimile/tei:graphic", ns)
                graphic.set("url", iiif_thumbnail_uri)
                print(label + ": done")

        tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
