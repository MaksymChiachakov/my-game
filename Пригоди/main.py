import pygame 
import os, sys
from typing import Any
import random 
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT, K_ESCAPE, KEYDOWN, K_F2, K_F3
import sqlite3
current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from db import get_sprinter, delete_sprinter_score

pygame.init()

pygame.display.set_caption('Пригоди')
FPS = pygame.time.Clock()
w, h = 1200, 800


volume_level = 0.5
pygame.mixer.init()
pygame.mixer.music.set_volume(volume_level)
pygame.mixer.music.load('audio/for hack/fon.ogg')
pygame.mixer.music.play(1000000000)
money = pygame.mixer.Sound('audio/for hack/money.ogg')
pygame.mixer.Sound.set_volume(money, volume_level)
kick = pygame.mixer.Sound('audio/for hack/kick.ogg')
pygame.mixer.Sound.set_volume(kick, volume_level)


FONT = pygame.font.SysFont('Verdana', 20)
FIN = pygame.font.SysFont('Verdana', 45)
text_font2 = pygame.font.Font(None, 40)

color_white = (255, 255, 255)
player_size = (20, 20)
color_black = (0, 0, 0)
color_blue = (0, 0 , 255)
color_red = (255, 0, 0)

main_display = pygame.display.set_mode((w, h))

health = pygame.transform.scale(pygame.image.load('img/for hack/coeur.png'), (25, 25))
health2 = pygame.transform.scale(pygame.image.load('img/for hack/coeur2.png'), (25, 25))
health3 = pygame.transform.scale(pygame.image.load('img/for hack/coeur3.png'), (25, 25))
bg = pygame.transform.scale(pygame.image.load('img/for hack/background.png'), (w,h))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Пригоди/move"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
JUMP_DOWN_PATH = 'Пригоди/jump-down'
PLAYER_JUMP_DOWN = os.listdir(JUMP_DOWN_PATH)
JUMP_UP_PATH = 'Пригоди/jump-up'
PLAYER_JUMP_UP = os.listdir(JUMP_UP_PATH)
DEAD_PATH = 'Пригоди/dead'
PLAYER_DEAD = os.listdir(DEAD_PATH)
BOOM_PATH = 'Пригоди/boom'
ENEMY_BOOM = os.listdir(BOOM_PATH)


player = pygame.image.load('img/for hack/player.png')
player_rect = player.get_rect(center=(w/2, h/2))
player_move_down = [0, 4]
player_speed_right = [4, 0]
player_speed_left = [-4, 0]
player_move_up = [0, -4]

# Надсилання очок у DB
def push_to_db():
    first = []
    first.append(score)
    data = first.copy()

    int_element = data[0]

    conn = sqlite3.connect('DB.db')

    cursor = conn.cursor()

    cursor.execute('''INSERT INTO sprinter (score) VALUES (?)''', (int_element,))

    conn.commit()

def create_enemy():
    enemy = pygame.image.load('img/for hack/enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(w, random.randint(enemy.get_height(), h - enemy.get_height()), *enemy.get_size())
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus = pygame.image.load('img/for hack/bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(300, w), -bonus.get_height(), *bonus.get_size())
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

def show_level(text_list, text_color):
    for i in range(len(text_list)):
        main_display.blit(text_font2.render(
            text_list[i], 1, text_color), (250, ((i+1)*50)))

CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
CHANGE_IMAGE = pygame.USEREVENT + 3
JUMP_IMAGE = pygame.USEREVENT + 4
pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 3000)
pygame.time.set_timer(CHANGE_IMAGE, 200)
pygame.time.set_timer(JUMP_IMAGE, 200)

enemies = []
bonuses = []


healt  = 3
score = 0
loser = ['You lose!', 'Again!']

jump_up_index = 0
jump_down_index = 0
image_index = 0
dead_index = 0
boom_index = 0
playing = True
finish = False

while playing:
    FPS.tick(660)

    for event in pygame.event.get():
        if event.type == QUIT:
            push_to_db()
            get_sprinter()
            delete_sprinter_score()
            playing = False
            
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
        elif event.type == KEYDOWN:  
            if event.key == K_F3 and volume_level < 1:
                volume_level  = round(volume_level + 0.1, 1)
                pygame.mixer.music.set_volume(volume_level)
                pygame.mixer.Sound.set_volume(money, volume_level)
                pygame.mixer.Sound.set_volume(kick, volume_level)
            if event.key == K_F2 and volume_level > 0: 
                volume_level = round(volume_level - 0.1, 1)
                pygame.mixer.music.set_volume(volume_level)
                pygame.mixer.Sound.set_volume(money, volume_level)
                pygame.mixer.Sound.set_volume(kick, volume_level)
            if event.key == K_ESCAPE:
                push_to_db()
                get_sprinter()
                delete_sprinter_score()
                playing = False
                

    
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))
    main_display.blit(health, (20, 20))
    main_display.blit(health2, (40, 20))
    main_display.blit(health3, (60, 20))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < h:
        player_rect = player_rect.move(player_move_down)
        player = pygame.image.load(os.path.join(JUMP_DOWN_PATH, PLAYER_JUMP_DOWN[jump_down_index]))
        jump_down_index += 1
        if jump_down_index >= len(PLAYER_JUMP_DOWN):
            jump_down_index = 0

    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)
        player = pygame.image.load(os.path.join(JUMP_UP_PATH, PLAYER_JUMP_UP[jump_up_index]))
        jump_up_index += 1
        if jump_up_index >= len(PLAYER_JUMP_UP):
            jump_up_index = 0

    if keys[K_RIGHT] and player_rect.right < w:
        player_rect = player_rect.move(player_speed_right)

    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_speed_left)


    
    if score == 15:
        push_to_db()
        get_sprinter()
        delete_sprinter_score()
        playing = False

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])


        if player_rect.colliderect(enemy[1]):

            player = pygame.image.load(os.path.join(DEAD_PATH, PLAYER_DEAD[dead_index]))
            kick.play()
            dead_index += 1
            if dead_index >= len(PLAYER_DEAD):
                dead_index = 0
            healt -= 1
            if healt == 2:
                health3.set_alpha(0)
            if healt ==  1:
                health2.set_alpha(0)
            if healt == 0:
                health.set_alpha(0)
                main_display.blit(FIN.render(str(loser), True, color_black), (520, h/2))
                pygame.mixer.music.stop()
                main_display.fill((255,255,255))
                show_level(loser, (0, 0, 0))
                push_to_db()
                get_sprinter()
                delete_sprinter_score()
                playing = False
                
                
            enemies.pop(enemies.index(enemy))
            

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))
            money.play()
            

    main_display.blit(FONT.render(str(score), True, color_black), (w-50, 20)) 
    main_display.blit(player, player_rect)


    pygame.display.flip()


    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > h:
            bonuses.pop(bonuses.index(bonus))