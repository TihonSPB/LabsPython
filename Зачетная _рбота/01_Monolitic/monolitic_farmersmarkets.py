# -*- coding: utf-8 -*-

#######################################################################################
# Представление (View) Отвечает за вывод пользователю

MINS_IN_HOUR = 60
SECS_IN_MIN = 60
ROW_COUNT = 20

def degree_minutes_seconds(location): # Разбивка локации на градусы, минуты, секунды

    minutes, degrees = math.modf(location)
    degrees = int(degrees)
    minutes *= MINS_IN_HOUR
    seconds, minutes = math.modf(minutes)
    minutes = int(minutes)
    seconds = SECS_IN_MIN * seconds
    return degrees, minutes, seconds # Кортеж

def format_location(location): # Вывод градусов в формате (025°44'16.00"N,080°13'29.17"W)
    
    # Если location пустой (None или пустой список/кортеж), возвращаем пустую строку
    if not location[0] or not location[1] or len(location) < 2:
        return "отсутствуют"
    
    # Определяем полушарие 
    ns = ""
    if location[0] < 0:
        ns = 'S'
    elif location[0] > 0:
        ns = 'N'

    ew = ""
    if location[1] < 0:
        ew = 'W'
    elif location[1] > 0:
        ew = 'E'

    format_string = '{:03d}\xb0{:0d}\'{:.2f}"' # Градусы{:03d}-(03-3 знака; d-целое число); \xb0-символ "°"; Минуты{:0d}\'-0 будет сохраннен; Секунды{:.2f}"-Дробное с двумя знаками после запятой.
    latdegree, latmin, latsecs = degree_minutes_seconds(abs(location[0]))
    latitude = format_string.format(latdegree, latmin, latsecs)
    longdegree, longmin, longsecs = degree_minutes_seconds(abs(location[1]))
    longitude = format_string.format(longdegree, longmin, longsecs)
    return '(' + latitude + ns + ',' + longitude + ew + ')'

# Сообщение для тестирования, можно переделать для log файлов
def print_msg(msg):
    symbol = "!"
    frame_length = len(msg) + 4
    horizontal_frame = "\n" + symbol * frame_length + symbol * 2
    vertical_indentation = "\n" + symbol + " " * frame_length + symbol
    info_msg = "\n" + symbol + " " * 2 + msg + " " * 2  + symbol
    print(horizontal_frame + vertical_indentation + info_msg + vertical_indentation + horizontal_frame + "\n")

def print_request_username():
    print("\nВведите имя пользователя: ", end='')
    
def print_request_password():
    print("Введите пароль: ", end='')
    
def print_authorization_failed():
    print("Неверное имя пользователя или пароль!")
    
def print_logout():
    print("Вы вышли из системы.")
    
def print_login():
    print("Успешный вход!")
    
def print_login_error():
    print("Ошибка входа!")
    
def print_require_auth():
    print("Для этого действия требуется войти в систему")
    
def print_prompt(user):
    name, lastname, username = user
    auth_str = ""
    in_out_str = "Вход"
    if username:
        auth_str = f"{name} {lastname} |{username}| "
        in_out_str = "Выход пользователя"
    
    print(f"""{auth_str}Команды: 
    
    D - Удалить все изменения, внесенные в базу данных.
    1 - {in_out_str} {username}
    2 - Просмотр списка всех фермерских рынков в стране.
    3 - Поиск фермерского рынка по городу и штату.
    4 - Поиск фермерского рынка по id с возможностью ограничить зону поиска дальностью.
    5 - Подробная информация о рынке.(включая рецензии и рейтинги)
    6 - Оценить рынок, оставить отзыв
    0 - Закрыть.
          
Введите команду => """, end='')

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

def print_table(my_list, headers=None): # Печать списка оформленного в таблицу
        
    if not my_list:
        return
    # Определяем количество столбцов (по первому кортежу)
    num_columns = len(my_list[0])
    
    # Проверяем, что все кортежи имеют одинаковую длину
    for t in my_list:
        if len(t) != num_columns:
            raise ValueError("Все кортежи должны иметь одинаковое количество элементов")
    
    # Если заголовки переданы, проверяем их длину
    if headers is not None:
        if len(headers) != num_columns:
            raise ValueError("Количество заголовков должно совпадать с количеством столбцов")
    
    # Находим максимальную ширину для каждого столбца (учитывая заголовки, если они есть)
    column_widths = [0] * num_columns
    for t in my_list:
        for i in range(num_columns):
            column_widths[i] = max(column_widths[i], len(str(t[i])))
    
    # Если есть заголовки, проверяем их ширину
    if headers is not None:
        for i in range(num_columns):
            column_widths[i] = max(column_widths[i], len(str(headers[i])))
            
    # Функция для создания разделительной строки
    def make_separator():
        return " ".join("-" * width for width in column_widths)
    
    # Функция для форматирования строки (с выравниванием по левому краю)
    def format_row(row_items):
        formatted = []
        for i in range(num_columns):
            # Форматируем каждый элемент с учетом максимальной ширины столбца
            # str(t[i]) - Преобразует элемент кортежа в строку
            # :< - Спецификатор форматирования ":" - начало блока форматирования "<" - выравнивание по левому краю
            # column_widths[i] - Минимальная ширина. Строка дополнена пробелами справа если короче
            formatted.append(f"{str(row_items[i]):<{column_widths[i]}}")
        return (" ".join(formatted))
    
    # Печатаем верхнюю границу таблицы
    print(make_separator())
    
    # Если есть заголовки, печатаем их
    if headers is not None:
        print(format_row(headers))
        print(make_separator())
    
    # Печатаем строки таблицы
    for t in my_list:
        print(format_row(t))
        
    # Печатаем нижнюю границу таблицы
    print(make_separator())

