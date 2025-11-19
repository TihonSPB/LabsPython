# -*- coding: utf-8 -*-
"""
Контроллер, Маршруты
"""

from flask import render_template, flash, redirect, url_for, request  #функция url_for() для ссылок, функция request для доступа к параметрам запроса
from app import app, db # Импортируем объект базы данных

from app.forms import LoginForm, RegistrationForm # Импорт классов LoginForm, RegistrationForm из модуля forms.py в пакете app

from flask_login import current_user, login_user, logout_user, login_required   # Импортируем текущего пользователя, функцию входа и выхода
import sqlalchemy as sa # SQLAlchemy для построения запросов
from app.models import User # Импортируем модель пользователя

from urllib.parse import urlsplit  # Для анализа URL


# Декоратор. '/' - связывает функцию с URL-адресом '/' (главная страница).
# Когда веб-браузер запрашивает любой из этих двух URL-адресов, Flask собирается вызвать 
# эту функцию и передать возвращаемое значение обратно браузеру в качестве ответа.
@app.route('/')
@app.route('/index')
# декоратор @login_required перехватит запрос и ответит перенаправлением на полный URL /login?next=/index
# аргумент next имеет исходный URL /index, приложение может использовать для перенаправления обратно после входа в систему
@login_required 
def index():

    # Список, где каждый элемент представляет собой словарь с полями author и body
    posts = [
        {
            'author': {'username': 'Джон'},
            'body': 'Прекрасный день в Портленде!'
        },
        {
            'author': {'username': 'Сюзи'},
            'body': 'Фильм «Мстители» был такой классный!'
        }
    ]
    
    return render_template('index.html', title='Home', posts=posts)


# Функция представления. Обрабатывает запросы к /login
# methods=['GET', 'POST'] разрешает обработку GET (загрузка страницы) и POST (отправка формы) запросов
# Аргумент methods, сообщает Flask, что функция принимает запросы GET и POST.
# GET запросы - возвращают информацию клиенту (в данном случае веб-браузеру)
# POST запросы - используются, когда браузер отправляет данные формы на сервер (GET для этой цели, не рекомендуемая практика)
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Проверяем, не вошел ли пользователь уже в систему
    if current_user.is_authenticated:
        # Если пользователь уже аутентифицирован, перенаправляем его на главную страницу
        return redirect(url_for('index'))
    
    # Создаем экземпляр формы LoginForm (предположительно, это форма Flask-WTF)
    form = LoginForm() # Объект будет использоваться в шаблоне для отображения полей формы
    
    # Проверяем, была ли форма отправлена (POST) и прошла ли валидацию
    if form.validate_on_submit():
        # Ищем пользователя в базе данных по имени пользователя
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        
        # Проверяем, существует ли пользователь и правильный ли пароль
        if user is None or not user.check_password(form.password.data):    
            # Если пользователь не найден или пароль неверный, показываем сообщение об ошибке
            flash('Неверное имя пользователя или пароль!')
            # Перенаправляем обратно на страницу входа
            return redirect(url_for('login'))
        
        # Если аутентификация успешна, выполняем вход пользователя
        login_user(user, remember=form.remember_me.data)
        
        # КРИТИЧЕСКИ ВАЖНАЯ ЧАСТЬ: Безопасное перенаправление после входа
        # Получаем URL страницы, на которую пользователь пытался попасть до аутентификации
        next_page = request.args.get('next')
        # Проверяем безопасность URL для предотвращения атак
        if not next_page or urlsplit(next_page).netloc != '':
            # Если нет страницы для перенаправления ИЛИ
            # URL содержит домен (возможная попытка перенаправления на внешний сайт)
            next_page = url_for('index')  # Перенаправляем на главную по умолчанию
        
        # Выполняем безопасное перенаправление
        return redirect(next_page)
    
    # Если форма не отправлена или не прошла валидацию,
    # render_template ищет шаблон login.html в папке templates
    # Передает в шаблон:
    # title='Sign In' - заголовок страницы
    # form=form - экземпляр формы для отображения
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """
    Обрабатывает выход пользователя из системы.
    Удаляет информацию о пользователе из сессии браузера.
    """
    # Вызывает функцию logout_user() из Flask-Login
    # Эта функция очищает сессию пользователя и "забывает" его
    logout_user()
    # Перенаправляем пользователя на главную страницу
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST']) # Маршрут для регистрации, принимает GET и POST запросы
def register():
    """
    Обрабатывает регистрацию новых пользователей.
    GET - показывает форму регистрации
    POST - обрабатывает отправленную форму
    """    
    # Проверяем, не вошел ли пользователь уже в систему
    if current_user.is_authenticated:
        # Перенаправляем на главную страницу если пользователь уже аутентифицирован
        return redirect(url_for('index'))
    # Создаем экземпляр формы регистрации
    # Для GET-запроса - пустая форма, для POST - с данными от пользователя
    form = RegistrationForm()
    
    # Проверяем, была ли форма отправлена и прошла ли всю валидацию
    if form.validate_on_submit(): # validate_on_submit() возвращает True только для POST с валидными данными
        # СОЗДАНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ
        # Создаем нового пользователя с данными из формы    
        user = User(username=form.username.data, email=form.email.data)
        # Устанавливаем хэшированный пароль для пользователя
        user.set_password(form.password.data)
        # СОХРАНЕНИЕ В БАЗУ ДАННЫХ
        # Добавляем нового пользователя в сессию базы данных
        db.session.add(user)
        # Фиксируем изменения в базе данных (сохраняем пользователя)
        db.session.commit()
        flash('Поздравляем, теперь вы зарегистрированный пользователь!')
        # Перенаправляем пользователя на страницу входа
        return redirect(url_for('login'))
    
    # ОТОБРАЖЕНИЕ ФОРМЫ РЕГИСТРАЦИИ
    # Этот код выполняется для:
    # - GET запросов (первый заход на страницу)
    # - POST запросов с невалидными данными (форма покажется с ошибками)
    return render_template('register.html', title='Register', form=form)