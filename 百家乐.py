#先用控制台写出代码
#1.先定义牌堆，52张牌
#2.定义玩家和庄家
#3.洗牌，每人发两张牌
#4.判断玩家和庄家的牌面大小
#5.判断玩家和庄家的牌面大小，大的为胜者
import random

suit = ['黑桃', '红桃', '方片', '梅花']
rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
cards = []
for s in suit:
    for r in rank:
        card=(s,r)
        cards.append(card)
# print(cards)
# print(len(cards))
player1_name=input('请输入玩家1的姓名：')
player2_name=input('请输入玩家2的姓名：')
#3.洗牌，每人发两张牌
random.shuffle(cards)
player1=cards[0:2]
del cards[0:2]
player2=cards[0:2]
del cards[0:2]
#4.判断玩家和庄家的牌面大小
rank_value={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':0,'J':0,'Q':0,'K':0,'A':1}
player1_value=(rank_value[player1[0][1]]+rank_value[player1[1][1]])%10
player2_value=(rank_value[player2[0][1]]+rank_value[player2[1][1]])%10
print(f'{player1_name}的牌为{player1[0][0]}{player1[0][1]}和{player1[1][0]}{player1[1][1]},{player1_name}的牌面大小为{player1_value},{player2_name}的牌为{player2[0][0]}{player2[0][1]}和{player2[1][0]}{player2[1][1]},{player2_name}的牌面大小为{player2_value}')
#5.判断玩家和庄家的牌面大小，大的为胜者
if player1_value>player2_value:
    print(f'{player1_name}赢啦')
elif player1_value<player2_value:
    print(f'{player2_name}赢啦')
else:
    print('平局')
