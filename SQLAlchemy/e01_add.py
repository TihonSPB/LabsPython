# -*- coding: utf-8 -*-

# Импортируем Session для работы с БД
from sqlalchemy.orm import Session
# Импорт компонентов из файла e00_create.py
#   engine - подключение к БД
#   User, Address - наши модели (классы)
from e00_create import engine, User, Address


# Создаем сессию для работы с БД
#   Session(engine) - создает новую сессию, привязанную к нашему движку
#   with ... as session - контекстный менеджер автоматически закрывает сессию
with Session(engine) as session:
    # СПОСОБ 1: Простое создание пользователей без связей
    # Создаем объект пользователя на основе класса User
    my_user1 = User(name="patrick", fullname="Patrick Star")
    
    # СПОСОБ 2: Создание пользователя со связанными адресами
    # Одновременно создаем User и связанные с ним Address через relationship
    my_user2 = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        # Используем связь "addresses", определенную в модели User
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )    
    
    my_user3 = User(
        name="sandy",
        fullname="Sandy Cheeks",
        # Создаем список из объектов Address
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    
    # ДОБАВЛЕНИЕ ОБЪЕКТОВ В СЕССИЮ:
    
    # Способ 1: add_all() - добавляет несколько объектов сразу
    session.add_all([my_user1, my_user2])
    # Способ 2: add() - добавляет один объект
    session.add(my_user3)
    
    # СОХРАНЕНИЕ В БАЗУ ДАННЫХ:
    # commit() - выполняет транзакцию:
    # 1. Сохраняет всех пользователей в таблицу user_account
    # 2. Сохраняет адреса в таблицу address  
    # 3. Автоматически устанавливает правильные user_id для адресов
    # 4. Фиксирует изменения в БД
    session.commit()
    
    