import re,pymysql
# import jieba
# jieba.load_userdict('judge_dict.txt')


class ReInfo:
    def __init__(self):
        self.conn=pymysql.Connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='lawdata',charset='utf8')
        self.cursor=self.conn.cursor()

    def select(self,sql):
        cursor= self.cursor
        cursor.execute(sql)
        r= cursor.fetchall()
        return r

    def re_search(self,rule,text):
        ptn=re.compile(rule)
        result=ptn.search(text)
        # print(result.start())
        if result:
           # print(result.group())
           return result.group()

    def re_match(self,rule,text):
        ptn=re.compile(rule)
        result=ptn.match(text)
        # print(result.start())
        if result:
           # print(result.group())
           return result.groups()

    def re_findall(self,rule,text):
        ptn=re.compile(rule)
        result=ptn.findall(text)
        # print(result.start())
        if result:
           # print(result.group())
           return result

    def re_split(self,rule,text):
        ptn=re.compile(rule)
        result=ptn.split(text)
        # print(result.start())
        if result:
           # print(result.group())
           return result

    def judge_rule_long(self):
        rule_list=[r"代理审判员(.*?)\s",
                   r"代审判员(.*?)\s",
                   r"助理审判员(.*?)\s",
                   r"代理书记员(.*?)\s",
                   r"代书记员(.*?)\s",
                   r"审判长(.*?)\s",
                   r"人民陪审员(.*?)\s",
                   r"执行员(.*?)\s",
                   r"法官助理(.*?)\s",
                   r"书记员(.*?)\s",
                   r"审判员(.*?)\s",
                   ]
        return rule_list

    def judge_title_rule(self):
        rule_list = [r"代理审判员(.*?)",
                     r"代审判员(.*?)",
                     r"助理审判员(.*?)",
                     r"代理书记员(.*?)",
                     r"代书记员(.*?)",
                     r"执行员(.*?)",
                     r"审判长(.*?)",
                     r"人民陪审员(.*?)",
                     r"法官助理(.*?)",
                     r"书记员(.*?)",
                     r"审判员(.*?)",
                     ]
        return rule_list

    def judge_title(self):
        rule_list = [r"代理审判员",
                     r"代审判员",
                     r"助理审判员",
                     r"代理书记员",
                     r"代书记员",
                     r"执行员",
                     r"审判长",
                     r"人民陪审员",
                     r"法官助理",
                     r"书记员",
                     r"审判员",
                     ]
        return rule_list

    def title_name(self,title_list):
        l=[]
        if type(title_list)==list:
            for title in title_list:
                rule=r"{}(.*?)(\s|$)".format(title)
                l.append(rule)
        return l

    def title_name_further(self):
        pass



    def date_rule(self):
        rule_list=[
            "二(.*?)年(.*?)月(.*?)日\s",
            "二(.*?)年(.*?)月(.*?)日",
            # "一(.*?)年(.*?)月(.*?)日\s",
            # "一(.*?)年(.*?)月(.*?)日",
        ]
        return  rule_list

    def search_title(self,text,rule_list):
        l=[]
        t=text
        for i in range(0,len(rule_list)):
            result=self.re_search(rule_list[i],t)
            # print('text:','\n',t)
            # print('result:', result)
            # print('*'*20)s
            if result is None:
                i+=1
            else:
                l.append(result.strip())
                t=t.replace(result,'')
                i+=1
        return l





if __name__=='__main__':
    # sql= "SELECT judges FROM caseshare_data_new LIMIT 100000"
    a=ReInfo()
    # r=a.select(sql)
    # rule_list = a.judge_title()
    rule_list = a.judge_title_rule()
    # text = '审判长韩咏梅\r\n代理审判员程全法代审判员王长坡\r\n二〇一一年元月十九日\r\n'
    r=re.sub()


    # for info in r:
    #     text= info[0]
    #     print(text)
    #
    #
    #     titles= a.search_title(text,rule_list)
    #     # print(titles)
    #     for title in titles:
    #
    #         new='\r\n{}'.format(title)
    #         text=text.replace(title,new)
    #     new_rules=a.title_name(titles)
    #     l=[]
    #     for rule in new_rules:
    #         r=a.re_search(rule,text)
    #         if r:
    #             l.append(r.strip())
    #
    #     print(l)
    #     print('='*10)



    # text = '审判长韩咏梅\r\n代理审判员程全法代审判员王长坡\r\n二〇一一年元月十九日\r\n'




    # sql= "SELECT judges FROM caseshare_data_new LIMIT 1000"
    # a=ReInfo()
    # r=a.select(sql)
    # for info in r:
    #     texts= info[0]
    #     l=[]
    #     # text='审判长韩咏梅\r\n审判员程全法代审判员王长坡\r\n二〇一一年元月十九日\r\n'
    #     for text in texts.split('\r\n'):
    #         # for i in a.judge_title():
    #         #     result=a.re_judge(i,text)
    #         #     if result:
    #         #         l.append(result.strip())
    #     result_list=list(set(l))
    #     print(texts)
    #     print(result_list)
    #     print('-'*10)