import pygame
import random

class Objects():
    def __init__(self) -> None:
        self.gameReseting = False # 正在重置游戏
        # screen
        self.padding = 50 # 填充
        self.screenWidth = 400 + self.padding * 2
        self.screenHeight = 400 + self.padding * 2

        # objects
        self.selectObjects = [] # 跟随player白点的对象
        self.tempMergeObjects = [] # 可合并对象（蓝点）
        self.tempDamageObjects = [] # 可消除对象（红点）

        # merageobj（合并对象）
        self.mergeObjWidthRange = (10,30)
        self.mergeObjHeightRange = (10,30)
    
        self.MergeObjXRange = (self.padding + self.mergeObjWidthRange[1],
                            self.screenWidth - self.mergeObjWidthRange[1] - self.padding)
        self.MergeObjYRange = (self.padding + self.mergeObjHeightRange[1],
                            self.screenHeight - self.mergeObjHeightRange[1] - self.padding)
        self.MergeObjColor = "#5030e7"

        # damageobj（消除对象）
        self.damageObjWidthRange = (10,50)
        self.damageObjHeightRange = (10,50)

        self.DamageObjXRange = (self.padding + self.damageObjWidthRange[1],
                            self.screenWidth - self.damageObjWidthRange[1] - self.padding)
        self.DamageObjYRange = (self.padding + self.damageObjHeightRange[1],
                            self.screenHeight - self.damageObjHeightRange[1] - self.padding)
        self.DamageObjColor = "#e27959"

        self.mergeGenerateCount = 2
        self.damageGenerateCount = 2 # 方块合并后产生的危险方块数

        # player
        self.playerWidthRange = (10,10)
        self.playerHeightRange = (10,10)
        self.playerMoveStep = 1
        self.playerFast = False # 加速移动
        self.playerColor = "#dddddd"

        self.gameMerageBlocks = 0
        self.gameMaxMerageBlocks = 0
obj = Objects()

class Player(pygame.sprite.Sprite): # 白点
    def __init__(self,pos): # ,color
        pygame.sprite.Sprite.__init__(self)
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

class MergeItem(Player): # 合并方块
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        w = random.randint(*obj.mergeObjWidthRange)
        h = random.randint(*obj.mergeObjHeightRange)
        self.image = pygame.Surface((w,h))
        self.image.fill(color=obj.MergeObjColor)
        self.rect = self.image.get_rect(center=pos)     #rect外框，移动位置

    # def draw(self,aSurface):
    #     aSurface.blit(self.image,self.rect)

class DamageItem(Player): # 消除方块
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        w = random.randint(*obj.damageObjWidthRange)
        h = random.randint(*obj.damageObjHeightRange)
        self.image = pygame.Surface((w,h))
        self.image.fill(color=obj.DamageObjColor)           
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
def itemMove(): # 跟随白点移动
    while True:
        if obj.playerFast:
            obj.playerMoveStep = 3
        else:
            obj.playerMoveStep = 1
        for o in obj.selectObjects:
            if exevent.downKeyValue == pygame.K_RIGHT:
                o.rect.x += obj.playerMoveStep
            elif exevent.downKeyValue == pygame.K_LEFT:
                o.rect.x -= obj.playerMoveStep
            elif exevent.downKeyValue == pygame.K_UP:
                o.rect.y -= obj.playerMoveStep
            elif exevent.downKeyValue == pygame.K_DOWN:
                o.rect.y += obj.playerMoveStep
        time.sleep(0.02)

def mergeEvent(): # 合并消除时间
    while True:
        for i in obj.tempMergeObjects: # 合并检查
            for j in obj.selectObjects:
                if pygame.sprite.collide_rect(i, j):
                    # 将临时的合并块加入到selectobjects的整体中
                    mergesound.play() # 播放音频
                    obj.selectObjects.append(i)
                    if obj.gameReseting: return # 多线程带来的问题,好像并不能解决
                    obj.tempMergeObjects.remove(i) 
                    for i in range(obj.damageGenerateCount):
                        newObject("damage") # 合并后新增一个危险块
                    for i in range(obj.mergeGenerateCount):
                        newObject("merge")
                    # ==
                    obj.gameMerageBlocks += 1 # 合并方块总数
                    obj.gameMaxMerageBlocks = max(len(obj.selectObjects), obj.gameMaxMerageBlocks) # 最大的合并数
                    break
        for i in obj.tempDamageObjects: # 危险检查
            for j in obj.selectObjects:
                if pygame.sprite.collide_rect(i, j):
                    damagesound.play()
                    if obj.gameReseting: return # 多线程带来的问题,好像并不能解决
                    obj.tempDamageObjects.remove(i) # 移除被碰到的危险块
                    # 移除一半的方块（注：此处可以更改消除的比例，是消除一个-1还是消除一遍//2）
                    obj.selectObjects = obj.selectObjects[:len(obj.selectObjects) // 2]
                    break
        if len(obj.selectObjects) == 0:
            gameFinish()
        time.sleep(0.01)

class ExpandEvents():
    def __init__(self) -> None:
        self.downKeyValue = None # 实现长按功能（记录按下的键）
        self.itemMoveThread = threading.Thread(target=itemMove)
        self.mergeEventThread = threading.Thread(target=mergeEvent)
        self.itemMoveThread.start()
        self.mergeEventThread.start()

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
    obj.gameReseting = True
    obj.selectObjects = [] # 跟随移动对象
    obj.selectObjects.append(Player((obj.screenWidth // 2, obj.screenHeight // 2)))
    obj.tempMergeObjects = [] # 蓝色方块
    obj.tempDamageObjects = [] # 红色方块
    newObject("merge")
    obj.gameReseting = False

gameinit()
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
                exevent.downKeyValue = event.key
            if event.key in [pygame.K_LCTRL,pygame.K_RCTRL]: # 加速移动
                obj.playerFast = True

        if event.type==pygame.KEYUP: # 松开后就按键清空
            exevent.downKeyValue = None
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