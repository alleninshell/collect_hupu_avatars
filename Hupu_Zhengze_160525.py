import urllib.request as request
import string
import re
import os
import urllib.error as error
import time
import random
import datetime

xiayiye = 1
print("""
+++++++++++++++++++++++
       虎扑头像
       爬虫程序
+++++++++++++++++++++++
     """)


def hupu_tupian(weburl, webheader, begin_page, end_page, imgre1, imgre2):
    global xiayiye
    for i in range(begin_page, end_page + 1):
        time.sleep(random.uniform(1, 2))
        # j = i - begin_page + 1

        start = time.time()
        print('于' + str(datetime.datetime.now()) + '正在抓取第' + str(i) + '个页面')
        xiayiye = 1
        zhuaqu_daxiao(weburl, webheader, '', i, imgre1, imgre2)
        xiayiye = 1
        zhuaqu_daxiao(weburl, webheader, "/following", i, imgre1, imgre2)
        xiayiye = 1
        zhuaqu_daxiao(weburl, webheader, "/follower", i, imgre1, imgre2)
        end = time.time()
        print("耗时" + str(end - start) + "秒")


def zhuaqu_daxiao(weburl, webheader, houzhui, i, imgre1, imgre2):
    global xiayiye

    houzhuibianhao = 0

    if houzhui == "/following":
        weburl_count = weburl + str(i) + houzhui + '?&page=' + str(xiayiye)
        houzhuibianhao = 1

    elif houzhui == "/follower":
        weburl_count = weburl + str(i) + houzhui + '?page=' + str(xiayiye)
        houzhuibianhao = 2
    else:
        weburl_count = weburl + str(i)

    try:
        req = request.Request(url=weburl_count, headers=webheader)
        webpage = request.urlopen(req)
    except:
        print('打开链接错误')
        return

    m = webpage.read()

    imglist = re.findall(imgre1, m.decode('GBK', 'ignore'))

    imglist2 = re.findall(imgre2, m.decode('GBK', 'ignore'))

    imglist += imglist2

    x = 1
    dirpath = 'd:/test1/'
    dirname = str(i)

    if imglist:
        for imgurl in imglist:
            try:
                request.urlretrieve(imgurl.replace("small", "big"),
                                    dirpath + dirname + '_' + str(houzhuibianhao) + '_' + str(xiayiye) + '_' + str(
                                        x) + '.jpg')
                print('抓取' + houzhui + '的第' + str(xiayiye) + '页的第' + str(x) + '张图片')
                x += 1
                # 创建目录保存每个网页上的图片

            except:
                print("获取图片错误")
        print('共抓取' + str(x - 1) + '张图片')
        if webpage.url == "http://my.hupu.com/" or webpage.url == "my.hupu.com" or webpage.url == "https://my.hupu.com/":
            return

        if x > 3 and houzhuibianhao > 0:
            xiayiye += 1
            zhuaqu_daxiao(weburl, webheader, houzhui, i, imgre1, imgre2)

    else:
        xiayiye = 1


if __name__ == "__main__":
    weburl = "http://my.hupu.com/"
    webheader1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    webheader2 = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        # 'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.douban.com',
        'DNT': '1'
    }
    reg = r'src="(.*?small_.\.jpg)" '
    imgre1 = re.compile(reg)

    reg = r'src="(.*?big_.\.jpg)" '
    imgre2 = re.compile(reg)

    begin_page = 14560980
    end_page = 99999999
    before = 201727
    hupu_tupian(weburl, webheader1, begin_page, end_page, imgre1, imgre2)
