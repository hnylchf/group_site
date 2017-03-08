#!/usr/bin/python
# -*- coding:utf-8 -*-
from ConfigUtil import *
import os


class FileUtil():
    base_path = 'host'
    start_path = ''
    content = ''
    image = ''
    info = ''
    video = ''
    path = ''
    #原始文件名
    original_image = ""
    original_content = ""
    original_info = ""
    original_video = ""



    def __init__(self, path):
        self.path = path
        self.start_path = getConfig(self.base_path, 'start_path')
        self.content = self.start_path + self.path + getConfig(self.base_path, 'content')
        self.image = self.start_path + self.path + getConfig(self.base_path, 'image')
        self.info = self.start_path + self.path + getConfig(self.base_path, 'info')
        self.video = self.start_path + self.path + getConfig(self.base_path, 'video')
        self.original_image = getConfig(self.base_path, 'image')
        self.original_content = getConfig(self.base_path, 'content')
        self.original_info = getConfig(self.base_path, 'info')
        self.original_video = getConfig(self.base_path, 'video')


    def initPath(self):
        if not os.path.exists(self.start_path):
            os.mkdir(self.start_path)
        if not os.path.exists(self.content):
            os.mkdir(self.content)
        if not os.path.exists(self.image):
            os.mkdir(self.image)
        if not os.path.exists(self.info):
            os.mkdir(self.info)
        if not os.path.exists(self.video):
            os.mkdir(self.video)

    def write(self, path, str):
        file_object = open(path, 'w')
        file_object.write(str)
        file_object.close()

    def saveInfo(self, file_name, info):
        str = ''
        if info.has_key('title'):
            str = str + "title:" + info['title'] + "\n"
        if info.has_key('keywords'):
            str = str + "keywords:" + info['keywords'] + "\n"
        if info.has_key('description'):
            str = str + "description:" + info['description'] + "\n"
        self.write(self.info + file_name + ".info", str)

    def saveContent(self, file_name, html):
        self.write(self.content + file_name + ".html", html)
