import pygame
import random
import math
from pygame import mixer

# initiallization
pygame.init ( )

# Creating screen
screen = pygame.display.set_mode ((800, 600))

# background
background = pygame.image.load ('back2.jpg')

# bck sound
# mixer.music.load("background.wav")
# mixer.music.play(-1)
back = mixer.Sound ("background.wav")
back.play ( )

# title & icon
pygame.display.set_caption ("Space Invaders")
icon = pygame.image.load ("ufo.png")
pygame.display.set_icon (icon)

# player
playerImg = pygame.image.load ("gaming.png")
playerX = 370
playerY = 490
playerX_change = 0

# enemy image
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
enemyX_change = []
num_of_enemies = 6
for i in range (num_of_enemies):
    enemyImg.append (pygame.image.load ("enem.png"))
    enemyX.append (random.randint (0, 735))
    enemyY.append (random.randint (50, 150))
    enemyY_change.append (40)
    enemyX_change.append (3)

# bullet image
bulletImg = pygame.image.load ("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 10
bulletX_change = 0
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font ("freesansbold.ttf", 32)
go_font = pygame.font.Font("freesansbold.ttf",64)
textX = 10
textY = 10
gameOverX = 200
gameOverY = 200

def showScore(x, y):
    score = font.render ("Score : " + str (score_value), True, (255, 255, 255))
    screen.blit (score, (x, y))

def gameOver():
    gO = go_font.render ("Game Over!", True, (255, 0, 0))
    screen.blit (gO, (235, 250))

# playerimage function
def player(x, y):
    screen.blit (playerImg, (x, y))  # blit means draw the image


def enemy(x, y, i):
    screen.blit (enemyImg[i], (x, y))  # blit means draw the image


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit (bulletImg, (x + 20, y + 15))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt (math.pow ((enemyX - bulletX), 2) + math.pow ((enemyY - bulletY), 2))
    if distance < 30:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB color
    # screen.fill ((0, 0, 0))
    screen.blit (background, (0, 0))
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            running = False

        # key stroke is pressed or not
        if event.type == pygame.KEYDOWN:  # keydown means key pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound ("laser.wav")
                    bullet_Sound.play ()
                    bulletX = playerX
                    fire (bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # player mechanism
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy mechanism
    for i in range (num_of_enemies):
        if enemyY[i] > 420:
            for i in range (num_of_enemies):
                enemyY[i] = 2000
            gameOver()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        # collision

        collision = isCollision (enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound ("explosion.wav")
            explosion_Sound.play ( )
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            if(score_value > 50 and score_value <100):
                num_of_enemies=10
                for i in range (6,10):
                    enemyImg.append (pygame.image.load ("enem.png"))
                    enemyX.append (random.randint (0, 735))
                    enemyY.append (random.randint (50, 150))
                    enemyY_change.append (40)
                    enemyX_change.append (3)
            elif(score_value > 50 and score_value <100):
                num_of_enemies+=16
                for i in range (10,16):
                    enemyImg.append (pygame.image.load ("enem.png"))
                    enemyX.append (random.randint (0, 735))
                    enemyY.append (random.randint (50, 150))
                    enemyY_change.append (40)
                    enemyX_change.append (3)
            enemyX[i] = random.randint (0, 800)
            enemyY[i] = random.randint (50, 150)

        enemy (enemyX[i], enemyY[i], i)

    # bullet mechanism
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire (bulletX, bulletY)
        bulletY -= bulletY_change

    player (playerX, playerY)
    showScore (textX, textY)
    # updating the window
    pygame.display.update ( )
