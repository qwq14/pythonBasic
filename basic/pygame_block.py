import pygame
import random

class Objects():
    def __init__(self) -> None:
        # screen
        self.padding = 50 # 填充
        self.screenWidth = 400 + self.padding * 2
        self.screenHeight = 400 + self.padding * 2

        # objects
        self.selectObjects = [] # 跟随player白点的对象
        self.tempMergeObjects = [] # 可合并对象（蓝点）
        self.tempDamageObjects = [] # 可消除对象（红点）

        # merageobj（合并对象）
        self.mergeObjWidthRange = (15,20)
        self.mergeObjHeightRange = (15,20)
    
        self.MergeObjXRange = (self.padding + self.mergeObjWidthRange[1],
                            self.screenWidth - self.mergeObjWidthRange[1] - self.padding)
        self.MergeObjYRange = (self.padding + self.mergeObjHeightRange[1],
                            self.screenHeight - self.mergeObjHeightRange[1] - self.padding)
        self.MergeObjColor = "#5030e7"

        # damageobj（消除对象）
        self.damageObjWidthRange = (5,50)
        self.damageObjHeightRange = (5,50)

        self.DamageObjXRange = (self.padding + self.damageObjWidthRange[1],
                            self.screenWidth - self.damageObjWidthRange[1] - self.padding)
        self.DamageObjYRange = (self.padding + self.damageObjHeightRange[1],
                            self.screenHeight - self.damageObjHeightRange[1] - self.padding)
        self.DamageObjColor = "#e27959"

        self.mergeGenerateCount = 1
        self.damageGenerateCount = 2 # 方块合并后产生的危险方块数

        # player
        self.playerWidthRange = (10,10)
        self.playerHeightRange = (10,10)
        self.playerMoveStep = 1
        self.playerFast = False # 加速移动
        self.playerColor = "#dddddd"

        self.gameMerageBlocks = 0
        self.gameMaxMerageBlocks = 0

        self.limitMergeTime = 5
        self.mergeTime = self.limitMergeTime

obj = Objects()

class Player(pygame.sprite.Sprite): # 白点
    def __init__(self,pos): # ,color
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        w = random.randint(*obj.playerWidthRange)
        h = random.randint(*obj.playerHeightRange)
        self.image = pygame.Surface((w,h))
        self.image.fill(color=obj.playerColor)            
        # self.image.set_colorkey((3,4,5))      #设置这个颜色为透明色
        # self.image.fill((3,4,5))            #底色透明
        # pygame.draw.MergeItem(self.image,pygame.Color(color),(w // 2, h // 2),15)
        self.rect = self.image.get_rect(center=pos)     #rect外框，移动位置

    def draw(self,aSurface):
        aSurface.blit(self.image,self.rect)


class BaseItem(pygame.sprite.Sprite): # 白点
    def __init__(self,pos): # ,color
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1,1))
        self.rect = self.image.get_rect(center=pos)     #rect外框，移动位置

    def draw(self,aSurface):
        aSurface.blit(self.image,self.rect)
    
    def setColor(self, color):
        self.color = color
        self.image.fill(color = self.color)
    
    def setPos(self, pos):
        self.rect = self.image.get_rect(center=pos)

class MergeItem(BaseItem): # 合并方块
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.color = obj.MergeObjColor
        w = random.randint(*obj.mergeObjWidthRange)
        h = random.randint(*obj.mergeObjHeightRange)
        self.image = pygame.Surface((w,h))
        self.image.fill(color = self.color)
        self.rect = self.image.get_rect(center=pos)     #rect外框，移动位置

class DamageItem(BaseItem): # 消除方块
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        # color position
        self.pos = list(pos)
        self.color = obj.DamageObjColor
        # move speed
        self.speedx = random.randint(1,3) / 10
        self.speedy = random.randint(1,3) / 10
        # width
        w = random.randint(*obj.damageObjWidthRange)
        h = random.randint(*obj.damageObjHeightRange)
        self.image = pygame.Surface((w,h))
        # color
        self.image.fill(color = self.color)           
        # pos
        self.rect = self.image.get_rect(center=pos)     #rect外框，移动位置

