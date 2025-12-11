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

# Импортируем модули для логирования
import logging
from logging.handlers import SMTPHandler  # Обработчик логов, отправляющий письма

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


# Условие: НЕ в режиме отладки (debug=False)
# В разработке ошибки показываются в браузере, в продакшене - отправляются на email
if not app.debug:
    # Проверяем, настроен ли почтовый сервер в конфигурации (config.py)
    if app.config['MAIL_SERVER']:
        # 1. Настройка аутентификации для почтового сервера
        auth = None  # По умолчанию без аутентификации
        
        # Если в конфигурации (config.py) есть логин и пароль
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            # Создаем кортеж с учетными данными
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        
        # 2. Настройка безопасного соединения
        secure = None  # По умолчанию без шифрования
        
        # Если в конфигурации (config.py) включен TLS
        if app.config['MAIL_USE_TLS']:
            secure = ()  # Пустой кортеж включает TLS
            
        # 3. Создаем обработчик логов для отправки email
        mail_handler = SMTPHandler(
            # Адрес почтового сервера и порт из конфигурации (config.py)
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),            
            # Отправитель (no-reply чтобы не отвечали на письма об ошибках)
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],            
            # Получатели - список администраторов из конфигурации (config.py)
            toaddrs=app.config['ADMINS'],            
            # Тема письма
            subject='Microblog Failure',            
            # Учетные данные (логин/пароль)
            credentials=auth,            
            # Настройки шифрования
            secure=secure
        )
        
        # 4. Настраиваем уровень логирования
        # Будем получать письма только при ОШИБКАХ (ERROR и выше)
        mail_handler.setLevel(logging.ERROR)
        
        # 5. Добавляем обработчик к логгеру приложения
        app.logger.addHandler(mail_handler)


# Импортируем модули
# Нижний импорт - решение, позволяющее избежать циклического импорта, распространенной проблемы с приложениями Flask
from app import routes, models, errors # модули: 
# routes.py функции просмотра страниц
# models.py определяет структуру базы данных
# errors.py обработчик ошибок