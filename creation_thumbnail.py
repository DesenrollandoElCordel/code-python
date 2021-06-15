import cv2
import os

path = 'images'

for filename in os.listdir(path):
    if not filename.endswith('Store'):
        img_path = os.path.join(path, filename)
        label, ext = os.path.splitext(filename)

        if label.endswith('1'):
            image = cv2.imread(img_path)

            r = 150 / image.shape[0]
            dim = (int(image.shape[1] * r), 150)

            thumbnail = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

            path_thumbnail = 'thumbnails/'
            if not os.path.isdir(path_thumbnail):
                os.mkdir(path_thumbnail)

            new_name = label[:-2] + '_thumbnail' + ext
            # print(new_name)
            img_thumbnail_path = os.path.join(path_thumbnail, new_name)
            # print(img_thumbnail_path)

            if not os.path.isfile(img_thumbnail_path):
                cv2.imwrite(img_thumbnail_path, thumbnail)
