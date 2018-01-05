import pymysql,re


class parse_judges():
    def __init__(self):
        self.conn=pymysql.Connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='lawdata',charset='utf8')

    def get_data(self,sql):
        conn = self.conn    
        cursor =conn.cursor()        
        cursor.execute(sql)
        result=cursor.fetchall()
        return result

    def parse(self,sql):
        result = self.get_data(sql)
        # print(result[0])
        for item in result:
            id=item[0]
            judges_info=item[1]
            # print(judges_info)
            judges = self.re_judges_info(judges_info)
            print(id,judges)
    
    def re_judges_info(self,judges_info):
        list=judges_info.split('\r\n')
        judges=[]
        for info in list:
            i =self.select(info)
            if i !=None:        
                judges.append(i)
        return judges
        # print(judges)

    def select(self,word):
        if '代理审判员' in word:
            data ={
                '代理审判员':word.replace('代理审判员','')
            } 
            return data           
        elif '助理审判员' in word:
            data ={
                '助理审判员':word.replace('助理审判员','')
            } 
            return data           
        elif '审判长' in word:
            data ={
                '审判长':word.replace('审判长','')
            } 
            return data           
        elif '人民陪审员' in word:
            data ={
                '人民陪审员':word.replace('人民陪审员','')
            }   
            return data         
        elif '执行员' in word:
            data ={
                '执行员':word.replace('执行员','')
            }  
            return data          
        elif '法官助理' in word:
            data ={
                '法官助理':word.replace('法官助理','')
            }  
            return data          
        elif '书记员' in word:
            data ={
                '书记员':word.replace('书记员','')
            } 
            return data
        elif '审判员' in word:
            data ={
                '审判员':word.replace('审判员','')
            } 
            return data 
        else:
            return None      
        
        
if __name__=='__main__':
    sql='SELECT id,judges FROM caseshare_data_new LIMIT 10000'
    a=parse_judges()
    a.parse(sql)
    # word=a.parse(sql)
    # a.re_judges_info(word)
    


    '''原意图对日期进行匹配处理'''

    # def re_date(self,date):
    #     list=date.replace('年','-').replace('月','-').replace('日','').split('-')
    #     return list

    #     # print(list)

    # def year(self,year):        
    #     dict={ '一':1, '二':2,'三':3,
    #         '四':4,'五':5,'六':6,
    #         '七':7,'八':8,'九':9,
    #         '〇':0,'零':0,
    #     }
    #     new=[]
    #     for num in year:
    #         for k,v in dict.items():
    #             if num ==k:
    #                 new.append(str(v))
    #     print(int(''.join(new)))

    # def month(self,month):
    #     dict={ '一':1, '二':2,'三':3,
    #         '四':4,'五':5,'六':6,
    #         '七':7,'八':8,'九':9,
    #         '十':10,'十一':11,'十二':12,
    #     }
    #     for k,v in dict.items():
    #         if month==k:
    #             month=v
    #     print(month)

    # def day(self,day):
    #     list=[i for i in day]
    #     if len(list)==1:
    #         dict={ '一':1, '二':2,'三':3,
    #         '四':4,'五':5,'六':6,
    #         '七':7,'八':8,'九':9,            
    #     }
    #         for k,v in dict.items():
    #             day=list[0]
    #             if day==k:
    #                 day=v
    #         print(day)
    #     elif len(list)==2:            
    #         dict={ '一':1, '二':2,'三':3,
    #         '四':4,'五':5,'六':6,
    #         '七':7,'八':8,'九':9,'十':10
    #         } 
    #         j=0           
    #         for i in list:
    #             for k,v in dict.items():                    
    #                 if i==k:                        
    #                     j+=v
    #         print(j)
    #     elif len(list)==3:
    #         dict={ '一':1, '二':2,'三':3,
    #         '四':4,'五':5,'六':6,
    #         '七':7,'八':8,'九':9,'十':10
    #         } 
    #         j=[]
    #         for i in list:
    #             for k,v in dict.items():
    #                 if i==k:
    #                     j.append(v)
    #         day=j[0]*j[1]+j[2]
    #         print(day)
                        
        


