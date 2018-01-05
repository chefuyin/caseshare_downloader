from .sql import Sql
from ..items import CaseshareDownloaderItem,LawFirmListItem

class CasesharePipeline(object):
    def process_item(self,item,spider):
        if isinstance(item,CaseshareDownloaderItem):
            url=item['url']
            ret=Sql.select_url(url)
            if ret[0]==1:
                print('已经存在了')
                pass
                # lawfirm_name=Sql.select_lawfirm_name_value(url)
                # lawyer_name = Sql.select_lawyer_name_value(url)
                # if lawfirm_name[0]==item['lawfirm_name'] and lawyer_name[0]==item['lawyer_name']:
                #     print('律所名律师名均已存在')
                #     pass
                # elif lawfirm_name[0]!=item['lawfirm_name']:
                #     lawfirm_name = ','.join([lawfirm_name[0], item['lawfirm_name']])
                #     Sql.update_lawfirm_name(url,lawfirm_name)
                # elif lawyer_name[0]!=item['lawyer_name']:
                #     lawyer_name = ','.join([lawyer_name[0], item['lawyer_name']])
                #     Sql.update_lawyer_name(url,lawyer_name)
            else:
                cs_title=item['title']
                cs_url = item['url']
                cs_case_num=item['case_num']
                cs_court=item['court']
                cs_date = item['date']
                cs_content = item['content']
                cs_judges=item['judges']
                cs_lawfirm_name=item['lawfirm_name']
                cs_lawyer_name=item['lawyer_name']
                Sql.create_index(cs_url)
                Sql.insert_caseshare_data(cs_title,cs_url,cs_court,cs_case_num,cs_date,cs_content,cs_judges,cs_lawfirm_name,cs_lawyer_name)
                print('开始写入')

# class WriteLawFirmPipeline(object):
#     def process_item(self, item, spider):
#         if isinstance(item,LawFirmListItem):
#             name = item['lawfirm_name']
#             ret = Sql.select_lawfirm_name(name)
#             if ret[0] == 1:
#                 print('已经存在了')
#                 pass
#             else:
#                 lawfirm_name = item['lawfirm_name']
#                 area_name = item['area_name']
#                 area_code = item['area_code']
#                 province_name = item['province_name']
#                 province_code = item['province_code']
#                 city_name = item['city_name']
#                 city_code = item['city_code']
#                 Sql.insert_lawfirms_data(lawfirm_name,area_name,area_code,province_name,province_code,city_name,city_code)
#                 print('开始写入')

