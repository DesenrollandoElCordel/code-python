import csv
import xml.etree.ElementTree as eT

with open('../pliegos_iiif.csv') as csvFile:
    csv_reader = csv.reader(csvFile)
    list_rows = list(csv_reader)

xmlFile = "../Encodage/Moreno-TEI-files/Moreno_001.xml"
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

tree = eT.parse(xmlFile)
root = tree.getroot()
# print(root)

for i in range(len(list_rows)):
    # print(list_rows[i][7])
    for pb in root.findall(".//tei:pb", ns):
        imgName = pb.get('source')
        # print(imgName)
        if imgName == list_rows[i][7]:
            pb.set('facs', list_rows[i][8][29:])
            print(pb.get('facs'))
            # tree.write(xmlFile, encoding="UTF-8", xml_declaration=True)


# print(list_rows[1][7])
