import os
import xml.etree.ElementTree as eT
import re

xml_folder = '../Encodage/Moreno-TEI-files/tei-files-v2'

for file in os.listdir(xml_folder):
    if file.endswith(".xml"):
        xml_path = os.path.join(xml_folder, file)  # Path to TEI folder
        label, ext = os.path.splitext(file)  # We split the filename
        # print(xml_path)
        print(label)

        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}  # Namespace declaration
        eT.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        tree = eT.parse(xml_path)  # We parse the XML tree
        root = tree.getroot()  # We get the root <TEI>
        # print(root)
        id_doc = root.get("{http://www.w3.org/XML/1998/namespace}id")  # We get the @xml:id

        # New URI for the pages
        pbList = root.findall(".//tei:pb", ns)
        for pb in pbList:
            oldFacs = pb.get('facs')
            nbPage = pb.get('source')
            newIIIFpath = "moreno/" + nbPage
            # print(newIIIFpath)
            newFacs = re.sub(r"fedora.*", newIIIFpath, oldFacs)
            # print(newFacs)
            pb.set('facs', newFacs)

        # New URI for woodcuts
        decoDesc = root.find('.//tei:decoDesc', ns)
        # print(decoDesc)
        woodcutsList = decoDesc.findall(".//tei:item", ns)
        for woodcut in woodcutsList:
            oldImg = woodcut.get('facs')
            newImgPath = "moreno/" + label + "_1.jpg"
            newImg = re.sub(r"(fedora_ug\d+)", newImgPath, oldImg)
            # print(newImg)
            woodcut.set('facs', newImg)

        # We remove the manifest from the TEI files
        facsimile = root.find(".//tei:facsimile", ns)
        attributs = facsimile.attrib
        attributs.clear()

        # New URI for thumbnails
        graphic = facsimile.find("./tei:graphic", ns)
        oldThumbnail = graphic.get('url')
        newThumbnailPath = "moreno/" + label + "_1.jpg"
        newThumbnail = re.sub(r"(fedora_ug\d+)", newThumbnailPath, oldThumbnail)
        # print(newThumbnail)
        graphic.set('url', newThumbnail)

        tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
