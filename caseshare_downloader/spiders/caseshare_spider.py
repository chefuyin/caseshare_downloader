import math
import scrapy
from scrapy_redis.spiders import RedisSpider#使用Redis来调度
import pymysql
from scrapy.http import Request
from ..items import CaseshareDownloaderItem   #..为相对引用
import lxml.html
# from lxml.html import etree

# class MySpider(scrapy.Spider):
class MySpider(RedisSpider):#使用Redisspider替换scrapyspider
    name = 'caseshare_spider'
    allowed_domains=['caseshare.cn']
    base_url='http://caseshare.cn'
    redis_key='CaseShareRedis:start_urls'
    index_url='http://caseshare.cn/search/cause'
    number_url='http://caseshare.cn/api/chart/GetRecordCountByCauseCategory'
    # request_url='http://caseshare.cn/Search/RecordSearch?FilterType=Cause&IsAdv=False'
    firm_lawyer_url='http://caseshare.cn/Search/RecordSearch?FilterType=LawFirmOrLawyer&IsAdv=False'
    lawfirm_url='http://caseshare.cn/Search/ClassSearch?FilterType=LawFirmOrLawyer&IsAdv=False'
    conn=pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='lawdata',
            charset='utf8')
# #start test user-agent
#     start_urls = ['http://exercise.kingname.info/exercise_middleware_ua/6',
#                   'http://exercise.kingname.info/exercise_middleware_ua/4',
#                   'http://exercise.kingname.info/exercise_middleware_ua/1',
#                   'http://exercise.kingname.info/exercise_middleware_ua/2',
#                   'http://exercise.kingname.info/exercise_middleware_ua/3',
#                   'http://exercise.kingname.info/exercise_middleware_ua/5',
#                   'http://exercise.kingname.info/exercise_middleware_ua/7',
#                   'http://exercise.kingname.info/exercise_middleware_ua/8',
#                   ]
#     def start_requests(self):
#         for i in self.start_urls:
#             yield Request(i,callback=self.parse)
#
#     def parse(self, response):
#         print(response.body.decode())
# #end test user-agent

    def start_requests(self):
        result=self.get_lawfirm_info()
        url=self.lawfirm_url
        for info in result:
            lawfirm_name=info[0]
            city_code=info[1]
            data=self.make_data(lawfirm_name,city_code)
            yield scrapy.FormRequest(url,formdata=data,meta={'lawfirm_name':lawfirm_name,'city_code':city_code},callback=self.parse)

    def parse(self, response):
        selector=lxml.html.fromstring(response.text)
        lawfirm_name=response.meta['lawfirm_name']
        city_code=response.meta['city_code']
        lawyers=selector.xpath('//div[@cluster_index="1"]/div/ul/li/a/text()')
        if lawyers !=None:
            for lawyer in lawyers:
                # print(lawyers)
                lawyer_name=lawyer.split('(')[0]
                case_num=int(lawyer.split('(')[1].replace(')',''))
                if case_num<=10:
                   total_page=1
                elif case_num >1000:
                    total_page=101
                else:
                    total_page=math.ceil(case_num)
                # print(total_page)
                for page in range(0,total_page):
                    url=self.firm_lawyer_url
                    # print(page)
                    # print(lawyer_name)
                    request_data=self.make_request_data(page,lawfirm_name,city_code,lawyer_name)
                    yield scrapy.FormRequest(url,formdata=request_data,
                        meta={'lawfirm_name':lawfirm_name,'lawyer_name':lawyer_name},callback=self.get_list)

    def get_list(self,response):
        lawfirm_name=response.meta['lawfirm_name']
        lawyer_name=response.meta['lawyer_name']
        selector=lxml.html.fromstring(response.text)
        hrefs=selector.xpath('//div[@id="dataList"]/ul/li/a/@href')
        # print(hrefs)
        titles=selector.xpath('//div[@id="dataList"]/ul/li/a/text()')
        dates=selector.xpath('//div[@class="annexInfo"]/span[1]/text()')
        courts=selector.xpath('//div[@class="annexInfo"]/a/text()')
        case_nums=selector.xpath('//div[@class="annexInfo"]/span[2]/text()')
        for href,title,date,court,case_num in zip(hrefs,titles,dates,courts,case_nums):
            url=self.base_url+href
            title=title.strip()
            date=date.strip()
            court=court.strip()
            case_num=case_num.strip()
            # print(title)
            # print(date)
            # print(court)
            # print(url)
            yield Request(url,self.get_content,meta={'url':url,
                                    'title':title,
                                    'date':date,
                                    'court':court,
                                    'case_num':case_num,
                                    'lawfirm_name':lawfirm_name,
                                    'lawyer_name':lawyer_name},
                          )
    #
    def get_content(self,response):
        item=CaseshareDownloaderItem()
        # print(response.text)
        item['title']=response.meta['title']
        item['url']=response.meta['url']
        item['date']=response.meta['date']
        item['court']=response.meta['court']
        item['case_num']=response.meta['case_num']
        item['lawfirm_name']=response.meta['lawfirm_name']
        item['lawyer_name']=response.meta['lawyer_name']
        selector=lxml.html.fromstring(response.text)
        contents=selector.xpath('//div[@class="fullCon"]/text()')
        judges=selector.xpath('//div[@align="right"]/text()')
        content_list=[]
        for content in contents:
            if content.strip()!='':
                content_list.append(content.strip().replace('\u3000',''))
        new_content=('\r\n').join(content_list)
        # print(new_content)
        item['content']=new_content
        judge_list=[]
        if judges=='':
            new_judges=None
        else:
            for judge in judges:
                if judge.strip()!='':
                    judge_list.append(judge.strip().replace('\u3000',''))
            new_judges=('\r\n').join(judge_list)
        # print(new_judges)
        item['judges']=new_judges
        # print(item['judges'])
        # print(item)
        return item


    def get_lawfirm_info(self):
        conn=self.conn
        cursor = conn.cursor()
        sql = "SELECT lawfirm_name, city_code FROM caseshare_lawfirms_data"
        cursor.execute(sql)
        result=cursor.fetchall()
        return result

    def make_data(self,lawfirm_name,city_code):
        data={'IsLeaf':'True',
        'Keywords':'',
        'Cause':'',
        'LawFirm':lawfirm_name,
        'Lawyer':'',
        'AreaCode':str(city_code),
        'Court':'',
        'Judger':'',
        'ClassCodeKey':'',
        'IsGuide':'False',
        'SubKeywords':'',
        'X-Requested-With':'XMLHttpRequest'
       }
        return data

    def make_request_data(self,page,lawfirm_name,city_code,lawyer_name):
        request_data={
            'IsLeaf': 'True',
            'Keywords':'',
            'Cause':'',
            'LawFirm':lawfirm_name,
            'Lawyer':'',
            'AreaCode':city_code,
            'Court':'',
            'Judger':'',
            'ClassCodeKey':',{},'.format(lawyer_name),
            'IsGuide': 'False',
            'SubKeywords':'',
            'Pager.PageIndex':str(page),
            'X-Requested-With': 'XMLHttpRequest',
        }
        return request_data

