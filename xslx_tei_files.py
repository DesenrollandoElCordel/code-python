from openpyxl import load_workbook
from lxml import etree
import xml.etree.ElementTree as eT
import os


# Fonction pour la gestion des mots-clés
def add_list_keywords(keyword):
    tree = eT.parse('/Users/elinaleblanc/Documents/Postdoctorat/Encodage/TEI_tests/Index_gravures/taxonomy_grabados.xml')
    root = tree.getroot()
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    list_keywords = etree.SubElement(keywords, "term")

    for x in root.findall('.//tei:category', ns):
        att = x.get('{http://www.w3.org/XML/1998/namespace}id')
        catdesc = x[0].text
        if att == keyword:
            list_keywords.text = catdesc


def add_keywords(keyword, category, element):
    keyword = str(keyword)
    if keyword is not None:
        if "," in keyword:  # Gestion des catégories avec plusieurs mots-clés
            keyword_split = keyword.split(",")
            for k in keyword_split:
                catref = etree.SubElement(element, "catRef", scheme="#" + category, target="#" + k)
                add_list_keywords(k)
        else:
            catref = etree.SubElement(element, "catRef", scheme="#" + category, target="#" + keyword)
            add_list_keywords(keyword)


wb = load_workbook(filename='/Users/elinaleblanc/Downloads/Index_Grabados_Moreno.xlsx')
index = wb['Feuil1']
# print(index)

# Récupération des noms de colonnes
list_name_columns = []
for row in index.iter_rows(max_row=1, max_col=23, values_only=True):
    list_name_columns.append(row)
# print(list_name_columns)

# Récupération des descriptions
title_engravings = []
for row in index.iter_rows(min_row=2, max_row=10, max_col=23, values_only=True):
    row_list = list(row)
    title_engravings.append(row_list)
# print(title_engravings)

