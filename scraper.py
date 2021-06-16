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

BASE_URL = 'https://www.windy.com/'
SPECIAL_CASES_THAT_I_HATE = ["wind", "snowcover"]
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
    if token in SPECIAL_CASES_THAT_I_HATE:
        for j in range(len(config["regexs"][token])):
            regexMaker = config["regexs"][token][str(j)]
            expression = re.compile(regexMaker ,flags=re.MULTILINE)
            search = expression.finditer(parsedHtml)

            if search != None:
                for i in search:
                    print(i.group(0)[:config["slices"][token][str(j)]])
                    break
                if i.group(0)[:config["slices"][token][str(j)]] == str(0):
                    break

    else:
        regexMaker = config["regexs"][token]
        expression = re.compile(regexMaker, flags=re.MULTILINE)
        search = expression.finditer(parsedHtml)
        if search != None:
            for i in search:
                print(i.group(0)[:config["slices"][token]])
                break

listy = ["radar","satellite","wind","gust","gustAccu","rain","rainAccu","snowAccu","snowcover"]

pageGetter("snowcover")