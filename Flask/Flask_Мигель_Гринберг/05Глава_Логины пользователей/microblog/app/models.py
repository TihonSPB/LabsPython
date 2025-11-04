# -*- coding: utf-8 -*-
"""
Модель пользовательской базы данных
"""

from typing import Optional
# импорт модулей sqlalchemy и sqlalchemy.orm из пакета SQLAlchemy, псевдонимы sa и so
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone

from app import db


"""
Таблица user:
id | username | email | password_hash
---|----------|-------|---------------
   |          |       |
"""

class User(db.Model): # Класс наследуется от db.Model
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