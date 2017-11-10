import urllib.request
import re
import os
import datetime

targetDir = os.path.dirname(os.path.abspath(__file__))
nowdate = datetime.datetime.now().strftime('%Y-%m-%d')


def destFile(path):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    t = os.path.join(targetDir, nowdate+'.jpg')
    return t


if __name__ == "__main__":
    run = True
    error = True
    if os.path.exists(nowdate+'.jpg'):
        print("we have owned it!")
    else:
        while(run):
            try:
                hostname = "https://apod.nasa.gov/apod/astropix.html"
                req = urllib.request.Request(hostname)
                webpage = urllib.request.urlopen(req)
                contentBytes = webpage.read()
                # print(contentBytes)
                guanwang = r'https://apod.nasa.gov/apod/'
                notget = True
                print(targetDir)
                for link, t in set(re.findall(r'(href[^\s]*?(jpg|png|gif))', str(contentBytes))):
                    print(link[6:])
                    urllib.request.urlretrieve(guanwang+link[6:], destFile(link))
                    print("we get it")
                run=False
            except:
                if error:
                    print("something wrong")
                    print("check your internet and wait a minute......")
                    error = False
