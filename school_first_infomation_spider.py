import requests
import json
from selenium import webdriver
import time
from urllib import request,parse
from lxml import etree
import pymysql

class School_infomation_spider(object):
    driver_path=r"D:\ProgramApp\ChromeDriver\chromedriver.exe"
    def __init__(self):
        self.headers = headers = {
            'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
            'Referer': 'https://gkcx.eol.cn/special', }
        self.driver = webdriver.Chrome(executable_path=School_infomation_spider.driver_path)
        self.conn = pymysql.connect(host='localhost', user='root', password='root', database='graduation_design',
                                    port=3306)
    def school_first(self):
        for i in range(1,145):
            major_list_url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_dual_class=&keyword=&page={page}&province_id=&request_type=2&school_type=&signsafe=&size=20&sort=view_total&type=&uri=apigkcx/api/school/hotlists'.format(page=i)
            print(major_list_url)
            major_list_json = request.Request(major_list_url, headers=self.headers)
            json_result = request.urlopen(major_list_json).read().decode('utf-8')
            target = json.loads(json_result)
            for j in range(20):
                id = target["data"]["item"][j]["school_id"]  #
                name = target["data"]["item"][j]["name"]  #
                heat_rank = target["data"]["item"][j]["rank"]  #
                heat_total = target["data"]["item"][j]["view_total_number"]  #
                heat_rank_type = target["data"]["item"][j]["rank_type"]  #
                level_name = target["data"]["item"][j]["level_name"]  # 本科/专科
                type_name = target["data"]["item"][j]["type_name"]  # 学校是什么类型 如：理工类、综合类
                belong = target["data"]["item"][j]["belong"]  # 是否属于教育部
                is_211 = target["data"]["item"][j]["f211"]  #
                school_type = target["data"]["item"][j]["type"]  #
                city_name = target["data"]["item"][j]["city_name"]  #
                county_name = target["data"]["item"][j]["county_name"]  # 区域名称 如新华区
                dual_class = target["data"]["item"][j]["dual_class"]  # 双重类别名称 38001:一流大学建设高校;38000:一流学科建设高校;2800
                province_name = target["data"]["item"][j]["province_name"]
                nature_name = target["data"]["item"][j]["nature_name"]  # 是否公办
                province_id = target["data"]["item"][j]["province_id"]  #
                city_id = target["data"]["item"][j]["city_id"]  #
                is_985 = target["data"]["item"][j]["f985"]  # 1:985 2:非985
                is_top = target["data"]["item"][j]["is_top"]  #
                self.insert_infomation(id, name, heat_rank, heat_total, heat_rank_type, level_name, type_name, belong,
                                       is_211, school_type, city_name,
                                       county_name, dual_class, province_name, nature_name, province_id, city_id,
                                       is_985, is_top)
        self.conn.close()

    def insert_infomation(self,id,name,heat_rank,heat_total,heat_rank_type,level_name,type_name,belong,is_211,school_type,city_name,
                                   county_name,dual_class,province_name,nature_name,province_id,city_id,is_985,is_top):
        cursor =self.conn.cursor()

        sql_1 ="""
            insert into school_infomation(school_id,school_name,heat_rank,heat_total,heat_rank_type,level_name,type_name,belong,is_211,school_type,county_name,dual_class,nature_name,province_id,city_id,is_985,is_top)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql_1,(id,name,heat_rank,heat_total,heat_rank_type,level_name,type_name,belong,is_211,school_type,county_name,dual_class,nature_name,province_id,city_id,is_985,is_top))
        self.conn.commit()

        sql_3 ="""
            insert into city_infomation(city_id,city_name) values (%s,%s) on duplicate KEY UPDATE city_id=city_id
        """
        cursor.execute(sql_3,(city_id,city_name))
        self.conn.commit()
        sql_2 = """
                    insert into province_infomation(province_id,province_name) values (%s,%s) on duplicate KEY UPDATE province_id=province_id
                """
        cursor.execute(sql_2, (province_id, province_name))
        self.conn.commit()
        cursor.close()














if __name__ == '__main__':
    spider = School_infomation_spider()
    spider.school_first()
