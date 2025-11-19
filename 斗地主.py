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



#游戏主体       
def start_game():
    class Player: #把玩家的属性和方法封装在一个类中
        def __init__(self,id,ai=True):
            self.id=id
            self.in_hand=[] #玩家手中的牌
            self.playing_cards=[] #正在选的牌，准备出
            self.played_cards=[] #刚刚出的牌,已经出过的牌，在牌桌上
            self.landlord=False #是否是地主,默认不是
            self.turn=False #是否是出牌回合,默认不是
            self.ai=ai #是否是AI玩家,默认是
        #定义回合
        def play_turn(self): #出牌
            self.out_card(self.played_cards)
        #回合开始，切换到出牌回合
        #判断自己选的牌是否比last_played_cards大
        def possible_cards(self) -> list: #可以出的牌，不用传参，参数是固定的，自己的牌和牌桌上的牌,可以直接调用
        #按照类型筛选出可以出的牌，要针对对方打出的牌的类型
            last=game_status['last_played_cards']
            #重构一下，暴力枚举太慢了。
            #筛选自己的所有牌形，分类看。多张牌的用counter
            #1.单张
            possible_single=[[card] for card in self.in_hand if getcardtype([card])=='单张' and can_beat([card],last)]
            #2.对子
            count=Counter([card[1] for card in self.in_hand]) #数每个值，返回字典，键是值，值是出现次数，这个后面还可以用
            pairlistrank=[k for k,v in count.items() if v>=2 and v!='王'] #筛选出出现次数大于等于2的牌值，排除王
            #根据牌值从手牌中筛选出对子
            possible_pairs=[]
            for rank in pairlistrank:
                cards_of_rank=[card for card in self.in_hand if card[1]==rank] #从手牌中筛选出牌值为rank的牌，比如rank为2，那么就筛选出所有不同花色的2
                #从牌值为rank的牌中筛选出对子
                for pair in combinations(cards_of_rank, 2):
                        possible_pairs.append(list(pair)) #t每个Pair是单独牌型，需转化为列表

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
                for i in range(len(ranklist)):
                    
                for i in range(len(ranklist)-4): #从牌值列表中筛选出顺子
                    if rank_value[ranklist[i+4]]-rank_value[ranklist[i]]==4: #如果最后一张减第一张等于4，那么就是顺子
                    possible_straight.append(ranklist[i:i+5]) #加入到顺子列表中，注意是切片，包括i，不包括i+5



            #5.三带1
            triple_with_one=[[card,card,card,extra] for card in self.in_hand for extra in self.in_hand if getcardtype([card,card,card,extra])==4 and can_beat([card,card,card,extra],last)] 








            if last==None: #如果是第一个回合，那么可以出任意牌
                #需要考虑不同牌型的情况
                possible_cards=[]
                #先用字典整理出可以出的牌型的长度
                valid={'单张':1,'对子':2,'三不带牌':3,'炸弹':4,'三带1':4,'三带二':5,'顺子':range(5,12,1),'连对':range(6,23,2),'飞机':[6,8,10,12,9,16]}
                valid_lengths=set() #可以出的牌型的长度
                for key in valid:
                    if isinstance(valid[key],Iterable): #如果是可迭代对象，那么就是范围
                        valid_lengths.update(valid[key]) #更新可以出的牌型的长度，用集合避免重复
                    else:
                        valid_lengths.add(valid[key]) #如果不是可迭代对象，那么就是单个数字
                #筛选出可以出的牌型
                for length in valid_lengths:
                    combo=combinations(self.in_hand,length) #从当前牌中选出length张牌,length张牌会组成一个元组，每张又是元组
                    possible_combo=[list(tuple(el)) for el in combo if getcardtype(list(el))] #筛选出可以出的牌型
                    possible_cards.extend(possible_combo) #将可以出的牌型加入到列表中
                return possible_cards #返回可以出的牌型的列表
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

                return combo+combobomb+jokercombo #返回可以出的牌,这是个列表，每个元素是列表，是可以出的牌。

        def start_turn(self): #开始自己的回合,并选择要出的牌
            self.turn=True #切换到出牌回合
           
          
            if self.played_cards==game_status['last_played_cards']: #如果自己出的牌和上一个回合出的牌相同，说明是自己打的牌。
                game_status['last_played_cards']=None   # 自己重新出任意牌       
            
            # print(f'玩家{self.id}请选择要出的牌，')
            #先模拟随便出牌，筛选出可以出的牌
            possible_cards=self.possible_cards()
            print(f'{self.id}可以出的牌为：')
            possible_cards.sort(key=lambda x:len(x)) #按牌型长度排序
            for i in range(len(possible_cards)):
                possible_cards[i].sort(key=lambda x:rank_value[x[1]]) #按牌值排序
                print(f'{i+1}',possible_cards[i]) #按牌值排序

            if self.ai == False:
                if possible_cards:
                    index=int(input('请选择要出的牌，输入牌型的序号'))
                    self.playing_cards=possible_cards[index-1] #选择出最后一个牌型
                    self.out_card(self.playing_cards)
                    game_status['last_played_cards']=self.playing_cards #记录刚刚出的牌
                else:
                    print('没有可以出的牌，回合结束')
                print(f'{self.id}出的牌为：',self.playing_cards)
                
            else:
                if possible_cards:
                    self.playing_cards=possible_cards[-1] #选择出第一个牌型
                    self.out_card(self.playing_cards)
                    game_status['last_played_cards']=self.playing_cards #记录刚刚出的牌
                    print(f'{self.id}出的牌为：',self.playing_cards)
                    print(f'{self.id}打出的牌形为：',getcardtype(self.playing_cards))

                else:
                    print(f'{self.id}要不起，回合结束')
            if not self.in_hand: #如果自己手上没牌了，就结束回合
                if self.landlord:
                    game_status['winner']=[self] #记录赢家
                    print('地主胜利')
                else:
                    game_status['winner']=[player for player in game_status['playerlist'] if player.landlord==False] #记录赢家
                    print('农民胜利')
                
        def out_card(self,cards): #出牌
            self.played_cards=cards #记录刚刚出的牌
            # print(f'玩家{self.id}出的牌群为：',cards)
            for card in cards:
                # print(f'玩家{self.id}出的牌为：',card)
                self.in_hand.remove(card)
            self.turn=False #出牌回合结束，切换到下一个回合
            
        def call_turn(self,follow_or_not:bool): #叫牌回合
            #玩家选择要出的牌，或者不要。
            pass #先默认有大牌必出
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

       

