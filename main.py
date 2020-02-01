import pygame
import random
import math
from pygame import mixer

# initialize
pygame.init()
start_time = pygame.time.get_ticks()
screen = pygame.display.set_mode((800, 600))
winning_score = 50
play_time = 10

# background image

background = pygame.image.load('space.png')

# background sound
mixer.music.load('music.wav')
mixer.music.play(-1)

# title and logo
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('undertake.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('spaceship (1).png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num = 6

for i in range(num):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(100)

# bullet
# ready state in which you cant see bullet
# fir is moving state of bullet

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# GAME OVER

fontG = pygame.font.Font('my game.ttf', 70)


def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def game_over_text():
    over = fontG.render("GAME OVER : ", True, (255, 255, 255))
    screen.blit(over, (200, 250))


def draw_time(screen, x, y, time_left):
    fontT = pygame.font.Font('freesansbold.ttf', 30)
    textT = fontT.render("Time : " + str(time_left), True, (255, 255, 255))
    screen.blit(textT, (50, 510))


# loop

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    time_left = pygame.time.get_ticks() - start_time
    time_left = time_left / 1000
    time_left = play_time - time_left
    time_left = int(time_left)
    if time_left >= 0:
        draw_time(screen, 50, 450, time_left)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        # key pressing

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('shoot.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_DOWN:
                playerY_change = 0
            if event.key == pygame.K_UP:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement

    for i in range(num):
        if time_left is 0:
            for j in range(num):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2

        if enemyY[i] <= 0:
            enemyY_change[i] = 2
        elif enemyY[i] >= 536:
            enemyY_change[i] = -2

        # collision
        collide = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collide:
            explosion_Sound = mixer.Sound('destroy.wav')
            explosion_Sound.play()
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            score_value += 1

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
