import os
import xml.etree.ElementTree as et
from openpyxl import Workbook

wb = Workbook()
wb_filename = "../Index_Grabados_Varios.xlsx"

ws1 = wb.active
ws1.title = "metadata"

list_xml = "../OCR_Training/Varios-OCR-files"
list_woodcuts = []

for subdir, dirs, files in os.walk(list_xml):
    for file in files:
        xml_path = os.path.join(subdir, file)
        # print(xml_path)
        label, ext = os.path.splitext(file)
        # print(label)
        ns = {'alto': 'http://www.loc.gov/standards/alto/ns-v4#'}

        if file.endswith('.xml'):
            document = et.parse(xml_path)
            root = document.getroot()
            # print(root)
            woodcutCounter = 0

            for ImgBlock in root.findall('.//alto:TextBlock[@TAGREFS="BT224"]', ns):
                xStart = int(ImgBlock.get('HPOS')[:-2])
                yStart = int(ImgBlock.get('VPOS')[:-2])
                xEnd = int(ImgBlock.get('WIDTH')[:-2]) + xStart
                yEnd = int(ImgBlock.get('HEIGHT')[:-2]) + yStart
                coords = str(xStart) + "," + str(yStart) + "," + str(xEnd) + "," + str(yEnd)

                '''pliegoTitle = root.find('.//alto:TextBlock[@TAGREFS="BT223"]/alto:TextLine/alto:String/[@CONTENT]', ns)
                if pliegoTitle:
                    print(label, pliegoTitle)'''

                for ImgName in root.findall('.//alto:fileName', ns):
                    pliegoName = ImgName.text[:-6]
                    pageName = ImgName.text[:-4]
                    woodcutCounter = woodcutCounter + 1
                    woodcutName = 'grabado_v' + ImgName.text[6:-5] + str(woodcutCounter)
                    for i in range(len(ImgBlock)):
                        list_woodcuts.append([woodcutName, pliegoName, pageName, coords])


# wb.save(filename=wb_filename)
