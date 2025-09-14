# -*- coding: utf-8 -*-
"""
Маршрут на главную страницу
"""

from flask import render_template
from app import app

# Декоратор. '/' - связывает функцию с URL-адресом '/' (главная страница).
# Когда веб-браузер запрашивает любой из этих двух URL-адресов, Flask собирается вызвать 
# эту функцию и передать возвращаемое значение обратно браузеру в качестве ответа.
@app.route('/')
@app.route('/index')
def index():
    # Макет пользователя как словарь
    user = {'username': 'Miguel'}
    
    # Возвращает полную HTML-страницу из функции просмотра
    # return '''
    #     <html>
    #         <head>
    #             <title>Home Page - Microblog</title>
    #         </head>
    #         <body>
    #             <h1>Hello, ''' + user['username'] + '''!</h1>
    #         </body>
    #     </html>
    #     '''
    
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