import os
import xml.etree.ElementTree as ET

# Folder with HTR predictions in PAGE or Alto XML
list_folder = ""

# Iteration through the folders
for subdir, dirs, files in os.walk(list_folder):
    list_file = []  # List with XML files

    for file in files:
        if not file.endswith('.DS_Store') | file.endswith('mets.xml') | file.startswith('Masterfile'):
            '''print(os.path.join(subdir, file))'''
            label, ext = os.path.splitext(file)  # We get the label and the extension of the file
            list_file.append(file)  # We add the XML file to the list
            list_file.sort()  # We sort them alphabetically
            # print(list_file)

            # Creation of a new XML file with XInclude
            root = ET.Element("master", attrib={"xmlns:xi": "http://www.w3.org/2001/XInclude"})
            
            for x in list_file:  # Iteration through the list of files
                ET.SubElement(root, "xi:include", {"href": x})

            tree = ET.ElementTree(root)  # Creation of the XML tree
            masterfile_name = 'Masterfile_' + label[:10] + '.xml'  # Name of the new XML file
            masterfile_path = os.path.join(subdir, masterfile_name)  # Path to save the file
            tree.write(masterfile_path, encoding="UTF-8", xml_declaration=True, method="xml")
