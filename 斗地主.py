#1.新建牌堆
#2.定义牌型，包括单张，对子，三带1，三带2，顺子，连对，四带二，炸弹 同牌形可以压过
#3.定义牌值的大小，3最小，joker最大，2第二
#4.游戏规则：三人游戏，轮流发牌，剩3张时，随机选一名玩家当地主。获得地主牌。地主先出。
#5.所有玩家的牌按牌值从大到小排序。
#6.分数系统，每人初始100分，地主赢一局加2分，输一局减2分。
#7.AI出牌逻辑：自己出优先出单张。别人出，有大牌就压。
#可视化：牌桌上显示当前在出的牌，玩家手中看到自己的牌，叠放。其他人的牌只显示背面。显示：开始按钮，下一局按钮。分数，出版记录。
import pygame
import deck as d
import pygame.freetype
from collections import Counter
#定义常量
#定义颜色
green=(0,128,0)
#基础设置
pygame.freetype.init()  # 初始化字体，才能显示中文
# 定义输入框需要的颜色
WHITE = (255,255,255)
GRAY = (200,200,200)  # 输入框激活时的背景色
BLUE = (0,0,210)      # 输入框边框色
BLACK = (0,0,0)       # 输入框文字色

font_path='MSYH.TTC'
font = pygame.freetype.Font(font_path, 28)
large_font = pygame.freetype.Font(font_path, 48)
#默认玩家姓名
player1_name="玩家1"
player2_name="玩家2"
player3_name="玩家3"
#定义牌值，牌型
def getjokervalue(card):
    if card[0]=="red":
        return 20
    else:
        return 19
