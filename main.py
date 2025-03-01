import time
import random
import threading
import sqlite3
import os
import platform


time_up = False


# ---------------------- Инициализация БД
def initialize_db():
    conn = sqlite3.connect('math_trainer.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS results
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     chapter TEXT NOT NULL,
                     result INTEGER NOT NULL,
                     difficult INTEGER NOT NULL,
                     datetime TEXT NOT NULL)''')
    conn.commit()
    conn.close()


# ---------------------- Добавление результата в БД
def add_result(name, chapter, points, difficult):
    conn = sqlite3.connect('math_trainer.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (name, chapter, result, difficult, datetime) VALUES (?,?,?,?,?)",
                   (name, chapter, points, difficult, time.strftime('%H:%M %d-%m-%Y')))
    conn.commit()
    conn.close()
    

# ---------------------- Запрос 10 лучших результатов из БД
def result_request(chapter, difficult):
    conn = sqlite3.connect('math_trainer.db')
    cursor = conn.cursor()
    
    query = '''
    SELECT id, name, chapter, result, difficult, datetime
    FROM results
    WHERE chapter = ? AND difficult = ?
    ORDER BY result DESC
    LIMIT 10;
    '''
    
    cursor.execute(query, (chapter, difficult,))
    
    results = cursor.fetchall()
    
    if not results:
        clear_terminal()
        print('Ещё никто не пробовал свои силы в этом разделе. Пробуй ты!')
    else:
        place = 0
        for row in results:
            place += 1
            print('----------------------------------------')
            print(f'Место в рейтинге: {place}')
            print(f'Имя: {row[1]}')
            print(f'Раздел: {row[2]}')
            print(f'Результат: {row[3]} очков')
            print(f'Максимальный операнд: {row[4]}')
            print(f'Дата: {row[5]}')
            print('----------------------------------------')
    
    conn.close()
    
    menu_confirm = input('Для возврата в главное меню введи любой символ.')
    if menu_confirm is not None:
        main()
    

# ---------------------- Меню выбора раздела ТОП-10 результатов
def show_best():
    clear_terminal()
    
    while True:
        print('Выбери раздел:')
        print('1. Сложение ТОП-10')
        print('2. Вычитание ТОП-10')
        print('3. Умножение ТОП-10')
        print('4. Деление ТОП-10')
        print('5. Назад в меню')
        
        choice = input('>>> ')
        
        if choice == '1':
            choose_num_limit('Сложение')
        elif choice == '2':
            choose_num_limit('Вычитание')
        elif choice == '3':
            choose_num_limit('Умножение')
        elif choice == '4':
            choose_num_limit('Деление')
        elif choice == '5':
            main()
        else:
            print('Неверный запрос. Попробуй ещё раз!')


# ---------------------- Меню выбора раздела ТОП-10 результатов
def choose_num_limit(chapter):
    clear_terminal()
    
    while True:
        print('Выбери раздел:')
        print('1. Операнды до 10')
        print('2. Операнды до 100')
        print('3. Операнды до 1000')
        print('4. Операнды до 10000')
        print('5. Операнды до 100000')
        print('6. Операнды до 1000000')
        print('7. Выход в главное меню.')
        
        choice = input('>>> ')
        
        if choice == '1':
            result_request(chapter, 10)
        elif choice == '2':
            result_request(chapter, 100)
        elif choice == '3':
            result_request(chapter, 1000)
        elif choice == '4':
            result_request(chapter, 10000)
        elif choice == '5':
            result_request(chapter, 100000)
        elif choice == '6':
            result_request(chapter, 1000000)
        elif choice == '7':
            main()
        else:
            print('Неверный запрос. Попробуй ещё раз!')
            

# ---------------------- Очистка терминала
def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
        

# ---------------------- Склонение слова "очко"
def points_declension(points):
    if points == 1:
        return 'очко'
    elif points in range(2, 5):
        return 'очка'
    else:
        return 'очков'


# ---------------------- Генератор уравнения
def math_generator(range_limit, chapter):
    a = random.randint(1, range_limit)
    
    if chapter == 'Сложение':
        operator = '+'
        b = random.randint(1, range_limit)
    elif chapter == 'Вычитание':
        operator = '-'
        b = random.randint(1, a)
    elif chapter == 'Умножение':
        operator = '*'
        b = random.randint(1, range_limit)
    elif chapter == 'Деление':
        operator = '/'
        b = random.randint(1, a)
        while a % b != 0:
            b = random.randint(1, a)
        
    problem = f'{a} {operator} {b}'
    answer = eval(problem)
    return problem, answer


# ---------------------- Метематическая викторина
def math_quiz(range_limit, name, chapter):
    global time_up
    time_up = False
    start_time = time.time()
    time_limit = 60
    points = 0
    str_points = points_declension(points)
    
    threading.Thread(target=timer).start
    
    while not time_up:
        problem, answer = math_generator(range_limit, chapter)
        print(f'Реши пример: {problem} =')
        
        while not time_up:
            try:
                user_answer = int(input('>>> '))
                if user_answer == answer:
                    print('Верно!')
                    points += 1
                    break
                else:
                    print('Неверно!')
                    print(f'Попробуй ещё раз: {problem} =')
            except ValueError:
                print('Пожалуйста, введи число!')
        
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit:
            time_up = True
            clear_terminal()
            print('Время вышло!')
            print(f'Ты набрал {points} {str_points}!')
            add_result(name, chapter, points, range_limit)
            input('Нажми ENTER, что бы вернуться в главное меню.')
            main()


# ---------------------- Таймер
def timer():
    global time_up
    time.sleep(60)
    time_up = True
    print('Время вышло!')


# ---------------------- Выбор максимального числа для примеров
def range_limit_choice():
    while True:
        print('Выбери максимальный операнд:')
        print('1. До 10')
        print('2. До 100')
        print('3. До 1000')
        print('4. До 10000')
        print('5. До 100000')
        print('6. До 1000000')
        
        range_choice = input('>>> ')
        
        if range_choice == '1':
            range_limit = 10
            return range_limit
        elif range_choice == '2':
            range_limit = 100
            return range_limit
        elif range_choice == '3':
            range_limit = 1000
            return range_limit
        elif range_choice == '4':
            range_limit = 10000
            return range_limit
        elif range_choice == '5':
            range_limit = 100000
            return range_limit
        elif range_choice == '6':
            range_limit = 1000000
            return range_limit
        else:
            print('Некорректный выбор. Введи ещё раз!')
            

# ---------------------- Главное меню
def main():
    clear_terminal()
 
    while True:
        print('Привет, дорогой ученик!')
        name = input('Введи своё имя: ')
        print('Выбери тему для практики:')
        print('1. Сложение')
        print('2. Вычитание')
        print('3. Умножение')
        print('4. Деление')
        print('5. Просмотр 10 лучших результатов')
        print('6. Выход')
        
        math_choice = input('>>> ')
        
        if math_choice == '1':
            clear_terminal()
            print('Ответь на все вопросы за 60 секунд!')
            range_limit = range_limit_choice()
            math_quiz(range_limit, name, 'Сложение')
        elif math_choice == '2':
            clear_terminal()
            print('Ответь на все вопросы за 60 секунд!')
            range_limit = range_limit_choice()
            math_quiz(range_limit, name, 'Вычитание')
        elif math_choice == '3':
            clear_terminal()
            print('Ответь на все вопросы за 60 секунд!')
            range_limit = range_limit_choice()
            math_quiz(range_limit, name, 'Умножение')
        elif math_choice == '4':
            clear_terminal()
            print('Ответь на все вопросы за 60 секунд!')
            range_limit = range_limit_choice()
            math_quiz(range_limit, name, 'Деление')
        elif math_choice == '5':
            show_best()
        elif math_choice == '6':
            clear_terminal()
            print('Пока! До скорых встреч!')
            break
        else:
            clear_terminal()
            print('Некорректный запрос. Попробуй ещё раз!')


if __name__ == '__main__':
    initialize_db()
    main()