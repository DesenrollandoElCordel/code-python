# Developed by Elina Leblanc (University of Geneva)

import os
import xml.etree.ElementTree as eT
import csv
import re

xml_folder = "../Encodage/Moreno-TEI-files"
new_csvLine = []  # List to create a new CSV file

for file in os.listdir(xml_folder):
    if file.endswith('.xml'):
        xml_path = os.path.join(xml_folder, file)  # We create a path to the files

        # TEI Namespace declaration
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = eT.parse(xml_path)  # We parse the TEI files
        root = tree.getroot()  # We get the root
        id_doc = root.get("{http://www.w3.org/XML/1998/namespace}id")  # We get the ID of the document

        with open('../pliegos-ner/moreno-ner/nerList_Moreno_Wikidata.csv', encoding='utf-8') as f:
            csv_file = csv.reader(f)  # We parse the CSV file
            next(csv_file)  # We skip the first line

            loc_list_deduplicated = []  # List with original names (no duplicate)
            loc_list_normalized = []  # List with normalised names (with duplicates)
            loc_list_normalized_geo = []  # List with normalised names + geographical coordinates (with duplicates)
            loc_list_normalized_wkd = []  # List with normalised names + wikidata id (with duplicates)
            loc_list_occurrences = []

            for line in csv_file:  # We parse the csv file
                if line[1].lower() == id_doc.lower():  # If the line has the same id as the TEI file
                    loc_list_normalized.append(line[6])  # List with normalised names
                    loc_list_normalized_geo.append([line[6], line[5]])  # Nested list with normalised names + coordinates
                    loc_list_normalized_wkd.append([line[6], line[3]])  # Nested list with normalised names + id Wkd

                    # We create a deduplicate list with the normalised names
                    if line[2] not in loc_list_deduplicated:
                        loc_list_deduplicated.append(line[2])

                    # We get information in the TEI files
                    shortTitle = root.find('.//tei:titleStmt/tei:title', ns).text
                    shortTitle = re.sub(r"\n( +)", " ", shortTitle)
                    printer = root.find('.//tei:publisher', ns).text
                    pubPlace = root.find('.//tei:pubPlace', ns).text
                    typeText = root.find('.//tei:keywords/tei:term', ns).text
                    genre = root.find(".//tei:keywords//tei:term[@type='sagrado_profano']", ns).text
                    date = root.find('.//tei:date', ns)
                    # print(genre.text)

                    # We get the longitude and latitude
                    if line[5] != '':
                        new_coords = line[5].split(',')
                        # print(new_coords[0])
                        long = new_coords[0]
                        lat = new_coords[1]

                    # We add the TEI information at the end of each line
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

                    new_csvLine.append(line)
                    # print(line)

            # Deduplicated list for geographical coordinates
            total_geo = {}
            for k, v in loc_list_normalized_geo:
                total_geo[k] = str(total_geo.get(k, v))
            loc_list_geo_deduplicated = [list(t) for t in total_geo.items()]

            # Deduplicated list for WKD id
            total_wkd = {}
            for p, w in loc_list_normalized_wkd:
                total_wkd[p] = str(total_wkd.get(p, w))
            loc_list_wkd_deduplicated = [list(e) for e in total_wkd.items()]
            # print(loc_list_wkd)

            # We add a <name> element inside the body of the TEI file
            for l in root.findall(".//tei:l", ns):
                if l.text is not None:
                    # print(id_doc, l.text, '->', type(l))
                    for i in range(len(loc_list_deduplicated)):
                        # On vérifie que le nom de lieu est dans le texte et on l'encode avec <name>
                        if loc_list_deduplicated[i] in l.text and l.text is not None:
                            new_line = l.text.replace(loc_list_deduplicated[i], '<name>' + loc_list_deduplicated[i] + '</name>')
                            l.text = new_line

            # We create a list of place in the <teiHeader>
            sourceDesc = root.find('.//tei:sourceDesc', ns)
            listPlace = eT.SubElement(sourceDesc, 'listPlace')  # We add <listPlace> in <sourceDesc>
            # We add an @xml:base attribute with URL of Wikidata
            listPlace.set("{http://www.w3.org/XML/1998/namespace}base", "https://www.wikidata.org/wiki/")

            for place in loc_list_geo_deduplicated:
                if place[0] != "":
                    placeElement = eT.SubElement(listPlace, "place")  # We add <place> in <listPlace>
                    placeNb = loc_list_normalized.count(place[0])  # We count the number of time a name appears in the text
                    placeElement.set("n", str(placeNb))  # @n with the numbre of occurrences
                    placeElement.set("key", place[0].replace(" ", "_"))  # @key with the name of the place

                    for i in range(len(loc_list_wkd_deduplicated)):
                        if loc_list_wkd_deduplicated[i][0] == place[0]:
                            placeElement.set("corresp", loc_list_wkd_deduplicated[i][1])  # @corresp with id Wkd

                    placeName = eT.SubElement(placeElement, "placeName")  # We add the element <placeName>
                    placeName.text = place[0].title()  # We add the name of place

                    location = eT.SubElement(placeElement, "location")  # We add a <location> element
                    geo = eT.SubElement(location, "geo")  # We add a <geo> element
                    geo.text = place[1].replace(",", " ")  # We add the geographical coordinates

        # Print the XML tree in the console
        # eT.dump(listPlace)
        # print('\n')

        # We modify the TEI files
        # tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
        # print(file + ": DONE.")

# Creation of a new CSV file with the TEI information
# List with the name of the columns
new_csv_header = ['index', 'id_doc', 'original_name', 'id_wkd', 'type_place', 'coord', 'normalized_name',
                  'longitude', 'latitude', 'shortTitle', 'pubPlace', 'printer', "date", "type_text", 'genre', 'url']
# print(new_csvLine)

with open('../Encodage/nerList_v3.csv', 'w', encoding='utf-8', newline='') as newCsv:
    writer = csv.writer(newCsv)
    writer.writerow(new_csv_header)  # 1st line with the name of columns
    writer.writerows(new_csvLine)  # We add the new lines
    newCsv.close()
