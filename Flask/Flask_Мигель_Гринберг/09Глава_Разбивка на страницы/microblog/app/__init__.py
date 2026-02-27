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

from logging.handlers import RotatingFileHandler # Импортируем обработчик для ротации лог-файлов
import os  # Для работы с файловой системой

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
        
    
    # 1. Создаем папку для логов, если она не существует
    # Это предотвращает ошибку при попытке записи в несуществующую директорию
    if not os.path.exists('logs'):
        os.mkdir('logs')  # Создаем папку 'logs' в текущей директории
    
    # 2. Создаем ротирующий обработчик лог-файлов
    # RotatingFileHandler автоматически архивирует старые логи
    file_handler = RotatingFileHandler(
        'logs/microblog.log',  # Путь к основному лог-файлу
        maxBytes=10240,        # Максимальный размер файла (10 КБ)
        backupCount=10         # Хранить 10 архивных файлов
    )
    
    # 3. Настраиваем формат записей в логе
    file_handler.setFormatter(logging.Formatter(
        # Шаблон записи:
        # Время Уровень: Сообщение [в путь_к_файлу:номер_строки]
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    
    # 4. Устанавливаем уровень логирования для файла
    # INFO и выше: INFO, WARNING, ERROR, CRITICAL
    # DEBUG записи НЕ будут попадать в файл в продакшене
    file_handler.setLevel(logging.INFO)
    
    # 5. Добавляем обработчик к логгеру приложения
    app.logger.addHandler(file_handler)
    
    # 6. Устанавливаем общий уровень логирования для приложения
    app.logger.setLevel(logging.INFO)
    
    # 7. Записываем стартовое сообщение в лог
    app.logger.info('Microblog startup')


# Импортируем модули
# Нижний импорт - решение, позволяющее избежать циклического импорта, распространенной проблемы с приложениями Flask
from app import routes, models, errors # модули: 
# routes.py функции просмотра страниц
# models.py определяет структуру базы данных
# errors.py обработчик ошибок