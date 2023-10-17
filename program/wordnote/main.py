from flask import Flask, render_template,request,send_file,Response
from sql import sqls
import json

'''
输入端：
    0. 先手动录入
    inputWord("apple", "苹果", "I have a apple")

    1. 校验是否正确
    正确：
        checkWord("apple", True)
    错误：
        checkWord("apple", False)

    2. 现实tip和usage,可供修改
        changeText("apple", "苹果", "I have two apple")

    3. 下一个单词 goto 1
    
'''

app = Flask(__name__)

class WordNote():
    def __init__(self) -> None:
        self.Sql = sqls("word.db")
        self.month = "threeTenMonth"
        self.Sql.CTable("%s (word text,tip text, usage text, truecount int, errorcount int)"%(self.month))
        self.operation = [] # 操作
        self.datas = [] # 操作数据

    def openSql(self): # 打开数据库
        if not self.Sql:
            self.Sql = sqls("word.db")
            self.Sql.CTable("%s (word text,tip text, usage text, truecount int, errorcount int)"%(self.month))

    def inputWord(self, word, tip, usage, truecount = 0, errorcount = 0,op = False): # 录入单词
        self.Sql.insert(self.month, (word, tip , usage, truecount, errorcount))
        if op:
            self.operation.append("input")
            self.datas.append((word, tip, usage))
        self.save()

    def changeUsage(self, word:str, tip:str = "", usage:str = "", op = True): # 更改tip和usage
        # 完全覆盖式的更新tip和usage
        words = self.findWord(word)
        if op and words:
            words = words[0]
            self.operation.append("cusage")
            self.datas.append((word, words[1], words[2]))
        if tip != "":  self.Sql.update(self.month,"tip = '" + tip + "' where word = '" + word + "'")
        if usage != "":  self.Sql.update(self.month,"usage = '" + usage + "' where word = '" + word + "'")
        self.save()

    def checkWord(self,word:str, TOrF) -> None:
        # 更新
        # if self.Sql.find(self.month, "where word = '" + word + "'"):
        if TOrF: # 更新对错次数
            self.Sql.update(self.month,"truecount = truecount + 1" + " where word = '" + word + "'")
        else:
            self.Sql.update(self.month,"errorcount = errorcount + 1" + " where word = '" + word + "'")

    def findWord(self, word): # 查找单词
        return self.Sql.find(self.month, "where word = '" + word + "'")

    def deleteWord(self, word, op = True): # 删除单词
        words = wordnote.findWord(word)
        if words:
            words = words[0]
            if op:
                self.operation.append("del") # 在operation中添加操作记录
                self.datas.append((words[0], words[1], words[2], words[3], words[4])) # 添加操作数据
        self.Sql.delete(self.month, "where word = '" + word + "'")
        self.save()

    def breakChange(self): # 撤销操作
        print (self.operation, "\n", self.datas)
        if not self.operation:
            return {"op":"null","word":""}
        op = self.operation.pop()
        data = self.datas.pop()
        if op == "del":
            self.inputWord(*data, op=False)
            return {"op":op, "word":data[0], "tip":data[1], "usage":data[2]}
        
        elif op == "cusage":
            self.changeUsage(*data, op=False)
            return {"op":op, "word":data[0], "tip":data[1], "usage":data[2]}
        
        elif op == "input":
            self.deleteWord(data[0], op=False)
        return {"op":"null","word":""}

    def save(self): # 保持数据库
        self.Sql.save()
    
    def close(self): # 关闭数据库
        self.Sql.close()
        self.Sql = None

    # def 获取单词
    
wordnote = WordNote()
# wordnote.inputWord("apple", "苹果", "I have a apple")

# 实现真正的检测就是获取单词 == 输入单词
# wordnote.checkWord("apple",TOrF=True)
# wordnote.changeUsage("apple", "青苹果", "I have ten apple")
# wordnote.save()

print (wordnote.Sql.find(wordnote.month, "where word = 'apple'"))

# ==========page============
@app.route('/index') 
def url_index():
    return render_template('index.html')

@app.route('/defindex')
def url_defindex():
    return render_template('defindex.html')


@app.route('/findWord', methods=['GET', 'POST'])  
def findWord(): # 查找单词
    word = request.values.get('word').strip() #对应了data
    words = wordnote.findWord(word)
    if words:
        words = words[0]
        return {"word":words[0], "tip":words[1], "usage":words[2]}
    else:
        return {"word":"", "tip":"", "usage":""}

@app.route('/changeUsage', methods=['GET', 'POST']) 
def changeUsage(): # 更改内容
    word = request.values.get('word').strip() #对应了data
    tip = request.values.get('tip').strip() #对应了data
    usage = request.values.get('usage').strip() #对应了data

    words = wordnote.findWord(word)
    if words: # 有单词
        words = words[0]
        wordnote.changeUsage(word, tip, usage)

    else: # 没有单词
        wordnote.inputWord(word, tip, usage)

    return json.dumps({"info":""})

@app.route('/deleteWord', methods=['GET', 'POST'])  # 删除单词
def deleteWord():
    word = request.values.get("word")
    wordnote.deleteWord(word)
    return json.dumps({"info":""})

@app.route('/breakChange', methods=['GET', 'POST'])  # 撤销操作
def breakChange():
    return json.dumps(wordnote.breakChange())
# def voice():
#     return Response(voice, mimetype="audio/mp3") #mpeg3

# =================image==================
@app.route("/defindex/n.png", methods=["GET"])
def getN():
    return getImg("./img/n.png")

@app.route("/defindex/o.png", methods=["GET"])
def getO():
    return getImg("./img/o.png")

@app.route("/defindex/t.png", methods=["GET"])
def getT():
    return getImg("./img/t.png")

@app.route("/defindex/e.png", methods=["GET"])
def getE():
    return getImg("./img/e.png")

def getImg(name = ""):
    with open(name, "rb") as f:
        return f.read()
    
app.run(host='127.0.0.1', port=80,debug=False) #, debug=True