import deck as dk
deck=dk.Deck()
deck.shuffle()
player1_card=deck.deal(3)
print(player1_card)
player2_card=deck.deal(3)
print(player2_card)
#定义一个函数，提取三张牌花色的数值
def suit_to_value(cards):
    #三张牌的花色转换为数值
    suit=(suit_value[cards[0][0]],suit_value[cards[1][0]],suit_value[cards[2][0]])  #花色,将花色转换为数值
    return suit
#定义一个函数，来把牌值转换为数值
def rank_to_value(cards):
    #三张牌的牌值转换为数值
    rank=(rank_value[cards[0][1]],rank_value[cards[1][1]],rank_value[cards[2][1]])  #牌值,将牌值转换为数值
    return rank

#定义大小规则,不同游戏还是要重新定义
rank_value={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':0,'J':11,'Q':12,'K':13,'A':14}
#定义花色规则，值一样的时候，花色大的为胜者
suit_value={'黑桃':4,'红桃':3,'方片':2,'梅花':1}
#定义特殊牌形
#1.三张牌值一样，为豹子
#2.三张牌值同花，为同花,同花+顺子=同花顺
#3.连续的三张牌，为顺子
#4.有对子，为对子
#5.其他情况，为普通牌形，按最大的比

def get_cardform_value(cards):
    suit=suit_to_value(cards)  #花色转为数值，是元组
    rank=rank_to_value(cards)  #牌值,将牌值转换为数值
    #对牌值进行排序
    rank_inorder=sorted(rank)  #牌值排序，是列表
    #定义牌形值，豹子为6，同花顺为5，小同花顺为4.5，同花为4，顺子为3，小顺子为2.5，对子为2，普通牌形为1
    cardform_value= 1
    #1.三张牌值一样，为豹子
    if rank[0]==rank[1]==rank[2]:
        cardform_value=6
        return cardform_value
    #2.三张牌值同花，为同花，且是顺子，为同花顺
    if suit[0]==suit[1]==suit[2] and rank_inorder[0]==rank_inorder[1]-1==rank_inorder[2]-2 :
        cardform_value=5
        return cardform_value
        #2.特殊情况，A23为小同花顺
    elif suit[0]==suit[1]==suit[2] and rank_inorder[0]==2 and rank_inorder[1]==3 and rank_inorder[2]==14:
        cardform_value=4.5
        return cardform_value
    #3.同花但不是顺子，为同花
    if suit[0]==suit[1]==suit[2]:
        cardform_value=4
        return cardform_value
    #4.连续的三张牌，为顺子
    if rank_inorder[0]==rank_inorder[1]-1==rank_inorder[2]-2 :           
        cardform_value=3
        return cardform_value
    #4.特殊情况，A23为小顺子
    if rank_inorder[0]==2 and rank_inorder[1]==3 and rank_inorder[2]==14:
        cardform_value=2.5
        return cardform_value 
    #5.有对子，为对子
    if rank_inorder[0]==rank_inorder[1] or rank_inorder[1]==rank_inorder[2]:
        cardform_value=2
        return cardform_value
    #6.其他情况，为普通牌形，按最大的比
    cardform_value=1
    return cardform_value

#定义一个比较同级的函数，True为玩家1赢，False为玩家2赢
def compare_cardvalue(player1_card,player2_card):
    suit1=suit_to_value(player1_card)  #花色转为数值，是元组，保留原来的顺序，并和下方的数值一一对应
    rank1=rank_to_value(player1_card)  #牌值,将牌值转换为数值
    suit2=suit_to_value(player2_card)  #花色转为数值，是元组，保留原来的顺序，并和下方的数值一一对应
    rank2=rank_to_value(player2_card)  #牌值,将牌值转换为数值
    #对牌值进行排序
    rank_inorder1=sorted(rank1)
    rank_inorder2=sorted(rank2)
    #如果牌形值不同，比较牌形值
    if get_cardform_value(player1_card)!=get_cardform_value(player2_card):
        if get_cardform_value(player1_card)>get_cardform_value(player2_card):
            return True
        else:
            return False
    #如果牌形值相同，比较牌值。豹子比一个值，对子比对子的值，其他牌形比最大的牌值，相同值比花色。特殊：A23为小顺子，A23为小同花顺，需比较3的花色。
    if get_cardform_value(player1_card)==get_cardform_value(player2_card):
      #如果牌形值相同，比较牌值。豹子比一个值，对子比对子的值，其他牌形比最大的牌值，
      
      if get_cardform_value(player1_card)==6:
          #如果是豹子，比牌值
          if rank_inorder1[0]>rank_inorder2[0]:
              return True
          else:
              return False
      elif get_cardform_value(player1_card)==2:
          #如果是对子，比对子的值
          #先找到对子的牌值,并保留另一个牌值
          if rank_inorder1[0]==rank_inorder1[1]:
              player1_pair=rank_inorder1[0]
              player1_other=rank_inorder1[2]
          elif rank_inorder1[1]==rank_inorder1[2]:
              player1_pair=rank_inorder1[1]
              player1_other=rank_inorder1[0]
          else:
              player1_pair=rank_inorder1[2]
              player1_other=rank_inorder1[1]
              #找到玩家2对子的牌值,并保留另一个牌值，同样逻辑
          if rank_inorder2[0]==rank_inorder2[1]:
              player2_pair=rank_inorder2[0]
              player2_other=rank_inorder2[2]
          else:
              player2_pair=rank_inorder2[2]
              player2_other=rank_inorder2[0]  
          if player1_pair>player2_pair:
              return True
          else:
              if player1_pair==player2_pair:
                  #如果对子的值相同，比另一个牌值
                  if player1_other>player2_other:
                      return True
                  else:
                    if player1_other==player2_other:
                      #比花色，用列表推导式先定位到原来的花色
                      player1_suit=[suit1[i] for i in range(3) if rank1[i]==player1_pair]
                      player2_suit=[suit2[i] for i in range(3) if rank2[i]==player2_pair]
                      if player1_suit[0]>player2_suit[0]:
                          return True
                      else:
                          return False
                    else:
                        return False
      elif get_cardform_value(player1_card)==1 or get_cardform_value(player1_card)==4:
          #如果是普通牌或同花，比最大的牌值
          if rank_inorder1[2]>rank_inorder2[2]:
              return True
          elif rank_inorder1[2]==rank_inorder2[2]:
              #如果最大的牌值相同，比第二大的牌值
              if rank_inorder1[1]>rank_inorder2[1]:
                  return True
              elif rank_inorder1[1]==rank_inorder2[1]:
                  #如果第二大的牌值相同，比最后一个值
                  if rank_inorder1[0]>rank_inorder2[0]:
                      return True
                  elif rank_inorder1[0]==rank_inorder2[0]:
                      #如果最后一个值相同，比最大值的花色
                      player1_suit=[suit1[i] for i in range(3) if rank1[i]==rank_inorder1[2]]
                      player2_suit=[suit2[i] for i in range(3) if rank2[i]==rank_inorder2[2]]
                      if player1_suit[0]>player2_suit[0]:
                          return True
                      else:
                          return False
                  else:
                      return False
              else:
                  return False
          else:
              return False
      elif get_cardform_value(player1_card)==4.5 or get_cardform_value(player1_card)==2.5:
          #如果是小顺子，或小同花顺，比3的花色
          player1_suit=[suit1[i] for i in range(3) if rank1[i]==3]
          player2_suit=[suit2[i] for i in range(3) if rank2[i]==3]
          if player1_suit[0]>player2_suit[0]:
              return True
          else:
              return False
      elif get_cardform_value(player1_card)==3 or get_cardform_value(player1_card)==5:
          #如果是普通顺子或同花顺,比最大的牌值
          if rank_inorder1[2]>rank_inorder2[2]:
              return True
          elif rank_inorder1[2]==rank_inorder2[2]:
              #如果最大的牌值相同，比花色
              player1_suit=[suit1[i] for i in range(3) if rank1[i]==rank_inorder1[2]]
              player2_suit=[suit2[i] for i in range(3) if rank2[i]==rank_inorder2[2]]
              if player1_suit[0]>player2_suit[0]:
                  return True
              else:
                  return False
            
          else:
              return False
    else:
        raise ValueError('出现了未知的牌形值')

#建立牌形值与牌形的对应关系
cardform_dict={1:'普通牌',2:'对子',3:'普通顺子',4:'同花',4.5:'小顺子',5:'同花顺',6:'豹子',2.5:'小顺子'}
cardform_cn_player1=cardform_dict[get_cardform_value(player1_card)]        
cardform_cn_player2=cardform_dict[get_cardform_value(player2_card)]
print(f'玩家1的牌为【{player1_card[0][0]}{player1_card[0][1]}】和【{player1_card[1][0]}{player1_card[1][1]}】,【{player1_card[2][0]}{player1_card[2][1]}】，玩家1牌形为{cardform_cn_player1}')
print(f'玩家2的牌为【{player2_card[0][0]}{player2_card[0][1]}】和【{player2_card[1][0]}{player2_card[1][1]}】,【{player2_card[2][0]}{player2_card[2][1]}】，玩家2牌形为{cardform_cn_player2}')
#判断玩家1是否赢了
result=compare_cardvalue(player1_card,player2_card)
if result:
    print('玩家1赢了')
else:
    print('玩家2赢了')