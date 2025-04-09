# -*- coding: utf-8 -*-

import sqlite3 # Импортировать пакет для работы с SQLite
import csv # Импортировать пакет для работы с csv файлами
import os  # Для работы с путями
try:
    from . import random_users  # когда импортируется как модуль
except ImportError:
    import random_users  # когда запускается напрямую    
try:
    from . import random_review  # когда импортируется как модуль
except ImportError:
    import random_review  # когда запускается напрямую

NAME_DB = os.path.join(os.path.dirname(__file__), 'farmersmarkets.db')

def creating_or_reloading_db():
    
    # Указываем путь к CSV-файлам относительно папки modul_db
    categories_csv = os.path.join(os.path.dirname(__file__), 'categories.csv')
    states_csv = os.path.join(os.path.dirname(__file__), 'states.csv')
    cities_csv = os.path.join(os.path.dirname(__file__), 'cities.csv')
    markets_csv = os.path.join(os.path.dirname(__file__), 'markets.csv')
    markets_categories_csv = os.path.join(os.path.dirname(__file__), 'markets_categories.csv')
    users_list = random_users.users_list(500) # Создаем список юзеров (количество)
    
    conn = sqlite3.connect(NAME_DB) # Создает объект connection, а также новый файл farmersmarkets.db в рабочей директории, если такого файла нет.

    cur = conn.cursor() # Создать курсор

    # Создаем таблицы и зависимости
    try:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id integer PRIMARY KEY,
            category varchar(255)
        );
        ''')
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS states (
            state_id integer PRIMARY KEY,
            state_full varchar(255),
            state_abbr character(2) NOT NULL
        );
        ''')
            
        cur.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            city_id integer PRIMARY KEY,
            city varchar(255) NOT NULL,
            state_id integer NOT NULL,
            FOREIGN KEY (state_id) REFERENCES states(state_id)
        );
        ''')
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS markets (
            market_id integer PRIMARY KEY,
            market_name varchar(255),
            street varchar(255),
            city integer,
            state integer,
            zip integer,
            lat real,
            lon real,
            FOREIGN KEY (city) REFERENCES cities(city_id),
            FOREIGN KEY (state) REFERENCES states(state_id)
        );
        ''')
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS markets_categories (
            market_category_id integer NOT NULL,
            market_id integer NOT NULL,
            category_id integer NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(category_id),
            FOREIGN KEY (market_id) REFERENCES markets(market_id)
        );
        ''')
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id integer PRIMARY KEY,
            fname varchar(255),
            lname varchar(255),
            username varchar(255) NOT NULL,
            password_hash varchar(255) NOT NULL
        );
        ''')
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            review_id integer PRIMARY KEY,
            user_id integer NOT NULL,
            market_id integer NOT NULL,
            date_time date NOT NULL,
            score smallint NOT NULL,
            review text,
            FOREIGN KEY (market_id) REFERENCES markets(market_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        ''')  
        
        conn.commit()# Сохраняет изменения для объекта соединения
        
        # print("Таблицы созданы: categories, cities, markets, markets_categories, reviews, states, users")
    except Exception as e:
        print(f"Ошибка! Таблицы не созданы: {e}")

    # Удаление данных из таблиц
    try:
        cur.execute("DELETE FROM reviews;")
        conn.commit()
        cur.execute("DELETE FROM users;")
        conn.commit()
        cur.execute("DELETE FROM markets_categories;")
        conn.commit()
        cur.execute("DELETE FROM markets;")
        conn.commit()
        cur.execute("DELETE FROM cities;")
        conn.commit()
        cur.execute("DELETE FROM states;")
        conn.commit()
        cur.execute("DELETE FROM categories;")
        conn.commit()
    except Exception as e:
        print(f"Ошибка при удалении данных: {e}")

    # Чтение categories.csv и вставка данных в таблицу
    try:
        with open(categories_csv, 'r', encoding='utf-8') as file:
            next(file)  # Пропускаем заголовок
            reader = csv.reader(file)
            cur.executemany('''
                INSERT INTO categories (category_id, category)
                VALUES (?, ?)
            ''', reader)
    except Exception as e:
        print(f"Ошибка при вставке данных в categories: {e}")

    # Чтение states.csv и вставка данных в таблицу
    try:
        with open(states_csv, 'r', encoding='utf-8') as file:
            next(file)  # Пропускаем заголовок
            reader = csv.reader(file)
            cur.executemany('''
                INSERT INTO states (state_id, state_full, state_abbr)
                VALUES (?, ?, ?)
            ''', reader)
    except Exception as e:
        print(f"Ошибка при вставке данных в states: {e}")

    # Чтение cities.csv и вставка данных в таблицу
    try:
        with open(cities_csv, 'r', encoding='utf-8') as file:
            next(file)  # Пропускаем заголовок
            reader = csv.reader(file)
            cur.executemany('''
                INSERT INTO cities (city_id, city, state_id)
                VALUES (?, ?, ?)
            ''', reader)
    except Exception as e:
        print(f"Ошибка при вставке данных в cities: {e}")

    # Чтение markets.csv и вставка данных в таблицу
    try:
        with open(markets_csv, 'r', encoding='utf-8') as file:
            next(file)  # Пропускаем заголовок
            reader = csv.reader(file)
            cur.executemany('''
                INSERT INTO markets (market_id, market_name, street, city, state, zip, lat, lon)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', reader)
    except Exception as e:
        print(f"Ошибка при вставке данных в markets: {e}")

    # Чтение markets_categories.csv и вставка данных в таблицу
    try:
        with open(markets_categories_csv, 'r', encoding='utf-8') as file:
            next(file)  # Пропускаем заголовок
            reader = csv.reader(file)
            cur.executemany('''
                INSERT INTO markets_categories (market_category_id, market_id, category_id)
                VALUES (?, ?, ?)
            ''', reader)
    except Exception as e:
        print(f"Ошибка при вставке данных в markets_categories: {e}")
        
    # Заполнение таблицы users
    try:
        # Вставляем данные
        cur.executemany('''
        INSERT INTO users (user_id, fname, lname, username, password_hash)
        VALUES (?, ?, ?, ?, ?)
        ''', users_list)
        conn.commit()
    except Exception as e:
        print(f"Ошибка при вставке данных в users: {e}")
    
    conn.commit()# Сохраняет изменения для объекта соединения
    
    conn.close()


if __name__ == "__main__":
    
    creating_or_reloading_db();
    
    conn = sqlite3.connect(NAME_DB) # Создает объект connection, а также новый файл farmersmarkets.db в рабочей директории, если такого файла нет.

    cur = conn.cursor() # Создать курсор
    
    cur.execute("SELECT * FROM categories;")
    all_results = cur.fetchall()
    print('categories результат \n', all_results) # 

    cur.execute("SELECT * FROM states;")
    all_results = cur.fetchall()
    print('states результат \n', all_results) #   

    cur.execute("SELECT * FROM cities;")
    all_results = cur.fetchall()
    print('cities результат \n', all_results) # 

    cur.execute("SELECT * FROM markets;")
    all_results = cur.fetchall()
    print('markets результат \n', all_results) # 

    cur.execute("SELECT * FROM markets_categories;")
    all_results = cur.fetchall()
    print('markets_categories результат \n', all_results) # 
    
    cur.execute("SELECT * FROM users;")
    all_results = cur.fetchall()
    print('users результат \n', all_results) # 
    
    conn.close()
    
    input("нажать клавишу")
