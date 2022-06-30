import os
import xml.etree.ElementTree as et

list_xml = "../OCR_Training/Varios-OCR-files"

for subdir, dirs, files in os.walk(list_xml):
    for file in files:
        xml_path = os.path.join(subdir, file)
        # print(xml_path)
        label, ext = os.path.splitext(file)
        # print(label)
        list_coord_str = []
        ns = {'alto': 'http://www.loc.gov/standards/alto/ns-v4#'}

        if file.endswith('.xml'):
            document = et.parse(xml_path)
            root = document.getroot()
            # print(root)

            for ImgBlock in root.findall('.//alto:TextBlock[@TAGREFS="BT224"]', ns):
                xStart = int(ImgBlock.get('HPOS')[:-2])
                yStart = int(ImgBlock.get('VPOS')[:-2])
                xEnd = int(ImgBlock.get('WIDTH')[:-2]) + xStart
                yEnd = int(ImgBlock.get('HEIGHT')[:-2]) + yStart
                coords = str(xStart) + "," + str(yStart) + "," + str(xEnd) + "," + str(yEnd)
                # print(coords)

                # TO DO : Find titles, id pliego, image number // Put the data in Excel file
