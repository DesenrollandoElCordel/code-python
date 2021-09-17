import cv2
import os

folder_name = "Images"

for filename in os.listdir(folder_name):
    if filename.endswith(".jpg"):
        image_path = os.path.join(folder_name, filename)  # Création du chemin vers l'image
        # print(image_path)
        label, ext = os.path.splitext(filename)  # Récupération du nom de l'image
        # print(label[-2])

        path_img_cropped = 'Images_Decoupees/'  # Création du dossier pour sauvegarder les nouvelles images
        if not os.path.isdir(path_img_cropped):
            os.mkdir(path_img_cropped)

        image = cv2.imread(image_path)  # Lecture de l'image
        h, w = image.shape[:2]  # Récupération de la hauteur et de la largeur

        if label[-2] == '-' or label[-3] == '-':  # Pour les pages doubles, on coupe l'image en deux
            page_gauche = image[0:h, 0:int(w / 2)]
            page_droite = image[0:h, int(w / 2):w]

            if len(label) == 16:  # Renommage des fichiers pour les pliegos de plus de 10 pages
                page_gauche_name = label[:11] + label[-5:-3] + ext
                page_droite_name = label[:11] + label[-2:] + ext
                # print(page_gauche_name)
                page_gauche_path = path_img_cropped + page_gauche_name
                page_droite_path = path_img_cropped + page_droite_name
                if not os.path.isfile(page_droite_path or page_gauche_path):
                    cv2.imwrite(page_gauche_path, page_gauche)
                    cv2.imwrite(page_droite_path, page_droite)

            else:  # Renommage des fichiers pour les pliegos de moins de 10 pages
                page_gauche_name = label[:11] + label[-3] + ext
                page_droite_name = label[:11] + label[-1] + ext
                # print(page_droite_name)
                page_gauche_path = path_img_cropped + page_gauche_name
                page_droite_path = path_img_cropped + page_droite_name
                # print(page_gauche_path)
                if not os.path.isfile(page_droite_path or page_gauche_path):
                    cv2.imwrite(page_gauche_path, page_gauche)
                    cv2.imwrite(page_droite_path, page_droite)

        else:  # Pour les pages seules entourées de noir, on enlève 1/4 de l'image
            page = image[0:int((h / 4) * 3), int(w / 4):w]
            page_path = path_img_cropped + filename
            if not os.path.isfile(page_path):
                cv2.imwrite(page_path, page)
