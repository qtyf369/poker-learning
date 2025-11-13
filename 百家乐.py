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

# 玩家输入框边上的标签
input1_label,input1_label_rect = font.render('请输入玩家1姓名:', WHITE)
input2_label,input2_label_rect = font.render('请输入玩家2姓名:', WHITE)
input2_label_pos=(input2_rect.x-250,input2_rect.y+5)
input1_label_pos=(input1_rect.x-250,input1_rect.y+5)
# 开始游戏按钮

class Button:
    def __init__(self,text,pos,font,color=WHITE,bg_color=BLUE):
        self.text=text
        self.pos=pos
        self.font=font
        self.color=color
        self.bg_color=bg_color
        _,text_rect=font.render(text,color) #渲染了一个矩形获取文字的宽高
        text_width,text_height=text_rect.size
        self.rect=pygame.Rect(pos[0],pos[1],text_width+20,text_height+10)#把Rect实例作为self的属性。
        #Rect的参数是（x,y,width,height）
        #Rect的属性可以通过self.rect.x,self.rect.y,self.rect.width,self.rect.height来访问和修改
    def draw(self,screen): #绘制按钮的方法
        pygame.draw.rect(screen,self.bg_color,self.rect) #rect矩形对象绘制，参数是（surface,color,rect）
        self.font.render_to(screen,self.pos,self.text,self.color)
    def click(self,pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

start_button=Button('开始游戏',(screen_width//2+350,screen_height//2-100 ),large_font)
start_status=False #未开始
next_button=Button('下一局游戏',(screen_width//2+350,screen_height//2-100),large_font)
reset_button=Button('重置游戏',(screen_width//2+350,screen_height//2+50),large_font)
#映射牌面，定义些规则下的牌面大小
suit = ['黑桃', '红桃', '方片', '梅花']
suit_map={'黑桃':'spades','红桃':'hearts','方片':'diamonds','梅花':'clubs'}
rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_map={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':'jack','Q':'queen','K':'king','A':'ace'}


#初始设置
player1_name='玩家1'
player2_name='玩家2'

#5.定义牌面图片位置，常量，不变
player1_card1_pos=(screen_width//2-100,screen_height//2-150) #//代表向下整除
player1_card2_pos=(screen_width//2+100,screen_height//2-150)
player2_card1_pos=(screen_width//2-100,screen_height//2+100)
player2_card2_pos=(screen_width//2+100,screen_height//2+100)

#4.判断玩家和庄家的牌面大小
rank_value={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':0,'J':0,'Q':0,'K':0,'A':1}

count=0
player1_win=0 #记录玩家1赢的次数
player2_win=0 #记录玩家2赢的次数
result_text=''
#开始游戏
def start_game():
    global result_text,player1_win,player2_win,player1,player2,player1_card1,player1_card2,player2_card1,player2_card2,deck,player1_name,player2_name,player1_value,player2_value
    deck=d.Deck()
    deck.shuffle()
    
    

#发牌，每人发两张牌
    player1=deck.deal(2)
    player2=deck.deal(2)
    player1_value=(rank_value[player1[0][1]]+rank_value[player1[1][1]])%10
    player2_value=(rank_value[player2[0][1]]+rank_value[player2[1][1]])%10

#渲染，每次发牌都要渲染一次牌面图片，因为有变化 
    player1_card1=card_load(player1[0])
    player1_card2=card_load(player1[1])
    player2_card1=card_load(player2[0])
    player2_card2=card_load(player2[1])
    if player1_value>player2_value:
        print(f'{player1_name}赢啦')
        player1_win+=10
        result_text=f'{player1_name}赢啦'
    elif player1_value<player2_value:
        print(f'{player2_name}赢啦')
        player2_win+=10
        result_text=f'{player2_name}赢啦'
    else:
        print('平局')    
        result_text='平局'  

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

            if start_button.click(event.pos) and start_status==False:
                start_status=True
                start_game()
            if next_button.click(event.pos) and start_status==True:
                start_game()
            if reset_button.click(event.pos) and start_status==True:
                player1_win=0
                player2_win=0
                result_text=''
                start_status=False
        # 处理输入事件
        if event.type == pygame.KEYDOWN:
            # 当输入框有焦点且按下回车键时
            if event.key == pygame.K_RETURN and start_status==False:
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
   
    
    if start_status==False: #未开始状态
        start_button.draw(screen) #显示开始按钮
    if start_status==True: #游戏开始后，绘制下一局按钮
        next_button.draw(screen) #显示下一局按钮
        reset_button.draw(screen) #显示重置按钮
    if start_status==False: #未开始状态，绘制玩家姓名输入框
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
    #分数框
   

    # 绘制玩家姓名
    screen.blit(player1_name_text, player1_name_pos)
    screen.blit(player2_name_text, player2_name_pos)    

    # 绘制玩家1和玩家2的牌面图片
    if start_status==True:
        screen.blit(player1_card1, player1_card1_pos)
        screen.blit(player1_card2, player1_card2_pos)
        screen.blit(player2_card1, player2_card1_pos)
        screen.blit(player2_card2, player2_card2_pos)
    # 绘制结果文字
    result_text_surface,result_text_rect=large_font.render(result_text,WHITE)
    result_text_pos=(500,100)
    screen.blit(result_text_surface,result_text_pos)

    #分数实时更新
    if start_status==True:
        large_font.render_to(screen, (player1_name_pos[0], player1_name_pos[1]-50), f'{player1_win}分', WHITE)
        large_font.render_to(screen, (player2_name_pos[0], player2_name_pos[1]-50), f'{player2_win}分', WHITE)
    # font.render_to(screen, (200, 200), f'{player1_name}的牌面大小为{player1_value}', BLACK)
    # font.render_to(screen, (200, 300), f'{player2_name}的牌面大小为{player2_value}', BLACK)

    pygame.display.flip()