pygame.init()
screen = pygame.display.set_mode((obj.screenWidth, obj.screenHeight))
pygame.display.set_caption("碰撞-连接")
clock = pygame.time.Clock()
run=True

# pygame.mixer.init()
mergesound = pygame.mixer.Sound("merge.mp3")  # 加载音乐  
damagesound = pygame.mixer.Sound("damage.mp3")  # 加载音乐  
mergesound.set_volume(0.3)
damagesound.set_volume(0.3)

import threading
import time
def playerMove(): # 跟随白点移动
    while True:
        if obj.playerFast:
            obj.playerMoveStep = 3
        else:
            obj.playerMoveStep = 1

        x = 0
        y = 0

        for key in exevent.downKeyValue:
            if key == pygame.K_RIGHT:
                x = obj.playerMoveStep
            elif key == pygame.K_LEFT:
                x = -obj.playerMoveStep
            if key == pygame.K_UP:
                y = -obj.playerMoveStep
            elif key == pygame.K_DOWN:
                y = obj.playerMoveStep

        for o in obj.selectObjects:
            o.rect.x += x
            o.rect.y += y

        time.sleep(0.02)

def mergeEvent(): # 合并消除时间
    while True:
        for i in obj.tempMergeObjects: # 合并检查
            for j in obj.selectObjects:
                if pygame.sprite.collide_rect(i, j):
                    # 将临时的合并块加入到selectobjects的整体中
                    mergesound.play() # 播放音频
                    obj.selectObjects.append(i)
                    obj.tempMergeObjects.remove(i) 
                    for i in range(obj.damageGenerateCount):
                        newObject("damage") # 合并后新增一个危险块
                    for i in range(obj.mergeGenerateCount):
                        newObject("merge")
                    # ==
                    obj.gameMerageBlocks += 1 # 合并方块总数
                    obj.gameMaxMerageBlocks = max(len(obj.selectObjects), obj.gameMaxMerageBlocks) # 最大的合并数
                    #==
                    obj.mergeTime = obj.limitMergeTime # 重置合并时间
                    break
        for i in obj.tempDamageObjects: # 危险检查
            for j in obj.selectObjects:
                if pygame.sprite.collide_rect(i, j):
                    if isinstance(i, Player):
                        gameFinish() # 玩家（白点）碰到就算游戏结束
                        return
                    damagesound.play()
                    obj.tempDamageObjects.remove(i) # 移除被碰到的危险块
                    # 移除一半的方块（注：此处可以更改消除的比例，是消除一个-1还是消除一遍//2）
                    obj.selectObjects = obj.selectObjects[:len(obj.selectObjects) - 1]
                    break
        if len(obj.selectObjects) == 0:
            gameFinish()
            return
        if obj.mergeTime < 0:
            gameFinish()
            return
        time.sleep(0.01)

def damgeMove():
    while True:
        for i in obj.tempDamageObjects:
            # if not getattr(i, "speedx", None):
            #     setattr(i, "speedx", random.randint(1,3) / 10)
            #     setattr(i, "speedy", random.randint(1,3) / 10)
            i.pos[0] += i.speedx
            i.pos[1] += i.speedy
            if i.pos[0] > obj.DamageObjXRange[1] or i.pos[0] < obj.DamageObjXRange[0]:
                i.speedx = -i.speedx
            if i.pos[1] > obj.DamageObjYRange[1] or i.pos[1] < obj.DamageObjYRange[0]:
                i.speedy = -i.speedy
            # w = random.randint(*obj.playerWidthRange)
            # h = random.randint(*obj.playerHeightRange)
            # i.image = pygame.Surface((w,h))
            i.setPos(i.pos)
        time.sleep(0.01)

def damageColorChange(): # 定时更改颜色
    while True:
        obj.DamageObjColor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        for i in obj.tempDamageObjects:  # 更改damage样式
            i.setColor(obj.DamageObjColor)
        time.sleep(random.randint(10,20))

