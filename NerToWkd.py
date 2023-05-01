import os
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

endpoint_url = "https://query.wikidata.org/sparql"

loc_list = ['España', 'Lóndres', 'Madrid', 'Puerto-Rico']
prefix = """SELECT DISTINCT ?item ?num ?countryLabel ?coordinate ?typeLabel ?type {
    SERVICE wikibase:mwapi {
        bd:serviceParam wikibase:api "EntitySearch".
        bd:serviceParam wikibase:endpoint "www.wikidata.org".
        bd:serviceParam mwapi:search \""""

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
LIMIT 2"""

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results_all = "value\tcountry\tcoordinates\n"
for entity in loc_list:
    results = get_results(endpoint_url, prefix + entity + suffix)
    for result in results["results"]["bindings"]:
        results_all += result["item"]["value"]+'\t'+result["countryLabel"]["value"]+'\t'+result["coordinate"]["value"] + os.linesep

text_file = open("Output.txt", "w")
text_file.write(results_all.strip())
text_file.close()
