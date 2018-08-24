import urllib.request
import urllib.error
import re
import os
import datetime
import time
import sys


targetDir = os.path.dirname(os.path.abspath(__file__))


def destFile(path, nowdate):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    t = os.path.join(targetDir, nowdate+'.jpg')
    return t


def titleTrans(title):
    title = title[1:(len(title) - 9)].replace(':', ' ')
    title = title.replace('\\', ' ')
    title = title.replace('/', ' ')
    title = title.replace('*', ' ')
    title = title.replace('?', ' ')
    title = title.replace('<', ' ')
    title = title.replace('>', ' ')
    title = title.replace('|', ' ')
    title = title.replace('"', ' ')
    return title.strip()


def getWebList(count=1):
    hostname = "https://apod.nasa.gov/apod/archivepix.html"
    req = urllib.request.Request(hostname)
    webpage = urllib.request.urlopen(req)
    htmlText = str(webpage.read())
    webList = []
    for i in range(count):
        match = re.search(r'(ap([0-9]*).html)', htmlText)
        htmlText = htmlText[match.end():]
        webList.append(match.group())
    return webList


def downloadPic(web):
    nowdate = web[2:-5]
    hostname = "https://apod.nasa.gov/apod/" + web
    req = urllib.request.Request(hostname)
    webpage = urllib.request.urlopen(req)
    contentBytes = webpage.read()
    guanwang = r'https://apod.nasa.gov/apod/'
    for link, t in set(re.findall(r'(href="image[^\s]*?(jpg|png|gif))', str(contentBytes))):
        for title, t in set(re.findall(r'(- (.*)title>)', str(contentBytes))):
            title = titleTrans(title)
            print(nowdate + title)
            if os.path.exists(nowdate + ' ' + title + '.jpg'):
                print("we have owned it!")
            else:
                urllib.request.urlretrieve(guanwang + link[6:],
                                           destFile(link, nowdate + title))
                print("we get it")


if __name__ == '__main__':
    run = True
    while run:
        try:
            webList = getWebList(7)
            for web in webList:
                downloadPic(web)
            run = False
        except urllib.error.URLError as e:
            print(time.strftime("%H:%M:%S")+' '+str(e.reason))
            print("check your internet and wait a minute......")
            time.sleep(5)
        except Exception as e:
            with open('error.log', 'a') as f:
                f.write(time.asctime(time.localtime(time.time()))+' '+repr(e)+'\n')
            run = False
