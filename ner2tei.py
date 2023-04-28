import xml.etree.ElementTree as eT

ner_file = "../Encodage/moreno_035/Moreno_035.conll"
xml_file = "../Encodage/Moreno-TEI-files/Moreno_035.xml"

with open(ner_file, 'r') as f:
    text = f.read()

ner_list_raw = []
ner_list_normalized = []
ner_list_deduplicated = []

# On découpe le texte par ligne
new_text = text.split('\n')

# Pour chaque ligne, si elle finit par 'LOC', on l'ajoute à la liste ner_list_raw
for line in new_text:
    if line.endswith('LOC'):
        ner_list_raw.append(line)

# Boucle spéciale pour les noms de lieux avec plusieurs tokens (B-LOC + I-LOC)
# On récupére l'index (i) et chaque élément (e) de ner_list_raw
for i, e in enumerate(ner_list_raw):
    # print(i, '->', e)
    # On cible uniquement les éléments qui finissent par 'I-LOC' et dont l'élément précédent est un 'B-LOC'
    if e.endswith('I-LOC') and ner_list_raw[i-1].endswith('B-LOC'):
        new_ILOC = e.replace(" I-LOC", "")  # On enlève 'I-LOC'
        new_BLOC = ner_list_raw[i-1].replace(" B-LOC", "")  # On enlève 'B-LOC'
        ner_list_normalized.append(new_BLOC + " " + new_ILOC)  # On concatène les tokens pour reformer le nom de lieu
        ner_list_raw.remove(e)  # On enlève l'élément avec 'I-LOC' de ner_list_raw
        ner_list_raw.pop(i-1)  # On enlève l'élément avec 'B-LOC' de ner_list_raw
        # print(ner_list_raw[i-1] + " " + e)
# print(ner_list_raw)

# Boucle pour les autres noms de lieux
for l in ner_list_raw:
    new_loc = l.replace(" B-LOC", "")  # On enlève 'B-LOC'
    ner_list_normalized.append(new_loc)  # On ajoute les noms de lieux à ner_list_normalized
# print(ner_list_normalized)
ner_list_normalized.sort()  # On trie les lieux par ordre alphabétique

# On crée une liste spéciale sans doublons
for item in ner_list_normalized:
    if item not in ner_list_deduplicated:
        ner_list_deduplicated.append(item)
# print(ner_list_deduplicated)

tree = eT.parse(xml_file)  # On parse le fichier XML-TEI
root = tree.getroot()  # On récupére la racine du fichier TEI

# Déclaration du namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

# Encodage des noms de lieu dans le texte
for l in root.findall(".//tei:l", ns):
    # On récupère l'index de chaque élément de la liste
    for i in range(len(ner_list_deduplicated)):
        # print(ner_list[i])
        # On vérifie que le nom de lieu est dans le texte et on l'encode avec <name>
        if ner_list_deduplicated[i] in l.text:
            new_line = l.text.replace(ner_list_deduplicated[i], '<name>' + ner_list_deduplicated[i] + '</name>')
            l.text = new_line

# Encodage des noms de lieu dans le teiHeader
sourceDesc = root.find('.//tei:sourceDesc', ns)  # On récupère l'élément <sourceDesc>
listPlace = eT.SubElement(sourceDesc, 'listPlace')  # On ajoute à <sourceDesc> l'élément <listPlace>

for place in ner_list_deduplicated:
    placeElement = eT.SubElement(listPlace, "place")  # On ajoute l'élément <place>
    placeName = eT.SubElement(placeElement, "placeName")  # Puis l'élément <placeName>
    placeName.text = place.title()  # On ajoute à <placeName> les noms de lieux en rétablissant les majuscules
    placeNb = ner_list_normalized.count(place)  # On compte le nb de fois où le nom de lieu apparaît dans le texte
    placeElement.set("n", str(placeNb))  # On ajoute à <placeName> un @n avec le nb d'occurrences du lieu

# eT.dump(sourceDesc)
# tree.write(xml_file, encoding="UTF-8", xml_declaration=True)
