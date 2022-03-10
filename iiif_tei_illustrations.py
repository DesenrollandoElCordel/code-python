import csv
import os
import xml.etree.ElementTree as eT

# Conversion cvs > list
with open('../pliegos_iiif.csv') as csvFile:
    csv_reader = csv.reader(csvFile)
    list_rows = list(csv_reader)
    # print(list_rows[1][8][46:50])

for xmlFile in os.listdir('../Encodage/TEI_tests/'):
    if xmlFile.endswith('.xml'):
        xml_path = os.path.join('../Encodage/TEI_tests/', xmlFile)
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = eT.parse(xml_path)
        root = tree.getroot()

        for i in range(len(list_rows)):
            for image in root.findall('.//tei:figure/tei:graphic', ns):
                imgName = image.get('source')
                coords = image.get('n')
                coords = coords.replace(" ", "")
                # print(imgName, coords)

                if imgName == list_rows[i][7]:
                    imgURI = list_rows[i][8][:46] + coords + list_rows[i][8][50:]
                    image.set('url', imgURI[29:])

        tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
