# -*- coding: utf-8 -*-
"""
Класс Config в модуле config, для хранения переменных конфигурации
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Настройка секретного ключа
    Flask и некоторые из его расширений используют значение секретного ключа
    в качестве криптографического ключа, полезного для генерации подписей или
    токенов.Flask-WTF использует его для защиты веб-форм от вредоносной атаки,
    называемой подделкой межсайтовых запросов или CSRF (произносится "seasurf").
   
    Задается как выражение с двумя объектами, объединенное оператором or.
    Первый объект ищет значение переменной окружения, также называемой SECRET_KEY
    Второй объект - это просто жестко запрограммированная строка.
   
    когда это приложение будет развернуто на производственном сервере, установить
    уникальное и трудно угадываемое значение в среде, чтобы у сервера был
    безопасный ключ, который больше никто не знает.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # SQLALCHEMY_DATABASE_URI - Flask-SQLAlchemy определяет местоположение базы данных приложения    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    """
    Переменные конфигурации для электронной почты включают сервер и порт, 
    логический флаг для включения зашифрованных подключений и 
    необязательные имя пользователя и пароль. 
    """
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # Порт почтового сервера может быть указан в переменной окружения, если он не задан, используется порт 25
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']