import pygame
import random
import math
from pygame import mixer

# Initialising pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('images/rocket.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('images/background.jpg')

# Background sound
mixer.music.load("sounds/background3.wav")
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('images/space2.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

for i in range(num_of_enemies) :
    enemyImg.append(pygame.image.load('images/Enemy1.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(2)  # speed of alien is increase from 0.3 to 0.9 after adding background image
    enemyY_change.append(40)  # By how many pixels alien comes down when it hits the boundary

# Bullet
bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10  # Speed of bullet
bullet_state = "ready"  # Ready - You cant see the bullet on the screen and Fire - the bullet is currently moving

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game Over Text:
over_font = pygame.font.Font("freesansbold.ttf", 64)
score_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y) :
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))  # Drawing the player img


def player(x, y):
    screen.blit(playerImg, (x, y))  # Drawing the player img


def enemy(x, y, i) :
    screen.blit(enemyImg[i], (int(x), int(y)))  # Drawing the player img


def fire_bullet(x, y) :
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # 16 and 10 are added so that bullet appears to be fired from right place


def isCollision(enemyX, enemyY, bulletX, bulletY) :
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27 :  # to kill the enemy
        return True
    else :
        return False


def game_over_text() :
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))  # Drawing the player img


# # game over sound
# def sound() :
#     game_over_sound = mixer.Sound('playerkilled1.wav')
#     game_over_sound.play()
#
#
# def level_completed() :
#     score_text = score_font.render("LEVEL COMPLETED", True, (255, 255, 255))
#     screen.blit(score_text, (100, 250))


# Game loop
running = True
while running :
    # RGB - Red, Green, BLue
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

        # if Key stroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                playerX_change = -4
            if event.key == pygame.K_RIGHT :
                playerX_change = 4
            if event.key == pygame.K_SPACE :
                if bullet_state == "ready" :  # so that bullet doesnt move if space is pressed again
                    bullet_Sound = mixer.Sound('sounds/shoot1.wav')
                    bullet_Sound.play()
                    bulletX = playerX  # so that x co ordinate of bullet remains constant
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0

    # Checking for boundaries of spaceship so that it doesnt go out of bounds
    playerX += playerX_change
    if playerX <= 0 :
        playerX = 0
    elif playerX >= 736 :
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies) :

        # Game Over
        if enemyY[i] > 450 :
            for j in range(num_of_enemies) :
                enemyY[j] = 2000
            game_over_text()

            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= -25 :
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 720 :
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision :
            explosion_Sound = mixer.Sound('sounds/explosion2.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 5
            enemyX[i] = random.randint(0, 736)  # these are repeated to change the position of enemy after it is killed
            enemyY[i] = random.randint(50, 200)

        enemy(enemyX[i], enemyY[i], i)  # replaced its position in for loop

    # Bullet Movement
    if bulletY <= 40 :
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire" :
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
