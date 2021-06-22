import time
import re
import json
import csv
from bs4 import BeautifulSoup
from selenium import webdriver

f = open('config.json', 'r')
config = json.load(f)

lat = config["coords"]["lat"]
long = config["coords"]["long"]

tokens = config["tokens"]
BASE_URL = 'https://www.windy.com/'
SPECIAL_CASES_THAT_I_HATE = ["", "snowcover"]

def pageGetter(name, out):
    tempList = [name]
    token = tokens[name]
    browser = webdriver.Chrome(r'chromedriver.exe')
    browser.get(URLMaker(token))
    time.sleep(2)
    html = browser.page_source
    browser.close()
    souper(token, html, tempList, out)

def URLMaker(token):
    URL = BASE_URL + lat + '/' + long + '?' + token + ',' + lat + ',' + long
    return URL

def souper(token,htmlPage, tempList, out):
    soup = BeautifulSoup(htmlPage,'html.parser')
    parsedPage = str(soup.find(class_="picker-content noselect"))
    regex(token, parsedPage, tempList, out)

def regex(token,parsedHtml, tempList, out):
    if token in SPECIAL_CASES_THAT_I_HATE:
        for j in range(len(config["regexs"][token])):
            regexMaker = config["regexs"][token][str(j)]
            expression = re.compile(regexMaker ,flags=re.MULTILINE)
            search = expression.finditer(parsedHtml)
            if search != None:
                for i in search:
                    tempList.append(i.group(0)[:config["slices"][token][str(j)]])
                    break
                if i.group(0)[:config["slices"][token][str(j)]] == str(0):
                    break
        out.writerow(tempList)

    else:
        regexMaker = config["regexs"][token]
        expression = re.compile(regexMaker, flags=re.MULTILINE)
        search = expression.finditer(parsedHtml)
        if search != None:
            for i in search:
                tempList.append(i.group(0)[:config["slices"][token]])
                break
        else:
            tempList.append('ERROR')

        out.writerow(tempList)

def getAll(allTokens, out):
    for i in allTokens:
        pageGetter(i, out)

def main():
    timeStart = time.time()
    with open(config["output"], mode='w', newline='') as outputFile:
        outputFileWrite = csv.writer(outputFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        getAll(tokens, outputFileWrite)
    print("Time Taken: " + str(time.time() - timeStart))

if __name__ == "__main__":
    main()
