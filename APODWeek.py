import urllib.request
import urllib.error
import re
import os
import time
import sys

targetDir = os.path.dirname(os.path.abspath(__file__))


def Schedule(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # 设置下载进度条
    f = sys.stdout
    pervent = min(recv_size / totalsize, 1.0)
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    f.write('\r')


def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except Exception:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % (G)
        else:
            return "%.3fM" % (M)
    else:
        return "%.3fK" % (kb)


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
    htmlText = str(urllib.request.urlopen(urllib.request.Request(hostname)).read())
    webList = []
    for i in range(count):
        match = re.search(r'(ap([0-9]*).html)', htmlText)
        htmlText = htmlText[match.end():]
        webList.append(match.group())
    return webList


def downloadPic(web):
    nowdate = web[2:-5]
    hostname = "https://apod.nasa.gov/apod/" + web
    htmlText = str(urllib.request.urlopen(urllib.request.Request(hostname)).read())
    guanwang = r'https://apod.nasa.gov/apod/'
    for link, t in set(re.findall(r'(href="image[^\s]*?(jpg|png|gif))', htmlText)):
        for title, t in set(re.findall(r'(- (.*)title>)', htmlText)):
            title = titleTrans(title)
            print(nowdate + ' ' + title)
            if os.path.exists(nowdate + ' ' + title + '.jpg'):
                print("we have owned it!")
            else:
                urllib.request.urlretrieve(guanwang + link[6:],
                                           destFile(link, nowdate + ' ' + title),
                                           Schedule)
                print('100.00%')


def testInternetConnect(errorInfo):
    try:
        urllib.request.urlopen(urllib.request.Request("http://www.baidu.com"))
        print(errorInfo)
        with open('error.log', 'a') as f:
            f.write(errorInfo)
        return False
    except urllib.error.URLError as urle:
        print(time.strftime("%H:%M:%S") + ' ' + str(urle.reason))
        print("check your internet and wait a minute......")
        time.sleep(10)
        return True


if __name__ == '__main__':
    # TODO: 修复下载完成后下载项可能重复进行的问题
    print(time.strftime("%H:%M:%S") + ' ' + '程序正在启动...')
    webList = []
    webListCount = 7
    runGetWebList = True
    runDownload = False

    while runGetWebList:
        try:
            print(time.strftime("%H:%M:%S") + ' ' + '正在获取图片列表...')
            webList = getWebList(webListCount)
            print(time.strftime("%H:%M:%S") + ' ' + '即将下载图片...')
            runGetWebList = False
            runDownload = True
        except urllib.error.URLError as e:
            runGetWebList = testInternetConnect(time.asctime(time.localtime(time.time()))
                                                + ' ' + '目录域名错误' + '\n')
        except Exception as e:
            with open('error.log', 'a') as f:
                f.write(time.asctime(time.localtime(time.time()))+' '+repr(e)+'\n')
            runGetWebList = False

    while runDownload:
        for web in webList:
            try:
                start_time = time.time()
                downloadPic(web)
            except urllib.error.URLError as e:
                testInternetConnect(time.asctime(time.localtime(time.time())) + " https://apod.nasa.gov/apod/"
                                    + web + '图片域名错误' + '\n')
            except Exception as e:
                with open('error.log', 'a') as f:
                    f.write(time.asctime(time.localtime(time.time())) + ' ' + repr(e) + '\n')
        runDownload = False

