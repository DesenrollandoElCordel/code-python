# Python scripts

This folder contains the different Python scripts we have used during the project.

## Chapbooks processings
- [decoupage_pliegos](decoupage_pliegos.py): Script to crop and rename the images of the *Pliegos Varios* corpus.
- [creation_masterfiles](creation_masterfiles.py): Concatenation of several XML files in single XML file, called masterfile, with XInclude.
- [iiif_tei_additions](iiif_tei_additions.py): Inserting IIIF URI — stored in a CSV file – into XML-TEI files.

## Woodcuts processings
- [extractionWoodcutsAltoXml](extractionWoodcutsAltoXml.py): Extraction of data about woodcuts from Alto-XML files (coordinates, document identifier, page number) and creation of an Excel worksheet.
- [extractionWoodcutsPageXML](extractionWoodcutsPageXml.py): Extraction of data about woodcuts from PAGE-XML files (coordinates, document identifier, page number) and creation of an Excel worksheet.
- [Excel_To_TEI](Excel_To_TEI.py): Creation of XML-TEI files from an Excel worksheet (Used for the woodcuts catalogue).  
- [TEI_To_Excel](TEI_To_Excel.py): Extraction of data from XML-TEI files (title, date, printer) and addition of these data in a pre-existing Excel worksheet (Used for the woodcuts catalogue).
- [iiif_tei_illustration](iiif_tei_illustrations.py): Inserting IIIF URI - stored in a CSV file – into XML-TEI file + Modification of URI to target specific portions of an image, based on the coordinates given by XML files.
- [webScrapping](webScrapping.py): This code automatically extracts information from the metadata of a digital library (in our case, title of documents and IIIF links).

## NER processings
- [NerToWkd](NerTowkd.py): This code can be used to launch several SPARQL queries on the Wikidata endpoint from a list of names.
- [csv2json](csv2json.py): This code generates a JSON file in [Linked Places](https://github.com/LinkedPasts/linked-places-format) format from a CSV file. The resulting JSON file is used to display places on a map created with the Peripleo application.
- [ner2csv](ner2csv.py): This code transforms an IOB (Inside-Outside-Beginning) format file into a CSV file. It recovers only the named entities and reconstructs the entities in several parts (e.g. "Santa B-LOC Ana I-LOC" becomes "Santa Ana" in the CSV).
- [ner2tei](ner2tei.py): This code enriches a CSV file with new information extracted from TEI XML files ([example](../pliegos-ner/moreno-ner/nerList_Moreno_enriched.csv)). It also inserts geographic information contained in the CSV into these TEI files: in the body of the text with `<name>` elements and in the `<teiHeader>` with a `<listPlace>` element ([example](../Moreno-TEI-files/tei-files-v2/Moreno_001.xml)).
- [ner2tei_index](ner2tei_index.py): This code creates a TEI index of place names from a CSV file.
- [ner_count](ner_count.py): This code counts the number of occurrences of a word in a list and outputs the results in a spreadsheet.
