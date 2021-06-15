import os
import xml.etree.ElementTree as ET

# Dossier de départ
list_folder = "transcriptions"

# On itère à travers les sous-dossiers
for subdir, dirs, files in os.walk(list_folder):
    list_file = []  # Liste avec les noms de fichiers .xml

    for file in files:
        if not file.endswith('.DS_Store') | file.endswith('mets.xml') | file.startswith('Masterfile'):
            '''print(os.path.join(subdir, file))'''
            label, ext = os.path.splitext(file)  # On récupère le nom sans l'extension
            list_file.append(file)  # On ajoute les fichiers .xml à la liste
            list_file.sort()  # On les organise par ordre alphabétique
            '''print(list_file)'''

            # Création du fichier xml avec pour racine <master>
            root = ET.Element("master", attrib={"xmlns:xi": "http://www.w3.org/2001/XInclude"})
            
            for x in list_file:  # On itère dans la liste des fichiers .xml
                ET.SubElement(root, "xi:include", {"href": x})  # Pour chaque fichier, on crée un élément <xi:include>, enfant de master

            tree = ET.ElementTree(root)  # On organise les éléments en arbre XML
            masterfile_name = 'Masterfile_' + label[:10] + '.xml'  # On crée le nom du masterfile
            masterfile_path = os.path.join(subdir, masterfile_name)  # On crée le chemin du masterfile
            tree.write(masterfile_path, encoding="UTF-8", xml_declaration=True, method="xml")  # On crée le fichier .xml
