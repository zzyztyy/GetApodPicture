import urllib.request
import re
import os
import datetime


targetDir = os.path.dirname(os.path.abspath(__file__))


def destFile(path, nowdate):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    t = os.path.join(targetDir, nowdate+'.jpg')
    return t


if __name__ == '__main__':
    run = True
    error = True
    i = 1
    while(run):
        nowdate = (datetime.datetime.now()+datetime.timedelta(days=-i)).strftime('%Y%m%d')[2:]
        print(nowdate)
        try:
            hostname = "https://apod.nasa.gov/apod/ap"+nowdate+".html"
            req = urllib.request.Request(hostname)
            webpage = urllib.request.urlopen(req)
            contentBytes = webpage.read()
            # print(contentBytes)
            guanwang = r'https://apod.nasa.gov/apod/'
            notget = True
            # print(targetDir)
            for link, t in set(re.findall(r'(href="image[^\s]*?(jpg|png|gif))', str(contentBytes))):
                # print(link[6:])
                # print(contentBytes)
                for title, t in set(re.findall(r'(- (.*)title>)', str(contentBytes))):
                    # print(type(title))
                    title = title[1:(len(title)-9)].replace(':', ' ')
                    title = title.replace('\\', ' ')
                    title = title.replace('/', ' ')
                    title = title.replace('*', ' ')
                    title = title.replace('?', ' ')
                    title = title.replace('<', ' ')
                    title = title.replace('>', ' ')
                    title = title.replace('|', ' ')
                    title = title.replace('"', ' ')
                    print(nowdate+title)
                    if os.path.exists(nowdate+title + '.jpg'):
                        print("we have owned it!")
                    else:
                        urllib.request.urlretrieve(guanwang+link[6:],
                                                   destFile(link, nowdate+title))
                        print("we get it")
            i = i + 1
            # print(i)
            if i > 8:
                run = False

        except:
            if error:
                print("something wrong")
                print("check your internet and wait a minute......")
                # error = False
    print(1)