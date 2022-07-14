from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from openpyxl import Workbook
import json

wb = Workbook()
wb_filename = "../cudl_data.xlsx"

ws = wb.active

url_base = 'https://cudl.lib.cam.ac.uk/collections/spanishchapbooks/'

item_url_list = []
item_data = []
manifests_url = []
test_list = []

for url in range(27, 28):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url_base + str(url))
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    item_page = soup.find_all('div', {'class': 'collections_carousel_text'})
    for i in item_page:
        item_page_link = i.find('a')
        item_url_list.append('https://cudl.lib.cam.ac.uk' + item_page_link.get('href'))
        # print(document_page_link.get('href'))
# print(item_url_list)

for item_url in item_url_list:
    req = requests.get(item_url)
    soup2 = BeautifulSoup(req.text, 'html.parser')
    iiif_button = soup2.find('div', {'id': 'iiifOption'})
    # print(iiif_button)
    iiif_div = iiif_button.find('div', {'class': 'button'})
    iiif_url = iiif_button.find('a', {'class': 'btn'}).get('href')
    manifest = iiif_url.split("?")
    manifests_url.append(manifest[1][9:])
    item_data.append([manifest[1][9:]])

for m in manifests_url:
    jsonFile = json.loads(requests.get(m).text)
    '''date = jsonFile["metadata"][0]["value"]
    printer = jsonFile["metadata"][8]["value"]
    title = jsonFile["metadata"][6]["value"]'''

    place = ""
    title = ""

    for i in jsonFile["metadata"]:
        # print(i.values())

        if "Place of Publication" in i.values():
            places = list(i.values())
            place = places[1].split(";")
            # test_list.append(place[1])
            # print(place[1])
        if "Date of Publication" in i.values():
            date = list(i.values())[1]
            # print(date)
        if "Title" in i.values():
            title = list(i.values())[1]
        if "Publisher" in i.values():
            printer = list(i.values())[1]
    test_list.append([place[1], title])

print(test_list)
driver.close()

# wb.save(filename=wb_filename)

# TO DO : Lire les informations concernant lieu, date et imprimeur depuis le fichier JSON
