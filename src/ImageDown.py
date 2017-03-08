#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib
from UrlUtil import *
from Util import *
from FileUtil import *
import HTMLParser
import logging
import logging.config


logging.config.fileConfig("../config/logging.conf")
logger = logging.getLogger()
# url = 'http://img.newyx.net/tj/201702/28/798fac1681.jpg'
# host = 'www_newyx_net'


url = ''
host = ''
if __name__ == '__main__':
   url = sys.argv[1]
   host = sys.argv[2]

if not url == '':
    u = UrlUtil(url)
    util = Util(url)
    file = FileUtil(host)
    main_md5 = util.getMd5(u.host)
    fall_md5 = util.getMd5(u.path_suffix)
    dir = file.image
    urllib.urlretrieve(url, file.image + util.converUrl(url))
    logger.info('success=>' + url)
else:
    logger.error('err=>没有图片路径' + url)
