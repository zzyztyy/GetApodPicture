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

def download(date):
    error = True
    date = date.strftime('%Y%m%d')[2:]
    try:
        hostname = "https://apod.nasa.gov/apod/ap" + date + ".html"
        req = urllib.request.Request(hostname)
        webpage = urllib.request.urlopen(req)
        contentBytes = webpage.read()
        guanwang = r'https://apod.nasa.gov/apod/'
        notget = True
        for link, t in set(re.findall(r'(href="image[^\s]*?(jpg|png|gif))', str(contentBytes))):
            for title, t in set(re.findall(r'(- (.*)title>)', str(contentBytes))):
                title = title[1:(len(title) - 9)].replace(':', ' ')
                title = title.replace('\\', ' ')
                title = title.replace('/', ' ')
                title = title.replace('*', ' ')
                title = title.replace('?', ' ')
                title = title.replace('<', ' ')
                title = title.replace('>', ' ')
                title = title.replace('|', ' ')
                title = title.replace('"', ' ')
                print(date + title)
                if os.path.exists(date + title + '.jpg'):
                    print("we have owned it!")
                else:
                    urllib.request.urlretrieve(guanwang + link[6:],
                                               destFile(link, date + title))
                    print("we get it")
                error = True
    except:
        if os.path.exists(date + title + '.jpg'):
            os.remove(date + title + '.jpg')
        if error:
            error = False
            print("something wrong")
            print("check your internet and wait a minute......")


if __name__ == '__main__':
    run = True
    now_date = int((datetime.datetime.now()+datetime.timedelta(-1)).strftime('%Y%m%d')[2:])
    print(u"欢迎使用本程序，本程序仅提供2000年1月1日之后至昨日的apod图片下载，祝您使用愉快！")

    while run:
        print(u"请输入开始日期八位数字，如20170501")
        start_date = input()
        start_date = re.sub("\D", "", start_date)

        print(u"请输入终止日期八位数字，如20170502")
        end_date = input()
        end_date = re.sub("\D", "", end_date)

        if len(start_date) != 8 or len(end_date) != 8:
            print("无法识别日期,请重新输入")
            print(len(start_date))
            print(start_date)

        else:
            start_date = int(start_date[2:])
            end_date = int(end_date[2:])
            try:
                a = datetime.datetime.strptime('20' + str(start_date), '%Y%m%d')
                b = datetime.datetime.strptime('20' + str(end_date), '%Y%m%d')
            except:
                start_date = end_date + 1
            if start_date > end_date or end_date > now_date:
                print(u"日期区间有误，无法下载，请重新输入！")
            else:
                run = False
                start_date = datetime.datetime.strptime('20'+str(start_date), '%Y%m%d')
                end_date = datetime.datetime.strptime('20'+str(end_date), '%Y%m%d')
                temp_date = start_date
                print(u"下载开始")
                print("…………………………………………………………………………")
                while (end_date - temp_date).days >= 0:
                    download(temp_date)
                    temp_date = temp_date + datetime.timedelta(days=1)