def print_paged_tuples(tuples_list, headers=None, rows_per_page = ROW_COUNT): # Постраничный вывод кортежа
    total_pages = (len(tuples_list) + rows_per_page - 1) // rows_per_page
    
    for page in range(total_pages):
        start_idx = page * rows_per_page
        end_idx = start_idx + rows_per_page
        
        print_table(tuples_list[start_idx:end_idx], headers)
        
        if page < total_pages - 1:
            user_input = input(f"Страница {page + 1}/{total_pages}. Нажмите Enter для продолжения или 'q'+Enter для выхода...\n")
            if user_input.lower() == 'q':
                print("Вывод прерван.")
                return
    
    print(f"Конец данных. Всего страниц: {total_pages}.")
    
def print_markets(tuples_list):
    headers = ["ID", "Наименование", "Город", "Штат", "Индекс", "Рейтинг"]
    print_paged_tuples(tuples_list, headers)
    
def print_market_info(market_info):
    location = market_info[0][7:9]
    print(f"""
-------------------
Наименование рынка: {market_info[0][1]}
------
Адрес: {market_info[0][2]}, {market_info[0][3]}, {market_info[0][5]}({market_info[0][4]}), {str(market_info[0][6])}
-----------
Координаты: {format_location(location)}
--------------------
Категории продуктов: {market_info[0][9]}""")
    
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
            result = []
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
            markets.zip,
            COALESCE(ROUND(AVG(r.score), 1), '-') AS avg_rating
        FROM 
            markets
        JOIN 
            cities ON markets.city = cities.city_id
        JOIN 
            states ON markets.state = states.state_id
        LEFT JOIN 
            reviews r ON markets.market_id = r.market_id
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
            m.zip,
            COALESCE(ROUND(AVG(r.score), 1), '-') AS avg_rating
        FROM 
            markets m
        JOIN 
            cities c ON m.city = c.city_id
        JOIN 
            states s ON m.state = s.state_id
        LEFT JOIN 
            reviews r ON m.market_id = r.market_id
        WHERE lower(c.city) = ? AND lower(s.state_abbr) = ?
        GROUP BY 
            m.market_id, m.market_name, c.city, s.state_abbr, m.zip
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
            COALESCE(ROUND(AVG(r.score), 1), '-') AS avg_rating,
            markets.lat,
            markets.lon
        FROM 
            markets
        JOIN 
            cities ON markets.city = cities.city_id
        JOIN 
            states ON markets.state = states.state_id
        LEFT JOIN 
            reviews r ON markets.market_id = r.market_id
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

# Поиск рецензий и рейтингов по id рынка
@db_connection
def reviews_search_by_id_market(cur, id_market):
    cur.execute('''
        SELECT 
            u.fname, u.lname, r.score, r.review, r.date_time
        FROM 
            reviews r
        JOIN users u ON r.user_id = u.user_id
        WHERE r.market_id = ?
        ORDER BY r.date_time DESC;
        ''', (id_market, ))
    return cur.fetchall()

#???NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///1 Тестовая
# Получение пользователей
@db_connection
def users_all(cur):
    cur.execute("SELECT * FROM users;")
    return cur.fetchall()

@db_connection
def reviews_test(cur):
    cur.execute("SELECT * FROM reviews;")
    return cur.fetchall()
#???NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///1 Тестовая

# Получение пользователя
@db_connection
def user_by_username(cur, username):
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cur.fetchone()  # Получаем первую найденную запись

#--------------------------------------------------------------------------------------
# Редактирование данных

#######################################################################################
# Класс AuthController (Ядро аутентификации)
from getpass import getpass  # Для безопасного ввода пароля
# from werkzeug.security import generate_password_hash, check_password_hash

