import argparse
import os
import xml.etree.ElementTree as et
from openpyxl import Workbook

# Creation of the argument
parser = argparse.ArgumentParser()
parser.add_argument('--alto', type=str, help="Le chemin du dossier des fichiers xml à charger.")
args = parser.parse_args()

# Creation of the file
wb = Workbook()
wb_filename = "../Index_Grabados_Varios.xlsx"

# Creation of the worksheet
ws1 = wb.active
ws1.title = "metadata"

# Lists for XML data
list_woodcuts = []
list_title = []

# Iteration through the folders and files
for subdir, dirs, files in os.walk(args.alto):
    for file in files:
        xml_path = os.path.join(subdir, file)  # Path of the XML files
        # print(xml_path)
        label, ext = os.path.splitext(file)  # Splitting of the filename
        # print(label)
        ns = {'alto': 'http://www.loc.gov/standards/alto/ns-v4#'}  # Alto-XML namespace

        if file.endswith('.xml'):
            document = et.parse(xml_path)
            root = document.getroot()
            # print(root)
            woodcutCounter = 0  # Initialisation of the woodcuts number after each iteration

            # Detection of image block (#BT224) in Alto-XML, following the SegmOnto identifier
            for ImgBlock in root.findall('.//alto:TextBlock[@TAGREFS="BT224"]', ns):
                xStart = int(ImgBlock.get('HPOS')[:-2])  # Upper Left X (ulx)
                yStart = int(ImgBlock.get('VPOS')[:-2])  # Upper Left Y (uly)
                xEnd = int(ImgBlock.get('WIDTH')[:-2]) + xStart  # Lower right X (lrx) = Width + ulx
                yEnd = int(ImgBlock.get('HEIGHT')[:-2]) + yStart  # Lower right Y (lry) = Height + uly
                coords = str(xStart) + "," + str(yStart) + "," + str(xEnd) + "," + str(yEnd)  # List of coordinates

                # For each XML file with an image, we get filename information
                for ImgName in root.findall('.//alto:fileName', ns):
                    pliegoName = ImgName.text[:-6]  # Id of the pliego
                    pageName = ImgName.text[:-4]  # Number of the page
                    woodcutCounter = woodcutCounter + 1  # We count the number of images per file
                    woodcutName = 'grabado_v' + ImgName.text[6:-5] + str(woodcutCounter)  # Id of the woodcut

                    # Detection of the title block (#BT223) in Alto-XML, following the SegmOnto identifier
                    pliegoTitle = root.find('.//alto:TextBlock[@TAGREFS="BT223"]/alto:TextLine[1]//alto:String', ns)
                    if label.endswith('_1') and pliegoTitle is not None:
                        list_title = pliegoTitle.get('CONTENT')  # We temporaly put the title in a list during the iteration
                    else:
                        list_title = 'None'

                    # All the information are put in a nested list
                    for i in range(len(ImgBlock)):
                        list_woodcuts.append([woodcutName, pliegoName, pageName, coords, list_title.lower()])

                    # From the information in list_woodcuts, we create the Excel file
                    row = 1  # Initialisation of the row
                    for x in list_woodcuts:
                        ws1.cell(column=1, row=row, value=x[0])
                        ws1.cell(column=2, row=row, value=x[1])
                        ws1.cell(column=3, row=row, value=x[2])
                        ws1.cell(column=4, row=row, value=x[3])
                        ws1.cell(column=5, row=row, value=x[4])
                        row += 1  # Incrementation of the row

print(list_woodcuts)
# wb.save(filename=wb_filename)
