import selenium
import requests
from bs4 import BeautifulSoup
import pprint
import PyPDF2
import urllib2
from tika import parser
from datetime import datetime
import re
import os.path
import json

# GLOBAL VARS

def main():
    urlList = getMainURLs()
    alltext = list()
    for url in urlList:
        alltext = get_data(url, alltext)
        print "Completed:", len(alltext)
    with open('data.txt', 'w') as outfile:
        json.dump(alltext, outfile)


def getMainURLs():
    mainURLS = ['http://www.cityofpaloalto.org/gov/agendas/council/default.asp']
    for year in range(2016, 2001, -1):
        newURL = 'http://www.cityofpaloalto.org/gov/agendas/council/' + str(year) + '.asp'
        mainURLS.append(newURL)
    return mainURLS

def get_data(URL, alltext):
    localalltext = alltext
    html = requests.get(URL)
    soup = BeautifulSoup(html.text, 'lxml')
    table = soup.find("tbody")

    #retrieves the link for all of the transcripts
    for row in table.findAll("tr"):
        columns = row.findAll("td")
        if len(columns) != 0:
            date = columns[0].text.encode('utf-8')
            for col in columns:
                if col.find('a'):
                    tag = col.text.encode('utf-8')
                    if tag in ["Transcript", "Action Minutes", "Minutes"]:
                        pdfurl = getPDFurl(col)
                        pdfpath = downloadPDF(date, tag, pdfurl)
                        # parsedPDF = parser.from_file(pdfpath)
                        # newJSONObj = createJSON(date, tag, pdfurl, pdfpath, parsedPDF)
                        # localalltext.append(newJSONObj)
    return localalltext



def getPDFurl(col):
    rawURL = col.find('a')['href']
    if 'http' in rawURL:
        return rawURL
    else:
        pdfurl = 'http://www.cityofpaloalto.org' + rawURL
        return pdfurl

def downloadPDF(date, tag, pdfurl):
    cleantag = tag.replace(" ", "")
    origdate = datetime.strptime(date.strip(' \t\n\r'), '%B %d, %Y')
    cleandate = origdate.strftime('%Y-%m-%d')
    path = "./" + tag + "/"

    if os.path.isdir(path):
        resp = requests.get(pdfurl)
        filename = path + cleantag + "_" + cleandate + ".pdf"
        with open(filename, 'wb') as f:
            f.write(resp.content)
            f.close()
    else:
        os.mkdir(path)
    return filename

def createJSON(date, tag, pdfurl, pdfpath, parsedPDF):
    note = dict()
    note['date'] = date
    note['tag'] = tag
    note['pdfurl'] = pdfurl
    note['pdfpath'] = pdfpath
    # note['parsedPDF_text'] = parsedPDF["content"]
    return note

main()
