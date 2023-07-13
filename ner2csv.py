# Developed by Dr. Kalitvianski Ruslan and Leblanc Elina

import os
import pandas as pd

ner_folder = "../pliegos-ner/moreno-ner/moreno-IOB"
ner_list = []

for file in os.listdir(ner_folder):
    ner_path = os.path.join(ner_folder, file)  # We create the path to read the files
    label, ext = os.path.splitext(file)  # We split the name and the extension of the files
    if file.endswith('.txt'):
        # We open the txt files
        with open(ner_path, 'r') as f:
            text = f.read()
            # print(text)

        lines = text.split('\n')  # We get the lines
        en = ""  # We initiate an empty variable for the named entities

        for line in lines:
            if line.endswith('O'):  # If a line ends by O (no entities)
                if len(en) > 0:  # Case 1: If en is not empty, we add en to ner_list and empty en
                    ner_list.append([label, en + ""])
                    en = ""
                else:  # Case 2: if en is empty, we move to the next line
                    pass
            elif line.endswith('B-LOC'):  # If a line ends by B-LOC
                if len(en) > 0:  # Case 1: If en is not empty, we add en to ner_list
                    ner_list.append([label, en+""])
                else:  # Case 2: If en is empty, we split the line to get only the entity name
                    en = line.split(" ")[0]
            else:  # If a line ends by I-LOC
                en += " "+line.split(" ")[0]  # Only case, we concat the entity name with en
print(ner_list)

# We create a dataframe
df = pd.DataFrame(ner_list, columns=['id_doc', 'original_name'])
# print(df)

# We export the dataframe in CSV
df.to_csv("nerList_Moreno.csv", encoding='utf-8')
