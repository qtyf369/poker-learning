import random
import pygame

#把建立牌堆，发牌都放在一个类中
class Deck:
    def __init__(self):
       suit = ['黑桃', '红桃', '方片', '梅花']
       rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
       self.cards = []
       for s in suit:
           for r in rank:
               card=(s,r)
               self.cards.append(card)
       self.shuffled=False
    
    def shuffle(self):
        if self.shuffled==False:
            random.shuffle(self.cards)
            self.shuffled=True
        else:
            print('牌已洗过')

    def deal(self,num=1): #默认发一张牌
        if self.shuffled==False:
            print('请先洗牌')
        else:
            if num>len(self.cards):
                print('牌不够了')
                return None
            cards=[] #即将要发的牌
            for i in range(num):
                card=self.cards.pop() #从牌堆中取出牌
                cards.append(card)
            return cards

# 加载牌面图片
def card_load(card : tuple,scale:tuple[int,int]=(100,150)):
    s,r=card
    suit_map={'黑桃':'spades','红桃':'hearts','方片':'diamonds','梅花':'clubs'}
    rank_map={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':'jack','Q':'queen','K':'king','A':'ace'}

    try:
        card_img=pygame.image.load(f'./cards/{rank_map[r]}_of_{suit_map[s]}.png')
        scale_card_img=pygame.transform.scale(card_img,scale)
        return scale_card_img
    except:
        print(f'没有{rank_map[r]} of {suit_map[s]}这张牌')
        return None
