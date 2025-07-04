import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("pygame")

import pygame
import random
import math
from pygame import mixer

""" AJ :
    1. pygame is not installed, throws error for me, I am lazy to install :-P
    2. always good to check if module installed, then install it for user!
"""
pygame.init()

#class for all elements in the game
class obj:
    def __init__(self, img, sizeX, sizeY, xpos, ypos, xChange, yChange):
        self.img = img
        self.img = pygame.image.load(str(self.img))
        self.img = pygame.transform.scale(self.img, (sizeX, sizeY))
        self.xpos = int(xpos)
        self.ypos = int(ypos)
        self.xChange = int(xChange)
        self.yChange = int(yChange)
        self.sizeX = int(sizeX)
        self.sizeY = int(sizeY)

#showing the elements
def show(img, x, y):
    screen.blit(img, (int(x),int(y)))


#config
speed = 2.5  #speed of space ship
go_left = pygame.K_LEFT    #change key binding (edit after "K_")
go_right = pygame.K_RIGHT   #change key binding (edit after "K_")
fire = pygame.K_SPACE   #fire bullet

#window screen
winSize = (800, 600)
screen = pygame.display.set_mode(winSize)

#Title, Icon, and bg
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
bg = pygame.image.load('bg.jpg')
bg = pygame.transform.scale(bg, winSize)
#bg music
mixer.music.load('background.wav')
mixer.music.play(-1)
lineX, lineY = (0, 460), (800, 460)

#player
player = obj("space-invaders.png", 70, 70, 370, 480, 0, 0)

#enemies
no_of_enemies = 5
enemies = []
for i in range(no_of_enemies):
    enemies.append(obj("alien.png", 70, 70, random.randint(0,720), random.randint(50, 150), 1.5, 40))

#bullet
bullet = obj("bullet.png", 35, 35, 0, 480, 0, 5)
bullet_state = "ready"  
#bullet_state = ready : can't see the bullet on screen
#bullet_state = fire : can see bullet and it is moving

def fireBullet(x,y):
    global bullet_state
    bullet_state = "fire"
    show(bullet.img, x+18, y-30)

#collision
def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx-bulletx, 2)+math.pow(enemyy-bullety, 2))
    if distance < 25:
        return True

#Score and instructions message
score = 0
font = pygame.font.Font("Antique Olive Std Nord Italic.otf", 25)
font2 = pygame.font.Font("Antique Olive Std Nord Italic.otf", 16)
textX, textY = 10,10
def show_score(x,y):
    score_img = font.render("Score : " + str(score), True, (255,255,255))
    screen.blit(score_img, (x,y))
text2X, text2Y = 225,15
def show_ins(x,y):
    ins_img = font2.render("Use left, right to move and spacebar to shoot.", True, (255,255,255))
    screen.blit(ins_img, (x,y))

#game over
over_font = pygame.font.Font("Antique Olive Std Nord Italic.otf", 50)
def game_over_text():
    over_img = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_img, (200, 250))

#game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0,0))

    #game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #player mechanics
        if event.type == pygame.KEYDOWN:
            if event.key == go_left:
                player.xChange = -(speed)
            if event.key == go_right:
                player.xChange = speed

            #firing bullets
            if event.key == fire and bullet_state=="ready":
                bullet.xpos = player.xpos
                fireBullet(bullet.xpos, bullet.ypos)
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == go_left or go_right : 
                player.xChange = 0

#Player
    #Player Border Checking
    if player.xpos <= 0:
        player.xpos = 0
    elif player.xpos >= 730:
        player.xpos = 730

    player.xpos += player.xChange
    show(player.img, player.xpos, player.ypos)

#Bullet
    #bullet movement
    if bullet.ypos<=0:
        bullet.ypos = 480
        bullet_state = "ready"
    if bullet_state == "fire" :
        fireBullet(bullet.xpos, bullet.ypos)
        bullet.ypos -= bullet.yChange
    if bullet_state == "unarmed":
        bullet.ypos = 2000

#Enemies
    for i in range(no_of_enemies):
    #Enemy Border Checking
        if enemies[i].xpos <= 0:
            enemies[i].xpos = 0
            enemies[i].xChange *= -1
            enemies[i].ypos += 40
        
        elif enemies[i].xpos >= 730:
            enemies[i].xpos = 730
            enemies[i].xChange *= -1
            enemies[i].ypos += 40

        #collision
        if isCollision(enemies[i].xpos, enemies[i].ypos, bullet.xpos, bullet.ypos):
            bullet.ypos = 480
            bullet_state = "ready"
            score += 1
            enemies[i].xpos, enemies[i].ypos = random.randint(0, 720), random.randint(50, 150)
            if enemies[i].xChange>0: 
                enemies[i].xChange += 0.2
            else:
                enemies[i].xChange -= 0.2
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
        
        #Game Over
        if enemies[i].ypos >420:
            for j in range(no_of_enemies):
                enemies[j].ypos = 2000
            game_over_text()
            player.ypos = 2000
            text2X,text2Y = 2000, 200
            textX,textY = 300, 300
            lineX, lineY = (2000,2000), (2000,2000)
            bullet_state = "unarmed"
            break

        enemies[i].xpos += enemies[i].xChange
        show(enemies[i].img, enemies[i].xpos, enemies[i].ypos)
    show_score(textX, textY)
    show_ins(text2X, text2Y)
    pygame.draw.line(screen, (255,255,255), lineX, lineY)

    pygame.display.update()
