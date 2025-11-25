#1.新建牌堆
#2.定义牌型，包括单张，对子，三带1，三带2，顺子，连对，四带二，炸弹 同牌形可以压过
#3.定义牌值的大小，3最小，joker最大，2第二
#4.游戏规则：三人游戏，轮流发牌，剩3张时，随机选一名玩家当地主。获得地主牌。地主先出。
#5.所有玩家的牌按牌值从大到小排序。
#6.分数系统，每人初始100分，地主赢一局加2分，输一局减2分。
#7.AI出牌逻辑：自己出优先出单张。别人出，有大牌就压。
#可视化：牌桌上显示当前在出的牌，玩家手中看到自己的牌，叠放。其他人的牌只显示背面。显示：开始按钮，下一局按钮。分数，出版记录。
# from termios import FF0
from typing import Any
import pygame
import deck as d
import pygame.freetype
from collections import Counter
from itertools import combinations
from collections.abc import Iterable 
from itertools import product #从itertools导入product函数，用来生成笛卡尔积
import random
import deck as d
import sys
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
# #默认玩家姓名
# player1_name="玩家1"
# player2_name="玩家2"
# player3_name="玩家3"
#定义牌值，牌型
def getjokervalue(card):
    if card[0]=="red":
        return 20
    else:
        return 19
joker_value=getjokervalue("red_joker")        
rank_value={
    "3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
    "J":11,"Q":12,"K":13,"A":14,"2":16,"王":20
}
suit_value={
    "梅花":1,"方块":2,"红心":3,"黑桃":4,'小':5,'大':6, #大小王的比较
}
cardtype={
    '单张':'单张','对子':'对子','三不带牌':'三不带牌','三带1':'三带1','三带2':'三带2','顺子':'顺子','连对':'连对','四带二':'四带二','八带四':'八带四','飞机不带牌':'飞机不带牌','飞机各带1张':'飞机各带1张','飞机各带2张':'飞机各带2张','三架飞机不带牌':'三架飞机不带牌','三架飞机各带1':'三架飞机各带1','三架飞机各带2':'三架飞机各带2','炸弹':100,'王炸':200
}




