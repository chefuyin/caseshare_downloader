import pymysql,jieba
# jieba.load_userdict('date.txt')
jieba.load_userdict('judge_dict.txt')




class ParseJudges():
    def __init__(self):
        self.conn=pymysql.Connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='lawdata',charset='utf8')
        self.cursor=self.conn.cursor()


    def get_data(self,sql):
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        return result


    def parse(self,sql):
        result = self.get_data(sql)
        # print(result[0])
        i=1
        for item in result:
            num = result.index(item)
            if num / 5000==i:#每5000个case提交一次
                # print(num,'*'*20)
                self.conn.commit()
                i+=1
            id=item[0]
            judges_info=item[1]
            # print(judges_info)
            judges = self.re_judges_info(judges_info)
            # print(id,judges)
            if judges!=[]:
                for info in judges:
                    for k,v in info.items():
                        # print(id,k,v)
                        self.write_data(k,v,id)
                        print(id)
        self.conn.commit()
        # print('end')


    def write_data(self,judge_title,judge_name,main_id):
        '''
        CREATE TABLE `caseshare_judges` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `judge_title` varchar(255) DEFAULT NULL,
          `judge_name` varchar(255) DEFAULT NULL,
          `main_id` int(11) NOT NULL,
          `createdtime` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        # sql = 'INSERT INTO caseshare_judges (`judge_title`,`judge_name`,`main_id`) VALUES (%(judge_title)s,%(judge_name)s,%(main_id)s)'
        # values = {'judge_title': judge_title,
        #           'judge_name':judge_name,
        #           'main_id':main_id}
        # self.cursor.execute(sql, values)
        sql = 'INSERT INTO caseshare_judges (`judge_title`,`judge_name`,`main_id`) ' \
              'VALUES ({},{},{})'.format(judge_title,judge_name,main_id)
        self.cursor.execute(sql)
        # self.conn.commit()##一次一提交存在效率障碍
    
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
                '代理审判员':word.replace('代理审判员','').replace(':','').replace('：','')
            } 
            return data           
        elif '助理审判员' in word:
            data ={
                '助理审判员':word.replace('助理审判员','').replace(':','').replace('：','')
            } 
            return data
        elif '代理书记员' in word:
            data ={
                '代理书记员':word.replace('代理书记员','').replace(':','').replace('：','')
            }
            return data
        elif '代书记员' in word:
            data ={
                '代书记员':word.replace('代书记员','').replace(':','').replace('：','')
            }
            return data
        elif '审判长' in word:
            data ={
                '审判长':word.replace('审判长','').replace(':','').replace('：','')
            } 
            return data           
        elif '人民陪审员' in word:
            data ={
                '人民陪审员':word.replace('人民陪审员','').replace(':','').replace('：','')
            }   
            return data
        elif '人民审判员' in word:
            data ={
                '人民审判员':word.replace('人民审判员','').replace(':','').replace('：','')
            }
            return data
        elif '执行员' in word:
            data ={
                '执行员':word.replace('执行员','').replace(':','').replace('：','')
            }  
            return data          
        elif '法官助理' in word:
            data ={
                '法官助理':word.replace('法官助理','').replace(':','').replace('：','')
            }  
            return data          
        elif '书记员' in word:
            data ={
                '书记员':word.replace('书记员','').replace(':','').replace('：','')
            } 
            return data
        elif '审判员' in word:
            data ={
                '审判员':word.replace('审判员','').replace(':','').replace('：','')
            } 
            return data 
        else:
            return None

    def select_incorrect(self,sql):
        '''choose the incorrect info'''
        result= self.get_data(sql)
        for info in result:
            id=info[0]
            judge_title = info[1]
            judge_name=info[2]
            main_id= info[3]
            list=[i for i in judge_name]
            if len(list)>=4:
                print(main_id,judge_title,judge_name)

    def search(self,main_id):
        sql= 'SELECT judges FROM caseshare_data_new WHERE id={}'.format(str(main_id))
        # values={'main_id':str(main_id)}
        cursor= self.conn.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        return result[0][0]


    def write_date_dict(self,word):
        word_list= word.split('\r\n')
        list=[]
        for w in word_list:
            if self.date_distinc(w):
                if w!='':
            # seg_list=jieba.cut(word0,cut_all=False)
            # list=[i for i in seg_list]
            # if len(list)>=5:
                    list.append(w)
        for i in self.set(list):
            print(i)
            self.write_txt('date.txt',i)

            # print(','.join(seg_list))

    def set(self,word_list):
        if type(word_list) is list:
            return list(set(word_list))

    def date_distinc(self,date):
        '''判断是否为日期，应包含年月日'''
        list= [i for i in date]
        if '年' in list and '月' in list and '日'in list:
            if 9<=len(list)<=11:
                return True

    def write_txt(self,filename,line):
        with open(filename,'a+',encoding='utf-8') as f:
            f.write(line+'\n')

    def cut(self,word):
        seg_list=jieba.cut(word)
        print('/'.join(seg_list))


        
        
if __name__=='__main__':
    '''select incorrect info'''
    sql='SELECT id,judge_title,judge_name,main_id FROM caseshare_judges LIMIT 10000'
    a=ParseJudges()
    # a.select_incorrect(sql)
    r=a.search(1304)
    print(r)

    '''write jieba dict'''
    # sql='SELECT id,judges FROM caseshare_data_new LIMIT 10000'
    # # sql = 'SELECT id,judges FROM caseshare_data_new'
    # # sql='SELECT id,judge_title,judge_name,main_id FROM caseshare_judges'
    # # sql = 'SELECT id,judge_name,main_id FROM caseshare_judges LIMIT 100'
    # a=ParseJudges()
    # result=a.get_data(sql)
    # for i in result:
    #     a.cut(i[1])




    '''write data from main table'''
    # # sql='SELECT id,judges FROM caseshare_data_new LIMIT 10000'
    # sql = 'SELECT id,judges FROM caseshare_data_new'
    # a=parse_judges()
    # a.parse(sql)
    # # word=a.parse(sql)
    # # a.re_judges_info(word)
    


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
                        
        


