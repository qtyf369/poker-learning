#先用控制台写出代码
#1.先定义牌堆，52张牌
#2.定义玩家和庄家
#3.洗牌，每人发两张牌
#4.判断玩家和庄家的牌面大小
#5.判断玩家和庄家的牌面大小，大的为胜者
import random
import pygame
#定义颜色
green=(0,128,0)
#基础设置
pygame.font.init()  # 初始化字体，才能显示中文
# 定义输入框需要的颜色
WHITE = (255,255,255)
GRAY = (200,200,200)  # 输入框激活时的背景色
BLUE = (0,0,255)      # 输入框边框色
BLACK = (0,0,0)       # 输入框文字色
# 字体：黑体、28号（支持中文）
font = pygame.font.SysFont('SimHei', 28)
# 输入框相关变量
input_active = 0  # 0=没激活，1=激活玩家1输入框，2=激活玩家2输入框
input_text1 = ""  # 存玩家1输入的姓名
input_text2 = ""  # 存玩家2输入的姓名
# 输入框位置和大小（x,y,宽,高）
input1_rect = pygame.Rect(350, 50, 300, 40)  # 玩家1输入框（中间偏上）
input2_rect = pygame.Rect(350, 110, 300, 40) # 玩家2输入框（在玩家1下面）

#窗口初始化
pygame.init()
screen_width=1000
screen_height=600

screen=pygame.display.set_mode((screen_width,screen_height))  
screen.fill(green)  
pygame.display.set_caption('百家乐')
def card_load(card : tuple):
    r,s=card
    try:
        card_img=pygame.image.load(f'./cards/{rank_map[s]}_of_{suit_map[r]}.png')
        scale_card_img=pygame.transform.scale(card_img,(100,150))
        return scale_card_img
    except:
        print(f'没有{rank_map[r]} of {suit_map[s]}这张牌')
        return None
suit = ['黑桃', '红桃', '方片', '梅花']
suit_map={'黑桃':'spades','红桃':'hearts','方片':'diamonds','梅花':'clubs'}
rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_map={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':'jack','Q':'queen','K':'king','A':'ace'}

def card_init():
    cards = []
    for s in suit:
        for r in rank:
            card=(s,r)
            cards.append(card)
    return cards
cards=card_init()
# print(cards)
# print(len(cards))
player1_name=input('请输入玩家1的姓名：')
player2_name=input('请输入玩家2的姓名：')
#3.洗牌，每人发两张牌
random.shuffle(cards)
player1=cards[0:2]
del cards[0:2]
player1_card1=card_load(player1[0])
player1_card2=card_load(player1[1])

player2=cards[0:2]
del cards[0:2]

player2_card1=card_load(player2[0])
player2_card2=card_load(player2[1])
player1_card1_pos=(screen_width//2-100,screen_height//2-150)
player1_card2_pos=(screen_width//2+100,screen_height//2-150)
player2_card1_pos=(screen_width//2-100,screen_height//2+100)
player2_card2_pos=(screen_width//2+100,screen_height//2+100)

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

#重置游戏
def reset_game():
    global player1,player2,player1_card1,player1_card2,player2_card1,player2_card2
    cards=card_init()
    random.shuffle(cards)
    player1=cards[0:2]
    del cards[0:2]
    player1_card1=card_load(player1[0])
    player1_card2=card_load(player1[1])
    player2=cards[0:2]
    del cards[0:2]
    player2_card1=card_load(player2[0])
    player2_card2=card_load(player2[1])
    if player1_value>player2_value:
        print(f'{player1_name}赢啦')
    elif player1_value<player2_value:
        print(f'{player2_name}赢啦')
    else:
        print('平局')    
    
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN and event.key==pygame.K_r:
            reset_game()
        # ========== 输入框交互逻辑（复制到 if event.type==pygame.QUIT: 下面）==========
# 1. 鼠标点击：激活对应的输入框
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input1_rect.collidepoint(event.pos):  # 点击玩家1输入框
                input_active = 1
            elif input2_rect.collidepoint(event.pos):  # 点击玩家2输入框
                input_active = 2
            else:  # 点击其他地方，取消激活
                input_active = 0

        # 2. 键盘输入：处理姓名输入
        if event.type == pygame.KEYDOWN:
            # 处理玩家1输入
            if input_active == 1:
                if event.key == pygame.K_RETURN:  # 按回车，确认玩家1姓名
                    if input_text1.strip() != "":  # 确保输入不为空
                        player1_name = input_text1.strip()  # 把输入的文字赋值给player1_name
                elif event.key == pygame.K_BACKSPACE:  # 按退格，删除最后一个字
                    input_text1 = input_text1[:-1]
                else:  # 输入文字（支持中文）
                    input_text1 += event.unicode  # 把按键文字加到input_text1里

            # 处理玩家2输入（和玩家1逻辑一样）
            elif input_active == 2:
                if event.key == pygame.K_RETURN:
                    if input_text2.strip() != "":
                        player2_name = input_text2.strip()
                elif event.key == pygame.K_BACKSPACE:
                    input_text2 = input_text2[:-1]
                else:
                    input_text2 += event.unicode    
    screen.blit(player1_card1,player1_card1_pos)
    screen.blit(player1_card2,player1_card2_pos)
    screen.blit(player2_card1,player2_card1_pos)
    screen.blit(player2_card2,player2_card2_pos)
    # 1. 画玩家1输入框
    if input_active == 1:  # 如果激活，背景变灰色
        pygame.draw.rect(screen, GRAY, input1_rect)
    else:  # 没激活，背景白色
        pygame.draw.rect(screen, WHITE, input1_rect)
    pygame.draw.rect(screen, BLUE, input1_rect, 2)  # 输入框边框（蓝色）
    # 画玩家1输入的文字
    text1 = font.render(input_text1, True, BLACK)
    screen.blit(text1, (input1_rect.x + 10, input1_rect.y + 5))  # 文字在输入框内
    # 玩家1输入提示（左边的“玩家1姓名：”）
    hint1 = font.render("玩家1姓名：", True, WHITE)
    screen.blit(hint1, (220, 55))  # 提示文字位置

    # 2. 画玩家2输入框（和玩家1逻辑一样）
    if input_active == 2:
        pygame.draw.rect(screen, GRAY, input2_rect)
    else:
        pygame.draw.rect(screen, WHITE, input2_rect)
    pygame.draw.rect(screen, BLUE, input2_rect, 2)
    text2 = font.render(input_text2, True, BLACK)
    screen.blit(text2, (input2_rect.x + 10, input2_rect.y + 5))
    # 玩家2输入提示
    hint2 = font.render("玩家2姓名：", True, WHITE)
    screen.blit(hint2, (220, 115))

    pygame.display.flip()