#先用控制台写出代码
#1.先定义牌堆，52张牌
#2.定义玩家和庄家
#3.洗牌，每人发两张牌
#4.判断玩家和庄家的牌面大小
#5.判断玩家和庄家的牌面大小，大的为胜者
import random
import pygame
import pygame.freetype
import deck as d
from deck import card_load
import sys
import os
#定义颜色
green=(0,128,0)
#基础设置
pygame.freetype.init()  # 初始化字体，才能显示中文
# 定义输入框需要的颜色
WHITE = (255,255,255)
GRAY = (200,200,200)  # 输入框激活时的背景色
BLUE = (0,0,210)      # 输入框边框色
BLACK = (0,0,0)       # 输入框文字色
# 字体：黑体、28号（支持中文）
# font = pygame.font.SysFont('SimHei', 28)






#窗口初始化
pygame.init()
screen_width=1200
screen_height=800

screen=pygame.display.set_mode((screen_width,screen_height))  

pygame.display.set_caption('百家乐')

# 确保pygame正确初始化字体系统
pygame.init()
pygame.font.init()
pygame.freetype.init()
# 输入框相关变量
input_active = 0  # 0=没激活，1=激活玩家1输入框，2=激活玩家2输入框
input_text1 = ""  # 存玩家1输入的姓名
input_text2 = ""  # 存玩家2输入的姓名
#输入框位置和大小（x,y,宽,高），现在先放外面，后续如果要消失，得放主循环里面，好像也可以通过不绘制来实现
input1_rect = pygame.Rect(350, 50, 300, 40)  # 玩家1输入框（中间偏上）
input2_rect = pygame.Rect(350, 110, 300, 40) # 玩家2输入框（在玩家1下面）
font_path='MSYH.TTC'
if os.path.exists(font_path):
    print(f'字体文件{font_path}存在')
font = pygame.freetype.Font(font_path, 28)
large_font = pygame.freetype.Font(font_path, 48)

# #render(
#     text,          # 必选：要渲染的文字（字符串，支持中文）
#     fgcolor,       # 必选：文字颜色（RGB元组，比如 (0,0,0) 黑色）
#     bgcolor=None,  # 可选：文字背景色（默认透明）
#     style=0,       # 可选：文字样式（加粗、斜体等，默认正常）
#     rotation=0,    # 可选：旋转角度（默认0度，不旋转）
#     size=0         # 可选：强制指定字号（默认0=用创建字体时的字号）
# ) render 的参数说明，抗锯齿不在这里，是创建对象的时候设置的，浪费我大量时间
#输入框边上的标签，直接渲染了。
input1_label,input1_label_rect = font.render('请输入玩家1姓名:', WHITE)
input2_label,input2_label_rect = font.render('请输入玩家2姓名:', WHITE)
input2_label_pos=(input2_rect.x-250,input2_rect.y+5)
input1_label_pos=(input1_rect.x-250,input1_rect.y+5)


# 玩家输入框




