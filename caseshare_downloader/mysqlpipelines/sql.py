import mysql.connector
from ..settings import *
# import pymysql
cnx= mysql.connector.connect(user=MYSQL_USER,password=MYSQL_PASSWORD,host=MYSQL_HOSTS,database=MYSQL_DB)
# cnx= pymysql.connect(user=MYSQL_USER,password=MYSQL_PASSWORD,host=MYSQL_HOSTS,database=MYSQL_DB)
cur=cnx.cursor(buffered=True)

class Sql:
    # @classmethod
    # def insert_caseshare_urls(cls, title, url, court, case_num, date,lawfirm_name, lawyer_name):
    #     sql = 'INSERT INTO caseshare_urls (`title`,`url`,`court`,`case_num`,`date`,`lawfirm_name`,`lawyer_name`) VALUES (%(title)s,%(url)s,%(court)s,%(case_num)s,%(date)s,%(lawfirm_name)s,%(lawyer_name)s)'
    #     value = {
    #         'title': title,
    #         'url': url,
    #         'court': court,
    #         'case_num': case_num,
    #         'date': date,
    #         'lawfirm_name': lawfirm_name,
    #         'lawyer_name': lawyer_name
    #     }
    #     cur.execute(sql, value)
    #     cnx.commit()

    @classmethod
    def insert_caseshare_data(cls,title,url,court,case_num,date,content,judges,lawfirm_name,lawyer_name):
        sql='INSERT INTO caseshare_data_new (`title`,`url`,`court`,`case_num`,`date`,`content`,`judges`,`lawfirm_name`,`lawyer_name`) VALUES (%(title)s,%(url)s,%(court)s,%(case_num)s,%(date)s,%(content)s,%(judges)s,%(lawfirm_name)s,%(lawyer_name)s)'
        value={
            'title':title,
            'url':url,
            'court':court,
            'case_num':case_num,
            'date': date,
            'content': content,
            'judges':judges,
            'lawfirm_name':lawfirm_name,
            'lawyer_name':lawyer_name
        }
        cur.execute(sql,value)
        cnx.commit()

    @classmethod
    def select_url(cls, url):
        sql = "SELECT EXISTS(SELECT 1 FROM caseshare_url_index WHERE url=%(url)s)"
        value = {
            'url': url
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]

    @classmethod
    def create_index(cls, url):
        sql = 'INSERT INTO caseshare_url_index (`url`) VALUES (%(url)s)'
        values = {'url': url}
        cur.execute(sql, values)
        cnx.commit()

    # @classmethod
    # def select_url(cls, url):
    #     sql = "SELECT EXISTS(SELECT 1 FROM caseshare_data_new WHERE url=%(url)s)"
    #     value = {
    #         'url': url
    #     }
    #     cur.execute(sql, value)
    #     return cur.fetchall()[0]

    # @classmethod
    # def select_url(cls,url):
    #     sql="SELECT EXISTS(SELECT 1 FROM caseshare_urls WHERE url=%(url)s)"
    #     value={
    #         'url':url
    #     }
    #     cur.execute(sql,value)
    #     return cur.fetchall()[0]

    # @classmethod
    # def select_lawfirm_name(cls,lawfirm_name):
    #     sql="SELECT EXISTS(SELECT 1 FROM lawfirms_data WHERE lawfirm_name=%(lawfirm_name)s)"
    #     value={
    #         'lawfirm_name':lawfirm_name
    #     }
    #     cur.execute(sql,value)
    #     return cur.fetchall()[0]

    # @classmethod
    # def update_lawfirm_name(cls, url,new_lawfirm_name):
    #     sql = "UPDATE caseshare_data SET lawfirm_name='%(new_lawfirm_name)s' WHERE url='%(url)s' "
    #     value = {
    #         'url':url,
    #         'new_lawfirm_name': new_lawfirm_name
    #     }
    #     cur.execute(sql, value)
    #     cnx.commit()
    #
    # @classmethod
    # def update_lawyer_name(cls, url, new_lawyer_name):
    #     sql = "UPDATE caseshare_data SET lawyer_name='%(new_lawyer_name)s' WHERE url='%(url)s' "
    #     value = {
    #         'url': url,
    #         'new_lawyer_name': new_lawyer_name
    #     }
    #     cur.execute(sql, value)
    #     cnx.commit()
    #
    # @classmethod
    # def select_lawfirm_name_value(cls, url):
    #     sql = "SELECT lawfirm_name FROM caseshare_data WHERE url='%(url)s'"
    #     value = {
    #         'url': url
    #     }
    #     cur.execute(sql, value)
    #     return cur.fetchall()[0]
    #
    # @classmethod
    # def select_lawyer_name_value(cls, url):
    #     sql = "SELECT lawyer_name FROM caseshare_data WHERE url='%(url)s'"
    #     value = {
    #         'url': url
    #     }
    #     cur.execute(sql, value)
    #     return cur.fetchall()[0]

    #爬取律所信息专用
    @classmethod
    def insert_lawfirms_data(cls,lawfirm_name,area_name,area_code,province_name,province_code,city_name,city_code):
        sql = 'INSERT INTO lawfirms_data (`lawfirm_name`,`area_name`,`area_code`,`province_name`,`province_code`,`city_name`,`city_code`) VALUES (%(lawfirm_name)s,%(area_name)s,%(area_code)s,%(province_name)s,%(province_code)s,%(city_name)s,%(city_code)s)'
        value = {
            'lawfirm_name': str(lawfirm_name),
            'area_name': str(area_name),
            'area_code': str(area_code),
            'province_name': str(province_name),
            'province_code': str(province_code),
            'city_name': str(city_name),
            'city_code': str(city_code)
        }
        cur.execute(sql, value)
        cnx.commit()

