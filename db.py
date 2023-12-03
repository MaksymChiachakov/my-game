import sqlite3, datetime

# Підключаємось до нашої DB
conn = sqlite3.connect('DB.db')

# cursor - працює з запитами у DB
cursor = conn.cursor()

today = datetime.datetime.now()

# Clear
def clear_file(filename):
    with open(filename, 'w') as file:
        file.truncate(0)  # Обрізати файл до нульової довжини

# Приклад використання:
filename = 'scores.txt'

# List
#records = []

# Посилаємо - запит у DB
def get_catch():
    cursor.execute('''SELECT MAX(score) FROM catch''')
    
    cursor.execute('SELECT name FROM users WHERE id = (SELECT MAX(id) FROM users)')

    player = cursor.fetchall()

    catch = cursor.fetchall()

    try:
        # Читаємо вміст файлу
        with open('scores.txt', 'r') as file:
            content = file.read()
            # Перевіряємо чи число вже є в файлі
            if str(f'Catch:\n{catch}') in content:
                pass
            else:
                # Додаємо число до файлу
                with open('scores.txt', 'a') as file:
                    file.write(f'\nGame: Catch\nPlayer: {player}\nScores: {catch}, \nDate: {today}\n')


    except FileNotFoundError:
        print('Файл не знайдено.')




def delete_catch_score():
    cursor.execute('''SELECT score FROM catch''')
    del_catch = cursor.fetchall()
    if len(del_catch) >= 2:
        cursor.execute('''DELETE FROM catch
                        WHERE score < (SELECT MAX(score) FROM catch)''')
        conn.commit()

def get_maze():
    cursor.execute('''SELECT MAX(score) FROM maze''')

    cursor.execute('SELECT name FROM users WHERE id = (SELECT MAX(id) FROM users)')

    player = cursor.fetchall()

    maze = cursor.fetchall()

    try:
        # Читаємо вміст файлу
        with open('scores.txt', 'r') as file:
            content = file.read()
            # Перевіряємо чи число вже є в файлі
            if str(f'\nMaze:\n{maze}, date: {today}\n') in content:
                pass
            else:
                # Додаємо число до файлу
                with open('scores.txt', 'a') as file:
                    file.write(f'\nGame: Maze\nPlayer: {player}\nScores: {maze}, \nDate: {today}\n')

    except FileNotFoundError:
        print('Файл не знайдено.')

def delete_maze_score():
    cursor.execute('''SELECT score FROM maze''')
    del_maze = cursor.fetchall()
    if len(del_maze) >= 2:
        cursor.execute('''DELETE FROM maze
                        WHERE score < (SELECT MAX(score) FROM maze)''')
        conn.commit()

def get_sprinter():
    cursor.execute('''SELECT MAX(score) FROM sprinter''')

    sprinter = cursor.fetchall()

    cursor.execute('SELECT name FROM users WHERE id = (SELECT MAX(id) FROM users)')

    player = cursor.fetchall()

    try:
        # Читаємо вміст файлу
        with open('scores.txt', 'r') as file:
            content = file.read()
            # Перевіряємо чи число вже є в файлі
            if str(f'\nSprinter:\n{sprinter}, date: {today}\n') in content:
                pass
            else:
                # Додаємо число до файлу
                with open('scores.txt', 'a') as file:
                    file.write(f'\nGame: Sprinter\nPlayer: {player}\nScores: {sprinter}, \nDate: {today}\n')

    except FileNotFoundError:
        print('Файл не знайдено.')

def delete_sprinter_score():
    cursor.execute('''SELECT score FROM sprinter''')
    del_sprinter = cursor.fetchall()
    if len(del_sprinter) >= 2:
        cursor.execute('''DELETE FROM sprinter
                        WHERE score < (SELECT MAX(score) FROM sprinter)''')
        conn.commit()


def addNickname(name):
    cursor.execute("""INSERT INTO users (name) VALUES (?)""", (name,))
    conn.commit()


def TestNickname(name):
    try:
        cursor.execute("""SELECT name FROM users WHERE name = (?)""", (name,))
        nick = cursor.fetchall()
        conn.commit()
        if nick == []:
            return True
        else:
            return False
    except:
        print("Error while adding user")
    
    

# Виключаємо підключення до нашої DB, після цього, ми не зможемо надсилати запити 
conn.commit()