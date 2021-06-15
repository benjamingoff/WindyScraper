import requests
import time
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver

f = open('config.json', 'r')
config = json.load(f)

lat = config["coords"]["lat"]
long = config["coords"]["long"]

BaseURL2 = 'https://www.windy.com/-34.330/175.184?radar,-34.394,175.184'
BASE_URL = 'https://www.windy.com/'
page = requests.get(BASE_URL)

def pageGetter(token):
    browser = webdriver.Chrome(r'chromedriver.exe')
    browser.get(URLMaker(token))
    time.sleep(5)
    html = browser.page_source
    browser.close()
    souper(token,html)

def URLMaker(token):
    URL = BASE_URL + lat + '/' + long + '?' + token + ',' + lat + ',' + long
    return URL

def souper(token,htmlPage):
    soup = BeautifulSoup(htmlPage,'html.parser')
    parsedPage = str(soup.find(class_="picker-content noselect"))
    print(parsedPage)
    regex(token, parsedPage)

def regex(token,parsedHtml):
    regexMaker = '\\' + config["regexs"][token]
    expression = re.compile(regexMaker ,flags=re.M)
    search = expression.findall(parsedHtml)

    if search != None:
        for i in search:
           print(i[:-3])

pageGetter("radar")