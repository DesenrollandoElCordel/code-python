import os
import argparse
import cv2
import xml.etree.ElementTree as et
import re
import numpy as np

# Création des arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", default='images', type=str, help="le chemin du dossier des images à charger")
parser.add_argument('--xml', default='OCR-files', type=str, help="Le chemin du dossier des fichiers xml à charger.")
args = parser.parse_args()

list_images = os.listdir(args.image)

for subdir, dirs, files in os.walk(args.xml):
    for file in files:
        xml_path = os.path.join(subdir, file)  # Chemin vers les fichiers .xml
        label, ext = os.path.splitext(file)  # Récupération du nom sans l'extension
        list_coord_str = []  # Liste avec les coordonnées "brutes" (en str)
        list_coord_int = []  # Liste avec les coordonnées transformées en int
        ns = {'page': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}  # Déclaration du namespace

        if file.endswith('.xml'):
            document = et.parse(xml_path)  # On parse le fichier .xml
            root = document.getroot()  # On récupère l'élément racine

            # On extrait les coordonnées des gravures et on les met dans la liste des str
            for coord in root.findall(".//page:GraphicRegion/page:Coords", ns):
                point = coord.get('points')
                point = point.replace(',', ' ')
                point_regex = re.split("\s", point)
                list_coord_str.append(point_regex)

            # On transforme les str en int
            for i in range(len(list_coord_str)):
                list_coord_int.append([])  # Nested list pour les coordonnées de chaque gravure
                for j in list_coord_str[i]:
                    number = int(j)
                    list_coord_int[i].append(number)

            # On extrait maintenant les images
            for filename_image in list_images:
                image_path = os.path.join(args.image, filename_image)  # Création du chemin vers les imgs
                label_img, ext_img = os.path.splitext(filename_image)  # Séparation du label de l'extension

                # On compare le nom du fichier .xml et de l'image
                if label_img == label:
                    # On crée le dossier 'gravures' s'il n'existe pas
                    path_gravure = '/Users/elinaleblanc/Documents/Postdoctorat/gravures/'

                    if not os.path.isdir(path_gravure):
                        os.mkdir(path_gravure)

                    # On découpe les images en fonction des coordonnées fournies par le fichier .xml
                    for k in range(len(list_coord_int)):
                        image = cv2.imread(image_path)
                        mask = np.zeros(image.shape[0:2], dtype=np.uint8)
                        # Pour éviter les pbs avec l'ordre des coordonnées, on définit une zone à partir de toutes les coordonnées
                        points = np.array([[[list_coord_int[k][0], list_coord_int[k][1]],
                                            [list_coord_int[k][2], list_coord_int[k][3]],
                                            [list_coord_int[k][4], list_coord_int[k][5]],
                                            [list_coord_int[k][6], list_coord_int[k][7]]]])
                        cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)

                        # On récupère la zone définie avec les coordonnées
                        res = cv2.bitwise_and(image, image, mask=mask)
                        # On récupère les coordonnées x et y + width et height de la zone
                        rect = cv2.boundingRect(points)
                        # On découpe l'image à partir de ces nouvelles coordonnées
                        cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]

                        # Création d'un nouveau nom pour l'image
                        new_name = 'grabado_m' + label_img[6:11] + str(k+1) + '.jpg'
                        # Création du chemin de la nouvelle image
                        item_gravure_path = os.path.join(path_gravure, new_name)

                        # On l'enregistre dans le dossier 'gravures' si elle n'existe pas
                        if not os.path.isfile(item_gravure_path):
                            cv2.imwrite(item_gravure_path, cropped)
