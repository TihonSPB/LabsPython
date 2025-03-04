# -*- coding: utf-8 -*-

####################################################################################### MySQL or PostgreSQL
# Модель (Model)
# Работа с данными. Ответ на запросы от основного приложения
import os # Для работы с путями
import sqlite3 # Импортировать пакет для работы с SQLite

#????????????????????????????????????
# Сообщение для тестирования, можно переделать для log файлов
def test_msg(msg):
    symbol = "!"
    frame_length = len(msg) + 4
    horizontal_frame = "\n" + symbol * frame_length + symbol * 2
    vertical_indentation = "\n" + symbol + " " * frame_length + symbol
    info_msg = "\n" + symbol + " " * 2 + msg + " " * 2  + symbol
    print(horizontal_frame + vertical_indentation + info_msg + vertical_indentation + horizontal_frame + "\n")
    
#????????????????????????????????????

try:
    from modul_db import creating_farmersmarkets_db_sqlite_db as fm_db
except Exception as e:
    test_msg(f"Ошибка modul_db! Error: {str(e)}")
   
# Путь к БД
db_path = os.path.join(os.path.dirname(__file__), 'modul_db', 'farmersmarkets.db')

# Создание новой БД или сброс к первоначальной.
def database_reset():
    fm_db.creating_or_reloading_db()
    test_msg(f"Файл базы данных создан: {db_path}")
    
# Проверка наличия БД
def database_check():
    if not(os.path.exists(db_path)):
        database_reset()
        
#--------------------------------------------------------------------------------------
# Чтение нормализация файла, или установка подключения к БД

# Декоратор подключения к БД
def db_connection(func):    
    def wrap():
        # Проверка наличия файла базы данных
        database_check()        
        conn = sqlite3.connect(db_path) # Создает объект connection
        cur = conn.cursor() # Создать курсор
        try:            
            result = func(cur)
            # Фиксация изменений
            conn.commit()
            # test_msg("Test commit!")
        except Exception as e:
            # Откат в случае ошибки
            conn.rollback()
            test_msg(f"Test rollback! Error: {str(e)}")
        finally:
            # Закрытие соединения
            cur.close()
            conn.close()
            # test_msg("Test close!")
            return result
    return wrap

#--------------------------------------------------------------------------------------
# Чтение данных
# Вывод всех рынков
@db_connection
def show_all(cur):
    cur.execute("SELECT * FROM markets;")
    return cur.fetchall() # 

# Поиск рынка по id

# Поиск id рынков по почтовому индексу

# Поиск id рынков по городу и штату

# Поиск рынков по отдалению от почтового индекса (30 миль)

#--------------------------------------------------------------------------------------
# Редактирование данных

#--------------------------------------------------------------------------------------
# Удаление данных

#######################################################################################
# Утилита (Util) Универсальная программа для расчета

#######################################################################################
# Представление (View) Отвечает за вывод пользователю
#import tabulate ?????????????????? Вылетает

def print_prompt():    
    print("""Команды: 
          
    1 - Удалить все изменения, внесенные в базу данных.
    2 - Просмотр списка всех фермерских рынков в стране (включая рецензии и рейтинги).
    3 - Поиск фермерского рынка по городу и штату.
    4 - Поиск фермерского рынка по почтовому индексу с возможностью ограничить зону поиска дальностью.
    5 - Подробная информация о рынке.
    0 - Выход.
          
Введите команду => """, end='')

    
def print_command(command):
    print(command)

def print_invalid_command():
    print("Неверная команнда")
    
def print_newline():
    print()
    
def print_exit():
    print("Выход")
    
def print_table(my_list):
    print(my_list)
    #print_list = tabulate.tabulate(my_list)
    #print(print_list)

#######################################################################################
# Контроллер (Controller)
# Взаимодействует с пользователем (Принимает ввод от пользователя). Соединяет модель и представление

if __name__ == "__main__":
    
    def new_db():
        database_reset()
    def process_two():
        print_table(show_all())
    def process_three():
        pass
        
    command = ""
        
    while command != '0':
                        
        print_prompt()
        command = input()
        print_command(command)
        command = command.strip().lower()
        if command == '1':
            new_db()
        elif command == '2':
            process_two()
        elif command == '3':
            process_three()
        elif command != '0':
            print_invalid_command()
        print_newline()
        
    print_exit()