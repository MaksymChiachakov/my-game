import pygame 
import subprocess, os
import webbrowser 
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT, K_ESCAPE
import pyautogui as pg
from db import addNickname, TestNickname

pygame.init()
# Задання властивостей нашому додатку
w = pygame.display.set_mode((500, 500))
w.fill((230, 230, 250))
clock = pygame.time.Clock()
pygame.display.set_caption('Менеджер')


# Клас поля
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = (30, 144, 255)
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(w, self.fill_color, self.rect)


# Клас зображень
class Picture(Area):
    def __init__(self, filename, x, y, width=10, height=10, color=None):
        Area.__init__(self, x, y, width, height, color)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw_picture(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


# Клас надписів 
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.text = text
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw_text(self, shift_x=0, shift_y=0):
        w.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


# Створення об'єктів для головного меню
menu_start = Picture('img/for menu/start_button.png', 200, 100, 100, 100)
menu_exit = Picture('img/for menu/exit_button.png', 220, 370, 50, 50)
menu_settings = Picture('img/for menu/settings_button.png', 20, 20, 50, 50)


# Створення об'єктів для меню настройок
sett_info = Label(25, 50, 100, 150)
sett_info.set_text('Щоб ознайомитися з документацією, нажміть на іконку "Файл" знизу.')
sett_back = Picture('img/for menu/return_button.png', 230, 370, 50, 50)
sett_documentary = Picture('img/for menu/documentary.png', 435, 430, 50, 50)

# Створення об'єктів для меню гри
play_info = Label(25, 50, 100, 150)
play_info.set_text('Щоб почати грати - виберіть 1 з 3-х ігор запропонованих нами:')
sett_1 = Picture('img/for menu/1.png', 70, 200, 100, 100)
sett_2 = Picture('img/for menu/2.png', 200, 200, 100, 100)
sett_3 = Picture('img/for menu/3.png', 330, 200, 100, 100)
sett_4 = Picture('img/for menu/star.png', 420, 420, 70, 70)
sett4_info = Label(25, 50, 100, 150)
sett4_info.set_text('Test')

""" font.init()
text_font = font.Font(None, 40)
# Показ
def show_level(text_list):
    for i in range(len(text_list)):
        w.blit(text_font.render(
            text_list[i], 1), (25, ((i+1)*50))) """

# Відкриття документації у браузері
def open_documentary():
    docs_path = 'github.com/MaksymChiachakov/project/blob/main/docs/documentary.md'
    documentary = 'https://{}'.format(docs_path)
    webbrowser.open(documentary)    

# Відкриваємо текстовий документ
def open_scores():
    filename = 'scores.txt'
    os.startfile(filename)

# Створення функцій для запускання ігор
def run_game1():
    game_file_path = 'Доганялки/main.py'
    try:
        subprocess.run(['python', game_file_path])
    except FileNotFoundError:
        print(f"Файл '{game_file_path}' не знайдено.")

def run_game2():
    game_file_path = 'Лабіринт/main.py'
    try:
        subprocess.run(['python', game_file_path])
    except FileNotFoundError:
        print(f"Файл '{game_file_path}' не знайдено.")

def run_game3():
    game_file_path = 'Пригоди/main.py'
    try:
        subprocess.run(['python', game_file_path])
    except FileNotFoundError:
        print(f"Файл '{game_file_path}' не знайдено.")


# Получаємо нікнейм користувача
while True:
    pg.alert("Welcome", "You are ready?", button="Yeah!")
    nickname = pg.prompt("Enter your nickname", "Your nickname")

    if TestNickname(name=nickname):
        addNickname(name=nickname)
        break
    else:
        response = pg.confirm("This nickname is already in use. Would you like to change it?", buttons=["Yes", "No"])
        if response == "No":
            break



# Ігровий цикл з меню
screen = 'menu'
while True:
    # Головне меню
    w.fill((230, 230, 250))
    if screen == 'menu':
        menu_start.draw_picture()
        menu_settings.draw_picture()
        menu_exit.draw_picture()


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menu_start.rect.collidepoint(x, y):
                    screen = 'game_start'
                if menu_settings.rect.collidepoint(x, y):
                    screen = 'settings'
                if menu_exit.rect.collidepoint(x, y):
                    pygame.quit()

            if event.type == pygame.QUIT:
                pygame.quit()
                    
    # Меню настройок
    elif screen == 'settings':
        sett_info.draw_text()
        sett_back.draw_picture()
        sett_documentary.draw_picture()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if sett_back.rect.collidepoint(x, y):
                    screen = 'menu'
                if sett_documentary.rect.collidepoint(x, y):
                    open_documentary()
            if event.type == pygame.QUIT:
                pygame.quit()

    # Ігрове меню
    elif screen == 'game_start':
        play_info.draw_text()
        sett_1.draw_picture()
        sett_2.draw_picture()
        sett_3.draw_picture()
        sett_4.draw_picture()
        sett_back.draw_picture()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if sett_back.rect.collidepoint(x, y):
                    screen = 'menu'
                if sett_1.rect.collidepoint(x, y):
                    run_game1()
                    screen = 'game_start'
                if sett_2.rect.collidepoint(x, y):
                    run_game2()
                    screen = 'game_start'
                if sett_3.rect.collidepoint(x, y):
                    run_game3()
                    screen = 'game_start'    
                if sett_4.rect.collidepoint(x, y):
                    open_scores()

            if event.type == pygame.QUIT:
                pygame.quit()

      
    clock.tick(40)
    pygame.display.update()

