#!/usr/bin/python
# -*- coding:utf-8 -*-
from Util import *
from bs4 import BeautifulSoup
from FileUtil import *
from UrlUtil import *
from client import*
import HTMLParser
import logging
import logging.config


logging.config.fileConfig("../config/logging.conf")
logger = logging.getLogger()
# url = 'http://www.newyx.net/games/124222.htm'
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
    html = u.getHtmlByGet()

    str = re.findall(r"gameId =(.+?);",html)#
    gameId =str[0].strip()
    if not gameId == '':
        ###填充下载地址
        down_html = u.getDownHtml(gameId)
        down_html = u.getUtf8Str(down_html)
        css_index = html.find("download fl")
        start_html = html[0: (css_index + 13)]
        end_html = html[css_index + 13: len(html)]
        html = start_html + down_html + end_html

    soup = BeautifulSoup(html)

    # 删除script标签
    [s.extract() for s in soup('script')]
    # 删除form标签
    [s.extract() for s in soup('form')]
    # 删除link标签
    [s.extract() for s in soup('link')]


    info = u.getInfo(soup)
    main_md5 = u.getMd5(urlinfo.host)
    minor_md5 = u.getMd5(urlinfo.path)
    f.saveInfo(main_md5 + "_" + minor_md5,info)

    #过滤顶部菜单
    u.filterColumn(soup)

    # 删除底部版权信息
    footer = soup.find(id="footer")
    footer.extract()
    #删除帮助内容
    tips_div = soup.find(attrs={'class': 'tips'})
    tips_div.extract()

    a_lsit = u.filterHtmlByA(soup,urlinfo)
    img_list = u.filterHtmlByImg(soup,urlinfo,f)

    for a in a_lsit:
        mq.push(a)

    for img in img_list:
        mq.push(img)

    f.saveContent(main_md5 + "_" + minor_md5 , u.getUtf8Str(soup))
    logger.info('success=>'+url)