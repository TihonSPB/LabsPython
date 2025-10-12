# -*- coding: utf-8 -*-

# Импорт из стандартной библиотеки
# List -  тип для аннотации списков
# Optional - тип для полей, которые могут быть None
from typing import List, Optional
# Импорты из SQLAlchemy Core
# ForeignKey - ограничение внешнего ключа (связь между таблицами на уровне БД)
# String - строковый тип данных с возможностью указания длины
# create_engine - функция для подключения к базе данных
from sqlalchemy import ForeignKey, String, create_engine
# Импорты из SQLAlchemy ORM
# DeclarativeBase - базовый класс для всех моделей
# Mapped - специальный тип для аннотации полей модели
# mapped_column - замена старого Column() (современный синтаксис)
#   Старый стиль: id = Column(Integer, primary_key=True)
#   Новый стиль: id: Mapped[int] = mapped_column(primary_key=True)
# relationship - определяет связи между моделями на уровне Python (не SQL!)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Базовый класс для всех моделей. Наследуется от DeclarativeBase (замена старого declarative_base() - более современный подход)
class Base(DeclarativeBase):
    pass


""" Аналог SQL-запроса
CREATE TABLE user_account (
    	id INTEGER NOT NULL, 
    	name VARCHAR(30) NOT NULL, 
    	fullname VARCHAR, 
    	PRIMARY KEY (id)
)

Таблица user_account:
id | name | fullname
---|------|----------
   |      |   
"""
class User(Base):
    __tablename__ = "user_account" # Имя таблицы в базе данных
    
    # Первичный ключ. Mapped[int] - аннотация типа (этот атрибут будет int)
    id: Mapped[int] = mapped_column(primary_key=True)
    # Строковое поле с ограничением длины (String(30) = VARCHAR(30))
    name: Mapped[str] = mapped_column(String(30))
    # Опциональное поле (может быть None). Без указания типа в mapped_column, тип по умолчанию (обычно Text или String)
    fullname: Mapped[Optional[str]] 
    """
    Связь один-ко-многим с таблицей Address
    поле addresses будет списком объектов Address
    List["Address"] - у одного User может быть несколько Address
    back_populates="user" - создает двустороннюю связь
    cascade="all, delete-orphan" - каскадные операции:
        all - все операции каскадируются
        delete-orphan - при удалении User удаляются все связанные Address
        также при удалении Address из списка, он удаляется из БД
    """
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")
    # Метод для отображения объекта при печати
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


""" Аналог SQL-запроса
CREATE TABLE address (
	id INTEGER NOT NULL, 
	email_address VARCHAR NOT NULL, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user_account (id)
)

Таблица address:
id | email_address | user_id
---|---------------|--------
   |               |
"""
class Address(Base):
    __tablename__ = "address" # Имя таблицы в базе данных
    
    # Первичный ключ. Mapped[int] - аннотация типа (этот атрибут будет int)
    id: Mapped[int] = mapped_column(primary_key=True)
    # Обязательное строковое поле (не может быть None)
    email_address: Mapped[str]
    # Внешний ключ, ссылается на user_account.id
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    """
    Связь многие-к-одному. Каждый Address принадлежит одному User
    back_populates="addresses" - обратная связь к User.addresses
    """
    user: Mapped["User"] = relationship(back_populates="addresses")
    # Метод для отображения объекта при печати
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# 1. СОЗДАЕМ ДВИЖОК - подключение к БД
#   SQLite сохранит данные в файл mydatabase.db
#   echo=True все SQL-запросы в консоли (полезно для отладки!) Для продакшена echo=False
engine = create_engine("sqlite:///mydatabase.db", echo=False)
"""
Альтернативные строки подключения:
    
# SQLite в памяти (временная БД)
engine = create_engine("sqlite:///:memory:", echo=True)

# PostgreSQL
engine = create_engine("postgresql://user:password@localhost/mydb")

# MySQL
engine = create_engine("mysql+pymysql://user:password@localhost/mydb")
"""

# 2. СОЗДАЕМ ТАБЛИЦЫ В БАЗЕ ДАННЫХ
#   Base.metadata содержит информацию о ВСЕХ наших моделях
#   create_all() генерирует CREATE TABLE для User и Address
#   Если таблицы уже существуют - ничего не происходит
#   Для продакшена лучше использовать миграции (Alembic) вместо create_all
Base.metadata.create_all(engine)