# Création des fichiers .xml
for i in range(len(title_engravings)):
    root = etree.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0", xmlid=title_engravings[i][0])
    teiHeader = etree.SubElement(root, "teiHeader")

    fileDesc = etree.SubElement(teiHeader, "fileDesc")
    titleStmt = etree.SubElement(fileDesc, "titleStmt")
    title = etree.SubElement(titleStmt, "title")
    title.text = title_engravings[i][0]

    respStmt = etree.SubElement(titleStmt, "respStmt")
    name = etree.SubElement(respStmt, "name")
    resp = etree.SubElement(respStmt, "resp")
    resp.text = "Codificación TEI"

    pubStmt = etree.SubElement(fileDesc, "publicationStmt")
    pubStmt_child1 = etree.SubElement(pubStmt, "authority")
    pubStmt_child1.text = "Bibliothèque Universitaire de Genève (BUNIGE)"
    pubStmt_child2 = etree.SubElement(pubStmt, "availability", status="restricted")
    licence = etree.SubElement(pubStmt_child2, "licence", n="cc by nc sa", target="https://creativecommons.org/licenses/by-nc-sa/4.0/")

    sourceDesc = etree.SubElement(fileDesc, "sourceDesc")
    bibl = etree.SubElement(sourceDesc, "bibl")

    title_bibl = etree.SubElement(bibl, "title")
    title_bibl.text = title_engravings[i][0]
    author = etree.SubElement(bibl, "author")

    publisher = etree.SubElement(bibl, "publisher")
    publisher.text = "José María Moreno"
    pubPlace = etree.SubElement(bibl, "pubPlace")
    pubPlace.text = "Carmona (Sevilla)"
    date = etree.SubElement(bibl, "date")
    date.text = str(title_engravings[i][5])
    if title_engravings[i][5] == "[s.a.]":
        date.set("when", "1800")
        date.set("cert", "low")
    else:
        date.set("when", str(title_engravings[i][5]))
        date.set("cert", "high")

    ident = etree.SubElement(bibl, "ident", type="DOI")

    figure = etree.SubElement(bibl, "figure")
    graphic = etree.SubElement(figure, "graphic", url="")
    figDesc = etree.SubElement(figure, "figDesc")
    locus1 = etree.SubElement(figDesc, "locus", target=title_engravings[i][1]+".xml")
    locus1.text = title_engravings[i][4]

    note1 = etree.SubElement(bibl, "note", type="similar_ejemplar")
    note2 = etree.SubElement(bibl, "note", type="origen")
    note2.text = "Grabado extraído del pliego " + title_engravings[i][1]

    encodingDesc = etree.SubElement(teiHeader, "encodingDesc")
    projectDesc = etree.SubElement(encodingDesc, "projectDesc")
    paragraph = etree.SubElement(projectDesc, "p")
    paragraph.text = "Este archivo fue creado en el marco del proyecto Desenrollando el Cordel/Démêler le cordel/Untangling the cordel, dirigido por la profesora Constance Carta de la Universidad de Ginebra, con el apoyo de la Fundación filantrópica Famille Sandoz-Monique de Meuron."

    profileDesc = etree.SubElement(teiHeader, "profileDesc")
    textClass = etree.SubElement(profileDesc, 'textClass')
    keywords = etree.SubElement(textClass, 'keywords')

    add_keywords(title_engravings[i][5], list_name_columns[0][5], textClass)  # Catégorie 'personaje_masculino'
    add_keywords(title_engravings[i][6], list_name_columns[0][6], textClass)  # Catégorie 'personaje_femenino'
    add_keywords(title_engravings[i][7], list_name_columns[0][7], textClass)  # Catégorie 'grupos_personajes'
    add_keywords(title_engravings[i][8], list_name_columns[0][8], textClass)  # Catégorie 'actitud'
    add_keywords(title_engravings[i][9], list_name_columns[0][9], textClass)  # Catégorie 'muerte'
    add_keywords(title_engravings[i][10], list_name_columns[0][10], textClass)  # Catégorie 'religion'
    add_keywords(title_engravings[i][11], list_name_columns[0][11], textClass)  # Catégorie 'monstruo'
    add_keywords(title_engravings[i][12], list_name_columns[0][12], textClass)  # Catégorie 'animales'
    add_keywords(title_engravings[i][13], list_name_columns[0][13], textClass)  # Catégorie 'atuendo'
    add_keywords(title_engravings[i][14], list_name_columns[0][14], textClass)  # Catégorie 'instrumento_musical'
    add_keywords(title_engravings[i][15], list_name_columns[0][15], textClass)  # Catégorie 'arma_de_fuego'
    add_keywords(title_engravings[i][16], list_name_columns[0][16], textClass)  # Catégorie 'arma_blanca'
    add_keywords(title_engravings[i][17], list_name_columns[0][17], textClass)  # Catégorie 'accesorios_varios'
    add_keywords(title_engravings[i][18], list_name_columns[0][18], textClass)  # Catégorie 'espacio_construido'
    add_keywords(title_engravings[i][19], list_name_columns[0][19], textClass)  # Catégorie 'ambiente_natural'
    add_keywords(title_engravings[i][20], list_name_columns[0][20], textClass)  # Catégorie 'ambiente_maritimo'
    add_keywords(title_engravings[i][21], list_name_columns[0][21], textClass)  # Catégorie 'elementos_decorativos'

    text = etree.SubElement(root, "text")
    body = etree.SubElement(text, "body")
    paragraph2 = etree.SubElement(body, "p")

    tree = etree.ElementTree(root)

    path_tei = '../TEI_Gravures/'
    if not os.path.isdir(path_tei):
        os.mkdir(path_tei)

    filename = title_engravings[i][0] + '.xml'
    # print(filename)

    filename_path = os.path.join(path_tei, filename)
    # print(filename_path)

    '''if not os.path.isfile(filename_path):
        tree.write(filename_path, xml_declaration=True, encoding='UTF-8', pretty_print=True)'''

    print(etree.tostring(root, xml_declaration=True, encoding='UTF-8', pretty_print=True))
