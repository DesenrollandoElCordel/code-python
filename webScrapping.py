from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

element_list = []
url_list = ['https://cudl.lib.cam.ac.uk/collections/spanishchapbooks/1']

for url in url_list:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    # title = driver.find_elements(By.NAME, 'h5')
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find_all('h5')
    for t in title:
        element_list.append(t.text)
    document_page = soup.find_all('div', {'class': 'collections_carousel_text'})
    for i in document_page:
        document_page_link = driver.find_element(By.LINK_TEXT, "a")
        # document_page_link = i.find('a')
        # driver.findElement(By.linkText("App Configuration")).click()
        document_page_link.click()
        # print(document_page_link)

# print(element_list)
driver.close()

# TO DO : Récupérer les URL des notices des documents et essayer de scrapper les informations avec BeautifulSoup.
# Important => Manifeste est dans la code source. On peut donc le scrapper sans Selenium !!

