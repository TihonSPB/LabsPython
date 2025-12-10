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

# импортируем расширение, управляет состоянием входа пользователя в систему
from flask_login import LoginManager

# Создаём объект app как экземпляр приложения, класса Flask
# В конструктор передаём название основного файла. (__name__)
# __name__ нужен, чтобы Flask знал, где искать шаблоны (templates) и статические файлы (static).
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app) # объект db, представляющий базу данных
migrate = Migrate(app, db) # migrate, представляет механизм миграции баз данных

login = LoginManager(app) # инициализируем Flask-Login после создания экземпляра приложения

# Настраивает важное поведение безопасности
# Когда неавторизованный пользователь пытается получить доступ к защищенной странице, 
# Flask-Login автоматически перенаправляет его на страницу входа
login.login_view = 'login' # 'login' - это имя функции-обработчика маршрута /login

# Импортируем модули
# Нижний импорт - решение, позволяющее избежать циклического импорта, распространенной проблемы с приложениями Flask
from app import routes, models, errors # модули: 
# routes.py функции просмотра страниц
# models.py определяет структуру базы данных
# errors.py обработчик ошибок