import requests
import time
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver

f = open('config.json', 'r')
config = json.load(f)

BaseURL2 = 'https://www.windy.com/-34.330/175.184?radar,-34.394,175.184'
BASE_URL = 'https://www.windy.com/'
page = requests.get(BASE_URL)

def pageGetter(token):


    browser = webdriver.Chrome(r'chromedriver.exe')
    browser.get(BASE_URL)
    time.sleep(5)
    html = browser.page_source

    browser.close()
soup = BeautifulSoup(html,'html.parser')

parsedHtml = str(soup.find(class_="picker-content noselect"))

search = re.findall(r"\d+(?:dBZ)",parsedHtml,flags=re.M)
if search != None:
    for i in search:
        print(i[:-3])