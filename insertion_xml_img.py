import xml.etree.ElementTree as eT
import os
import argparse

# Création des arguments
parser = argparse.ArgumentParser()
parser.add_argument('--xml', default='transcriptions', type=str, help="Le chemin du dossier des fichiers xml à charger.")
args = parser.parse_args()

for f in os.listdir(args.xml):
    if not f.endswith('.DS_Store'):
        xml_path = os.path.join(args.xml, f)  # Chemin vers les fichiers .xml
        label, extension = os.path.splitext(f)  # Récupération du nom du fichier sans l'extension
        # print(label)

        # Déclaration du namespace
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = eT.parse(xml_path)  # On parcourt chaque fichier .xml
        root = tree.getroot()  # On récupère l'élément racine
        # print(root)

        for pb in root.findall('.//tei:pb', ns):  # On itère à travers chaque <pb/>
            # print(pb)
            numberPage = pb.get('n')  # On récupère @n
            url = 'https://iiif.unige.ch/demelercordel/'  # On crée le 'base URI'
            pb.set('facs', url + label + '_' + numberPage + '.jpg')  # On ajoute un @facs à chaque <pb/> avec pour valeur le nouvel URI

        new_folder = "encodage_updated/"  # On crée un nouveau dossier pour enregistrer les nouveaux .xml
        if not os.path.isdir(new_folder):  # On vérifie s'il existe. Si non, on le crée
            os.mkdir(new_folder)

        new_path = os.path.join(new_folder, f)  # Création du nouveau chemin vers les nvx fichiers .xml
        # print(new_path)
        tree.write(new_path, encoding="UTF-8", xml_declaration=True)  # Création des nvx arbres .xml et enregistrement dans le nouveau dossier !
