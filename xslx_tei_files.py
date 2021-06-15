from openpyxl import load_workbook
from lxml import etree
import os


def traitement_motsclefs(motclef, element):
    if motclef is not None:
        if "," in motclef:
            motclefs_personajes_split = motclef.split(", ")
            for x in motclefs_personajes_split:
                item = etree.SubElement(element, "item", corresp="")
                item.text = x
        else:
            item = etree.SubElement(element, "item", corresp="")
            item.text = motclef


wb = load_workbook(filename='index_grabados.xlsx')
index = wb['Feuil1']

title_engravings = []

for row in index.iter_rows(min_row=2, max_row=6, max_col=6, values_only=True):
    row_list = list(row)
    title_engravings.append(row_list)

print(title_engravings)

for i in range(len(title_engravings)):
    root = etree.Element("TEI")

    teiHeader = etree.SubElement(root, "teiHeader", xmlns="http://www.tei-c.org/ns/1.0", xmlid=title_engravings[i][0])
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
    pubStmt_child2 = etree.SubElement(pubStmt, "availability")
    pubStmt_child2_p = etree.SubElement(pubStmt_child2, "p")
    pubStmt_child2_p.text = "CC-BY-NC-SA"
    sourceDesc = etree.SubElement(fileDesc, "sourceDesc")
    sourceDesc_p = etree.SubElement(sourceDesc, "p")
    sourceDesc_p.text = "Grabado extraído del pliego " + title_engravings[i][1]

    text = etree.SubElement(root, "text")
    body = etree.SubElement(text, "body")
    div = etree.SubElement(body, "div")
    figure = etree.SubElement(div, "figure")

    graphic = etree.SubElement(figure, "graphic", url=title_engravings[i][0]+".jpg")

    figDesc = etree.SubElement(figure, "figDesc")
    locus1 = etree.SubElement(figDesc, "locus", target=title_engravings[i][1]+".xml")
    locus1.text = title_engravings[i][2]
    date = etree.SubElement(figDesc, "date")
    date.text = str(title_engravings[i][3])

    keywords_personajes = etree.SubElement(figDesc, "list", type="personajes", xmlbase="http://vocab.getty.edu/page/aat/")
    traitement_motsclefs(title_engravings[i][4], keywords_personajes)

    keywords_objetos = etree.SubElement(figDesc, "list", type="objetos", xmlbase="http://vocab.getty.edu/page/aat/")
    traitement_motsclefs(title_engravings[i][5], keywords_objetos)

    tree = etree.ElementTree(root)

    path_tei = 'TEI_Gravures/'
    if not os.path.isdir(path_tei):
        os.mkdir(path_tei)

    filename = title_engravings[i][0] + '.xml'
    # print(filename)

    filename_path = os.path.join(path_tei, filename)
    # print(filename_path)

    if not os.path.isfile(filename_path):
        tree.write(filename_path, xml_declaration=True, encoding='UTF-8', pretty_print=True)

    # print(etree.tostring(root, xml_declaration=True, encoding='UTF-8', pretty_print=True))
