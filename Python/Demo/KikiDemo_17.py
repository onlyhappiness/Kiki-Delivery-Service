import pygame
from pygame import mixer
import random
import time

clock = pygame.time.Clock()

# pygame 초기화
pygame.init()

# 게임 화면 구현
# 15인치 화면에 호환되도록 하였기 때문에
# 다른 desktop에서 보면 작게 보일 수 있습니다...)
screen = pygame.display.set_mode((900, 650))

# color
green = (0,255,0)
white = (255, 255, 255)
light_green = (0,200,0)

# Title and Icon
pygame.display.set_caption("Kiki's Delivery Service")
icon = pygame.image.load('../images/Witch.png')
pygame.display.set_icon(icon)

# Image
background = pygame.image.load('../images/background.jpg')
intro_background = pygame.image.load('../images/intro.jpg')
playerImg = pygame.image.load('../images/kiki.png') # Player 구현
playerImg = pygame.transform.scale(playerImg, (180,150))

# Enemy 구현
enemyImg = [pygame.image.load('../images/enemy/1.png') , pygame.image.load('../images/enemy/2.png')]
#enemyImg = pygame.transform.scale(enemyImg, (110,130))
enemyMove = 0

# Background Sound
#mixer.music.load('BGM.mp3')
#mixer.music.play(-1)


# 폰트
font = pygame.font.Font('../Font/Goyang.ttf',35)

# 함수
def Message(size,mess,x_pos,y_pos):
    font = pygame.font.Font('../Font/Goyang.ttf',40)
    render = font.render(mess, True, white)
    screen.blit(render, (x_pos,y_pos))
    
def show_score(count):
    score = font.render("Score:" + str(count),True, white)
    screen.blit(score,(770,5))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x_random, y_random):
    global enemyMove

    if enemyMove + 1 >= 4:
        enemyMove = 0
        
    if y_random >= 0:
        screen.blit(enemyImg[enemyMove//2], (x_random, y_random))
        enemyMove += 1
    
def button(x_button, y_button, mess_b):
    pygame.draw.rect(screen, green, [x_button, y_button, 220, 50])
    Message(50, mess_b, x_button, y_button)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x_button < mouse[0] < x_button + 100 and y_button < mouse[1] < y_button+30:
        pygame.draw.rect(screen, light_green, [x_button, y_button, 100, 30])
        Message(50, mess_b, x_button, y_button)
        """
        if click == (1,0,0) and mess_b == "배달 시작!":
            Game_loop()
        elif click == (1,0,0) and mess_b == "나가기":
            pygame.quit()
        """
        if click == (1,0,0) and mess_b == "Start delivery!":
            Game_loop()
        elif click == (1,0,0) and mess_b == "Quit..":
            pygame.quit()
            
def game_intro():
    intro = True
    while intro:
        screen.blit(intro_background, (0,0))
        #Message(50, "키키의 배달 서비스" ,310, 50)
        #Message(50, "까마귀를 피해 배달 서비스를 완료하세요!", 150, 200)
        #button(100, 350, "배달 시작!")
        #button(600, 350, "나가기")
        Message(50, "Avoid the crows and complete the delivery service!", 100, 200)
        button(100, 350, "Start delivery!")
        button(600, 350, "Quit..")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
        
        pygame.display.update()

# 까마귀랑 충돌
def bird_strike(playerX,x_random,playerY,y_random):
    if x_random-60 < playerX < x_random+60 and y_random-60 < playerY < y_random+60:
    
        Message(100, "Be careful..!", 400, 300)
        pygame.display.update()
        time.sleep(1)
        game_intro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                

# 게임 루프
def Game_loop():
    playerX = 0
    playerY = 200
    playerX_change = 0
    playerY_change = 0

    x_random = 900
    y_random = random.randrange(0,600)

    count = 0
    
    running = True
    while running:
        # Background Image
        screen.blit(background,(0,0))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 키를 눌렀을 때 움직이는 이벤트
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX_change = -1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_change = 1
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    playerY_change = -1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    playerY_change = 1

                # ESC를 누르면 게임이 종료하도록..
                if event.key == pygame.K_ESCAPE:
                    running = False

            # 키키 컨셉에 맞춰 비행을 능숙하지 않다는 점을 고려하여
            # 이동키를 누르지 않으면 플레이어가 멈추는 것을 주석처리...
            """
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    playerX_change = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    playerY_change = 0
            """

        # player가 화면 밖으로 나갈 경우
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0

        elif playerX >= 850:
            playerX = 850

        playerY += playerY_change
        if playerY <= 0:
            playerY = 0

        elif playerY >= 550:
            playerY = 550

        player(playerX, playerY)
        enemy(x_random,y_random)
        x_random -= 4
        if x_random == 0:
            x_random = 900
            y_random = random.randrange(0,600)
            count += 1
        bird_strike(playerX,x_random,playerY,y_random)
        show_score(count)
        pygame.display.update()

game_intro()
pygame.display.update()

pygame.quit()

