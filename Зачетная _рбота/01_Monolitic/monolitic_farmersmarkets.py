# -*- coding: utf-8 -*-

#######################################################################################
# Утилита (Util) Универсальная программа для расчета расстояния на поверхности земли

import math

EARTH_RADIUS_MI = 3958.8
def calculate_distance(location1, location2):
    
    lat1 = math.radians(location1[0])
    lat2 = math.radians(location2[0])
    long1 = math.radians(location1[1])
    long2 = math.radians(location2[1])
    del_lat = (lat1 - lat2) / 2
    del_long = (long1 - long2) / 2
    angle = math.sin(del_lat)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(del_long)**2
    distance = 2 * EARTH_RADIUS_MI * math.asin(math.sqrt(angle))
    return distance

####################################################################################### MySQL or PostgreSQL
# Модель (Model)
# Работа с данными. Ответ на запросы от основного приложения
import os # Для работы с путями
import sqlite3 # Импортировать пакет для работы с SQLite

#???????????????????????????????????? Поместить в представление (View) или в отдельный класс
# Сообщение для тестирования, можно переделать для log файлов
def print_msg(msg):
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
    print_msg(f"Ошибка modul_db! Error: {str(e)}")
   
# Путь к БД
db_path = os.path.join(os.path.dirname(__file__), 'modul_db', 'farmersmarkets.db')

# Создание новой БД или сброс к первоначальной.
def database_reset():
    fm_db.creating_or_reloading_db()
    print_msg(f"Файл базы данных создан: {db_path}")
    
# Проверка наличия БД
def database_check():
    if not(os.path.exists(db_path)):
        database_reset()
        
#--------------------------------------------------------------------------------------
# Чтение нормализация файла, или установка подключения к БД

# Декоратор подключения к БД
def db_connection(func):    
    def wrap(*args, **kwargs): # функция wrap принимает *args и **kwargs, что позволяет передавать произвольное количество позиционных и именованных аргументов в обернутую функцию
        # Проверка наличия файла базы данных
        database_check()        
        conn = sqlite3.connect(db_path) # Создает объект connection
        cur = conn.cursor() # Создать курсор
        try:            
            result = func(cur, *args, **kwargs)
            # Фиксация изменений
            conn.commit()
        except Exception as e:
            # Откат в случае ошибки
            conn.rollback()
            print_msg(f"Test rollback! Error: {str(e)}")
        finally:
            # Закрытие соединения
            cur.close()
            conn.close()
            return result
    return wrap

#--------------------------------------------------------------------------------------
# Чтение данных
# Вывод всех рынков
@db_connection
def show_all(cur):
    cur.execute('''
        SELECT 
            markets.market_id,
            markets.market_name,
            cities.city,
            states.state_abbr,
            markets.zip
        FROM 
            markets
        JOIN 
            cities ON markets.city = cities.city_id
        JOIN 
            states ON markets.state = states.state_id
        GROUP BY 
            markets.market_id, markets.market_name, cities.city, states.state_abbr, markets.zip;''')
    return cur.fetchall()

# Поиск фермерских рынка по городу и штату.
@db_connection
def search_markets_loc(cur, city, state):
    cur.execute('''
        SELECT 
            m.market_id,
            m.market_name,
            c.city,
            s.state_abbr,
            m.zip
        FROM 
            markets m
        JOIN 
            cities c ON m.city = c.city_id
        JOIN 
            states s ON m.state = s.state_id
        WHERE lower(c.city) = ? AND lower(s.state_abbr) = ?
        ''', (city.lower(), state.lower()))
    return cur.fetchall()

# Поиск рынков по отдалению от id рынка (30 миль)
@db_connection
def search_markets_dist(cur, id_market, my_dist = 30):

    # Сначала получаем координаты переданного market_id
    cur.execute("SELECT lat, lon FROM markets WHERE market_id = ?", (id_market,))
    target_location = cur.fetchone()

    if not target_location or target_location[0] == '' or target_location[1] == '':
        return []
    
    # Получаем все рынки
    cur.execute('''
        SELECT 
            markets.market_id,
            markets.market_name,
            cities.city,
            states.state_abbr,
            markets.zip,
            markets.lat,
            markets.lon
        FROM 
            markets
        JOIN 
            cities ON markets.city = cities.city_id
        JOIN 
            states ON markets.state = states.state_id
        GROUP BY 
            markets.market_id, markets.market_name, cities.city, states.state_abbr, markets.zip, markets.lat, markets.lon;''')
    all_markets = cur.fetchall()
    
    # Фильтруем по расстоянию
    nearby_markets = []
    for market in all_markets:
        *market_info, lat, lon = market
        if lat != '' or lon != '':
            distance = calculate_distance(target_location, (lat, lon))
            if distance <= my_dist:
                #print(distance)#TEST///TEST///TEST///TEST///
                nearby_markets.append(tuple(market_info))
    return nearby_markets

# Поиск полной информации рынка по id
@db_connection
def market_search_by_id(cur, id_market):
    cur.execute('''
        SELECT 
            m.market_id,
            m.market_name,
            m.street,
            c.city,
            s.state_full,
            s.state_abbr,
            m.zip,
            m.lat,
            m.lon,
            GROUP_CONCAT(categories.category, ', ') AS categories
        FROM 
            markets m
        JOIN 
            cities c ON m.city = c.city_id
        JOIN 
            states s ON m.state = s.state_id
        LEFT JOIN 
            markets_categories ON m.market_id = markets_categories.market_id
        LEFT JOIN 
            categories ON markets_categories.category_id = categories.category_id
        WHERE m.market_id = ?
        GROUP BY 
            m.market_id, m.market_name, m.street, c.city, s.state_full, s.state_abbr, m.zip, m.lat, m.lon;
        ''', (id_market, ))
    return cur.fetchall()

