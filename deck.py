import random
import pygame

#把建立牌堆，发牌都放在一个类中
class Deck:
    def __init__(self):
       suit = ['黑桃', '红桃', '方片', '梅花']
       rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
       self.cards = [] #牌堆剩余的牌
       self.dealt_cards=[] #已经发出去的牌
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
                print('牌不够了，自动洗牌') 
                self.reset()
                return self.deal(num)
            cards=[] #即将要发的牌
            for _ in range(num):
                card=self.cards.pop() #从牌堆中取出牌
                cards.append(card)

            self.dealt_cards.extend(cards) #把发出去的牌加入到已经发出去的牌中
            return cards
    def reset(self): #重置牌堆，把已经发出去的牌加入到牌堆中,并洗牌
        self.cards.extend(self.dealt_cards)
        self.dealt_cards=[]
        self.shuffle()

    @classmethod #类方法：从多副牌创建一个 Deck 实例 和静态方法的区别是，里面调用了类本身，cls()，也可以用Deck()，但建议用cls()，因为如果以后继承了这个类，用Deck()就不是调用当前类了，而是调用父类
    def from_multiple_decks(cls, num_decks):
        """从多副牌创建一个 Deck 实例"""
        combined_cards = []
        for _ in range(num_decks):
            combined_cards.extend(cls().cards)  # 合并 num_decks 副牌
        new_deck = cls()  # 创建新实例
        new_deck.cards = combined_cards  # 替换 cards
        return new_deck

class DeckwithJoker(Deck):
    def __init__(self):
        super().__init__()
        self.cards.append((' 大','王'))
        self.cards.append((' 小','王'))
# 加载牌面图片
def card_load(card : tuple,scale:tuple[int,int]=(100,150)):
    s,r=card
    suit_map={'黑桃':'spades','红桃':'hearts','方片':'diamonds','梅花':'clubs',' 大':'red',' 小':'black'}
    rank_map={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':'jack','Q':'queen','K':'king','A':'ace','王':'joker'}

    try:
        card_img=pygame.image.load(f'./cards/{rank_map[r]}_of_{suit_map[s]}.png' )
        scale_card_img=pygame.transform.scale(card_img,scale)
        return scale_card_img
    except FileNotFoundError: 
        card_img=pygame.image.load(f'./cards/{suit_map[s]}_{rank_map[r]}.png' )
        scale_card_img=pygame.transform.scale(card_img,scale)
        return scale_card_img
    except :
        print(f'没有{rank_map[r]} of {suit_map[s]}这张牌')
        return None

# 测试
if __name__ == '__main__':
    deck = DeckwithJoker()
    print(deck.cards)  # 输出 54