joker_value=getjokervalue("red_joker")        
rank_value={
    "3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
    "J":11,"Q":12,"K":13,"A":14,"2":15,"王":20
}
suit_value={
    "梅花":1,"方块":2,"红心":3,"黑桃":4,'小':5,'大':6, #大小王的比较
}
cardtype={
    '单张':1,'对子':2,'三不带牌':3,'三带1':4,'三带2':5,'顺子':6,'连对':7,'四带二':8,'飞机不带牌':9,'飞机各带1张':10,'飞机各带2张':11,'三架飞机不带牌':12,'三架飞机各带1':13,'三架飞机各带2':14,'炸弹':100,'王炸':200
}
cardtype_value=0 #0代表无牌型，不能出牌
def getcardtype(cards:list):
    
    global cardtype_value
    #判断是否是顺子的函数
    def is_straight():
        for i in range(len(cards)-1):
            if rank_value[cards[i][1]]!=rank_value[cards[i+1][1]]+1:
                return False
        return True
    def is_consecutive_pairs(len): #判断是否是连对的函数
        if len%2!=0:
            return False #连对必须是偶数张
        for i in range(len//2):
            n=i*2
            #首先判断是对子组合
            if rank_value[cards[n][1]]!=rank_value[cards[n+1][1]]:
                return False
            if n==len-2: #防止超过索引范围
                break
            #判断对子是否连续
            elif rank_value[cards[n][1]]!=rank_value[cards[n+2][1]]+1:
                return False
           
        return True
    def is_airplane(): #判断是否是飞机的函数，如果是，返回飞机的类型，如果不是，返回False
      cardvalues=[rank_value[card[1]] for card in cards]
      count=Counter[int](cardvalues) #统计每个牌值出现的次数，这是一个字典
      airplane_list=[(k,v) for k,v in count.items() if v==3] #将字典的值转换为列表，只保留出现次数等于3的牌值和次数，也就是飞机的牌值和次数
      airplane_4times_list=[(k,v) for k,v in count.items() if v==4] #将字典的值转换为列表，只保留出现次数等于4的牌值和次数
      airplane_2times_list=[(k,v) for k,v in count.items() if v==2] #将字典的值转换为列表，只保留出现次数等于2的牌值和次数
      airplane_list.sort(key=lambda x:x[0],reverse=True) #对列表排序，方便后续判断,按牌值从大到小排序
      if len(cards)%3!=0 and len(cards)%2!=0: #如果牌的数量不是3的倍数且不是2的倍数，那么不是飞机
          return False
      if len(airplane_4times_list)!=0: #如果出现了4个，那么不是飞机
          return False
      if len(airplane_list)<2: #如果飞机的牌值出现次数小于2次，那么不是飞机
          return False
      elif len(airplane_list)==2: #如果飞机的牌值出现次数等于2次
          if airplane_list[0][0]==airplane_list[1][0]+1: #如果飞机的牌值相差1
            if len(cards)==6:
                return cardtype['飞机不带牌']
            elif len(cards)==8:
                print('飞机各带1张')
                return cardtype['飞机各带1张']
            elif len(cards)==10:
               if len(airplane_2times_list)==2:
                print('飞机各带2张')
                return cardtype['飞机各带2张']
          else:
              return False
      elif len(airplane_list)==3: #如果飞机的牌值出现次数等于3次,那么可能有三架飞机
          if airplane_list[0][0]==airplane_list[1][0]+1==airplane_list[2][0]+2: #如果飞机的牌值相差1
            if len(cards)==9:
                return cardtype['三架飞机不带牌']
            elif len(cards)==12:
                print('三架飞机各带1张')
                return cardtype['三架飞机各带1']
            elif len(cards)==14:
                print('三架飞机各带2张')
                if len(airplane_2times_list)==3:
                    return cardtype['三架飞机各带2']
                else:
                    return False
          else:
              return False
              #先暂定最多三架飞机吧。
      
     

    #函数主体：
    #先把cards按牌值从大到小排序，方便后续判断
    cards.sort(key=lambda x:rank_value[x[1]],reverse=True)
    if len(cards)==1:
        cardtype_value=cardtype['单张']
    elif len(cards)==2:
        if cards[0][1]==cards[1][1] and cards[0][1]!='王':
            cardtype_value=cardtype['对子']
        elif cards[0][1]=='王' and cards[1][1]=='王':
            cardtype_value=cardtype['王炸']
        else:
            cardtype_value=0
    elif len(cards)==3:
        if cards[0][1]==cards[1][1]==cards[2][1]:
            cardtype_value=cardtype['三不带牌']
        else:
            cardtype_value=0
    elif len(cards)==4:
        if cards[0][1]==cards[1][1]==cards[2][1]==cards[3][1]:
            cardtype_value=cardtype['炸弹']
        elif cards[0][1]==cards[1][1]==cards[2][1] or cards[0][1]==cards[1][1]==cards[3][1] or cards[0][1]==cards[2][1]==cards[3][1] or cards[1][1]==cards[3][1]==cards[2][1]:
            cardtype_value=cardtype['三带1']
        else:
            cardtype_value=0
    elif len(cards)==5:
        #先判断是否是顺子,5张只能是顺子或三带二

        if is_straight():
            cardtype_value=cardtype['顺子']
        elif cards[0][1]==cards[1][1] and cards[2][1]==cards[3][1]==cards[4][1] or cards[0][1]==cards[1][1] == cards[2][1] and cards[3][1]==cards[4][1]:
            cardtype_value=cardtype['三带二']
        else:
            cardtype_value=0
    elif len(cards) >=6:
      if is_straight():
            cardtype_value=cardtype['顺子']
       
      if is_consecutive_pairs(len(cards)):
            cardtype_value=cardtype['连对']

        else:
            cardtype_value=0
        for i in range(4):
            if rank_value[cards[i][1]]!=rank_value[cards[i+1][1]]-2:
                cardtype_value=0
                break
        if is_consecutive_pairs:
            cardtype_value=cardtype['连对']
        else:
            cardtype_value=0
def start_game():
    deck=d.DeckwithJoker()
    print(deck.cards)
start_game()    