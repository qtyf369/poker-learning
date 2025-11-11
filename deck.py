import random
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
