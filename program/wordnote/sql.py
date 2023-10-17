import sqlite3 as sql
class sqls():
    def __init__(self,name):
        self.conn = sql.connect(name, check_same_thread=False)
        self.cur = self.conn.cursor()
        #self.CTable(ctable)
        
    def CTable(self,names):
        #创建表
        self.cur.execute('''CREATE TABLE IF NOT EXISTS {}'''.format(names))
        
    def getTable(self):
        #获得表
        self.cur.execute("select name from sqlite_master where type='table'")
        return self.cur.fetchall()

    def getField(self,names):
        #获得字段
        self.cur.execute('pragma table_info({})'.format(names)) #获得字段
        return self.cur.fetchall()
    
    def insert(self,tables,data):
        self.cur.execute('INSERT INTO {} VALUES(?'.format(tables) + ",?" * (len(data) - 1) + ');',data)
        
    def inserts(self,tables,data):
        #多个数据输入
        self.cur.executemany('INSERT INTO {} VALUES(?'.format(tables) + ",?" * (len(data[0]) - 1) + ');',data)

    def update(self,tables,data):
        self.cur.execute('UPDATE  {}  SET {}'.format(tables,data))
    
    def delete(self,tables,way):
        self.cur.execute('DELETE FROM {} {}'.format(tables,way))

    def delTable(self,table):
        self.conn.execute("DROP TABLE " + table)
        
    def find(self,tables, way = "",field = "*"):
        print ("*sql.py*: ", 'SELECT {} FROM {} {}'.format(field,tables,way))
        self.cur.execute('SELECT {} FROM {} {}'.format(field,tables,way))
        text = self.cur.fetchall()
        if text != []:
            return text
        return ""
    

    def clear(self,tables):
        #清空表
        self.cur.execute("DELETE FROM {}".format(tables))
        
    def save(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def one(self):
        self.cur.execute("SELECT DISTINCT * FROM texts;")
        return self.cur.fetchall()

    def count(self,table):
        c=self.cur.execute('''SELECT * FROM '''+table)
        return len(c.fetchall())

    def updates(self):
        self.conn.execute("VACUUM")

    def selects(self,text):
        #需要自己编写语句
        self.cur.execute(text)
        return self.cur.fetchall()

if __name__ == "__main__":
    a = sqls("text.db")
    a.CTable("texts (file text, row int,strings text)")
    '''
    a.insert("texts",("a.txt",1,'for i in range(10)'))
    
    records = [("a.txt",1, 'Alen'),
               ("b.js",2, 'Elliot'),
               ("c.py",3, 'Bob')]
    a.inserts("texts",records)
    '''
    print (a.getTable())
    #a.delete("texts","")
    print (a.getField("texts"))
    #print (a.find("texts",'where file = "E:/projectsss/实验/ccccccccccccc.py"'))

    a.clear("texts")
    #print (a.one())
    a.save()
    a.close()
