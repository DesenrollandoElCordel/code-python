import csv
from collections import defaultdict
from lxml import etree

placeNames = []  # Liste avec les noms normalisés sans doublon
placeNamesCoords = []  # Liste avec les noms normalisés + coordonnées géo + id. Wikidata
placesNamesOriginal = []  # Liste avec les noms normalisés + originaux avec doublons
placesNamesDeduplicated = []  # Liste avec les noms normalisés + originaux sans doublon

with open('../pliegos-ner/moreno-ner/nerList_Moreno_Wikidata.csv', encoding='utf-8') as f:
    csv_file = csv.reader(f)  # On parcourt le fichier CSV
    next(csv_file)  # On passe la première ligne

    for line in csv_file:
        # On élimine les doublons et les lieux inclassables
        if line[6] not in placeNames and line[6] != '':
            placeNames.append(line[6])
            placeNames.sort()
            placeNamesCoords.append([line[6], [line[5], line[3]]])

        #
        for name in placeNames:
            if line[6] == name:
                placesNamesOriginal.append([line[6], line[2]])

    for p in placesNamesOriginal:
        if p not in placesNamesDeduplicated:
            placesNamesDeduplicated.append(p)
            placesNamesDeduplicated.sort()
    # print(placesNamesDeduplicated)

    data = defaultdict(list)
    for key, value in placesNamesDeduplicated:
        data[key].append(value)
    # print(data.items())
    placesNamesPairs = [list(t) for t in data.items()]
    # print(placesNamesPairs)

root = etree.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")

teiHeader = etree.SubElement(root, "teiHeader")
fileDesc = etree.SubElement(teiHeader, "fileDesc")
titleStmt = etree.SubElement(fileDesc, "titleStmt")
title = etree.SubElement(titleStmt, "title")
title.text = "Desenrollando el cordel: Índice de lugares"

pubStmt = etree.SubElement(fileDesc, "publicationStmt")
pubStmt_child1 = etree.SubElement(pubStmt, "authority")
pubStmt_child1.text = "Bibliothèque Universitaire de Genève (BUNIGE)"
pubStmt_child2 = etree.SubElement(pubStmt, "availability", status="restricted")
licence = etree.SubElement(pubStmt_child2, "licence",
                           n="cc by nc sa", target="https://creativecommons.org/licenses/by-nc-sa/4.0/")
sourceDesc = etree.SubElement(fileDesc, "sourceDesc")
sourceDescP = etree.SubElement(sourceDesc, "p")

standoff = etree.SubElement(root, "standOff")
listPlace = etree.SubElement(standoff, "listPlace")
for i in placeNames:
    place = etree.SubElement(listPlace, "place")
    place.set("{http://www.w3.org/XML/1998/namespace}id", i.replace(" ", "_"))
    place.set("n", i)
    placeName = etree.SubElement(place, "placeName")
    placeName.set("type", "main")
    placeName.text = i
    for n in range(len(placesNamesPairs)):
        if i == placesNamesPairs[n][0] and i not in placesNamesPairs[n][1]:
            altName = etree.SubElement(place, "placeName")
            altName.set("type", "alt")
            altName.text = str(placesNamesPairs[n][1]).replace('[', "").replace(']', "").replace("'", "")
    location = etree.SubElement(place, "location")
    for g in range(len(placeNamesCoords)):
        if i == placeNamesCoords[g][0]:
            geo = etree.SubElement(location, "geo")
            geo.text = placeNamesCoords[g][1][0]
            desc = etree.SubElement(place, "desc")
            ref = etree.SubElement(desc, "ref")
            ref.set("target", "https://www.wikidata.org/wiki/" + placeNamesCoords[g][1][1])
            ref.text = placeNamesCoords[g][1][1]

# tree = etree.ElementTree(root)

# print(etree.tostring(root, xml_declaration=True, encoding='UTF-8', pretty_print=True))
# tree.write("places.xml", xml_declaration=True, encoding='UTF-8', pretty_print=True)