# 游戏开始
    import deck as d
    deck=d.DeckwithJoker() #带小王和大王
    # print(deck.cards)
    player1=Player('玩家1')
    player2=Player('玩家2')
    player3=Player('玩家3')
    deck.shuffle() #洗牌
    # print(deck.cards)
    #发牌，每人发17张牌，剩3张
    player1.in_hand=deck.deal(17)
    player2.in_hand=deck.deal(17)
    player3.in_hand=deck.deal(17)
    #用一个字典记录牌局状态，每局要变的东西，放在游戏函数里面
    game_status={
    'player1_in_hand':player1.in_hand,
    'player2_in_hand':player2.in_hand,
    'player3_in_hand':player3.in_hand,
    'middle_cards':[],
    'landlord':None,
    'last_played_cards':None, #上一个回合出的牌
    'turn':None, #当前回合的玩家
    'playerlist':[player1,player2,player3], #玩家列表，方便循环
    'winner':None, #赢家
}
    def call_landlord(): #返回地主的名字
        player1_call=input('玩家1是否要叫地主？(y/n)')
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
        
  
    game_status['middle_cards']=deck.deal(3) #中间3张牌
    game_status['landlord']=None #初始时，没有地主
    game_status['last_played_cards']=None #上一个回合出牌的牌
    #叫地主
    game_status['landlord']=call_landlord() #该函数轮流选地主，产生地主
   
    game_status['landlord'].start_turn() #地主出牌回合
    print(game_status['turn'],'这是有效的')
    #地主出完了，下一个回合
    #有玩家手上没牌了，就结束
    while not game_status['winner']: #如果赢家为空，就继续循环
        game_status['turn']=game_status['playerlist'][(game_status['playerlist'].index(game_status['turn'])+1)%3] #切换到下一个回合的玩家
        game_status['turn'].start_turn() #切换到下一个回合的玩家出牌回合
    for winner in game_status['winner']:
        print(winner.id,'是赢家')    


start_game()    