import time
import scrapy
import json
import requests
from bs4 import BeautifulSoup
from scrapy.http import Request
from ..items import LawFirmListItem  #..为相对引用
import lxml.html
from lxml.html import etree
import pymysql

class MySpider(scrapy.Spider):
    name = 'lawfirmlist_spider'
    allowed_domains = ['caseshare.cn']
    base_url = 'http://caseshare.cn'
    lawfirm_lawyer_index = 'http://caseshare.cn/search/lawfirmorlawyer'
    number_url = 'http://caseshare.cn/api/chart/GetRecordCountByCauseCategory'
    request_url = 'http://caseshare.cn/Search/RecordSearch?FilterType=Cause&IsAdv=False'


    def start_requests(self):
        response = requests.get(self.lawfirm_lawyer_index)
        selector = lxml.html.fromstring(response.text)
        urls = selector.xpath('//div[@class="crumbsType"]/a/@href')
        provinces = selector.xpath('//div[@class="crumbsType"]/a/text()')
        for url, province in zip(urls, provinces):
            province_code = url.split('=')[1]
            full_url=self.base_url + url
            province_name= province
            province_code=province_code
            yield Request(full_url,meta={
                'province_name':province_name,
                'province_code':province_code
            },callback=self.parse)

    def parse(self, response):
        selector=lxml.html.fromstring(response.text)
        meta=response.meta        #
        # province_name=response.meta['province_name']
        # province_code:response.meta['province_code']
        city_hrefs=selector.xpath('//div[@class="crumbsType"]/a/@href')
        city_names=selector.xpath('//div[@class="crumbsType"]/a/text()')
        for city_href,city_name in zip(city_hrefs,city_names):
            city_id=city_href.split('=')[1]
            for page in range(0,60):
                url='http://caseshare.cn/Tool/NavLawFirm?pagesize=18&pageindex={}&areacode={}&firstletter='.format(page,city_id)
                yield Request(url,meta={
                    'province_name': meta['province_name'],
                    'province_code': meta['province_code'],
                    'city_name':city_name,
                    'city_code':city_id,
                },callback=self.get_lawfirm)


    def get_lawfirm(self,response):
        meta=response.meta

        if response.text is None:
            print('None')
            pass
        else:
            data = json.loads(response.text)
            if len(data) !=0:
               # print(data)
               for i in data:
                   yield self.write_info(i,meta)

    def write_info(self,info,meta):
        item = LawFirmListItem()
        item['lawfirm_name'] = info.setdefault('name', None)
        item['area_name'] = info.setdefault('areaName', None)
        item['area_code'] = info.setdefault('areaCode', None).replace(' ', '')
        item['province_name'] = meta['province_name']
        item['province_code'] = meta['province_code']
        item['city_name'] = meta['city_name']
        item['city_code'] = meta['city_code']
        # print(item)
        return item





