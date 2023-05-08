import os
import pandas as pd

ner_folder = "../Encodage/moreno_035"

ner_list_concat = []

for file in os.listdir(ner_folder):
    ner_path = os.path.join(ner_folder, file)  # Chemin vers le fichier .conll
    label, ext = os.path.splitext(file)  # On sépare le nom du fichier de son extension
    if file.endswith('.conll'):
        with open(ner_path, 'r') as f:
            text = f.read()
            # print(text)

        ner_list = []
        lines = text.split('\n')  # On découpe le texte ligne par ligne

        # Pour chaque ligne, si elle finit par 'LOC', on l'ajoute à ner_list
        for line in lines:
            if line.endswith('LOC'):
                ner_list.append(line)
        # print(ner_list)

        # Boucle spéciale pour les noms de lieux avec plusieurs tokens (B-LOC + I-LOC)
        # On récupére l'index (i) et chaque élément (e) de ner_list
        for i, e in enumerate(ner_list):
            # print(i, '->', e)
            # On cible uniquement les éléments qui finissent par 'I-LOC' et dont l'élément précédent 'B-LOC'
            if e.endswith('I-LOC') and ner_list[i-1].endswith('B-LOC'):
                new_ILOC = e.replace(" I-LOC", "")  # On enlève 'I-LOC'
                new_BLOC = ner_list[i-1].replace(" B-LOC", "")  # On enlève 'B-LOC'
                ner_list_concat.append([label.title(), new_BLOC + " " + new_ILOC])  # On concatène les tokens pour reformer le nom de lieu
                ner_list.remove(e)  # On enlève l'élément avec 'I-LOC' de ner_list
                ner_list.pop(i-1)  # On enlève l'élément avec 'B-LOC' de ner_list
                # print(ner_list[i-1] + " " + e)
        # print(ner_list)

        # Boucle pour les autres noms de lieux
        for l in ner_list:
            if l.endswith("B-LOC"):
                new_loc = l.replace(" B-LOC", "")  # On enlève 'B-LOC'
                ner_list_concat.append([label.title(), new_loc])  # On ajoute les noms de lieux à ner_list_concat
        ner_list_concat.sort()  # On trie les lieux par ordre alphabétique
print(ner_list_concat)

df = pd.DataFrame(ner_list_concat, columns=['id_doc', 'original_name'])  # On crée un DataFrame à partir de la liste
# print(df)
# df.to_csv("../Encodage/moreno_035/nerList_v1.csv", encoding='utf-8')  # On exporte en CSV