class AuthController:
    def __init__(self):
        self.current_user = None  # ID текущего пользователя (None если не авторизован)
        self.name = ""
        self.lastname = ""
        self.username = ""  # Имя пользователя для отображения
        self.password_hash = ""  # Хеш пароля (можно использовать для проверок)
   
    def get_user(self, username):        
        user = user_by_username(username)        
        return user  # Возвращает кортеж с данными пользователя или None
   
    def verify_password(self, stored_hash, password):
        # Проверяет соответствие пароля его хешу
        # В реальном приложении использовать:
        # from werkzeug.security import check_password_hash
        # return check_password_hash(stored_hash, password)
        return stored_hash == password  # Временная заглушка!

    def login(self):
        #Обрабатывает процесс входа пользователя
        print_request_username()
        username = input()
        # print_request_password()
        password = getpass()  # Скрытый ввод пароля
        
        user = self.get_user(username)  # Ищем пользователя в БД
        
        if user and self.verify_password(user[4], password):
            # Если пользователь найден и пароль верный:
            self.current_user = user[0]  # Сохраняем ID (первое поле в таблице)
            self.name = user[1]
            self.lastname = user[2]
            self.username = username
            self.password_hash = user[4]  # Поле с хешем пароля
            return True
        print_authorization_failed()
        return False  # Авторизация не удалась
    
    def logout(self):
        #Сбрасывает данные авторизации
        self.current_user = None
        self.name = ""
        self.lastname = ""
        self.username = ""
        self.password_hash = ""

    def require_auth(self):
        # Проверяет авторизацию, если нет - предлагает войти
        if not self.current_user:            
            print_require_auth()
            if self.login():  # Предлагаем войти
                return True  # Пользователь успешно авторизовался
            return False  # Пользователь не смог войти
        return True  # Уже авторизован


#######################################################################################
# Контроллер (Controller)
# Взаимодействует с пользователем (Принимает ввод от пользователя). Соединяет модель и представление
import random

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
    if ([t[:-1] for t in search_markets_loc("San Francisco", "CA")]==[(1009080, 'San Francisco Certified Alemany Farmers Market', 'San Francisco', 'CA', 94110), (1020193, 'Ferry Plaza Farmers Market', 'San Francisco', 'CA', 94111), (1020195, 'Mission Community Market', 'San Francisco', 'CA', 94111)]):
        passed += 1
    else:
        print_msg("ОШИБКА тест 2.")
        failed += 1
    
    # тест 3 Проверка
    if ([t[:-1] for t in search_markets_loc("san francisco", "ca")]==[(1009080, 'San Francisco Certified Alemany Farmers Market', 'San Francisco', 'CA', 94110), (1020193, 'Ferry Plaza Farmers Market', 'San Francisco', 'CA', 94111), (1020195, 'Mission Community Market', 'San Francisco', 'CA', 94111)]):
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
    
#???NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///2 Тестовая         
    # print (search_markets_dist("Привет мир!"))
    # print (search_markets_dist("1011689"))    
    # print(market_search_by_id("1021728"))
    # print_table(search_markets_loc("Chicago", "IL"))
    # print([t[:-1] for t in search_markets_loc("San Francisco", "CA")])
    # print_table(user_users_all())
    # print_table(reviews_test())
#???NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///2 Тестовая    
    # Итог тестирования
    if (failed == 0):
        print(f'Все тесты ({passed}) успешно пройдены')
    else:
        print(f'Провалено {failed} тестов.{passed} успешно пройдены') 
        
#--------------------------------------------------------------------------------------    
#???NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///3 Тестовая
    def user_login_password():
        print("\nДля входа воспользуйтесь одной из учетных записей: ")
        tuples_list = users_all()
        # Выбираем случайные кортежи
        random_tuples = random.sample(tuples_list, min(3, len(tuples_list)))
        # Оставляем только два последних элемента в каждом кортеже
        result = [t[-2:] for t in random_tuples]
        
        print_table(result, ["Имя пользователя", "Пароль"])
#???NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///3 Тестовая
    auth = AuthController()
    def new_db():
        database_reset()
    def process_one():
        if auth.current_user:
            auth.logout()
            print_logout()
        else:
#???NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///4 Тестовая
            user_login_password()
#???NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///4 Тестовая
            if auth.login():
                print_login()
            else:
                print_login_error()
    def process_two():
        print_markets(show_all())
    def process_three():
        print_request_city()
        desired_city = input()
        print_request_state()
        desired_state = input()
        state_and_city_markets = search_markets_loc(desired_city, desired_state)
        if len(state_and_city_markets) != 0:
            print_markets(state_and_city_markets)
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
            print_markets(dist_markets)
        else:
            print_not_found()
    def process_five():
        print_request_id()
        market_id = input()
        market_info = market_search_by_id(market_id)
        if len(market_info) != 0:
            print_market_info(market_info)
            print_paged_tuples(reviews_search_by_id_market(market_id))
        else:
            print_not_found()
    def process_six():
        if not auth.require_auth(): # Проверка авторизации
#???NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///5 Тестовая
            user_login_password()
#???NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///NEW\\\NEW///5 Тестовая
            return
        print("Выполнение функции!")
        
    command = ""
        
    while command != '0':
        
        print_prompt([auth.name, auth.lastname, auth.username])
        command = input()
        
        command = command.strip().lower()
        if command == 'd':
            new_db()
        elif command == '1':
            process_one()
        elif command == '2':
            process_two()
        elif command == '3':
            process_three()
        elif command == '4':
            process_four()
        elif command == '5':
            process_five()
        elif command == '6':
            process_six()
        elif command != '0':
            print_invalid_command()
        print_newline()
        
    print_exit()