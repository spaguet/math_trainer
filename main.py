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
def result_request(choice):
    conn = sqlite3.connect('math_trainer.db')
    cursor = conn.cursor()
    
    query = '''
    SELECT id, name, chapter, result, difficult, datetime
    FROM results
    WHERE chapter = ?
    ORDER BY result DESC
    LIMIT 10;
    '''
    
    cursor.execute(query, (choice,))
    
    results = cursor.fetchall()
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
            result_request('Сложение')
        elif choice == '2':
            result_request('Вычитание')
        elif choice == '3':
            result_request('Умножение')
        elif choice == '4':
            result_request('Деление')
        elif choice == '5':
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
    b = random.randint(1, range_limit)
    
    if chapter == 'Сложение':
        operator = '+'
    elif chapter == 'Вычитание':
        operator = '-'
    elif chapter == 'Умножение':
        operator = '*'
    else:
        operator = '/'
        
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
        try:
            range_limit = int(input('Напиши максимальное число, которое будет использовано в операциях: '))
            if range_limit < 2:
                print('Минимальное число для примеров должно быть больше 1!')
            else:
                return range_limit
        except ValueError:
            print('Пожалуйста, введи число!')
            

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