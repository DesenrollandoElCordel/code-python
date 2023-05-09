import os
import xml.etree.ElementTree as eT
import csv
import re

xml_folder = "../Encodage/moreno_035"
new_csvLine = []

for file in os.listdir(xml_folder):
    if file.endswith('.xml'):
        xml_path = os.path.join(xml_folder, file)

        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = eT.parse(xml_path)  # On parse le fichier XML-TEI
        root = tree.getroot()  # On récupére la racine du fichier TEI
        id_doc = root.get("{http://www.w3.org/XML/1998/namespace}id")  # On récupère l'id du document

        with open('../Encodage/moreno_035/nerList_v2.csv', encoding='utf-8') as f:
            csv_file = csv.reader(f)
            next(csv_file)  # On passe la première ligne

            loc_list_deduplicated = []  # Initialisation d'une liste avec les noms originaux sans doublon
            loc_list_normalized_all = []  # Initialisation d'une liste avec tous les noms normalisés
            # loc_list_normalized = []  # Initialisation d'une liste avec les noms normalisés sans doublon

            for line in csv_file:
                if line[1].lower() == id_doc:
                    loc_list_normalized_all.append([line[3], line[5]])
                    # if line[3] not in loc_list_normalized:
                        # loc_list_normalized.append(line[3])
                    if line[2] not in loc_list_deduplicated:
                        loc_list_deduplicated.append(line[2])

                    shortTitle = root.find('.//tei:titleStmt/tei:title', ns).text
                    shortTitle = re.sub(r"\n( +)", " ", shortTitle)
                    printer = root.find('.//tei:publisher', ns).text
                    pubPlace = root.find('.//tei:pubPlace', ns).text
                    typeText = root.find('.//tei:keywords/tei:term', ns).text

                    line.append(shortTitle)
                    line.append(pubPlace)
                    line.append(printer)
                    line.append(typeText)
                    new_csvLine.append(line)
                    # print(shortTitle)

            total = {}
            for k, v in loc_list_normalized_all:
                total[k] = str(total.get(k,v))
            loc_list_normalized = [list(t) for t in total.items()]

            for l in root.findall(".//tei:l", ns):
                # print(l.text)
                for i in range(len(loc_list_deduplicated)):
                    # print(ner_list[i])
                    # On vérifie que le nom de lieu est dans le texte et on l'encode avec <name>
                    if loc_list_deduplicated[i] in l.text:
                        new_line = l.text.replace(loc_list_deduplicated[i], '<name>' + loc_list_deduplicated[i] + '</name>')
                        l.text = new_line
        # eT.dump(root)

            sourceDesc = root.find('.//tei:sourceDesc', ns)  # On récupère l'élément <sourceDesc>
            listPlace = eT.SubElement(sourceDesc, 'listPlace')  # On ajoute à <sourceDesc> l'élément <listPlace>
            # print(loc_list_normalized_all)
            for place in loc_list_normalized:
                placeElement = eT.SubElement(listPlace, "place")  # On ajoute l'élément <place>
                placeNb = loc_list_normalized_all.count(place)  # On compte le nb de fois où le nom de lieu apparaît dans le texte
                placeElement.set("n", str(placeNb))  # On ajoute à <placeName> un @n avec le nb d'occurrences du lieu

                placeName = eT.SubElement(placeElement, "placeName")  # On ajoute l'élément <placeName>
                placeName.text = place[0].title()  # On ajoute à <placeName> les noms de lieux en rétablissant les majuscules

                location = eT.SubElement(placeElement, "location")
                geo = eT.SubElement(location, "geo")
                geo.text = place[1][6:-1]

        eT.dump(listPlace)
        print('\n')
        # tree.write(xml_path, encoding="UTF-8", xml_declaration=True)

new_csv_header = ['index', 'id_doc', 'original_name', 'normalized_name', 'id_wkd', 'coord', 'type_place',
                  'shortTitle', 'pubPlace', 'printer', "type_text"]

# with open('../Encodage/moreno_035/nerList_v3.csv', 'w', encoding='utf-8', newline='') as newCsv:
    # writer = csv.writer(newCsv)
    # writer.writerow(new_csv_header)
    # writer.writerows(new_csvLine)
