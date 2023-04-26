import xml.etree.ElementTree as eT

ner_file = "../Encodage/moreno_035/Moreno_035.conll"
xml_file = "../Encodage/Moreno-TEI-files/Moreno_035.xml"

with open(ner_file, 'r') as f:
    text = f.read()

ner_list_raw = []
ner_list_normalized = []

new_text = text.split('\n')
for line in new_text:
    if line.endswith('LOC'):
        ner_list_raw.append(line)

for i, e in enumerate(ner_list_raw):
    # print(i, '->', e)
    if e.endswith('I-LOC') and ner_list_raw[i-1].endswith('B-LOC'):
        # Enlever e de la liste ner_list_raw
        new_ILOC = e.replace(" I-LOC", "")
        new_BLOC = ner_list_raw[i-1].replace(" B-LOC", "")
        ner_list_normalized.append(new_BLOC + " " + new_ILOC)
        ner_list_raw.remove(e)
        ner_list_raw.pop(i-1)
        # print(ner_list_raw[i-1] + " " + e)
# print(ner_list_raw)

for l in ner_list_raw:
    new_loc = l.replace(" B-LOC", "")
    ner_list_normalized.append(new_loc)
# print(ner_list_normalized)

