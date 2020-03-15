import requests
import json
from selenium import webdriver
import time
from urllib import request,parse
from lxml import etree
import spcial_id as special_ids
import pymysql

class GaoKaoSpider(object):
    driver_path=r"D:\ProgramApp\ChromeDriver\chromedriver.exe"
    def __init__(self):

        self.url = 'https://api.eol.cn/gkcx/api/?access_token=&keyword=&level1=&level2=&page=?&signsafe=&size=20&uri=apidata/api/gk/special/lists'
        self.major_ids = special_ids.special_ids
        self.headers = headers={
                'User-Agent':'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                'Referer':'https://gkcx.eol.cn/special',}
        self.options=webdriver.ChromeOptions()
        self.options.add_argument("--proxy-server=http://60.13.42.239:9999")
        self.driver = webdriver.Chrome(executable_path=GaoKaoSpider.driver_path)
        self.conn = pymysql.connect(host='localhost',user='root',password='root',database='graduation_design',port=3306)
        self.driver.get("https://gkcx.eol.cn/special")
    def run(self):
        for major_id in self.major_ids:
            self.driver.get("https://gkcx.eol.cn/special/{major_id}".format(major_id=major_id))
            # self.driver.get("https://gkcx.eol.cn/special/1")
            source = self.driver.page_source
            self.parse_major_detail(source,major_id)
            time.sleep(2)
        self.conn.close()

    def parse_major_detail(self,source,major_id):
        html = etree.HTML(source)
        major_code = html.xpath(".//div[@class='basicInfo']/p/span[1]/span/text()")
        name = html.xpath(".//div[@class='leftinfo']/p/span[2]/text()")
        print(major_code)
        introduce = html.xpath(".//div[@class='showBig']/div/p[2]/text()")
        print(introduce)
        # employment_rata_2015 = html.xpath(".//div[@id='zhuJob']//ul[1]//span/text()")

        if len(major_code and introduce):
            ben = html.xpath(".//div[@class='leftinfo']/p/span[1]/text()")
            new_ben = ben[0].split('[', 1)[1].split(']', 1)[0]
            print(new_ben)
            major_heat = html.xpath(".//div[@class='basicInfo']/p/span[2]/span/text()")
            print(major_heat)
            if major_heat[0].isnumeric():
                print("有热度")
                degree = html.xpath(".//div[@class='basicInfo']/p/span[3]/span/text()")
                degree = ['无']
                print(degree)
                # 本科
                # school_length = html.xpath(".//div[@class='basicInfo']/p/span[4]/span/text()")
                # categories = html.xpath(".//div[@class='basicInfo']/p/span[5]/span/text()")
                # major_categories = html.xpath(".//div[@class='basicInfo']/p/span[6]/span/text()")
                # 专科
                school_length = html.xpath(".//div[@class='basicInfo']/p/span[3]/span/text()")
                categories = html.xpath(".//div[@class='basicInfo']/p/span[4]/span/text()")
                major_categories = html.xpath(".//div[@class='basicInfo']/p/span[5]/span/text()")
                print(school_length)
                print("第1个时间")

                print(categories)

                print(major_categories)
            else:
                # print("无热度")
                # major_heat =[]
                # print(major_heat)
                # degree = html.xpath(".//div[@class='basicInfo']/p/span[2]/span/text()")
                # print(degree)
                # school_length = html.xpath(".//div[@class='basicInfo']/p/span[3]/span/text()")
                # print(school_length)
                # print("第二个时间")
                # categories = html.xpath(".//div[@class='basicInfo']/p/span[4]/span/text()")
                # print(categories)
                # major_categories = html.xpath(".//div[@class='basicInfo']/p/span[5]/span/text()")
                # print(major_categories)
                degree = ['无']
                time.sleep(1)
                current_url = self.driver.current_url
                self.driver.get(current_url)
                current_source = self.driver.page_source
                self.parse_major_detail(current_source, major_id)
            proportion = html.xpath(".//div[@id='sanSex']/div[2]/text()[2]")
            employment_rata_2015 = html.xpath(".//div[@id='zhuJob']//ul[1]//span/text()")
            employment_rata_2016 = html.xpath(".//div[@id='zhuJob']//ul[2]//span/text()")
            employment_rata_2017 = html.xpath(".//div[@id='zhuJob']//ul[3]//span/text()")
            task = html.xpath(".//div[@class='showBig']/div/p[4]/text()")
            print(task)
            work = html.xpath(".//div[@class='showBig']/div/p[6]/text()")
            print(work)
            print(school_length)
            self.sql_write(major_code, name, new_ben, major_heat, degree, school_length, categories, major_categories,
                           proportion, employment_rata_2015, employment_rata_2016, employment_rata_2017, introduce,
                           task, work,major_id)
        else:
            time.sleep(5)
            current_url = self.driver.current_url
            self.driver.get(current_url)
            current_source = self.driver.page_source
            self.parse_major_detail(current_source,major_id)

    def sql_write(self,major_code,major_name,ben,major_heat,degree,school_length,categories,major_categories,proportion,employment_rata_2015,employment_rata_2016,employment_rata_2017,introduce,task,work,major_id):
        curcor = self.conn.cursor()
        # print(major_code+''+name+''+ben+''+major_heat+''+degree+''+school_length+''+categories+''+major_categories+''+introduce+''+task+''+major_id)

        sql = """insert into special_level4 (level4_id,major_name,ben,major_heat,categories,major_categories,introduce,works,task,major_id,school_length) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        curcor.execute(sql,(major_code,major_name,ben,major_heat,categories,major_categories,introduce,work,task,major_id,school_length))
        print("="*30)
        self.conn.commit()

    # 获取专业id
    def parse_id(self):
        for i in range(67):
            special_list_url = "https://api.eol.cn/gkcx/api/?access_token=&keyword=&level1=&level2=&page={page}&signsafe=&size=20&uri=apidata/api/gk/special/lists".format(page=i)
            special_list_json = request.Request(special_list_url,headers=self.headers)
            json_result = request.urlopen(special_list_json).read().decode('utf-8')
            target = json.loads(json_result)
            # print(person)
            for j in range(20):
                id = target["data"]['item'][j]['special_id']
                self.major_ids.append(id)
            time.sleep(3)
        # self.run()
        with open("major_id.text",'a+',encoding='utf-8') as fp:
                for major_id in self.major_ids:
                    fp.write(str(major_id))
        # print(self.major_ids)





if __name__ == '__main__':
    spider = GaoKaoSpider()
    spider.run()

# '020103T']','['国民经济管理']','本科','['经济学学士']','['经济学'' at line 1")