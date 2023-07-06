import os
import xml.etree.ElementTree as eT
import csv
import re

xml_folder = "../Encodage/Moreno-TEI-files"
new_csvLine = []  # Liste permettant de créer un nouveau fichier csv (ajout de données issues des fichiers TEI)

for file in os.listdir(xml_folder):  # On parcourt le dossier contenant les fichiers TEI
    if file.endswith('.xml'):
        xml_path = os.path.join(xml_folder, file)  # On reconstruit le chemin vers les fichiers

        # Déclaration du namespace TEI
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = eT.parse(xml_path)  # On parse le fichier XML-TEI
        root = tree.getroot()  # On récupére la racine du fichier TEI
        id_doc = root.get("{http://www.w3.org/XML/1998/namespace}id")  # On récupère l'id du document

        with open('../pliegos-ner/moreno-ner/nerList_Moreno_Wikidata.csv', encoding='utf-8') as f:
            csv_file = csv.reader(f)  # On parcourt le fichier CSV
            next(csv_file)  # On passe la première ligne

            loc_list_deduplicated = []  # Liste avec les noms originaux (sans doublon)
            loc_list_normalized = []  # Liste avec les noms normalisés (avec doublon)
            loc_list_normalized_geo = []  # Liste avec tous les noms normalisés + leurs coordonnées géo (avec doublon)
            loc_list_normalized_wkd = []  # Liste avec tous les noms normalisés + leur id Wikidata (avec doublon)
            loc_list_occurrences = []

            for line in csv_file:  # On parcourt chaque ligne du CSV
                if line[1].lower() == id_doc.lower():  # On cible les lignes qui ont le même ID qu'un fichier TEI
                    loc_list_normalized.append(line[6])  # On ajoute tous les noms normalisés à loc_list_normalized
                    loc_list_normalized_geo.append([line[6], line[5]])  # Nested list avec noms normalisés + coordonnées
                    loc_list_normalized_wkd.append([line[6], line[3]])  # Nested list avec noms normalisés + id Wikidata
                    loc_list_occurrences.append([line[6], loc_list_normalized.count(line[6])])
                    # On ajoute les noms de lieux originaux à loc_list_deduplicated (s'ils n'y sont pas déjà)
                    if line[2] not in loc_list_deduplicated:
                        loc_list_deduplicated.append(line[2])

                    # On récupère dans chaque fichier TEI des informations sur les documents
                    shortTitle = root.find('.//tei:titleStmt/tei:title', ns).text
                    shortTitle = re.sub(r"\n( +)", " ", shortTitle)
                    printer = root.find('.//tei:publisher', ns).text
                    pubPlace = root.find('.//tei:pubPlace', ns).text
                    typeText = root.find('.//tei:keywords/tei:term', ns).text
                    genre = root.find(".//tei:keywords//tei:term[@type='sagrado_profano']", ns).text
                    date = root.find('.//tei:date', ns)
                    # print(genre.text)

                    # On récupère la longitude et la latitude
                    if line[5] != '':
                        new_coords = line[5].split(',')
                        # print(new_coords[0])
                        long = new_coords[0]
                        lat = new_coords[1]

                    # On ajoute ces informations à la fin de chaque ligne
                    line.append(long)
                    line.append(lat)
                    line.append(shortTitle)
                    line.append(pubPlace)
                    line.append(printer)
                    if re.match("184[0-9]", date.text):
                        line.append('1840-1849')
                    elif re.match("185[0-9]", date.text):
                        line.append('1850-1859')
                    elif re.match("186[0-9]", date.text):
                        line.append('1860-1869')
                    elif re.match("187[0-9]", date.text):
                        line.append('1870-1879')
                    elif re.match("188[0-9]", date.text):
                        line.append('1880-1889')
                    else:
                        line.append('[s.a]')
                    line.append(typeText)
                    line.append(genre)
                    line.append('https://desenrollandoelcordel.unige.ch/Pliegos/' + file)

                    # On ajoute la nouvelle ligne à la new_csvLine
                    new_csvLine.append(line)
                    # print(line)

            # On retire les doublons de la nested list loc_list_normalized_geo
            total_geo = {}
            for k, v in loc_list_normalized_geo:
                total_geo[k] = str(total_geo.get(k, v))
            loc_list_geo_deduplicated = [list(t) for t in total_geo.items()]

            # On retire les doublons de la nested list loc_list_normalized_wkd
            total_wkd = {}
            for p, w in loc_list_normalized_wkd:
                total_wkd[p] = str(total_wkd.get(p, w))
            loc_list_wkd_deduplicated = [list(e) for e in total_wkd.items()]
            # print(loc_list_wkd)

            # Boucle pour ajouter les noms de lieu dans le texte
            for l in root.findall(".//tei:l", ns):
                if l.text is not None:
                    # print(id_doc, l.text, '->', type(l))
                    for i in range(len(loc_list_deduplicated)):
                        # On vérifie que le nom de lieu est dans le texte et on l'encode avec <name>
                        if loc_list_deduplicated[i] in l.text and l.text is not None:
                            new_line = l.text.replace(loc_list_deduplicated[i], '<name>' + loc_list_deduplicated[i] + '</name>')
                            l.text = new_line

            sourceDesc = root.find('.//tei:sourceDesc', ns)  # On récupère l'élément <sourceDesc>
            listPlace = eT.SubElement(sourceDesc, 'listPlace')  # On ajoute à <sourceDesc> l'élément <listPlace>
            listPlace.set("{http://www.w3.org/XML/1998/namespace}base", "https://www.wikidata.org/wiki/")  # On ajoute un attribut @xml:base avec l'URL de base de Wikidata

            # Boucle pour ajouter les noms de lieu dans le <teiHeader>
            for place in loc_list_geo_deduplicated:
                if place[0] != "":
                    placeElement = eT.SubElement(listPlace, "place")  # On ajoute l'élément <place>
                    placeNb = loc_list_normalized.count(place[0])  # On compte le nb de fois où le nom de lieu apparaît dans le texte
                    placeElement.set("n", str(placeNb))  # On ajoute à <placeName> un @n avec le nb d'occurrences du lieu
                    placeElement.set("key", place[0].replace(" ", "_"))

                    for i in range(len(loc_list_wkd_deduplicated)):
                        if loc_list_wkd_deduplicated[i][0] == place[0]:
                            placeElement.set("corresp", loc_list_wkd_deduplicated[i][1])  # On ajoute @corresp à <place> avec l'id wkd

                    placeName = eT.SubElement(placeElement, "placeName")  # On ajoute l'élément <placeName>
                    placeName.text = place[0].title()  # On ajoute à <placeName> les noms de lieux en rétablissant les majuscules

                    location = eT.SubElement(placeElement, "location")  # On ajoute l'élément <location>
                    geo = eT.SubElement(location, "geo")  # On ajoute l'élément <geo>
                    geo.text = place[1].replace(",", " ")  # On ajoute les coordonnées géographiques

        # Permet d'afficher tout ou partie d'un arbre xml dans la console
        # eT.dump(listPlace)
        # print('\n')

        # On modifie les fichiers TEI
        # tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
        # print(file + ": DONE.")

# Création d'un nouveau fichier CSV avec les informations issues des fichiers TEI
# Liste avec les noms des colonnes
new_csv_header = ['index', 'id_doc', 'original_name', 'id_wkd', 'type_place', 'coord', 'normalized_name',
                  'longitude', 'latitude', 'shortTitle', 'pubPlace', 'printer', "date", "type_text", 'genre', 'url']
# print(new_csvLine)

with open('../Encodage/nerList_v3.csv', 'w', encoding='utf-8', newline='') as newCsv:
    writer = csv.writer(newCsv)
    writer.writerow(new_csv_header)  # On ajoute la 1ère ligne avec le nom des colonnes
    writer.writerows(new_csvLine)  # On ajoute les nouvelles lignes
    newCsv.close()
