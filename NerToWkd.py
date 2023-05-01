import os
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

# Liste avec des noms de lieux
loc_list = ['España', 'Lóndres', 'Madrid', 'Puerto-Rico', 'Ungría', "París", "Dinamarca"]

# Début de la requête SPARQL (avant le nom de lieu)
prefix = """SELECT DISTINCT ?item ?itemLabel ?num ?countryLabel ?coordinate ?typeLabel ?type {
    SERVICE wikibase:mwapi {
        bd:serviceParam wikibase:api "EntitySearch".
        bd:serviceParam wikibase:endpoint "www.wikidata.org".
        bd:serviceParam mwapi:search \""""

# Fin de la requête SPARQL (après le nom de lieu)
suffix = """\".
        bd:serviceParam mwapi:language "es".
        ?item wikibase:apiOutputItem mwapi:item.
        ?num wikibase:apiOrdinal true.
    }
    ?item (wdt:P279|wdt:P31) ?type ;
           wdt:P17 ?country ;
           wdt:P625 ?coordinate .

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?num
LIMIT 5"""

# Fonction pour récupérer les résultats de la requête sur Wikidata
def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


# Variable qui contient l'ensemble des résultats
results_all = "item;itemlabel;country;coordinates;typeLabel" + os.linesep
# Pour chaque nom de lieu dans la liste, on concatène le début de la requête, le nom de lieu et la fin de la requête
for entity in loc_list:
    results = get_results(endpoint_url, prefix + entity + suffix)
    for result in results["results"]["bindings"]:
        # On récupère une partie des résultats et on les ajoute à results_all
        results_all += result["item"]["value"]+';'+result["itemLabel"]["value"]+';'+result["countryLabel"]["value"] + ';' + result["coordinate"]["value"] + ';' + result["typeLabel"]["value"] + os.linesep

# On exporte les résultats en CSV
text_file = open("WikidataOutput.csv", "w")
text_file.write(results_all.strip())
text_file.close()
