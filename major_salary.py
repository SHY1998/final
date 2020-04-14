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

class major_salary(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='root', database='graduation_design',
                                    port=3306)
    def ben(self):
        bens = ['本科','专科']
        for i in range(0,2):
            self.getUrl(bens[i])

    def getUrl(self,ben):
        if(ben=="本科"):
            for i in range(1,61):
                url = "https://www.jzyzy.cn/major_rank_list.jspx?onemajorname=&level={ben}&pageNo={page}".format(ben = ben,page = i)
                self.parseUrl(url)
        elif(ben == "专科"):
            for i in range(1,89):
                url = "https://www.jzyzy.cn/major_rank_list.jspx?onemajorname=&level={ben}&pageNo={page}".format(
                    ben=ben, page=i)
                self.parseUrl(url)

    def parseUrl(self,url):
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html  = etree.HTML(r.text)
            for i in range(1,11):
                major_name = html.xpath(".//tbody/tr[{line}]/td[2]//text()".format(line = i))[0]
                salary = html.xpath(".//tbody/tr[{line}]/td[4]/text()".format(line = i))[0]
                try:
                    self.sqlInsert(major_name,salary)
                except:
                    self.salaryProblem(url)

    def sqlInsert(self,major_name,salary):
        print(major_name)
        cursor = self.conn.cursor()
        sql = """
            UPDATE special_level4 set salary = '{salary}' where major_name = '{major_name}'
        """.format(salary = salary,major_name = major_name)
        cursor.execute(sql)
        self.conn.commit()
    def salaryProblem(self,url):
        urls = str(url) + "\n"
        with open("salary_problem.txt", 'a+', encoding='utf-8') as fp:
            fp.write(urls)
if __name__ == '__main__':
    spider = major_salary()
    spider.ben()