def timing(): # 1秒的限时器
    while True:
        obj.mergeTime -= 1 # 合并时间限制
        time.sleep(1)


class ExpandEvents():
    def __init__(self) -> None:
        self.downKeyValue = [] # 实现长按功能（记录按下的键）
        self.eventName = ["playerMove", "mergeEvent", "damgeMove", "timing", "damageColorChange"]
        self.events = [playerMove, mergeEvent, damgeMove, timing, damageColorChange]
        for index, name in enumerate(self.eventName):
            self.__dict__[name] = threading.Thread(target=self.events[index])
            
    def starts(self):
        for name in self.eventName:
            if not self.__dict__[name].is_alive():
                self.__dict__[name].start()

    def startof(self, name):
        if name in self.eventName:
            self.__dict__[name] = threading.Thread(target=self.events[self.eventName.index(name)])
            self.__dict__[name].start()


exevent = ExpandEvents()

def stackNewObject(blocktype): # 方块的具体生成
    count = 1
    checkobj = obj.selectObjects.copy()
    if blocktype == "merge":
        createobj = MergeItem
        xranges = obj.MergeObjXRange
        yranges = obj.MergeObjYRange
        checkobj.extend(obj.tempDamageObjects) # 合并块如果和危险块在一起，合并后成为一部分还是要被去除一半
    elif blocktype == "damage":
        createobj = DamageItem
        xranges = obj.DamageObjXRange
        yranges = obj.DamageObjYRange
    while count < 2000: # 2000次随机生成还没有早到合适位置，就认定为没有空间了
        x = random.randint(*xranges)
        y = random.randint(*yranges)
        o = createobj((x,y))
        for i in checkobj:
            if pygame.sprite.collide_rect(i, o): # 有碰撞
               break 
        else:
            return o
        count += 1
    return False
    

def newObject(blocktype):
    if blocktype == "merge":
        o = stackNewObject(blocktype)
        # print (o)
        if o == False:
            return gameFinish()
                
        obj.tempMergeObjects.append(o)
        
    elif blocktype == "damage":
        o = stackNewObject(blocktype)
        if o == False:
            return gameFinish()
        obj.tempDamageObjects.append(o)

    return False

def gameinit(): # 初始化游戏
    del obj.selectObjects,obj.tempMergeObjects,obj.tempDamageObjects
    obj.selectObjects = [] # 跟随移动对象
    obj.selectObjects.append(Player((obj.screenWidth // 2, obj.screenHeight // 2)))
    obj.tempMergeObjects = [] # 蓝色方块
    obj.tempDamageObjects = [] # 红色方块
    newObject("merge")
    obj.mergeTime = obj.limitMergeTime
    exevent.startof("mergeEvent")

gameinit()
exevent.starts()

def gameFinish(): # 结束游戏
    print ("共连接了%d个方块, 最大方块连接数：%d个"%(obj.gameMerageBlocks, obj.gameMaxMerageBlocks))
    gameinit()

while run:
    screen.fill((20,20,20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run=False

        if event.type==pygame.KEYDOWN:            #如是键按下事件
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
                exevent.downKeyValue.append(event.key)
            if event.key in [pygame.K_LCTRL,pygame.K_RCTRL]: # 加速移动
                obj.playerFast = True

        if event.type==pygame.KEYUP: # 松开后就按键清空
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
                exevent.downKeyValue.remove(event.key)
            if event.key in [pygame.K_LCTRL,pygame.K_RCTRL]: # 取消加速
                obj.playerFast = False
  
    # if pygame.sprite.collide_MergeItem(a,b):             #圆形碰撞检测
    # if pygame.sprite.collide_circle_ratio(0.5)(a,b):  #圆形碰撞检测(半径值)
    # 绘制
    for i in obj.selectObjects:
        i.draw(screen)
    for i in obj.tempMergeObjects:
        i.draw(screen)
    for i in obj.tempDamageObjects:
        i.draw(screen)

    clock.tick(30) # tick
    pygame.display.update() # 更新
pygame.quit()