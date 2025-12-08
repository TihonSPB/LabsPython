# -*- coding: utf-8 -*-
"""
Модель пользовательской базы данных
"""

from typing import Optional
# импорт модулей sqlalchemy и sqlalchemy.orm из пакета SQLAlchemy, псевдонимы sa и so
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone

from app import db, login

# импорт модулей для хэширования паролей и проверки без необходимости хранить исходные пароли
from werkzeug.security import generate_password_hash, check_password_hash

# импорт миксин-класса, стандартные реализации методов и свойств, необходимых Flask-Login для работы с моделью пользователя
from flask_login import UserMixin

# Импорт функции для создания MD5 хэша
from hashlib import md5


"""
Таблица user:
id | username | email | password_hash
---|----------|-------|---------------
   |          |       |
"""

class User(UserMixin, db.Model): # Класс наследуется от db.Model для работы с БД и миксин-класса для управлениями сессиями пользователей
    # so.Mapped[*] - тип столбца, указывает обязательность значения
    # so.Mapped[Optional[*]] - тип столбца, может быть пустым или обнуляемым
    # so.mapped_column() - дополнительные конфигурации столбца
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    # posts - не фактическое поле базы данных
    # so.WriteOnlyMapped - определение типа posts как тип коллекции с объектами Post внутри.
    # so.relationship() - класс модели, представляет другую сторону взаимосвязи.
    # back_populates - аргумент ссылается на имя атрибута отношения на другой стороне
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
   
    # Метод для отображения объекта при печати
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # Метод для генерации пароля
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # Метод для проверки пароля
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Метод добавляет визуальную идентификацию пользователя без хранения изображений
    def avatar(self, size):
        """
        Генерирует URL аватарки пользователя через Gravatar
        size: размер аватарки в пикселях (например, 128, 64, 32)
        """        
        # self.email.lower() - приводим email к нижнему регистру (Gravatar регистронезависимый)
        # .encode('utf-8') - преобразуем строку в байты (md5 работает с байтами)
        email_bytes = self.email.lower().encode('utf-8')
        # md5() - создает хэш-объект
        # .hexdigest() - преобразует хэш в 32-символьную шестнадцатеричную строку
        digest = md5(email_bytes).hexdigest()
        # f-строка подставляет хэш и размер
        # d=identicon - если у пользователя нет Gravatar, генерируется геометрическая иконка
        # s={size} - задает размер аватарки в пикселях
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

"""
Таблица post:
id | body | timestamp | user_id
---|------|-----------|---------
   |      |           |
"""

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140)) 
    # index=True - настроено на индексацию позволяет эффективно извлекать записи в хронологическом порядке
    # default - аргумент с лямбда функцией, которая возвращает текущее время в часовом поясе UTC
    #   Эти временные метки будут преобразованы в местное время пользователя при их отображении.
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    # user_id - внешний ключ к User.id. Поле, которое связывает публикацию с ее автором.
    # отношения один ко многим ("один" пользователь пишет "много" сообщений.)
    # index=True - добавлена явно, чтобы оптимизировать поиск по этому столбцу
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    
    # author - не фактическое поле базы данных
    # so.relationship() - класс модели, представляет другую сторону взаимосвязи.
    # back_populates - аргумент ссылается на имя атрибута отношения на другой стороне
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader # Регистрируем функцию как загрузчик для Flask-Login
def load_user(id): 
    """
    Функция-загрузчик пользователя для Flask-Login.
    Вызывается автоматически при каждом запросе для загрузки пользователя из БД.
    """
    return db.session.get(User, int(id)) # Преобразуем 'id' (str) в int и ищем в БД