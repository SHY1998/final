import pymysql
import selenium
from selenium import webdriver
from lxml import etree
import spcial_id as id
import os
import request
from urllib import request
import time
import requests
from bs4 import BeautifulSoup

class introduce(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='root', database='graduation_design',
                                    port=3306)
    def getURl(self):
        for i in range(43443,45943):
        # for i in range(43443, 43445):
            url = "https://www.jzyzy.cn/html/cgx/20180913/{id}.html".format(id=i)
            self.parseUrl(url)

    def parseUrl(self,url):
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = etree.HTML(r.text)
        intro = html.xpath(".//div[@class ='second2 warrper'][1]/div[1]/text()")[0]
        school_name = html.xpath(".//div[@class = 'txtBox']/h1/text()")[0]
        intro = "".join(intro.split())
        school_name = "".join(school_name.split())
        try:
            self.sqlInsert(intro, school_name)
        except:
            self.problemUrl(url)

    def sqlInsert(self,intro,school_name):
        print(school_name)

        cursor = self.conn.cursor()
        sql = """
            UPDATE school_infomation set introduce = '{introduce}' where school_name = '{school_name}'
        """.format(introduce = intro,school_name = school_name)
        cursor.execute(sql)
        self.conn.commit()
    def problemUrl(self,url):
        urls = str(url) + "\n"
        with open("intro_problem.txt", 'a+', encoding='utf-8') as fp:
            fp.write(urls)
if __name__ == '__main__':
    spider = introduce()
    spider.getURl()