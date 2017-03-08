#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import logging.config

# 采用配置文件
logging.config.fileConfig("../config/logging.conf")
logger = logging.getLogger()



i = "xxx"
try:
    i = i +1
except Exception,e:
    logging.error(e)