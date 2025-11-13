import pygame
import deck as d

screen=pygame.display.set_mode((1200,600))
pygame.display.set_caption('测试')

deck=d.DeckwithJoker()
deck.shuffle()
print(deck.cards)
player1card=deck.deal(10)
print(player1card)

def reset():
    global player1card
    if deck.shuffled==False:
        deck.shuffle()
    player1card=deck.deal(5)


clock=pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r:
                reset()
    clock.tick(60)
    screen.fill((0,128,0))
    # 加载牌面图片
    pos=0
    for card in player1card:
        card_img=d.card_load(card)
        screen.blit(card_img,(200+pos,300))
        pos+=200



    pygame.display.flip()