#--------------------------------------------------------------------------------------
# Редактирование данных

#######################################################################################
# Представление (View) Отвечает за вывод пользователю
import tabulate #?????????????????? Вылетает в консоли (Написать свою таблицу)

def print_prompt():    
    print("""Команды: 
          
    1 - Удалить все изменения, внесенные в базу данных.
    2 - Просмотр списка всех фермерских рынков в стране (включая рецензии и рейтинги).
    3 - Поиск фермерского рынка по городу и штату.
    4 - Поиск фермерского рынка по id с возможностью ограничить зону поиска дальностью.
    5 - Подробная информация о рынке.
    0 - Выход.
          
Введите команду => """, end='')

    
# def print_command(command):
#     print(command)

def print_invalid_command():
    print("Неверная команда")
    
def print_newline():
    print()

def print_request_city():
    print("Введите город => ", end='')

def print_request_state():
    print("Введите штат => ", end='')

def print_request_id():
    print("Введите id рынка => ", end='')
    
def print_request_radius():
    print("Введите радиус поиска рынков, в милях => ", end='')

def print_not_found():
    print("Не найдено!")

def print_exit():
    print("Выход")

def print_table(my_list):
    # print(my_list)     
    print(tabulate.tabulate(my_list))
    
#######################################################################################
# Контроллер (Controller)
# Взаимодействует с пользователем (Принимает ввод от пользователя). Соединяет модель и представление

if __name__ == "__main__":    
#--------------------------------------------------------------------------------------
# Тестирование    
    passed = 0
    failed = 0
    # тест 1 Проверка кол-во рынков
    if (len(show_all())==1680):
        passed += 1
    else:
        print_msg("ОШИБКА тест 1.")
        failed += 1
    
    # тест 2 Проверка фермерского рынка по городу и штату
    if (search_markets_loc("San Francisco", "CA")==[(1009080, 'San Francisco Certified Alemany Farmers Market', 'San Francisco', 'CA', 94110), (1020193, 'Ferry Plaza Farmers Market', 'San Francisco', 'CA', 94111), (1020195, 'Mission Community Market', 'San Francisco', 'CA', 94111)]):
        passed += 1
    else:
        print_msg("ОШИБКА тест 2.")
        failed += 1
    
    # тест 3 Проверка
    if (search_markets_loc("san francisco", "ca")==[(1009080, 'San Francisco Certified Alemany Farmers Market', 'San Francisco', 'CA', 94110), (1020193, 'Ferry Plaza Farmers Market', 'San Francisco', 'CA', 94111), (1020195, 'Mission Community Market', 'San Francisco', 'CA', 94111)]):
        passed += 1
    else:
        print_msg("ОШИБКА тест 3.")
        failed += 1
    
    # тест 4 Проверка подробной информации о рынке
    if (market_search_by_id("1021728")==[(1021728, 'Burrillville Farmers Market', '75 Tinkham Lane', 'Harrisville', 'Rhode Island', 'RI', 2830, 41.967496, -71.677124, 'Organic, Crafts, Flowers, Eggs, Herbs, Vegetables, Honey, Jams, Meat, Soap, Trees, Coffee, Fruits, WildHarvested')]):
        passed += 1
    else:
        print_msg("ОШИБКА тест 4.")
        failed += 1
        
    # тест 5 Проверка неправильного ввода id поиск по зоне
    if (search_markets_dist("Привет мир!")==[]):
        passed += 1
    else:
        print_msg("ОШИБКА тест 5.")
        failed += 1
        
    # тест 6 Проверка ввода id рынка (поиск по зоне) с отсутствующими координатами
    if (search_markets_dist("1011689")==[]):
        passed += 1
    else:
        print_msg("ОШИБКА тест 6.")
        failed += 1
#3///NEW///START///NEW///START///NEW///START///NEW///START///NEW///START///NEW///START         
    # print (search_markets_dist("Привет мир!"))
    # print (search_markets_dist("1011689"))    
    # print(market_search_by_id("1021728"))
    # print_table(search_markets_loc("Chicago", "IL"))
    # print(search_markets_loc("San Francisco", "CA"))
#3///NEW///END///NEW///END///NEW///END///NEW///END///NEW///END///NEW///END///NEW///END    
    # Итог тестирования
    if (failed == 0):
        print(f'Все тесты ({passed}) успешно пройдены')
    else:
        print(f'Провалено {failed} тестов.{passed} успешно пройдены') 
        

#--------------------------------------------------------------------------------------    
    def new_db():
        database_reset()
    def process_two():
        print_table(show_all())
    def process_three():
        print_request_city()
        desired_city = input()
        print_request_state()
        desired_state = input()
        state_and_city_markets = search_markets_loc(desired_city, desired_state)
        if len(state_and_city_markets) != 0:
            print_table(state_and_city_markets)
        else:
            print_not_found()
    def process_four():
        print_request_id()
        market = input()
        print_request_radius()
        radius = input()
        try:
            radius = float(radius)
        except ValueError:
            print_not_found()
            return
        dist_markets = search_markets_dist(market, radius)
        if len(dist_markets) != 0:
            print_table(dist_markets)
        else:
            print_not_found()
    def process_five():
        print_request_id()
        market_info = market_search_by_id(input())
        if len(market_info) != 0:
            print(market_info)
        else:
            print_not_found()
        
    command = ""
        
    while command != '0':
                        
        print_prompt()
        command = input()
        # print_command(command)
        command = command.strip().lower()
        if command == '1':
            new_db()
        elif command == '2':
            process_two()
        elif command == '3':
            process_three()
        elif command == '4':
            process_four()
        elif command == '5':
            process_five()
        elif command != '0':
            print_invalid_command()
        print_newline()
        
    print_exit()