#flag


    # def get_list(self, response):
    #     item=CaseshareDownloaderItem()
    #     item['lawfirm_name'] = response.meta['lawfirm_name']
    #     item['lawyer_name'] = response.meta['lawyer_name']
    #     selector = lxml.html.fromstring(response.text)
    #     hrefs = selector.xpath('//div[@id="dataList"]/ul/li/a/@href')
    #     # print(hrefs)
    #     titles = selector.xpath('//div[@id="dataList"]/ul/li/a/text()')
    #     dates = selector.xpath('//div[@class="annexInfo"]/span[1]/text()')
    #     courts = selector.xpath('//div[@class="annexInfo"]/a/text()')
    #     case_nums = selector.xpath('//div[@class="annexInfo"]/span[2]/text()')
    #     for href, title, date, court, case_num in zip(hrefs, titles, dates, courts, case_nums):
    #         item['url'] = self.base_url + href
    #         item['title'] = title.strip()
    #         item['date'] = date.strip()
    #         item['court'] = court.strip()
    #         item['case_num'] = case_num.strip()
    #         yield item
    # print(item)
    # print(title)
    # print(date)
    # print(court)
    # print(url)

    # def start_requests(self):
    # html=requests.get(self.number_url)
    # numbers=json.loads(html.text)
    # dict=self.get_numbers(numbers)
    # # print(dict)
    # for k,v in dict.items():
    #     total_pages= (v //10)
    #     for page in range(0,total_pages):
    #     # for page in range(0, 500):
    #         data=self.make_request_data(k,page)
    #         yield scrapy.FormRequest(
    #             url=self.request_url,
    #             formdata=data,
    #             callback=self.parse
    #         )

    # def parse(self, response):
    #     selector=lxml.html.fromstring(response.text)
    #     hrefs=selector.xpath('//div[@id="dataList"]/ul/li/a/@href')
    #     titles=selector.xpath('//div[@id="dataList"]/ul/li/a/text()')
    #     dates=selector.xpath('//div[@class="annexInfo"]/span[1]/text()')
    #     courts=selector.xpath('//div[@class="annexInfo"]/a/text()')
    #     case_nums=selector.xpath('//div[@class="annexInfo"]/span[2]/text()')
    #     for href,title,date,court,case_num in zip(hrefs,titles,dates,courts,case_nums):
    #         url=self.base_url+href
    #         title=title.strip()
    #         date=date.strip()
    #         court=court.strip()
    #         case_num=case_num.strip()
    #         # print(title)
    #         # print(date)
    #         # print(court)
    #         # print(case_num)
    #         yield Request(url,
    #                       meta={'url':url,'title':title,'date':date,'court':court,'case_num':case_num},
    #                       callback= self.get_content)
    # #
    # def get_content(self,response):
    #     item=CaseshareDownloaderItem()
    #     # print(response.text)
    #     item['title']=response.meta['title']
    #     item['url']=response.meta['url']
    #     item['date']=response.meta['date']
    #     item['court']=response.meta['court']
    #     item['case_num']=response.meta['case_num']
    #     selector=lxml.html.fromstring(response.text)
    #     contents=selector.xpath('//div[@class="fullCon"]/text()')
    #     judges=selector.xpath('//div[@align="right"]/text()')
    #     content_list=[]
    #     for content in contents:
    #         if content.strip()!='':
    #             content_list.append(content.strip().replace('\u3000',''))
    #     new_content=('\r\n').join(content_list)
    #     # print(new_content)
    #     item['content']=new_content
    #     judge_list=[]
    #     if judges=='':
    #         new_judges=None
    #     else:
    #         for judge in judges:
    #             if judge.strip()!='':
    #                 judge_list.append(judge.strip().replace('\u3000',''))
    #         new_judges=('\r\n').join(judge_list)
    #     # print(new_judges)
    #     item['judges']=new_judges
    #     # print(item)
    #     return item
    #
    # def make_request_data(self,cause,page):
    #     request_data={
    #         'IsLeaf': 'True',
    #         'Keywords':'',
    #         'Cause':str(cause),
    #         'LawFirm':'',
    #         'Lawyer':'',
    #         'AreaCode':'',
    #         'Court':'',
    #         'Judger':'',
    #         'ClassCodeKey':'',
    #         'IsGuide': 'False',
    #         'SubKeywords':'',
    #         'Pager.PageIndex':str(page),
    #         'X-Requested-With': 'XMLHttpRequest',
    #     }
    #     return request_data
    #
    # def get_numbers(self,numbers):
    #     dict={}
    #     for number in numbers:
    #         if number['name']=='刑事':
    #             data={
    #                 '001':number['count']
    #             }
    #             dict.update(data)
    #         elif number['name']=='民事':
    #             data={
    #                 '002':number['count']
    #             }
    #             dict.update(data)
    #         elif number['name'] == '知识产权':
    #             data = {
    #                 '003': number['count']
    #             }
    #             dict.update(data)
    #         elif number['name'] == '行政':
    #             data = {
    #                 '005': number['count']
    #             }
    #             dict.update(data)
    #         elif number['name'] == '执行':
    #             data = {
    #                 '006': number['count']
    #             }
    #             dict.update(data)
    #         elif number['name'] == '国家赔偿':
    #             data = {
    #                 '007': number['count']
    #             }
    #             dict.update(data)
    #     return dict