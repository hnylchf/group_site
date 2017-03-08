#!/usr/bin/python
# -*- coding:utf-8 -*-
from Util import *
from bs4 import BeautifulSoup
from FileUtil import *
from UrlUtil import *
from client import*
import logging
import logging.config

url = 'http://www.newyx.net'
host = 'www_newyx_net'
# if __name__ == '__main__':
#    url = sys.argv[1]
#    host = sys.argv[2]
logging.config.fileConfig("../config/logging.conf")
logger = logging.getLogger()

if not url == '':
    mq = lg_mq_client("127.0.0.1")
    f = FileUtil(host)
    f.initPath()  # 初始化目录结构
    u = Util(url)
    urlinfo = UrlUtil(url)
    soup = u.getSoup()
    info = u.getInfo(soup)
    main_md5 = u.getMd5(urlinfo.host)
    f.saveInfo(main_md5 + "_" + main_md5  , info)

    u.filterColumn(soup)

    a_lsit = u.filterHtmlByA(soup, urlinfo)
    img_list = u.filterHtmlByImg(soup, urlinfo,f)

    for a in a_lsit:
        mq.push(a)

    for img in img_list:
        mq.push(img)

    # 删除底部版权信息
    footer = soup.find(id="footer")
    footer.extract()



    f.saveContent(main_md5 + '_' + main_md5, u.getUtf8Str(soup))
    print 'ok'
else:
    logger.error("url为空")