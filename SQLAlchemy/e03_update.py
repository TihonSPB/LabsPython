# -*- coding: utf-8 -*-

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
# Импорт компонентов из файла e00_create.py
#   engine - подключение к БД
#   User, Address - наши модели (классы)
from e00_create import engine, User, Address


"""
Состояние базы данных после выполнения e01_add.py:

Таблица user_account:
id | name      | fullname
---|-----------|-------------------
1  | patrick   | Patrick Star
2  | spongebob | Spongebob Squarepants
3  | sandy     | Sandy Cheeks

Таблица address:
id | email_address            | user_id
---|--------------------------|--------
1  | spongebob@sqlalchemy.org | 2
2  | sandy@sqlalchemy.org     | 3
3  | sandy@squirrelpower.org  | 3
"""


############# 1. БЕЗОПАСНОЕ ДОБАВЛЕНИЕ НОВЫХ ДАННЫХ #############
# Создаем сессию для работы с БД
#   Session(engine) - создает новую сессию, привязанную к нашему движку
#   with ... as session - контекстный менеджер автоматически закрывает сессию session.close()
with Session(engine) as session:
    """
    my_select1 = select(User).where(User.name == "patrick")
   
    my_data1 = session.scalars(my_select1).one()
    my_data1.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
   
    session.commit()
    """
   
    try:
        # Находим пользователя (с обработкой ошибок)
        my_data1 = session.scalar(select(User).where(User.name == "patrick")) # Используем scalar() для одного результата
       
        if my_data1:
            # Способ 1: Через relationship
            # Добавляем новый адрес
            new_address = Address(email_address="patrickstar@sqlalchemy.org")
            my_data1.addresses.append(new_address)
           
            # Альтернативный способ: прямое создание с user_id
            # new_address = Address(
            #     email_address="patrickstar@sqlalchemy.org",
            #     user_id=my_data1.id
            # )
            # session.add(new_address)
           
            session.commit()
            print(f"✅ Добавлен адрес для {my_data1.name}")
        else:
            print("❌ Пользователь не найден")
           
    except Exception as e:
        session.rollback() # ОТКАТ всех изменений
        print(f"❌ Ошибка при добавлении адреса: {e}")
   
    """
    Таблица address:
    id | email_address              | user_id
    ---|----------------------------|--------
    1  | spongebob@sqlalchemy.org   | 2
    2  | sandy@sqlalchemy.org       | 3
    3  | sandy@squirrelpower.org    | 3
    4  | patrickstar@sqlalchemy.org | 1     *
    """


############# 2. ОБНОВЛЕНИЕ ДАННЫХ #############
with Session(engine) as session:
    """
    my_select2 = select(User).where(User.name == "sandy")
   
    my_data2 = session.scalars(my_select2).one()
    my_data2.addresses[1].email_address = "new_email@sandy.org"
   
    session.commit()
    """
   
    try:
        # Находим пользователя
        my_data2 = session.scalar(
            select(User)
            .where(User.name == "sandy")
        )
       
        if my_data2 and my_data2.addresses:
            print(f"Найдено адресов у пользователя {my_data2.name}: {len(my_data2.addresses)}")
           
            # Безопасное обновление - проверяем существование индекса
            if len(my_data2.addresses) > 1:
                old_email = my_data2.addresses[1].email_address
                my_data2.addresses[1].email_address = "new_email@sandy.org"
               
                session.commit()
                print(f"✅ Адрес обновлен: {old_email} → new_email@sandy.org")
            else:
                print("⚠️ У пользователя меньше 2 адресов, нельзя обновить addresses[1]")
        else:
            print("❌ Пользователь не найден или нет адресов")
           
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка при обновлении адреса: {e}")
   
    """
    Таблица address:
    id | email_address              | user_id
    ---|----------------------------|--------
    1  | spongebob@sqlalchemy.org   | 2
    2  | sandy@sqlalchemy.org       | 3
    3  | new_email@sandy.org        | 3     *
    4  | patrickstar@sqlalchemy.org | 1
    """
   
   
############# 2. ОБНОВЛЕНИЕ ВСЕХ ДАННЫХ ПОЛЬЗОВАТЕЛЯ В ОДНОЙ ТРАНЗАКЦИИ #############
with Session(engine) as session:  # ← ОДНА сессия
    try:
        # 1. Находим пользователя с адресами
        user = session.scalar(
            select(User)
            .where(User.id == 1)
            .options(selectinload(User.addresses)) # ← Жадно загружаем адреса
        )
       
        if not user:
            print("Пользователь не найден")
       
        # 2. ВСЕ изменения в одной транзакции
        # Меняем имя пользователя
        user.fullname = 'Patrick Super Star'
       
        # Меняем первый email адрес
        if user.addresses:
            user.addresses[0].email_address = 'patrick_super_star@sqlalchemy.org'
        else:
            # Если адреса нет - создаем новый
            new_address = Address(email_address='patrick_super_star@sqlalchemy.org')
            user.addresses.append(new_address)
       
        # 3. КОММИТ ВСЕХ ИЗМЕНЕНИЙ ОДНОВРЕМЕННО
        session.commit()  # ← ОДНА транзакция
        print("✅ Все данные пользователя обновлены")
       
    except Exception as e:
        session.rollback()  # Откат ВСЕХ изменений если что-то пошло не так
        print(f"❌ Ошибка: {e}")
       
    """
    Таблица user_account:
    id | name      | fullname
    ---|-----------|-----------------------
    1  | patrick   | Patrick Super Star     *
    2  | spongebob | Spongebob Squarepants
    3  | sandy     | Sandy Cheeks

    Таблица address:
    id | email_address                     | user_id
    ---|-----------------------------------|--------
    1  | spongebob@sqlalchemy.org          | 2
    2  | sandy@sqlalchemy.org              | 3
    3  | new_email@sandy.org               | 3
    4  | patrick_super_star@sqlalchemy.org | 1      *
    """