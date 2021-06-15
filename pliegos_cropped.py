from PIL import Image
import os

list_image = os.listdir('images')

for f in list_image:
    if f.endswith('.jpg'):
        fn, ftext = os.path.splitext(f)
        image_path = os.path.join('images/', f)
        im = Image.open(image_path)

        im.crop((0, 0, 1765, 2512)).save('single/{}_G{}'.format(fn, ftext))
        im.crop((1729, 3, 3466, 2511)).save('single/{}_D{}'.format(fn, ftext))
