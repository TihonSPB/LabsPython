# -*- coding: utf-8 -*-

####################################################################################### MySQL or PostgreSQL
# Модель (Model)
# Работа с данными. Ответ на запросы от основного приложения
import os # Для работы с путями
import sqlite3 # Импортировать пакет для работы с SQLite
from modul_db import creating_farmersmarkets_db_sqlite_db as fm_db

# Путь к БД
db_path = os.path.join(os.path.dirname(__file__), 'modul_db', 'farmersmarkets.db')

#????????????????????????????????????
# Сообщение для тестирования, можно переделать для log файлов
def test_msg(msg):
    frame_length = len(msg) + 4
    horizontal_frame = "#" * frame_length + "##"
    vertical_indentation = " " * frame_length
    print("\n" + horizontal_frame + "\n#" + vertical_indentation + "#\n#  " + msg + "  #\n#" + vertical_indentation + "#\n" + horizontal_frame + "\n")
    
#????????????????????????????????????

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
            func(cur)
            # Фиксация изменений
            conn.commit()
            test_msg("Test commit!")
        except:
            # Откат в случае ошибки
            conn.rollback()
            test_msg("Test rollback!")
        finally:
            # Закрытие соединения
            cur.close()
            conn.close()
            test_msg("Test close!")
    return wrap

#--------------------------------------------------------------------------------------
# Чтение данных

@db_connection
def my_test(cur):
    cur.execute("SELECT * FROM markets;")
    all_results = cur.fetchall()
    print('markets результат \n', all_results) # 

# Вывод всех рынков

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


def print_prompt():
    print("""Команды: 
          
    newdb - Удалить все изменения, внесенные в базу данных.
    two - Просмотр списка всех фермерских рынков в стране (включая рецензии и рейтинги).
    three - Поиск фермерского рынка по городу и штату.
    # - Поиск фермерского рынка по почтовому индексу с возможностью ограничить зону поиска дальностью.
    # - Подробная информация о рынке.
    end - Выход.
          
Введите команду => """, end='')
    
def print_command(command):
    print(command)

def print_invalid_command():
    print("Неверная команнда")
    
def print_newline():
    print()
    
def print_exit():
    print("Выход")

#######################################################################################
# Контроллер (Controller)
# Взаимодействует с пользователем (Принимает ввод от пользователя). Соединяет модель и представление

if __name__ == "__main__":
    
    def new_db():
        database_reset()
    def process_two():
        my_test()
    def process_three():
        pass
        
    command = ""
        
    while command != 'end':
                        
        print_prompt()
        command = input()
        print_command(command)
        command = command.strip().lower()
        if command == 'newdb':
            new_db()
        elif command == 'two':
            process_two()
        elif command == 'three':
            process_three()
        elif command != 'end':
            print_invalid_command()
        print_newline()
    print_exit()