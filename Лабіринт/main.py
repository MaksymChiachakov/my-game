from typing import Any
from pygame import  *
import os, sys
import sqlite3
current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from db import get_maze, delete_maze_score

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (70, 70))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()

        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_DOWN] and self.rect.y < w_h-70:
            self.rect.y += self.speed

        if keys[K_LEFT] and self.rect.x > 5:
            self.image = transform.scale(image.load("img/for maze/catch31.png"), (70, 70))
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < w_w-70:
            self.image = transform.scale(image.load("img/for maze/catch32.png"), (70, 70))
            self.rect.x += self.speed


class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 485:
            self.direction = 'right'
        if self.rect.x >= w_w-80:
            self.direction = 'left'
        if self.direction == 'right':
            self.rect.x += self.speed
            self.image = transform.scale(image.load("img/for maze/monster1.png"), (70, 70))
        else:
            self.rect.x -= self.speed
            self.image = transform.scale(image.load("img/for maze/monster2.png"), (70, 70))


class Wall(sprite.Sprite):
    def __init__(self, color, x, y, w, h):
        super().__init__()
        self.color = color
        self.width = w 
        self.height = h
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 

    def draw_wall(self):
        mw.blit(self.image,(self.rect.x, self.rect.y))
        
# Надсилання промахів у DB
def push_to_db():
    first = []
    first.append(touch)
    data = first.copy()

    int_element = data[0]

    conn = sqlite3.connect('DB.db')

        # cursor - працює з запитами у DB
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO maze (score) VALUES (?)''', [int_element])

    conn.commit()


w_w, w_h = 700, 500
mw = display.set_mode((w_w, w_h))
display.set_caption("Лабіринт")
background = transform.scale(image.load("img/for maze/background3.jpg"),(w_w, w_h))


mixer.init()
mixer.music.load('audio/for maze/jungles.ogg')
mixer.music.play()
kick = mixer.Sound('audio/for maze/kick.ogg')
money = mixer.Sound('audio/for maze/money.ogg')


font.init()
text = font.Font(None, 70)
win = text.render('YOU WIN!', 1, (255, 215, 0))
lose = text.render('TRY MORE!', True, (180, 0, 0))

player = Player("img/for maze/catch32.png", 5, w_h - 80, 4)
enemy = Enemy("img/for maze/monster2.png", w_w - 80, 280, 2)
treasure = GameSprite("img/for maze/treasure.png", w_w - 120, w_h - 80, 0)
w1 = Wall((154, 205, 50), 100, 20, 450, 10)  
w2 = Wall((154, 205, 50), 100, 480, 390, 10)
w3 = Wall((154, 205, 50), 100, 20, 10, 380)  
w4 = Wall((154, 205, 50), 200, 230, 10, 250)     
w5 = Wall((154, 205, 50), 200, 20, 10, 130)     
w6 = Wall((154, 205, 50), 300, 110, 10, 380)    
w7 = Wall((154, 205, 50), 390, 30, 10, 370)    
w8 = Wall((154, 205, 50), 480, 110, 10, 370)            
        
touch = 0
clock = time.Clock()
FPS = 60
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            push_to_db()
            get_maze()
            delete_maze_score()
            game = False

    if not finish:    
        mw.blit(background, (0,0))
        player.reset()
        player.update()
        enemy.reset()
        enemy.update()
        treasure.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()
        w8.draw_wall()


        if (
            sprite.collide_rect(player, enemy) or
            sprite.collide_rect(player, w1) or
            sprite.collide_rect(player, w2) or
            sprite.collide_rect(player, w3) or
            sprite.collide_rect(player, w4) or
            sprite.collide_rect(player, w5) or
            sprite.collide_rect(player, w6) or
            sprite.collide_rect(player, w7) or
            sprite.collide_rect(player, w8) ):
            finish = True
            mw.blit(lose, (200, 200))
            kick.play()
            touch += 1

        if sprite.collide_rect(player, treasure):
            finish = True
            mw.blit(win, (200, 200))
            money.play()
            time.wait(2000)
            push_to_db()
            get_maze()
            delete_maze_score()
            game = False

    
    else:
        time.delay(1000)
        finish = False

    display.update()   
    clock.tick(FPS)