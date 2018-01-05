# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class CaseshareDownloaderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    url = scrapy.Field()
    case_num = scrapy.Field()
    court = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    judges=scrapy.Field()
    lawfirm_name=scrapy.Field()
    lawyer_name=scrapy.Field()

class LawFirmListItem(scrapy.Item):
    lawfirm_name = scrapy.Field()
    area_name = scrapy.Field()
    area_code = scrapy.Field()
    province_name = scrapy.Field()
    province_code = scrapy.Field()
    city_name = scrapy.Field()
    city_code = scrapy.Field()