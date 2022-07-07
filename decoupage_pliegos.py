import cv2
import os

folder_name = "Images"

for filename in os.listdir(folder_name):
    if filename.endswith(".jpg"):
        image_path = os.path.join(folder_name, filename)  # Path to the image
        label, ext = os.path.splitext(filename)  # Splitting of the filename

        # New folder to save the cropped images
        path_img_cropped = 'Images_Decoupees/'
        if not os.path.isdir(path_img_cropped):
            os.mkdir(path_img_cropped)

        image = cv2.imread(image_path)
        h, w = image.shape[:2]  # We get the width and height of the image

        if label[-2] == '-' or label[-3] == '-':  # For double-page images, we cut them in half
            page_gauche = image[0:h, 0:int(w / 2)]
            page_droite = image[0:h, int(w / 2):w]

            if len(label) == 16:  # File renaming for documents longer than 10 pages
                page_gauche_name = label[:11] + label[-5:-3] + ext
                page_droite_name = label[:11] + label[-2:] + ext
                page_gauche_path = path_img_cropped + page_gauche_name  # New path for the left page
                page_droite_path = path_img_cropped + page_droite_name  # New path for the right page
                if not os.path.isfile(page_droite_path or page_gauche_path):  # Image saving
                    cv2.imwrite(page_gauche_path, page_gauche)
                    cv2.imwrite(page_droite_path, page_droite)

            else:  # File renaming for documents lesser than 10 pages
                page_gauche_name = label[:11] + label[-3] + ext
                page_droite_name = label[:11] + label[-1] + ext
                page_gauche_path = path_img_cropped + page_gauche_name  # New path for the left page
                page_droite_path = path_img_cropped + page_droite_name  # New path for the right page
                if not os.path.isfile(page_droite_path or page_gauche_path):  # Image saving
                    cv2.imwrite(page_gauche_path, page_gauche)
                    cv2.imwrite(page_droite_path, page_droite)

        else:  # For the images with one page, one quarter of the image is removed
            page = image[0:int((h / 4) * 3), int(w / 4):w]
            page_path = path_img_cropped + filename  # New path for the page
            if not os.path.isfile(page_path):
                cv2.imwrite(page_path, page)
