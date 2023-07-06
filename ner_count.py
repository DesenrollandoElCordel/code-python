import csv
import pandas as pd

places_all = []
places_deduplicated = []
places_count = []

with open('../pliegos-ner/moreno-ner/nerList_Moreno_enriched.csv', encoding='utf-8') as f:
    csv_file = csv.reader(f)  # On parcourt le fichier CSV
    next(csv_file)

    for line in csv_file:
        places_all.append(line[6])
        if line[6] != "" and line[6] not in places_deduplicated:
            places_deduplicated.append(line[6])
            places_deduplicated.sort()

# print(places_deduplicated)
for x in places_deduplicated:
    nb = places_all.count(x)
    places_count.append([x, nb])

# print(places_count)

# df = pd.DataFrame(places_count, columns=['Lieux', 'Occurrences'])
# print(df)
# df.to_excel("Moreno_Places.xlsx")
