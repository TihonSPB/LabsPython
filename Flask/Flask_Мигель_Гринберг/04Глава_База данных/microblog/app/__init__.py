# -*- coding: utf-8 -*-
"""
Экземпляр приложения Flask
"""
# импортируем класс Flask из пакета flask
from flask import Flask
from config import Config

# импортируем
from flask_sqlalchemy import SQLAlchemy # ORM Для работы с БД
from flask_migrate import Migrate # миграции

# Создаём объект app как экземпляр класса Flask
# В конструктор передаём название основного файла. (__name__)
# __name__ нужен, чтобы Flask знал, где искать шаблоны (templates) и статические файлы (static).
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app) # объект db, представляющий базу данных
migrate = Migrate(app, db) # migrate, представляет механизм миграции баз данных

# Импортируем модуль routes
# Нижний импорт - решение, позволяющее избежать циклического импорта, распространенной проблемы с приложениями Flask
from app import routes, models # новый модуль models определяет структуру базы данных