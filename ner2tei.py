import xml.etree.ElementTree as eT

ner_file = "../Encodage/moreno_035/Moreno_035.xml"

tree = eT.parse(ner_file)
root = tree.getroot()
# print(root)

ner_list = []
ne = ""

for loc in root.findall(".//de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token/de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity"):
    wkd = loc.get('identifier')
    ner_list.append([loc.text, wkd])

for loc in root.findall(".//de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity"):
    listloc = list(loc)
    wkd = loc.get('identifier')
    if (len(listloc) > 1):
        new_loc = ""
        for ne in listloc:
            new_loc += str(ne.text) + " "
            # print(new_loc + " ")
        ner_list.append([new_loc, wkd])
print(ner_list)
