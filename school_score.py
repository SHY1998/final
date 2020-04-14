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


class score(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='root', database='graduation_design',
                                    port=3306)
    def asd(self):
        url = 'http://college.gaokao.com/school/tinfo/2/result/33/1/'
        for school in range(1, 2001):
        # for school in range(1, 2):
            schoolthis = ''
            # for schooltype in range(1, 2):
            for schooltype in range(1, 3):
                schooltypethis = ''
                for province in range(1, 40):
                # for province in range(1, 2):
                    url = 'http://college.gaokao.com/school/tinfo/{school}/result/{province}/{type}/'.format(
                        province=province, school=school, type=schooltype)
                    text = self.getHTMLText(url)
                    html = etree.HTML(text)
                    try:
                        numb = len(html.xpath('.//tr'))
                        # for i in range(2, 3):
                        for i in range(2, numb + 1):
                            if (len(html.xpath(".//p[@class = 'btnFsxBox']/font[2]/text()")) == 0):
                                print("页面为空")
                                continue
                            else:
                                str = ".//tr[{name}]".format(name=i)
                                current_province = html.xpath(".//p[@class = 'btnFsxBox']/font[2]/text()")[0]
                                schoolthis = html.xpath(".//p[@class = 'btnFsxBox']/font[1]/text()")[0]
                                schooltypethis = html.xpath(".//p[@class = 'btnFsxBox']/font[3]/text()")[0]
                                year = html.xpath(str + '/td[1]//text()')[0]
                                min = html.xpath(str + '/td[2]//text()')[0]
                                max = html.xpath(str + '/td[3]//text()')[0]
                                avg = html.xpath(str + '/td[4]//text()')[0]
                                people_numb = html.xpath(str + '/td[5]//text()')[0]
                                type = html.xpath(str + '/td[6]//text()')[0]
                                self.sqlInsert(schoolthis, year, current_province, min, max, avg, people_numb, type,
                                               schooltypethis)
                            print("*" * 30)
                            print(current_province)
                            print("单一页面完成")
                        time.sleep(1)
                    except:
                        self.problemUrl(url)
                        continue
                print("类型完成")
                print(schooltypethis)
            print(schoolthis)
            print("所有学校完成")
    def getHTMLText(self,url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return ""

    def sqlInsert(self,school_name,year,province,min ,max,avg,people_nub,batch,type):
        cursor = self.conn.cursor()
        sql = """
        insert into Admission_score(school_name,years,province,minscore,maxscore,avgscore,people_numb,batch,study_type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql,(school_name,year,province,min,max,avg,people_nub,batch,type))
        self.conn.commit()
        # cursor.close()
    def problemUrl(self,url):
        urls = str(url)+"\n"
        with open("problem_url.txt",'a+',encoding='utf-8') as fp:
            fp.write(urls)
    def test(self):
        url = "http://college.gaokao.com/school/tinfo/2/result/7/1/"
        text = self.getHTMLText(url)
        html = etree.HTML(text)
        print(len(html.xpath(".//p[@class = 'btnFsxBox']/font[2]/text()")))
        if(len(html.xpath(".//p[@class = 'btnFsxBox']/font[2]/text()"))==0):
            print("页面为空")
        else:
            current_province = html.xpath(".//p[@class = 'btnFsxBox']/font[2]/text()")[0]
            print(current_province)

if __name__ == '__main__':
    spider = score()
    spider.asd()
