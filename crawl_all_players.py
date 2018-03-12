from urllib2 import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup
import csv
import requests
import time
import os
import re

fileIndex = 1


def getPageContent(url):
    try:
        webpage = urlopen(url).read()

        return webpage
    except HTTPError as e:
        print(e.code)
        return False
    except URLError as ue:
        print(ue.reason)
        return False


def getAllPlayers(url):
    global fileIndex
    webpage = getPageContent(url)

    if webpage == False:
        print "Error on retrieving URL content"
        return False

    # store html content to offline file
    # player_list_html = open("player_list.html", "w")
    # player_list_html.write(webpage)
    # player_list_html.close()

    # get urls using regex
    # print time.time()
    # urls = re.findall('/players/[a-z]{1}/[a-zA-Z0-9]*.html', webpage)
    # print time.time()

    soup = BeautifulSoup(webpage,"html.parser")

    table = soup.find("table",attrs={"id":"stats"}).find("tbody").findAll("tr",attrs={'class': None})
    header = soup.find("table",{"id":"stats"}).find("thead")
    paginationUrls = soup.find("div",attrs={"class":"p402_premium"}).find("p").find_all('a')
    nextPageUrl = ""

    #get next page url
    for pagination in paginationUrls:
        if pagination.get_text() == "Next page":
            nextPageUrl = "https://www.basketball-reference.com" + pagination.get('href')

    #add player profile url to array
    for index, t in enumerate(table):
        for target in t.find("td",attrs={"data-stat": "player"}).find_all('a'):
            table[index]["player_url"] = target.get('href')

    #output to csv file
    out = open('players-' + str(fileIndex) + '.csv','w')

    # do find_all on beautifulsoup object
    for j in header.find_all("th",class_="poptip"):
        out.write(j.get_text()+",")
    out.write("Player URL,")
    out.write("\n")

    for i in table:
        d=i.find("th")
        out.write(d.get_text()+",")
        for j in i.find_all("td"):
            out.write(j.get_text()+",")
        out.write(i.attrs.get("player_url")+",")
        out.write("\n")

    out.close()

    print url
    print 'Done!'

    if nextPageUrl != "":
        time.sleep(1)
        fileIndex += 1
        getAllPlayers(nextPageUrl)

def mergeCsvFiles():
    fout = open("players.csv", "w")

    # first file with header:
    for line in open("players-1.csv"):
        fout.write(line)

    os.remove("players-1.csv")

    # append rest of player files:
    for num in range(2, fileIndex+1):
        f = open("players-" + str(num) + ".csv")
        f.next()  # skip the header
        for line in f:
            fout.write(line)
        f.close()
        os.remove("players-" + str(num) + ".csv")
    fout.close()
    print "File merged"


# start crawling
# http://bkref.com/tiny/d0bF7 -> list of every players from 2007/08 to 2016/17 seasons.
getAllPlayers("http://bkref.com/tiny/d0bF7")
mergeCsvFiles()