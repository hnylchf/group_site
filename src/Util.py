#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import urllib2
import hashlib
from ConfigUtil import *
from bs4 import BeautifulSoup
from UrlUtil import *
import json
import gzip
import StringIO
import logging
import logging.config

logging.config.fileConfig("../config/logging.conf")
logger = logging.getLogger()
class Util():
    url = ''
    def __init__(self,url):
        self.url = url

    def getHtmlByGet(self):
        respone = urllib2.Request(self.url)
        respone.add_header("Accept", 'application/json, text/javascript, */*; q=0.01')
        respone.add_header("Accept-Encoding", "gzip, deflate")
        respone.add_header("Accept-Language", "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3")
        respone.add_header("Connection", "keep-alive")
        respone.add_header("Host", "www.newyx.net")
        respone.add_header("User-Agent","Jwspider")
        html = urllib2.urlopen(respone)
        return html.read()

    def getSoup(self):
        html = self.getHtmlByGet()
        soup = BeautifulSoup(html)
        # 删除script标签
        [s.extract() for s in soup('script')]
        # 删除form标签
        [s.extract() for s in soup('form')]
        # 删除link标签
        [s.extract() for s in soup('link')]
        return soup

    #过滤A标签 替换A标签href
    def filterHtmlByA(self,soup,urlinfo):
        a_list = soup.find_all('a')
        result = []
        for a in a_list:
            try:
                if a.attrs.has_key('href'):
                    a_url = self.getUtf8Str(a['href'])
                    if urlinfo.isCheckUrlHost(a_url):  # 查看是否是一个主域名下的域名
                        a['href'] = self.converUrl(a_url)
                        result.append(a_url)
            except Exception, e:
                logger.error(e)
        return result

    #过滤IMG标签 替换img的src和data属性
    def filterHtmlByImg(self, soup, urlinfo,f):
        img_list = soup.find_all('img')
        result = []
        for img in img_list:
            try:
                if img.attrs.has_key('src') or img.attrs.has_key('data-original'):
                    img_src = ''
                    if img.attrs.has_key('src'):
                        img_src = self.getUtf8Str(img['src'])
                        img['src'] = ".." + f.original_image + self.converUrl(img_src)
                    if img.attrs.has_key('data-original'):
                        img_src = self.getUtf8Str(img['data-original'])
                        img['data-original'] = ".." + f.original_image + self.converUrl(img_src)
                    if urlinfo.isCheckUrlHost(img_src):
                        result.append(img_src)
            except Exception, e:
                logger.error(e)
        return result

    def getUtf8Str(self,str):
        return str.encode('utf-8')

    def getMd5(self,str):
        m2 = hashlib.md5()
        m2.update(str)
        return m2.hexdigest()

    def converUrl(self,url):
        try:
            u = UrlUtil(url)
            if u.suffix == '':
                new_url = self.getMd5(u.host) + '_' + self.getMd5(u.path) + '.html'
            else:
                new_url = self.getMd5(u.host) + '_' + self.getMd5(u.path) + u.suffix
            return new_url
        except Exception, e:
            return ''

    def getFormat(self,str):
        str = str.lower()
        if str.endswith('.jpg') or str.endswith('.gif') or str.endswith('.png'):
            return 'img'
        elif str.endswith('.html') or str.endswith('.htm') or str.endswith('.shtml'):
            return 'htm'
        else:
            return ''

    def getInfo(self,soup):
        #获取网页标题
        title = self.getUtf8Str(soup.head.title.string)
        # 获取description
        meta = soup.meta
        try:
            description = self.getUtf8Str(soup.find(attrs={"name": "description"})['content'])
        except Exception,e:
            description = ''

        try:
            keywords = self.getUtf8Str(soup.find(attrs={"name": "keywords"})['content'])
        except Exception,e:
            keywords = ''
        return {'title':title,'keywords':keywords,'description':description}

    def filterColumn(self,soup):
        # 顶部菜单 去除二级域名菜单
        column_list = soup.find(attrs={'class': 'nav'})
        column_li_list = column_list.find_all('li')
        for li in column_li_list:
            a = li.find_all('a')
            href = a[0]['href']
            if href == 'http://map.newyx.net/':
                li.extract()
            if href == 'http://shouji.newyx.net/':
                li.extract()
            if href == 'http://tv.newyx.net/':
                li.extract()
            if href == 'http://web.newyx.net/':
                li.extract()
            if href == 'http://pic.newyx.net/':
                li.extract()

    def getDownHtml(self,id):
        logger.info('开始获取'+id+"的下载地址")
        try:
            if id == '':
                return ''
            url = "http://www.newyx.net/game/address?id=" + id
            respone = urllib2.Request(url)
            respone.add_header("Accept", 'application/json, text/javascript, */*; q=0.01')
            respone.add_header("Accept-Encoding", "gzip, deflate")
            respone.add_header("Accept-Language", "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3")
            respone.add_header("Connection", "keep-alive")
            respone.add_header("Host", "www.newyx.net")
            respone.add_header("Referer", "http://www.newyx.net/games/" + id + ".htm")
            respone.add_header("User-Agent",
                               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0")
            respone.add_header("X-Requested-With", "XMLHttpRequest")
            html = urllib2.urlopen(respone)
            h = html.read()
            compressedstream = StringIO.StringIO(h)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            data = gzipper.read()  # data就是解压后的数据
            js = json.loads(data)
            json_data = js['data']['html']
            return json_data
        except Exception,e:
            logger.error(e)