#工具函数，判断牌型
def getcardtype(cards:list): #定义牌形识别函数
    #定义工具函数
    
    #判断是否是顺子的函数
    def is_straight():
        for i in range(len(cards)-1):
            if rank_value[cards[i][1]]!=rank_value[cards[i+1][1]]+1:
                return False
        return True
    def is_consecutive_pairs(): #判断是否是连对的函数
        if len(cards)%2!=0:
            return False #连对必须是偶数张
        for i in range(len(cards)//2):
            n=i*2
            #首先判断是对子组合
            if rank_value[cards[n][1]]!=rank_value[cards[n+1][1]]:
                return False
            if n==len(cards)-2: #防止超过索引范围
                break
            #判断对子是否连续
            elif rank_value[cards[n][1]]!=rank_value[cards[n+2][1]]+1:
                return False
        return True
    def is_quadruple(): #判断是否是四带2的函数，如果是，返回四带2的类型，如果不是，返回False
        if len(cards)%6!=0:
            return False #四带2必须是6的倍数
        count=Counter([card[1] for card in cards]) #统计每个牌值出现的次数，这是一个字典
        #判断是否有4个牌值出现次数等于4次
        list4=[k for k,v in count.items() if v==4]
        list4.sort(reverse=True) #将字典的值转换为列表，只保留出现次数等于4的牌值
        if len(list4)==1 and len(cards)==6:
            return cardtype['四带二']
        if len(list4)==2 and list4[0]==list4[1]+1 and len(cards)==12:
            return cardtype['八带四']
       
         
       
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
                # print('飞机各带1张')
                return cardtype['飞机各带1张']
            elif len(cards)==10:
               if len(airplane_2times_list)==2:
                # print('飞机各带2张')
                return cardtype['飞机各带2张']
          else:
              return False
      elif len(airplane_list)==3: #如果飞机的牌值出现次数等于3次,那么可能有三架飞机
          if airplane_list[0][0]==airplane_list[1][0]+1==airplane_list[2][0]+2: #如果飞机的牌值相差1
            if len(cards)==9:
                return cardtype['三架飞机不带牌']
            elif len(cards)==12:
                # print('三架飞机各带1张')
                return cardtype['三架飞机各带1']
            elif len(cards)==14:
                # print('三架飞机各带2张')
                if len(airplane_2times_list)==3:
                    return cardtype['三架飞机各带2']
                else:
                    return False
          else:
              return False
              #先暂定最多三架飞机吧。
     #判断前者能否压后者牌的函数 
    

    #函数主体：
    #先把cards按牌值从大到小排序，方便后续判断
    cards.sort(key=lambda x:rank_value[x[1]],reverse=True)
    if len(cards)==1:
        return cardtype['单张']
    elif len(cards)==2:
        if cards[0][1]==cards[1][1] and cards[0][1]!='王':
            return cardtype['对子']
        elif cards[0][1]=='王' and cards[1][1]=='王':
            return cardtype['王炸']
        else:
            return 0
    elif len(cards)==3:
        if cards[0][1]==cards[1][1]==cards[2][1]:
            return cardtype['三不带牌']
        else:
            return 0
    elif len(cards)==4:
        if cards[0][1]==cards[1][1]==cards[2][1]==cards[3][1]:
            return cardtype['炸弹']
        elif cards[0][1]==cards[1][1]==cards[2][1] or cards[0][1]==cards[1][1]==cards[3][1] or cards[0][1]==cards[2][1]==cards[3][1] or cards[1][1]==cards[3][1]==cards[2][1]:
            return cardtype['三带1']
        else:
            return 0
    elif len(cards)==5:
        #先判断是否是顺子,5张只能是顺子或三带二

        if is_straight():
            return cardtype['顺子']
        elif cards[0][1]==cards[1][1] and cards[2][1]==cards[3][1]==cards[4][1] or cards[0][1]==cards[1][1] == cards[2][1] and cards[3][1]==cards[4][1]:
            return cardtype['三带2']
        else:
            return 0
    elif len(cards) >=6: #6张以上的牌，只能是顺子、连对、飞机或四带二
        if is_straight():
            return cardtype['顺子']
         
        if is_consecutive_pairs():
            return cardtype['连对']
        if is_airplane():
            return is_airplane() #如果是飞机，返回飞机的类型
        elif is_quadruple(): #如果是四带二，返回四带二
            return is_quadruple()
        else:
            return 0 #如果不是以上的牌型，那么就是错误的牌型
          
        
def can_beat(current_cards:list,last_played_cards:list=None) -> bool:
        if last_played_cards==None: #如果是第一个回合，那么可以出任意牌
            return True
        cur=getcardtype(current_cards)
        last=getcardtype(last_played_cards)
        if cur==200: #如果是王炸，绝对比他大
            return True
        if last==200: #如果对方是王炸，绝对比他小
            return False
        if cur==100 and last!=100: #如果是炸弹，绝对比他大
            return True
        #同级比较，除去以上情况。
        if cur!=last: #牌型不同无法压
            return False
        if cur==last: #如果牌型相同，那么比较牌值
            if cur=='单张' and rank_value[current_cards[0][1]]==rank_value[last_played_cards[0][1]]==20:
                if current_cards[0][0]=='大': #如果是大小王比较
                    return True
                return False
            if cur=='单张' and rank_value[current_cards[0][1]]!=rank_value[last_played_cards[0][1]]:
                return rank_value[current_cards[0][1]]>rank_value[last_played_cards[0][1]]
            if cur=='对子': 
                return rank_value[current_cards[0][1]]>rank_value[last_played_cards[0][1]]
            if cur=='三不带牌':
                return rank_value[current_cards[0][1]]>rank_value[last_played_cards[0][1]]
            if cur=='三带1':
                count1=Counter([card[1] for card in current_cards]) #数每个值，返回字典
                count2=Counter([card[1] for card in last_played_cards ])
                #解包字典，取出最大的牌值
                max1=count1.most_common(1)[0][0]
                max2=count2.most_common(1)[0][0]
                return rank_value[max1]>rank_value[max2]
            if cur=='三带2' or cur=='四带2' or cur=='八带四' or cur=='飞机不带牌' or cur=='飞机各带1张' or cur=='飞机各带2张' or cur=='三架飞机不带牌' or cur=='三架飞机各带2' or cur==100:
                count1=Counter([card[1] for card in current_cards]) #数每个值，返回字典
                count2=Counter([card[1] for card in last_played_cards ])
                #解包字典，取出最大的牌值
                max1=count1.most_common(1)[0][0]
                max2=count2.most_common(1)[0][0]
                return rank_value[max1]>rank_value[max2]
            if cur=='顺子' or cur=='连对':
               if len(current_cards)!=len(last_played_cards):
                    return False
               else:
                    current_cards.sort(key=lambda x:rank_value[x[1]],reverse=True)
                    max1=current_cards[0][1] 
                    last_played_cards.sort(key=lambda x:rank_value[x[1]],reverse=True)
                    max2=last_played_cards[0][1]
                    return rank_value[max1]>rank_value[max2]

       

def reset_game(game_status:dict):
    deck=d.DeckwithJoker() #带小王和大王新建一幅牌
    deck.shuffle() #洗牌
    player1,player2,player3=game_status['playerlist']
    #重置游戏状态
    game_status['middle_cards']=[]
    game_status['landlord']=None
    game_status['last_played_cards']=None #上一个回合出的牌
    game_status['turn']=None #当前回合的玩家
    game_status['winner']=None #赢家
      #发牌，每人发17张牌，剩3张
    player1.in_hand=deck.deal(17)
    player2.in_hand=deck.deal(17)
    player3.in_hand=deck.deal(17)
   
    def call_landlord(): #返回地主的名字
        player1_call='y'#测试
        # player1_call=input('玩家1是否要叫地主？(y/n)')
        if player1_call=='y':
            player1.in_hand.extend(game_status['middle_cards'])
            print('地主牌为：',game_status['middle_cards'])
            player1.landlord=True         
            game_status['turn']=player1 #切换到当前回合的玩家。用这个来确定谁出牌
            return player1
        player2_call=input('玩家2是否要叫地主？(y/n)')    
        if player2_call=='y':
            player2.in_hand.extend(game_status['middle_cards'])
            print('地主牌为：',game_status['middle_cards'])         
            player2.landlord=True
            player2.start_turn() #玩家2出牌回合
            game_status['turn']=player2 #切换到当前回合的玩家
            return player2  
        player3_call=input('玩家3是否要叫地主？(y/n)')
        if player3_call=='y':
            player3.in_hand.extend(game_status['middle_cards'])
            print('地主牌为：',game_status['middle_cards'])
            player3.landlord=True
            player3.start_turn() #玩家3出牌回合
            game_status['turn']=player3 #切换到当前回合的玩家
            return player3
        else:
            print('玩家1、2、3都不叫地主，随机选择地主')
        import random
        landlord=random.randint(1,3)
        if landlord==1:
            player1.in_hand.extend(game_status['middle_cards'])
            player1.landlord=True
            
            game_status['turn']=player1 #切换到当前回合的玩家
            
            print('玩家1成为地主')
        elif landlord==2:
            player2.in_hand.extend(game_status['middle_cards'])
            player2.landlord=True
            
            game_status['turn']=player2 #切换到当前回合的玩家
            
            print('玩家2成为地主')
        elif landlord==3:
            player3.in_hand.extend(game_status['middle_cards'])
            player3.landlord=True
            
            game_status['turn']=player3 #切换到当前回合的玩家
            
            print('玩家3成为地主')
        
    player1.ai=False
    game_status['middle_cards']=deck.deal(3) #中间3张牌
    game_status['landlord']=None #初始时，没有地主
    game_status['last_played_cards']=None #上一个回合出牌的牌
    #叫地主
    game_status['landlord']=call_landlord() #该函数轮流选地主，产生地主
   
    game_status['landlord'].start_turn() #地主出牌回合
    # print(game_status['turn'],'这是有效的')
    #地主出完了，下一个回合
    #有玩家手上没牌了，就结束
    while not game_status['winner']: #如果赢家为空，就继续循环
        game_status['turn']=game_status['playerlist'][(game_status['playerlist'].index(game_status['turn'])+1)%3] #切换到下一个回合的玩家
        game_status['turn'].start_turn() #切换到下一个回合的玩家出牌回合
    for winner in game_status['winner']:

        print(winner.id,'是赢家')    
    for player in game_status['playerlist']:
        print(f'{player.id}当前分数为：{player.score}')
#游戏主体       
def start_game():
    class Player: #把玩家的属性和方法封装在一个类中
        def __init__(self,id,ai=True):
            self.id=id
            self.in_hand=[] #玩家手中的牌
            self.playing_cards=[] #正在选的牌，准备出
            self.played_cards=[] #刚刚出的牌,已经出过的牌，在牌桌上
            self.landlord=False #是否是地主,默认不是
            self.ai=ai #是否是AI玩家,默认是
            self.score=100 #玩家的分数，默认100
        def pass_turn(self): #过牌
            
            print(f'{self.id}选择PASS')
        
        #回合开始，切换到出牌回合
        #判断自己选的牌是否比last_played_cards大
        def possible_cards(self) -> list: #可以出的牌，不用传参，参数是固定的，自己的牌和牌桌上的牌,可以直接调用
        #按照类型筛选出可以出的牌，要针对对方打出的牌的类型
            last=game_status['last_played_cards']
            #重构一下，暴力枚举太慢了。
            #筛选自己的所有牌形，分类看。多张牌的用counter
            if last==None:

            #1.单张
                possible_single=[[card] for card in self.in_hand]
                possible_single.sort(key=lambda x:rank_value[x[0][1]]) #根据牌值从大到小排序
            
            #2.对子
                count=Counter([card[1] for card in self.in_hand]) #数每个值，返回字典，键是值，值是出现次数，这个后面还可以用
                pairlistrank=[k for k,v in count.items() if v>=2 and k!='王'] #筛选出出现次数大于等于2的牌值,排除王
                #根据牌值从手牌中筛选出对子
                possible_pairs=[]
                for rank in pairlistrank:
                    cards_of_rank=[card for card in self.in_hand if card[1]==rank] #从手牌中筛选出牌值为rank的牌，比如rank为2，那么就筛选出所有不同花色的2
                    #从牌值为rank的牌中筛选出对子
                    for pair in combinations(cards_of_rank, 2):
                            possible_pairs.append(list(pair)) #每个Pair是单独牌型，需转化为列表
                    possible_pairs.sort(key=lambda x:rank_value[x[0][1]]) #根据牌值从大到小排序
            #3.三张牌，要考虑，带1或带2。

                triplelistrank=[k for k,v in count.items() if v>=3] #筛选出出现次数大于等于3的牌值
                possible_triple=[]
                possible_triple_with_one=[]
                possible_triple_with_pair=[]

                for rank in triplelistrank: #根据牌值遍历
                    cards_of_rank=[card for card in self.in_hand if card[1]==rank] #从手牌中筛选出牌值为rank的牌，比如rank为2，那么就筛选出所有不同花色的2
                    other_cards=[card for card in self.in_hand if card[1]!=rank] #从手牌中筛选出其他牌值的牌,只要不一样都能带
                    count_other=Counter([card[1] for card in other_cards]) #数其他牌值，返回字典，键是值，值是出现次数
                    pair_other_rank=[k for k,v in count_other.items() if v>=2] #筛选出其他牌值中出现次数大于等于2的牌值

                    # other_pair=[card for card in other_cards if card[1] in pair_other_rank] #从其他牌中筛选出对子

                    for triple in combinations(cards_of_rank, 3): #从牌值为rank的牌中筛选出三不带牌
                            possible_triple.append(list(triple)) #每个Triple是单独牌型，需转化为列表
                            for one in other_cards:
                                possible_triple_with_one.append(list(triple)+[one]) #三带1
                            for pair_rank in pair_other_rank:
                                cards_of_rank_pair=[card for card in other_cards if card[1]==pair_rank] #从其他牌中筛选出牌值为pair_rank的牌，比如pair_rank为2，那么就筛选出所有不同花色的2
                                for pair in combinations(cards_of_rank_pair, 2):
                                    possible_triple_with_pair.append(list(triple)+list(pair)) #三带2

            #4.炸弹
                possible_bomb=[]
                bomb_rank=[k for k,v in count.items() if v==4] #筛选出出现次数等于4的牌值
                for rank in bomb_rank:
                    cards_of_rank_bomb=[card for card in self.in_hand if card[1] == rank] #从手牌中筛选出牌值为炸弹的牌
                    possible_bomb.append(cards_of_rank_bomb) #每个炸弹是单独牌型，需转化为列表

            #5.顺子
                possible_straight=[]
                #挑选出所有的牌值，然后排序，去重
                ranklist=sorted(set([card[1] for card in self.in_hand if rank_value[card[1]]<=14]),key=lambda x:rank_value[x]) #从手牌中筛选出所有的牌值，然后排序，去重
                #顺子的张数为5-12张，3-A，顺子的特点是最后一张减第一张等于len-1
                if len(ranklist)>=5:
                    for length in range(5,13):

                        for i in range(len(ranklist)-length+1): #从牌值列表中筛选出顺子
                            if rank_value[ranklist[i+length-1]]-rank_value[ranklist[i]]==length-1: #如果最后一张减第一张等于length-1，那么就是顺子
                                straight_cards=[] #这是个中转列表，用来存储当前顺子的具体花色牌
                                for rank in ranklist[i:i+length]: #这个切片就是当前顺子的牌值列表，比如[3,4,5,6,7]
                                    cards_of_rank=[card for card in self.in_hand if card[1]==rank] #从手牌中筛选出牌值为rank的牌，比如rank为2，那么就筛选出所有不同花色的2
                                    straight_cards.append(cards_of_rank) #每个元素为一个列表，列表中为当前牌值的所有不同花色牌

                                cards=[list(card) for card in product(*straight_cards)]
                                #* straight_cards是一个列表，列表中每个元素为一个列表，列表中为当前牌值的所有不同花色牌
                                #比如straight_cards为[[3,3,3,3],[4,4,4,4],[5,5,5,5],[6,6,6,6],[7,7,7,7]]，那么product(*straight_cards)就是所有不同花色的顺子，比如(3,4,5,6,7)
                                #每个元素为一个元组，元组中为当前顺子的具体牌，比如(3,4,5,6,7)，需要将每个元组转化为列表，才能加入到possible_straight中
                                possible_straight.extend(cards) #这里上面已经是列表了，不能重复嵌套了。

            #6.连对
                possible_chain_pair=[]
                # 前面已经有pairlistrank=[k for k,v in count.items() if v>=2 and v!='王'] #筛选出出现次数大于等于2的牌值，排除王
                #挑选出所有对子的牌值，然后排序
                pairlistrank_inorder=sorted([rank for rank in pairlistrank if rank_value[rank]<=14],key=lambda x:rank_value[x]) #从手牌中筛选出所有的对子牌值，然后排序
                #连对的单张数为3-12张（实际张数*2），3-A，连对的特点是最后一张减第一张等于len-1，由于最多20张，也就是最多10对连对，最少3对

                if len(pairlistrank_inorder)>=3:  #如果对子数大于等于3，那么就可能有连对
                    for length in range(3,11): #连对最多10对，最少3对

                        for i in range(len(pairlistrank_inorder)-length+1): #从牌值列表中筛选出连对
                            if rank_value[pairlistrank_inorder[i+length-1]]-rank_value[pairlistrank_inorder[i]]==length-1: #如果最后一张减第一张等于length-1，那么就是连对
                                chain_pair_cards=[] #这是个中转列表，用来存储当前连对的具体花色牌
                                for rank in pairlistrank_inorder[i:i+length]: #这个切片就是当前连对的牌值列表，比如[3,4,5,6,7]
                                   cards_of_rank=[card for card in self.in_hand if card[1]==rank] #从手牌中筛选出牌值为rank的牌，比如rank为2，那么就筛选出所有不同花色的2
                                   paircards=combinations(cards_of_rank,2) #从当前牌值的所有不同花色牌中筛选出对子
                                   chain_pair_cards.append(list(paircards)) #每个元素为一个列表，列表中为当前牌值的所有不同花色对子牌
                                cards=[list(sum(card,())) for card in product(*chain_pair_cards)] #sum可以去掉一层嵌套，但必须是同类型的嵌套，这里是元组
                                #* chain_pair_cards是一个列表，列表中每个元素为一个列表，列表中为当前牌值的所有不同花色对子牌
                                #比如chain_pair_cards为[[[3,3],[3,4],[3,5],[3,6],[3,7]],[[4,4],[4,5],[4,6],[4,7]],[[5,5],[5,6],[5,7]],[[6,6],[6,7]],[[7,7]]]，那么product(*chain_pair_cards)就是所有不同花色的连对，比如(3,3,4,4,5,5)
                                #每个元素为一个元组，元组中为当前连对的具体牌，比如(3,3,4,4,5,5)，需要将每个元组转化为列表，才能加入到possible_chain_pair中
                                possible_chain_pair.extend(cards) 
            #7.飞机
                #triplelistrank=[k for k,v in count.items() if v>=3] #筛选出出现次数大于等于3的牌值 前面已经定义了
                #挑选出所有三张的牌值，然后排序
                triplelistrank_inorder=sorted([rank for rank in triplelistrank if rank_value[rank]<=14],key=lambda x:rank_value[x]) #从手牌中筛选出所有的三张牌值，然后排序，从小到大
                possible_airplane=[]
                #飞机需要两组以上的三张牌值。最多6组

                if len(triplelistrank_inorder)>=2: #如果三张一样的牌个数大于等于2，那么就可能有飞机
                    for length in range(2,7): #飞机最多6组，最少2组,length为飞机的架数

                        for i in range(len(triplelistrank_inorder)-length+1): #从牌值列表中筛选出飞机
                            if rank_value[triplelistrank_inorder[i+length-1]]-rank_value[triplelistrank_inorder[i]]==length-1: #如果最后一张减第一张等于length-1，那么就是飞机
                                airplane_cards=[] #这是个中转列表，用来存储当前飞机的具体花色牌
                                for rank in triplelistrank_inorder[i:i+length]: #这个切片就是当前飞机的牌值列表，比如[3,4,5,6,7]
                                    cards_of_rank=[card for card in self.in_hand if card[1]==rank] #从手牌中筛选出牌值为rank的牌，比如rank为2，那么就筛选出所有不同花色的2
                                    triplecards=combinations(cards_of_rank,3) #从当前牌值的所有不同花色牌中筛选出三张牌
                                    airplane_cards.append(list(triplecards)) #每个元素为一个列表，列表中为当前牌值的所有不同花色的三连牌
                                airplane_with_nocard=[list(sum(card,())) for card in product(*airplane_cards)] #这是飞机不带牌的牌组，用product可以得到所有不同花色的飞机，sum可以去掉一层嵌套
                                #* airplane_cards是一个列表，列表中每个元素为一个列表，列表中为当前牌值的所有不同花色的三连牌
                                #比如airplane_cards为[[[3,3,3],[3,3,4],[3,3,5],[3,3,6],[3,3,7]],[[4,4,4],[4,4,5],[4,4,6],[4,4,7]],[[5,5,5],[5,5,6],[5,5,7]],[[6,6,6],[6,6,7]],[[7,7,7]]]，那么product(*airplane_cards)就是所有不同花色的飞机，比如(3,3,3,4,4,4,5,5,5,6,6,6,7,7,7)

                                possible_airplane.extend(airplane_with_nocard) #将飞机不带牌的牌加入到列表中

                                #飞机带1张牌
                                airplane_with_one=[]
                                #筛选带牌池，需要和飞机牌不一样。
                                main_rank=triplelistrank_inorder[i:i+length]
                                band_pool=[card for card in self.in_hand if card[1] not in main_rank] #带牌池就是手牌中减去飞机主牌的所有不同花色的牌
                                if len(band_pool)>=length: #如果带牌池中的牌数大于等于飞机架数，那么就可能有飞机带1张牌，如果小于就不够了
                                    band_combo=list(combinations(band_pool,length)) #从带牌池中选出length张牌，每个元素为一个列表，列表中为当前带牌池中的牌
                                    for triple in airplane_with_nocard: #每个大飞机带length张牌
                                        for extra_cards in band_combo: #对带牌池中的每一张牌，都和当前飞机不带牌的牌组合起来
                                            airplane_with_one.append(triple+list(extra_cards)) #将当前飞机不带牌的牌和当前带牌池中的牌组合起来，加入到飞机带1张牌的列表中

                                    possible_airplane.extend(airplane_with_one) #将飞机带1张牌的牌加入到列表中
                                #飞机带2张牌
                                airplane_with_two=[]
                                #筛选带牌池，需要和飞机牌不一样。
                                #main_rank=triplelistrank_inorder[i:i+length]，这个已经定义了，所以这里不需要再定义一次 
                                band_pool=[card for card in self.in_hand if card[1] not in main_rank] #带牌池就是手牌中减去飞机主牌的所有不同花色的牌
                                #再数里面的对子
                                countbandpair=Counter([card[1] for card in band_pool]) #统计带牌池中的所有牌值的出现次数

                                band_pair_pool=[k for k,v in countbandpair.items() if v>=2] #筛选出带牌池中的对子牌值，这是一个列表  
                                if len(band_pair_pool)>=length: #如果带牌池中的对子牌数大于等于飞机架数，那么就可能有飞机带一对，如果小于就不够了
                                    pair_card_candicate=[] #这个列表用来存候选的对子牌
                                    for pair in band_pair_pool: #对带牌池中的每一张对子牌，都至少有2张或以上，需要列出所有不同花色的对子牌
                                        cards_of_rank=[card for card in band_pool if card[1]==pair] #从带牌池中筛选出牌值为pair的牌，比如pair为2，那么就筛选出所有不同花色的2
                                        combo=list(combinations(cards_of_rank,2)) #从当前对子牌值的所有不同花色的对子牌中筛选出2张牌.输出例子，假设2有3张：[（红桃2，黑桃2），(红桃2，梅花2),(黑桃2，梅花2)]
                                        #combo是一个列表，列表中每个元素为一个元组，元组中为当前对子牌值的所有不同花色的对子牌
                                        pair_card_candicate.append(combo) #将当前对子牌值的所有不同花色的对子牌加入到候选的对子牌列表中
                                    #从候选的对子牌列表中筛选出length组对子牌，每个元素为一个列表，列表中为当前带牌池中的对子牌，用combinations
                                    band_pair_cards=[]
                                    for band_pair_card in combinations(pair_card_candicate,length): #所有对子之间的组合，还需要遍历每个组合
                                        band_pair_combo=list(product(*band_pair_card)) #这个是length对对子牌的所有不同花色的组合
                                        band_pair_cards+=[list(sum(pair,())) for pair in band_pair_combo] #sum把（红桃2，黑桃2），(红桃3，梅花3)这种元组展开成列表：[红桃2，黑桃2，红桃3，梅花3]


                                    for triple in airplane_with_nocard: #每个大飞机带length个对子
                                        for band_pair in band_pair_cards: #对带牌池中的每一组对子牌，都和当前飞机不带牌的牌组合起来
                                            airplane_with_two.append(triple+band_pair) #将当前飞机不带牌的牌和当前带牌池中的对子牌组合起来，加入到飞机带2张牌的列表中
                                    possible_airplane.extend(airplane_with_two) #将飞机带2张牌的牌加入到列表中
                                #    

            #8.王炸
                possible_joker_bomb=[card for card in self.in_hand if card[1]=='王']
                if len(possible_joker_bomb)==2: #如果王炸牌数等于2，那么就是王炸
                    possible_joker_bomb=[possible_joker_bomb] #将王炸牌加入到列表中
                else: #如果王炸牌数不等于2，那么不是王炸
                    possible_joker_bomb=[]

            #9.四带2，可带散牌或对子
                possible_quad_with_two=[]
                # count=Counter([card[1] for card in self.in_hand]) #数每个值，返回字典，键是值，值是出现次数，这个后面还可以用
                quadlistrank=[k for k,v in count.items() if v==4] #筛选出出现次数等于4的牌值
                for rank in quadlistrank: #对每个四带主牌，都需要筛选出带牌池
                    cards_of_rank=[card for card in self.in_hand if card[1]==rank] #从手牌中筛选出四带主牌的所有不同花色的牌
                    band_pool=[card for card in self.in_hand if card[1] !=rank] #带牌池就是手牌中减去四带主牌的所有不同花色的牌
                    combo=list(combinations(band_pool,2)) #从带牌池中筛选出2张牌.输出例子，假设2有3张：[（红桃2，黑桃2），(红桃2，梅花2),(黑桃2，梅花2)]
                    for card in combo: #对每个带牌池中的2张牌，都需要和四带主牌组合起来
                        possible_quad_with_two.append(cards_of_rank+list(card)) #将四带主牌和当前带牌池中的2张牌组合起来，加入到列表中


                return possible_single+possible_pairs+possible_triple+possible_triple_with_one+possible_triple_with_pair+possible_airplane+possible_bomb+possible_straight+possible_chain_pair+possible_joker_bomb+possible_quad_with_two
            
           
           
           
           #不是自己回合，要考虑对方打的牌
            #如果对方是王炸,出不了牌
           
            if getcardtype(last)==200:
                return []
      
            length=len(last)
            if length==4: #如果长度4张牌，已经考虑到炸弹的情况了，只需要加上王炸的情况
                combo4=combinations(self.in_hand,length) #从当前牌中选出4张牌,四张牌会组成一个元组，每张又是元组
                #筛选出炸弹
                combo=[list[tuple](el) for el in combo4 if can_beat(list(el),last)] #每个元素是元组，先转化成列表。这是含有比对方大的炸弹牌的列表。combinations是一个迭代器，是一次性的。combinations被迭代返回的每个元素是元组，所以要转化成列表。
                jokercombo=[list[tuple](el) for el in combinations(self.in_hand,2) if can_beat(list(el),last)] #两张牌能比他大的就是王炸
                return combo+jokercombo #如果没有可以出的，那么返回空列表
            else:    
                combo=combinations(self.in_hand,length) #从当前牌中选出length张牌,length张牌会组成一个元组，每张又是元组
        
                combo=[list[tuple](el) for el in combo if can_beat(list(el),last)] #每个元素是元组，先转化成列表。
                #加上炸弹和王炸
                combobomb=[list[tuple](el) for el in combinations(self.in_hand,4) if can_beat(list(el),last)] #每个元素是元组，先转化成列表。这是含有比对方大的炸弹牌的列表。combinations是一个迭代器，是一次性的。combinations被迭代返回的每个元素是元组，所以要转化成列表。
                jokercombo=[list[tuple](el) for el in combinations(self.in_hand,2) if can_beat(list(el),last)] #两张牌能比他大的就是王炸
                combobomb.sort(key=lambda x:rank_value[x[0][1]]) #根据牌值从大到小排序

                return combo+combobomb+jokercombo #返回可以出的牌,这是个列表，每个元素是列表，是可以出的牌。    

        def start_turn(self): #开始自己的回合,并选择要出的牌
           
          
            if self.played_cards==game_status['last_played_cards']: #如果自己出的牌和上一个回合出的牌相同，说明是自己打的牌。
                game_status['last_played_cards']=None   # 自己重新出任意牌       
            
            # print(f'玩家{self.id}请选择要出的牌，')
            #先模拟随便出牌，筛选出可以出的牌
            possible_cards=self.possible_cards()
            print(f'{self.id}可以出的牌为：')
            possible_cards.sort(key=lambda x:len(x)) #按牌型长度排序
            if possible_cards:    
                for i in range(len(possible_cards)):
                    possible_cards[i].sort(key=lambda x:rank_value[x[1]]) #按牌值排序
                    print(f'{i+1}',possible_cards[i]) #按牌值排序
            else:
                print('没有可以出的牌。')
            if self.ai == False:
                if possible_cards:
                    try:
                        index=int(input('请选择要出的牌，输入牌型的序号'))
                    except ValueError:
                        print('输入错误，默认出第一张牌。')
                        index=1
                    if index > len(possible_cards):
                        print('输入错误，默认出最后一个牌形。')
                        index=0
                    self.playing_cards=possible_cards[index-1] 
                    self.out_card(self.playing_cards)
                    game_status['last_played_cards']=self.playing_cards #记录刚刚出的牌
                    print(f'{self.id}出的牌为：',self.playing_cards)
                    print(f'{self.id}打出的牌形为：',getcardtype(self.playing_cards))
                    print(f'{self.id}当前手上的牌为：',self.in_hand)
                    

                else:
                    print('没有可以出的牌。')
                    self.pass_turn()
                    return
                
            else:
                if game_status['last_played_cards']!=None:
                    #先设定玩家随机要不起，后续再改逻辑
                    if random.randint(0,1)==0:
                        self.pass_turn()
                        return
                    if possible_cards:
                        self.playing_cards=possible_cards[-1] #选择出第一个牌型
                        self.out_card(self.playing_cards)
                        game_status['last_played_cards']=self.playing_cards #记录刚刚出的牌
                        print(f'{self.id}出的牌为：',self.playing_cards)
                        print(f'{self.id}打出的牌形为：',getcardtype(self.playing_cards))

                    else:
                        self.pass_turn()
                        return
                else:
                     
                        self.playing_cards=possible_cards[-1] #选择出第一个牌型
                        self.out_card(self.playing_cards)
                        game_status['last_played_cards']=self.playing_cards #记录刚刚出的牌
                        print(f'{self.id}出的牌为：',self.playing_cards)
                        print(f'{self.id}打出的牌形为：',getcardtype(self.playing_cards))

            if not self.in_hand: #如果自己手上没牌了，就结束回合
                if self.landlord:
                    game_status['winner']=[self] #记录赢家
                    self.score+=10 #地主胜利，分数增加10
                    for player in game_status['playerlist']:
                        if player.landlord==False:
                            player.score-=5 #农民胜利，分数减少5
                    print('地主胜利')
                else:
                    game_status['winner']=[player for player in game_status['playerlist'] if player.landlord==False] #记录赢家
                    for player in game_status['winner']:
                        player.score+=5 #农民胜利，分数增加5
                    game_status['landlord'].score-=10 #地主分数-10    
                    print('农民胜利')
                

        def out_card(self,cards): #出牌
            self.played_cards=cards #记录刚刚出的牌
            # print(f'玩家{self.id}出的牌群为：',cards)
            for card in cards:
                # print(f'玩家{self.id}出的牌为：',card)
                self.in_hand.remove(card)
      

# 游戏开始
   
    
    player1=Player('玩家1')
    player2=Player('玩家2')
    player3=Player('玩家3')
    #用字典记录游戏状态，框架
    game_status={
    'player1.in_hand':player1.in_hand,
    'player2.in_hand':player2.in_hand,
    'player3.in_hand':player3.in_hand,
    'middle_cards':[],
    'landlord':None,
    'last_played_cards':None, #上一个回合出的牌
    'turn':None, #当前回合的玩家
    'playerlist':[player1,player2,player3], #玩家列表，方便循环
    'winner':None, #赢家
}
    #可视化pygame
    GREEN=(0,128,0)
    WHITE = (255,255,255)
    GRAY = (200,200,200)  # 输入框激活时的背景色
    BLUE = (0,0,210)      # 输入框边框色
    BLACK = (0,0,0)       # 输入框文字色

    pygame.init()
    screen_width=1200
    screen_height=800

    screen=pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption('斗地主')
    pygame.freetype.init()
    font_path = 'MSYH.TTC'
    font = pygame.freetype.Font(font_path, 28)
    large_font = pygame.freetype.Font(font_path, 48)


    input1_rect = pygame.Rect(350, 50, 300, 40)  # 玩家1输入框（中间偏上）
    input2_rect = pygame.Rect(350, 110, 300, 40) # 玩家2输入框（在玩家1下面）
    input3_rect = pygame.Rect(350, 170, 300, 40) # 玩家3输入框（在玩家2下面）
    input1_label,input1_label_rect = font.render('请输入玩家1姓名:', WHITE)
    input2_label,input2_label_rect = font.render('请输入玩家2姓名:', WHITE)
    input3_label,input3_label_rect = font.render('请输入玩家3姓名:', WHITE)
    input2_label_pos=(input2_rect.x-250,input2_rect.y+5)
    input1_label_pos=(input1_rect.x-250,input1_rect.y+5)
    input3_label_pos=(input3_rect.x-250,input3_rect.y+5)

    #创建按钮类
    class Button:
        def __init__(self,text,pos,font,color=WHITE,bg_color=BLUE):
            self.text=text
            self.pos=pos
            self.font=font
            self.color=color
            self.bg_color=bg_color
            _,text_rect=font.render(text,color) #渲染了一个矩形获取文字的宽高
            text_width,text_height=text_rect.size
            self.rect=pygame.Rect(pos[0],pos[1],text_width+20,text_height+10)#把Rect实例作为self的属性。
            #Rect的参数是（x,y,width,height）
            #Rect的属性可以通过self.rect.x,self.rect.y,self.rect.width,self.rect.height来访问和修改
        def draw(self,screen): #绘制按钮的方法
            pygame.draw.rect(screen,self.bg_color,self.rect) #rect矩形对象绘制，参数是（surface,color,rect）
            self.font.render_to(screen,self.pos,self.text,self.color)
        def click(self,pos):
            if self.rect.collidepoint(pos):
                return True
            else:
                return False

    #开始按钮和重置按钮
    start_button=Button('开始游戏',(screen_width//2+350,screen_height//2-100 ),large_font)
    start_status=False #未开始
    next_button=Button('下一局游戏',(screen_width//2+350,screen_height//2-100),large_font)
    reset_button=Button('重置游戏',(screen_width//2+350,screen_height//2+50),large_font)


    #游戏主循环
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(GREEN)
        # 渲染并绘制输入框中的文本
        # font.render_to(screen, (input1_rect.x+5, input1_rect.y+5), input_text1, BLACK)
        # font.render_to(screen, (input2_rect.x+5, input2_rect.y+5), input_text2, BLACK)
        # font.render_to(screen, (input3_rect.x+5, input3_rect.y+5), input_text3, BLACK)

        # 绘制输入框边上的标签
        screen.blit(input1_label, input1_label_pos)
        screen.blit(input2_label, input2_label_pos)
        screen.blit(input3_label, input3_label_pos)
        # 渲染玩家姓名
        player1_name=player1.id
        player2_name=None
        player3_name=None
        player1_name=player1_name if player1_name else "玩家1"
        player2_name=player2_name if player2_name else "玩家2"
        player3_name=player3_name if player3_name else "玩家3"
        player1_name_text,player1_name_rect = large_font.render(player1_name,  WHITE)
        player2_name_text,player2_name_rect = large_font.render(player2_name,  WHITE)
        player3_name_text,player3_name_rect = large_font.render(player3_name,  WHITE)
        # player1_name_pos=(player1_card1_pos[0]+450, player1_card1_pos[1]-200)
        # player2_name_pos=(player2_card1_pos[0]-200, player2_card1_pos[1]+100)    
        # player3_name_pos=(player3_card1_pos[0]+450, player3_card1_pos[1]-200)
        #分数框
        # score_rect=pygame.Rect(500,50,200,100)
        # pygame.draw.rect(screen,WHITE,score_rect)
        # font.render_to(screen,(550,70),f'玩家1:{player1.score}',BLACK)
        # font.render_to(screen,(550,130),f'玩家2:{player2.score}',BLACK)
        # font.render_to(screen,(550,190),f'玩家3:{player3.score}',BLACK)
        # # 绘制玩家姓名
        # screen.blit(player1_name_text, player1_name_pos)
        # screen.blit(player2_name_text, player2_name_pos)    
        # screen.blit(player3_name_text, player3_name_pos)
        
        pygame.display.flip()

        clock.tick(60)

    # reset_game(game_status)

start_game()