#映射牌面，定义些规则下的牌面大小
suit = ['黑桃', '红桃', '方片', '梅花']
suit_map={'黑桃':'spades','红桃':'hearts','方片':'diamonds','梅花':'clubs'}
rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_map={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':'jack','Q':'queen','K':'king','A':'ace'}

deck=d.Deck() #创建牌堆
deck.shuffle() #洗牌
#初始设置
player1_name='玩家1'
player2_name='玩家2'

#3.洗牌，每人发两张牌
player1=deck.deal(2)
player2=deck.deal(2)
#4.把牌面图片导入缓存
player1_card1=card_load(player1[0])
player1_card2=card_load(player1[1])
player2_card1=card_load(player2[0])
player2_card2=card_load(player2[1])

#5.定义牌面图片位置
player1_card1_pos=(screen_width//2-100,screen_height//2-150) #//代表向下整除
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
    global rank_value,player1,player2,player1_card1,player1_card2,player2_card1,player2_card2,deck,player1_name,player2_name,player1_value,player2_value
    deck=d.Deck()
    deck.shuffle()
    
    player1=deck.deal(2)
    player2=deck.deal(2)
    player1_value=(rank_value[player1[0][1]]+rank_value[player1[1][1]])%10
    player2_value=(rank_value[player2[0][1]]+rank_value[player2[1][1]])%10
    
    player1_card1=card_load(player1[0])
    player1_card2=card_load(player1[1])
    player2_card1=card_load(player2[0])
    player2_card2=card_load(player2[1])
    if player1_value>player2_value:
        print(f'{player1_name}赢啦')
    elif player1_value<player2_value:
        print(f'{player2_name}赢啦')
    else:
        print('平局')    

 #主循环   
running=True
clock = pygame.time.Clock()

while running:
    time_delta = clock.tick(60) / 1000.0
    events=pygame.event.get()

    for event in events:
       
        
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN and event.key==pygame.K_r:
            reset_game()
        
        # 处理鼠标点击事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查玩家1输入框是否被点击
            if input1_rect.collidepoint(event.pos):
                input_active = 1
                
            # 检查玩家2输入框是否被点击
            elif input2_rect.collidepoint(event.pos):
                input_active = 2
                
            else:
                input_active = 0  # 点击了其他地方，取消激活状态
        # 处理输入事件
        if event.type == pygame.KEYDOWN:
            # 当输入框有焦点且按下回车键时
            if event.key == pygame.K_RETURN:
                # 检查哪个输入框有焦点
                if input_active==1:
                    if input_text1.strip() != "":
                        player1_name = input_text1.strip()
                        input_active = 2  # 玩家1姓名输入完成，切换到玩家2输入框
                        input_text1=""
                        print(f"玩家1姓名已设置为: {player1_name}")
                elif input_active==2:
                    if input_text2.strip() != "":
                        player2_name = input_text2.strip()
                        input_active = 0  # 玩家2姓名输入完成，取消激活状态
                        input_text2=""
                        print(f"玩家2姓名已设置为: {player2_name}")
                else:
                    input_active=1
            if event.key == pygame.K_ESCAPE:#按下ESC键，取消激活状态
                input_active = 0  # 按下 ESC 键，取消激活状态
                input_text1=""
                input_text2=""
            if event.key == pygame.K_BACKSPACE:
                if input_active==1 :
                    input_text1 = input_text1[:-1]
                elif input_active==2:
                    input_text2 = input_text2[:-1]
            #如果是TAB键，切换到下一个输入框
            elif event.key == pygame.K_TAB:

                if input_active==1:
                    input_active=2
                elif input_active==2:
                    input_active=1

            else:
                # 处理其他按键，将其添加到当前激活的输入框,去除回车和制表符
                if input_active == 1 and event.unicode.isprintable():
                    input_text1 += event.unicode
                elif input_active == 2 and event.unicode.isprintable():
                    input_text2 += event.unicode

    # 绘制背景
    screen.fill(green)
    #绘制输入框，根据是否有焦点来绘制不同的颜色
    if input_active==1:
        pygame.draw.rect(screen, GRAY, input1_rect,border_radius=10)
    else:
        pygame.draw.rect(screen, WHITE, input1_rect,border_radius=10)
    if input_active==2:
        pygame.draw.rect(screen, GRAY, input2_rect,border_radius=10)    
    else:
        pygame.draw.rect(screen, WHITE, input2_rect,border_radius=10)

    # 渲染并绘制输入框中的文本
    font.render_to(screen, (input1_rect.x+5, input1_rect.y+5), input_text1, BLACK)
    font.render_to(screen, (input2_rect.x+5, input2_rect.y+5), input_text2, BLACK)

    # 绘制输入框边上的标签
    screen.blit(input1_label, input1_label_pos)
    screen.blit(input2_label, input2_label_pos)
    # 渲染玩家姓名
    player1_name=player1_name if player1_name else "玩家1"
    player2_name=player2_name if player2_name else "玩家2"
    player1_name_text,player1_name_rect = large_font.render(player1_name,  WHITE)
    player2_name_text,player2_name_rect = large_font.render(player2_name,  WHITE)
    player1_name_pos=(player1_card1_pos[0]+450, player1_card1_pos[1]-200)
    player2_name_pos=(player2_card1_pos[0]-200, player2_card1_pos[1]+100)    
    # 绘制玩家姓名
    screen.blit(player1_name_text, player1_name_pos)
    screen.blit(player2_name_text, player2_name_pos)    

    # 绘制玩家1和玩家2的牌面图片
    screen.blit(player1_card1, player1_card1_pos)
    screen.blit(player1_card2, player1_card2_pos)
    screen.blit(player2_card1, player2_card1_pos)
    screen.blit(player2_card2, player2_card2_pos)
    
    font.render_to(screen, (200, 200), f'{player1_name}的牌面大小为{player1_value}', BLACK)
    font.render_to(screen, (200, 300), f'{player2_name}的牌面大小为{player2_value}', BLACK)

    pygame.display.flip()