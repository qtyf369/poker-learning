import random
#把建立牌堆，发牌都放在一个类中
class Dock:
    def __init__(self):
       suit = ['黑桃', '红桃', '方片', '梅花']
       rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
       self.cards = []
       for s in suit:
           for r in rank:
               card=(s,r)
               self.cards.append(card)
       self.shuffle=False
    
    def shuffle(self):
        if self.shuffle==False:
            random.shuffle(self.cards)
            self.shuffle=True
        else:
            print('牌已洗过')

    