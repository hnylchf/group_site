#!/usr/bin/python
# -*- coding:utf-8 -*-
from Util import *
from bs4 import BeautifulSoup
from FileUtil import *
from UrlUtil import *
from client import*

# url = 'http://www.newyx.net/zq/wuxiadanji/'
# host = 'www_newyx_net'
url = ''
host = ''
if __name__ == '__main__':
   url = sys.argv[1]
   host = sys.argv[2]

if not url == '':
    mq = lg_mq_client("127.0.0.1")
    f = FileUtil(host)
    f.initPath()  # 初始化目录结构
    u = Util(url)
    urlinfo = UrlUtil(url)
    soup = u.getSoup()
    info = u.getInfo(soup)
    main_md5 = u.getMd5(urlinfo.host)
    minor_md5 = u.getMd5(urlinfo.path)
    f.saveInfo(main_md5 + "_" + minor_md5,info)

    #过滤顶部菜单
    u.filterColumn(soup)

    a_lsit = u.filterHtmlByA(soup,urlinfo)
    img_list = u.filterHtmlByImg(soup,urlinfo,f)

    for a in a_lsit:
        mq.push(a)

    for img in img_list:
        mq.push(img)

    #删除底部版权信息
    footer = soup.find(id="footer")
    footer.extract()






    f.saveContent(main_md5 + "_" + minor_md5 , u.getUtf8Str(soup))
    print 'success'