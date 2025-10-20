# -*- coding: utf-8 -*-
"""
Маршруты
"""

from flask import render_template, flash, redirect, url_for #функция url_for() для ссылок
from app import app

from app.forms import LoginForm # Импорт класса LoginForm из модуля forms.py в пакете app

# Декоратор. '/' - связывает функцию с URL-адресом '/' (главная страница).
# Когда веб-браузер запрашивает любой из этих двух URL-адресов, Flask собирается вызвать 
# эту функцию и передать возвращаемое значение обратно браузеру в качестве ответа.
@app.route('/')
@app.route('/index')
def index():
    # Макет пользователя как словарь
    user = {'username': 'Miguel'}
    
    # Список, где каждый элемент представляет собой словарь с полями author и body
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    
    return render_template('index.html', title='Home', user=user, posts=posts)


# Функция представления. Обрабатывает запросы к /login
# methods=['GET', 'POST'] разрешает обработку GET (загрузка страницы) и POST (отправка формы) запросов
# Аргумент methods, сообщает Flask, что функция принимает запросы GET и POST.
# GET запросы - возвращают информацию клиенту (в данном случае веб-браузеру)
# POST запросы - используются, когда браузер отправляет данные формы на сервер (GET для этой цели, не рекомендуемая практика)
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Создаем экземпляр формы LoginForm (предположительно, это форма Flask-WTF)
    form = LoginForm() # Объект будет использоваться в шаблоне для отображения полей формы
    
    # Проверяем, была ли форма отправлена (POST) и прошла ли валидацию
    if form.validate_on_submit():
        # Если форма валидна, показываем всплывающее сообщение с данными пользователя в base.html
        flash('Запрошен вход для пользователя {}, помнить меня / remember_me={}'.format(form.username.data, form.remember_me.data))
        # Перенаправляем пользователя на страницу '/index'
        return redirect(url_for('index'))
    
    # Если форма не отправлена или не прошла валидацию,
    # render_template ищет шаблон login.html в папке templates
    # Передает в шаблон:
    # title='Sign In' - заголовок страницы
    # form=form - экземпляр формы для отображения
    return render_template('login.html', title='Sign In', form=form)