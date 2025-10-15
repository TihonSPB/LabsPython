# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
# Импорт компонентов из файла e00_create.py
#   engine - подключение к БД
#   User, Address - наши модели (классы)
from e00_create import engine, User, Address


"""
Состояние базы данных после выполнения e03_delete.py:

Таблица user_account:
id | name      | fullname
---|-----------|------------------------
1  | patrick   | Patrick Super Star
2  | spongebob | Spongebob Squarepants
3  | sandy     | Sandy Cheeks

Таблица address:
id | email_address                     | user_id
---|-----------------------------------|--------
1  | spongebob@sqlalchemy.org          | 2
2  | sandy@sqlalchemy.org              | 3
3  | new_email@sandy.org               | 3
4  | patrick_super_star@sqlalchemy.org | 1
"""


session = Session(engine)

try:
    user = session.get(User, 2)
    if user:
        print(f"Удаляем пользователя: {user.name}")
        session.delete(user)
        session.commit()
        print("✅ Пользователь удален")
    else:
        print("❌ Пользователь с id=2 не найден")
except Exception as e:
    session.rollback()
    print(f"❌ Ошибка при удалении: {e}")
finally:
    session.close()

"""
Таблица user_account:
id | name      | fullname
---|-----------|------------------------
1  | patrick   | Patrick Super Star    
3  | sandy     | Sandy Cheeks

Таблица address:
id | email_address                     | user_id
---|-----------------------------------|--------
2  | sandy@sqlalchemy.org              | 3
3  | new_email@sandy.org               | 3
4  | patrick_super_star@sqlalchemy.org | 1
"""