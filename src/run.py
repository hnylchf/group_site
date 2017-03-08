#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import time
from client import *
from UrlUtil import *
import re

python_path = ''
client = lg_mq_client('127.0.0.1')

def main():
    while True:
        fp = os.popen("ps ax | grep python | grep -v grep | wc -l")
        cnt = fp.read()
        print '当前执行量:' + cnt
        if int(cnt) < 10:
            print 'start'
            run()
            #time.sleep(1)
            print 'end'
        else:
            time.sleep(1)
            pass


def run():
    url = client.pop()
    if not url == None:
        urlUtil = UrlUtil(url)
        python_shell = ''
        if url.find('/games/') >= 1:  # game下为下载游戏目录
            is_game_html = re.findall(r"\b\/\d*.htm\b", url)
            #game下载页面
            if len(is_game_html) >= 1:
                python_shell = "nohup python ./GameDown.py " + url + " www_newyx_net & > /dev/null"
            else:
                python_shell = "nohup python ./Content.py " + url + " www_newyx_net & > /dev/null"
        elif len(re.findall(r"/[^\s]+\.(jpg|gif|png|bmp)",url)) >= 1:
            python_shell = "nohup python ./ImageDown.py " + url + " www_newyx_net & > /dev/null"
        else:
            python_shell = "nohup python ./Content.py " + url + " www_newyx_net & > /dev/null"
        print python_shell
        os.popen(python_shell)
    else:
        print 'url is null'
if __name__ == "__main__":
    main()

