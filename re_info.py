import re


class ReInfo:

    @classmethod
    def re_judge(cls,rule,judges):
        ptn=re.compile(rule)
        result=ptn.search(judges)
        # print(result.start())
        if result:
           # print(result.group())
           return result.group()

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

    def date_rule(self):
        rule_list=[
            "二(.*?)年(.*?)月(.*?)日\s",
            "二(.*?)年(.*?)月(.*?)日",
            # "一(.*?)年(.*?)月(.*?)日\s",
            # "一(.*?)年(.*?)月(.*?)日",
        ]
        return  rule_list

if __name__=='__main__':
    a=ReInfo()
    l=[]
    judges='审判长韩咏梅\r\n审判员程全法代审判员王长坡\r\n二〇一一年元月十九日\r\n'
    for i in a.judge_title_rule():
        result=a.re_judge(i,judges)
        if result:
            l.append(result.strip())
    result_list=list(set(l))
    print(result_list)