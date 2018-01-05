import pymysql


class CreateIndex:
    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='alvincha',
            db='lawdata',
            charset='utf8')

    def get_url(self):
        conn = self.conn
        cursor = conn.cursor()
        sql = "SELECT `url` FROM caseshare_data_new"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def create_index(self,url):
        conn = self.conn
        cursor = conn.cursor()
        sql = 'INSERT INTO caseshare_url_index (`url`) VALUES (%(url)s)'
        values={'url':url}
        cursor.execute(sql,values)
        conn.commit()

if __name__ =='__main__':
    a=CreateIndex()
    result=a.get_url()
    count=1
    for i in result:
        url=i[0]
        a.create_index(url)
        print('write:',count)
        count+=1
        # print(i[0])
        # print(type(i[0]))