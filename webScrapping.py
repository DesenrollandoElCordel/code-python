from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from openpyxl import Workbook

wb = Workbook()
wb_filename = "../cudl_data.xlsx"

ws = wb.active

url_base = 'https://cudl.lib.cam.ac.uk/collections/spanishchapbooks/'
titles_list = []
item_url_list = []
manifests_list = []

for url in range(1, 3):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url_base + str(url))
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all('h5')
    for title in titles:
        titles_list.append(title.text)

    row = 1
    for t in titles_list:
        ws.cell(column=1, row=row, value=t)
        row += 1

    item_page = soup.find_all('div', {'class': 'collections_carousel_text'})
    for i in item_page:
        item_page_link = i.find('a')
        item_url_list.append('https://cudl.lib.cam.ac.uk' + item_page_link.get('href'))
        # print(document_page_link.get('href'))

for item_url in item_url_list:
    req = requests.get(item_url)
    soup2 = BeautifulSoup(req.text, 'html.parser')
    iiif_button = soup2.find('div', {'id': 'iiifOption'})
    # print(iiif_button)
    iiif_div = iiif_button.find('div', {'class': 'button'})
    iiif_url = iiif_button.find('a', {'class': 'btn'}).get('href')
    manifest = iiif_url.split("?")
    manifests_list.append(manifest[1])
    # print(manifest[1])

row2 = 1
for m in manifests_list:
    ws.cell(column=2, row=row2, value=m)
    row2 += 1


# print(element_list)
# print(item_url_list)
driver.close()

wb.save(filename=wb_filename)

# TO DO : Lire les informations concernant lieu, date et imprimeur depuis le fichier JSON
