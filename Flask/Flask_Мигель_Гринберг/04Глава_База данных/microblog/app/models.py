# -*- coding: utf-8 -*-
"""
Модель пользовательской базы данных
"""

from typing import Optional
# импорт модулей sqlalchemy и sqlalchemy.orm из пакета SQLAlchemy, псевдонимы sa и so
import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


"""
Таблица:
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
   
    # Метод для отображения объекта при печати
    def __repr__(self):
        return '<User {}>'.format(self.username)