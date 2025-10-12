# -*- coding: utf-8 -*-

from sqlalchemy import select
# Импортируем Session для работы с БД
from sqlalchemy.orm import Session
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


# Создаем сессию для работы с БД
# Session(engine) - создает новую сессию, привязанную к нашему движку. Это как "рабочая область" где происходят все операции с БД
session = Session(engine)


############# 1. ПРОСТОЙ SELECT - ВСЕ ПОЛЬЗОВАТЕЛИ #############
my_select1 = select(User) # Создаем запрос "SELECT * FROM user_account"

# session.scalars() - выполняет запрос и возвращает объекты моделей (User)
# .all() - получает все результаты сразу в виде списка
my_data1 = session.scalars(my_select1).all()
print(f"Найдено пользователей: {len(my_data1)}") # Найдено пользователей: 3
print(my_data1) # [User(id=1, name='patrick', fullname='Patrick Star'), User(id=2, name='spongebob', fullname='Spongebob Squarepants'), User(id=3, name='sandy', fullname='Sandy Cheeks')]
print(my_data1[0]) # User(id=1, name='patrick', fullname='Patrick Star')
print(my_data1[0].fullname) # Patrick Star
# Альтернатива: итерация по результатам (экономит память для больших данных)
for user in session.scalars(my_select1):
    print(user) # Каждый 'user' - это объект класса User
    """ 
    User(id=1, name='patrick', fullname='Patrick Star')
    User(id=2, name='spongebob', fullname='Spongebob Squarepants')
    User(id=3, name='sandy', fullname='Sandy Cheeks')
    """


############# 2. SELECT ОТДЕЛЬНЫХ ПОЛЕЙ (только имена) #############
my_select2 = select(User.name, User.fullname) # Выбираем только конкретные поля

# session.execute() возвращает строки, а не объекты моделей
my_data2 = session.execute(my_select2).all()
print(my_data2) # [('patrick', 'Patrick Star'), ('spongebob', 'Spongebob Squarepants'), ('sandy', 'Sandy Cheeks')]
print(my_data2[1]) # ('spongebob', 'Spongebob Squarepants')
print(my_data2[1].fullname) # Spongebob Squarepants
print(my_data2[1][1]) # Spongebob Squarepants
for name, fullname in session.execute(my_select2):
    print(f"Имя: {name}, Полное имя: {fullname}")
    """
    Имя: patrick, Полное имя: Patrick Star
    Имя: spongebob, Полное имя: Spongebob Squarepants
    Имя: sandy, Полное имя: Sandy Cheeks
    """


############# 3. SELECT С ФИЛЬТРАЦИЕЙ (WHERE) - точное совпадение имени #############
my_select3 = select(User).where(User.name == "spongebob")

# .one() - возвращает ОДИН результат. Выбросит ошибку если:
# - нет результатов (NoResultFound)
# - больше одного результата (MultipleResultsFound)
my_data3 = session.scalars(my_select3).one()
print(my_data3) # User(id=2, name='spongebob', fullname='Spongebob Squarepants')
print(my_data3.id) # 2


############# 4. SELECT С ФИЛЬТРАЦИЕЙ (WHERE) - по точному совпадению имен #############
my_select4 = select(User).where(User.name.in_(["spongebob", "patrick"]))

# .fetchall() - явно получаем все результаты (аналог .all())
my_data4 = session.scalars(my_select4).fetchall()
print(my_data4) # [User(id=1, name='patrick', fullname='Patrick Star'), User(id=2, name='spongebob', fullname='Spongebob Squarepants')]


############# 5. SELECT С ФИЛЬТРОМ (LIKE) поиск по шаблону - по первой букве имен #############
my_select5 = select(User).where(User.name.like("s%")) # Имена начинающиеся на 's'

# Комбинируем .execute() и .scalars() для получения объектов
my_data5 = session.execute(my_select5).scalars().all()
print(my_data5) # [User(id=2, name='spongebob', fullname='Spongebob Squarepants'), User(id=3, name='sandy', fullname='Sandy Cheeks')]


############# 6. SELECT С СОРТИРОВКОЙ (ORDER BY) - по имени #############
my_select6 = select(User).order_by(User.name) # Сортировка по возрастанию
# Для убывания: .order_by(User.name.desc())

my_data6 = session.execute(my_select6).scalars().all()
print("Пользователи отсортированные по name:")
for user in my_data6:
    print(f"{user.name}")
    """
    Пользователи отсортированные по name:
    patrick
    sandy
    spongebob
    """


############# 7. SELECT С ОГРАНИЧЕНИЕМ (LIMIT) #############
my_select7 = select(User).limit(2) # Берем только первые 2 записи

my_data7 = session.execute(my_select7).scalars().all()
print("Первые 2 пользователя:")
for user in my_data7:
    print(f"{user}")
    """
    Первые 2 пользователя:
    User(id=1, name='patrick', fullname='Patrick Star')
    User(id=2, name='spongebob', fullname='Spongebob Squarepants')
    """


############# 8. SELECT СО СВЯЗАННЫМИ ТАБЛИЦАМИ (JOIN) #############
my_select8 = (
    select(Address)
    .join(Address.user) # JOIN между address и user_account
    .where(User.name == "sandy")
    .where(Address.email_address == "sandy@sqlalchemy.org")
    )

my_data8 = session.scalars(my_select8).one()
print(my_data8) # Address(id=2, email_address='sandy@sqlalchemy.org')


############# 9. SELECT СО СВЯЗАННЫМИ ТАБЛИЦАМИ (JOIN) - все связанные адреса пользователя #############
my_select9 = (
    select(Address)
    .join(Address.user)
    .where(User.name == "sandy")
    )

my_data9 = session.execute(my_select9).scalars().all()
print(my_data9) # [Address(id=2, email_address='sandy@sqlalchemy.org'), Address(id=3, email_address='sandy@squirrelpower.org')]


############# 10. SELECT СО СВЯЗАННЫМИ ТАБЛИЦАМИ (JOIN) - данные пользователя + адреса пользователя #############
my_select10 = (
    select(User, Address)
    .join(User.addresses, isouter=True)  # LEFT OUTER JOIN
    .where(User.name == "sandy")
    .order_by(Address.id)
    )

my_data10 = session.execute(my_select10).all()
print(my_data10)
""" Вывод
[(User(id=3, name='sandy', fullname='Sandy Cheeks'), Address(id=2, email_address='sandy@sqlalchemy.org')), 
 (User(id=3, name='sandy', fullname='Sandy Cheeks'), Address(id=3, email_address='sandy@squirrelpower.org'))]
"""

# Вывод данных 
if my_data10:
    user = my_data10[0][0]  # Первый User из первой строки
    print(f"=== Информация о пользователе {user.name} ===")
    print(f"ID: {user.id}")
    print(f"Полное имя: {user.fullname}")
    print("Email адреса:")
    
    for row in my_data10:
        address = row[1]  # Address из каждой строки
        if address:  # Проверка на случай NULL из LEFT JOIN
            print(f"  - {address.email_address} (ID: {address.id})")
else:
    print("Пользователь не найден")
    
"""
=== Информация о пользователе sandy ===
ID: 3
Полное имя: Sandy Cheeks
Email адреса:
  - sandy@sqlalchemy.org (ID: 2)
  - sandy@squirrelpower.org (ID: 3)
"""


# ВАЖНО: Всегда закрывайте сессию чтобы освободить соединения с БД
session.close()