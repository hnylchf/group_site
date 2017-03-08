#!/usr/bin/python
# -*- coding:utf-8 -*-
from FileUtil import *
from UrlUtil import *
from client import*
import hashlib
from Util import *
from bs4 import BeautifulSoup
import httplib
import StringIO
import gzip
import json
import re
from Logger import *



# f = FileUtil('www_abc_com')

#
# url = 'http://www.baidu.com'
#
# u = UrlUtil(url)
# print u.isCheckUrlHost('umg.baidu.com/asdfasfasf/asdf/saf/as')


# mq = lg_mq_client("127.0.0.1")


# mq.push("abc")
# mq.push("abc")
# mq.push("abc")
# mq.push("abc")
# mq.push("abc")

# print mq.pop()
# u = Util('WWW.baidu.com')
# print u.getMd5('/top/')

#print hashlib.md5('0f4adf5d14c84fe9724277586ac66757')



# url = "http://www.newyx.net/game/address?id=108031"
# respone = urllib2.Request(url)
# respone.add_header("Accept",'application/json, text/javascript, */*; q=0.01')
# respone.add_header("Accept-Encoding","gzip, deflate")
# respone.add_header("Accept-Language","zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3")
# respone.add_header("Connection","keep-alive")
# respone.add_header("Host","www.newyx.net")
# respone.add_header("Referer","http://www.newyx.net/games/108031.htm")
# respone.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0")
# respone.add_header("X-Requested-With","XMLHttpRequest")
# html = urllib2.urlopen(respone)
# h =  html.read()
# compressedstream = StringIO.StringIO(h)
# gzipper = gzip.GzipFile(fileobj=compressedstream)
# data = gzipper.read() # data就是解压后的数据
#
# json =  json.loads(data)
# print json['data']['html']


# print data

# soup = BeautifulSoup(data)
# print soup.prettify()

# str = "var gameId = 108031;"
#
# s = re.findall(r"gameId =(.+?);",str)#
# s = s[0].strip()
# print s

# url = 'http://www.newyx.net/games/sydnb_list3.htm'
# str = re.findall(r"\b\/\d*.html\b", url)


url = 'http://www.newyx.net/zsgws/'
str = re.findall(r"/[^\s]+\.(jpg|gif|png|bmp)",url)

print len(str)
print str
