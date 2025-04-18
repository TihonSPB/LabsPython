# -*- coding: utf-8 -*-

import sqlite3 # Импортировать пакет для работы с SQLite
import csv # Импортировать пакет для работы с csv файлами

NAME_DB = 'farmersmarkets.db'

def creating_or_reloading_db():
    
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
        
        print("Таблицы созданы: categories, cities, markets, markets_categories, reviews, states, users")
    except:
        print("Ошибка! Таблицы не созданы")

    # Удаление данных из таблиц
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

    # Чтение categories.csv и вставка данных в таблицу
    with open('categories.csv', 'r', encoding='utf-8') as file:
        # Пропускаем заголовок (если он есть)
        next(file)
        reader = csv.reader(file)
        # Вставляем данные
        cur.executemany('''
            INSERT INTO categories (category_id, category)
            VALUES (?, ?)
        ''', reader)
        
    # Чтение states.csv и вставка данных в таблицу
    with open('states.csv', 'r', encoding='utf-8') as file:
        # Пропускаем заголовок (если он есть)
        next(file)
        reader = csv.reader(file)
        # Вставляем данные
        cur.executemany('''
            INSERT INTO states (state_id, state_full, state_abbr)
            VALUES (?, ?, ?)
        ''', reader)

    # Чтение cities.csv и вставка данных в таблицу
    with open('cities.csv', 'r', encoding='utf-8') as file:
        # Пропускаем заголовок (если он есть)
        next(file)
        reader = csv.reader(file)
        # Вставляем данные
        cur.executemany('''
            INSERT INTO cities (city_id, city, state_id)
            VALUES (?, ?, ?)
        ''', reader)

    ## Чтение markets.csv и вставка данных в таблицу
    with open('markets.csv', 'r', encoding='utf-8') as file:
        # Пропускаем заголовок (если он есть)
        next(file)
        reader = csv.reader(file)
        # Вставляем данные
        cur.executemany('''
            INSERT INTO markets (market_id, market_name, street, city, state, zip, lat, lon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', reader)

    # Чтение markets_categories.csv и вставка данных в таблицу
    with open('markets_categories.csv', 'r', encoding='utf-8') as file:
        # Пропускаем заголовок (если он есть)
        next(file)
        reader = csv.reader(file)
        # Вставляем данные
        cur.executemany('''
            INSERT INTO markets_categories (market_category_id, market_id, category_id)
            VALUES (?, ?, ?)
        ''', reader)

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
    
    conn.close()
    
    input("нажать клавишу")
