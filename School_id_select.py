import pymysql
import selenium
from selenium import webdriver
from lxml import etree
import spcial_id as id
import os
import request
from urllib import request
import time


class School_infomation(object):
    driver_path=r"D:\ProgramApp\ChromeDriver\chromedriver.exe"




    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__),'images')
        self.conn = pymysql.connect(host='localhost', user='root', password='root', database='graduation_design',
                                    port=3306)
        self.base_url = 'https://gkcx.eol.cn/school/{school_id}'
        self.school_ids = id.current_id
        self.headers = headers = {
            'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
            'Referer': 'https://gkcx.eol.cn/special', }
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(executable_path=School_infomation.driver_path)





#统计学校ID，方便生成url
    def select(self):
        cursor = self.conn.cursor()
        sql = """
        select school_id from school_infomation
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            self.school_ids.append(result[0])
        self.conn.close()
        print(self.school_ids)
        self.driver_start()



    # 生成各个学校的url
    def driver_start(self):
        # this_url = self.base_url.format(school_id =55)
        # school_id=55
        # self.driver.get(this_url)
        # page_source = self.driver.page_source
        # self.page_detail(school_id,page_source)
        # page_source = self.driver.page_source
        for school_id in self.school_ids:
            time.sleep(1)
            this_url = self.base_url.format(school_id=school_id)
            try:
                self.driver.get(this_url)
                page_source = self.driver.page_source
                self.page_detail(school_id, page_source)
            except:
                print(school_id)
                print("发生错误")
                #记录未爬取的学校编号
                problem = str(school_id)+"\n"
                with open("problem.txt",'a+',encoding='utf-8') as fp:
                    fp.write(problem)
                continue
            # self.driver.get(this_url)
            # page_source = self.driver.page_source
            # self.page_detail(school_id, page_source)

    # 对学校页面进行分析
    def page_detail(self,school_id,source):
        html = etree.HTML(source)
        school_name = html.xpath(".//span[@class='line1-schoolName']/text()")[0]                    #校名
        home_page = html.xpath(".//div[@class='schoolName clearfix']//span/a/@href")[0]             #主页链接
        school_phone_line = html.xpath(".//div[@class='schoolName clearfix']//div[@class='line3_item'][2]/span/text()")[0]
        school_phone = school_phone_line.split('：',1)[-1]                                           #学校电话
        school_email_line = html.xpath(".//div[@class='schoolName clearfix']//div[@class='line3_item'][3]/span/text()")[0]#
        school_email = school_email_line.split('：',1)[-1]                                           #学校邮箱
        learning_index = html.xpath(".//div[@class='evaluate_box clearfix']/div[1]//span/text()")[0]   #学习指数
        life_index =  html.xpath(".//div[@class='evaluate_box clearfix']/div[2]//span/text()")[0]      #生活指数
        employment_index =  html.xpath(".//div[@class='evaluate_box clearfix']/div[3]//span/text()")[0]#就业指数
        composite_score = html.xpath(".//div[@class='evaluate_box clearfix']/div[4]//span/text()")[0]  #综合评分
        doctoral_degree = html.xpath(".//div[@class='base_info_item_top clearfix']/div[1]/p/text()")#博士点
        the_master = html.xpath(".//div[@class='base_info_item_top clearfix']/div[2]/p/text()")     #硕士点
        key_discipline = html.xpath(".//div[@class='base_info_item_top clearfix']/div[3]/p/text()") #重点学科
        key_laboratory = html.xpath(".//div[@class='base_info_item_top clearfix']/div[3]/p/text()") #重点实验室
        male_rate = html.xpath(".//div[@class='rate_num clearfix']/span[1]/text()")                 #男生比例
        famale_rate = html.xpath(".//div[@class='rate_num clearfix']/span[2]/text()")               #女生比例
        job_rate= html.xpath(".//div[@class='job_circle']/text()")                                  #就业率
        graduation_rate = html.xpath(".//div[@class='job_circle job_circle2']/text()")              #升学率
        go_abroad_rate = html.xpath(".//div[@class='job_circle job_circle3']/text()")               #出国率
        crest = html.xpath(".//div[@class='schoolLogo clearfix']/img/@src")[0]                      #校徽
        print(learning_index)

        self.sql_insert(home_page or 0,school_phone or 0,school_email or 0,learning_index or 0,life_index or 0,employment_index or 0,composite_score or 0,doctoral_degree or 0,the_master or 0,key_discipline or 0,key_laboratory or 0,
                        male_rate or 0,famale_rate or 0,job_rate or 0,graduation_rate or 0,go_abroad_rate or 0,school_id)


        school_pics = html.xpath(".//div[@class='swiper-container swiper-thumbs swiper-container-initialized swiper-container-horizontal swiper-container-thumbs']//img/@src")#校园风光
        self.crest_download(school_name, crest)
        try:
            for school_pic in school_pics:
                print(school_pic)
                self.image_download(school_name, school_pic)
        except:
            print(school_name)
            print("图片未插入")







    def crest_download(self,name,crest):
        png_name = name+'.jpg'
        print(png_name)
        crest_path = os.path.join(self.path,name)
        if not os.path.exists(crest_path):
            os.mkdir(crest_path)
        request.urlretrieve(crest,os.path.join(crest_path,png_name))



    def image_download(self,name,school_pic):
        crest_path = os.path.join(self.path, name)
        if not os.path.exists(crest_path):
            os.mkdir(crest_path)
        image_name = school_pic.split('/')[-1]
        request.urlretrieve(school_pic, os.path.join(crest_path, image_name))




    def sql_insert(self,home_page,school_phone,school_email,learning_index,life_index,employment_index,composite_score,doctoral_degree,the_master,key_discipline,key_laboratory,male_rate,famale_rate,job_rate,graduation_rate,go_abroad_rate,school_id):
        curcor = self.conn.cursor()
        #当有where时，只能用update，不能insert
        sql ="""
        update school_infomation set home_page=%s,school_phone=%s,school_email=%s,learning_index=%s,life_index=%s,employment_index=%s,composite_score=%s,doctoral_degree=%s,the_master=%s,key_discipline=%s,key_laboratory=%s,male_rate=%s,famale_rate=%s,job_rate=%s,graduation_rate=%s,go_abroad_rate=%s where school_id=%s
        """
        curcor.execute(sql,(home_page,school_phone,school_email,learning_index,life_index,employment_index,composite_score,doctoral_degree,the_master,key_discipline,key_laboratory,male_rate,famale_rate,job_rate,graduation_rate,go_abroad_rate,school_id))
        self.conn.commit()



if __name__ == '__main__':
    sql = School_infomation()
    # # sql.select()
    sql.driver_start()
