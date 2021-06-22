#BWG 062221 V1.0
#For PERSONAL USE only, only intented to get weather data for personal uses.
#Will be taken down upon request.

import time
import re
import json
import csv
from bs4 import BeautifulSoup
from selenium import webdriver

#Gets the config file from the same directory and loads it in
f = open('config.json', 'r')
config = json.load(f)

#Getting the editable coordinates from the
lat = config["coords"]["lat"]
long = config["coords"]["long"]

#Loading the tokens which correspond to the URL endpoints used to scrape
tokens = config["tokens"]
BASE_URL = 'https://www.windy.com/'

#List of special cases where I need to grab more than one thing and need to run it through multiple regular expressions
SPECIAL_CASES_THAT_I_HATE = ["", "snowcover"]

#Driver to open the page that calls the URLMaker function to get the URL it needs to run on
#Will sleep for a few seconds after getting the page otherwise it will sometimes not get the content I need
#Then calls the bs4 function to parse.
def pageGetter(name, out):
    #tempList that will hold the name of the data I'm getting and will have the data appended to later.
    tempList = [name]
    token = tokens[name]
    browser = webdriver.Chrome(r'chromedriver.exe')
    browser.get(URLMaker(token))
    time.sleep(2)
    html = browser.page_source
    browser.close()
    souper(token, html, tempList, out)

#Helper function to make the URL based on the token that is passed in.
def URLMaker(token):
    URL = BASE_URL + lat + '/' + long + '?' + token + ',' + lat + ',' + long
    return URL

#Parses the page for a subsection that has the information thats I want
#Then calls the regex function that will regex magic the data out
def souper(token,htmlPage, tempList, out):
    soup = BeautifulSoup(htmlPage,'html.parser')
    parsedPage = str(soup.find(class_="picker-content noselect"))
    regex(token, parsedPage, tempList, out)

#Runs a regular expression on the string of the HTML that the souper function has parsed for me
def regex(token,parsedHtml, tempList, out):
    #If it's in the special cases where I need to run multiple regexs it will go into this
    if token in SPECIAL_CASES_THAT_I_HATE:
        #Run this as for many regexes apply to this case
        for j in range(len(config["regexs"][token])):
            #Makes an regex expression object and then searches the parsedHTML for data.
            regexMaker = config["regexs"][token][str(j)]
            expression = re.compile(regexMaker ,flags=re.MULTILINE)
            search = expression.finditer(parsedHtml)

            #If it finds something
            if search != None:
                #I don't remember why this is a for loop but it breaks if it isn't ¯\_(ツ)_/¯
                for i in search:
                    #Appends what the regex returns minus the units on the end, get's the slice index from the config file and the token passed
                    tempList.append(i.group(0)[:config["slices"][token][str(j)]])
                    break
                #Also don't remember why this is here but also breaks if I take it out ¯\_(ツ)_/¯
                if i.group(0)[:config["slices"][token][str(j)]] == str(0):
                    break
            else:
                tempList.append('ERROR')
        #Writes the list to the csv file as a row
        out.writerow(tempList)

    else:
        #Same as above, but this is for the single regex method
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

#Function that will run a loop of the driving function on all of the tokens in config.
def getAll(allTokens, out):
    for i in allTokens:
        pageGetter(i, out)

#Main that tracks the time and will print to terminal when done, also handles the opening of the file to be written to
def main():
    timeStart = time.time()
    with open(config["output"], mode='w', newline='') as outputFile:
        outputFileWrite = csv.writer(outputFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        getAll(tokens, outputFileWrite)
    print("Time Taken: " + str(time.time() - timeStart))

#Boilerplate python stuff
if __name__ == "__main__":
    main()
