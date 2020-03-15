import requests
from lxml import etree
import pymysql
import time
from selenium import webdriver
HEADERS = {

    'User-Agent':'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Referer':'http://kaoshi.edu.sina.com.cn/college/scorelist?tab=file&wl=&local=1&syear=2019&page=2',
}
BASE_URL = 'http://kaoshi.edu.sina.com.cn/college/scorelist?tab=file&wl=&local={local}&syear=&page={page}'

class grade(object):
    driver_path=r"D:\ProgramApp\ChromeDriver\chromedriver.exe"
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='root', database='graduation_design',
                                    port=3306)
        # self.options=webdriver.ChromeOptions()
        # self.driver = webdriver.Chrome(executable_path=grade.driver_path)

    def provence_spider(self):
        for provence in range(1,32):
            for page in range(1,400):
                total_url = BASE_URL.format(local=provence, page=page)
                time.sleep(1)
                try:
                    response = requests.get(url=total_url, headers=HEADERS)
                    response.encoding = response.apparent_encoding
                    html = etree.HTML(response.text)
                    for line in range(1, 21):
                        position = line + 1
                        year_xpath = ".//div[@class='tabsContainer']/table/tr[{position}]/td[position()<7][1]/text()".format(
                            position=position)
                        provience_xpath = ".//div[@class='tabsContainer']/table/tr[{position}]/td[position()<7][2]/text()".format(
                            position=position)
                        exam_type_xpath = ".//div[@class='tabsContainer']/table/tr[{position}]/td[position()<7][3]/text()".format(
                            position=position)
                        grade_xpath = ".//div[@class='tabsContainer']/table/tr[{position}]/td[position()<7][4]/text()".format(
                            position=position)
                        current_number_xpath = ".//div[@class='tabsContainer']/table/tr[{position}]/td[position()<7][5]/text()".format(
                            position=position)
                        total_number_xpath = ".//div[@class='tabsContainer']/table/tr[{position}]/td[position()<7][6]/text()".format(
                            position=position)
                        year = html.xpath(year_xpath)
                        provience = html.xpath(provience_xpath)
                        exam_type = html.xpath(exam_type_xpath)
                        grade = html.xpath(grade_xpath)
                        current_number = html.xpath(current_number_xpath)
                        total_number = html.xpath(total_number_xpath)
                        self.infomation_sql(year, provience, exam_type, grade, current_number, total_number)
                except:
                    print('错误')
                    print(total_url)
                    print(provence)
                    print(page)
                    break

                print(provence, end='')
                print("城市",end='')
                print(page,end='')
                print("页完成",end='')
                print('')
            print('')
            print("完成城市",end='')
            print(provence,end='')
        self.conn.close()

    def infomation_sql(self,year, provience, exam_type, grade, current_number, total_number):
        cursor = self.conn.cursor()
        sql = """
        insert into one_minute_one_gear_table(分数段,考生所在地,考生类别,本段人数,累计人数,年份) values (%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql,(grade,provience,exam_type,current_number,total_number,year))
        self.conn.commit()
        cursor.close()


    def text(self):
        for i in range(3):

            print(i)
if __name__ == '__main__':
    spider = grade()
    spider.provence_spider()
    # spider.text()