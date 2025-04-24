# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for # Импорт класса Flask и функций render_template, url_for из библиотеки flask
# функция url_for используется в шаблоне html

# Создаём объект app на основе класса Flask
app = Flask(__name__)


# Декоратор. URL-адреса '/', '/home'
@app.route('/') 
@app.route('/home')
# Функция может иметь любое имя, но index() — общепринятое название для главной страницы.
def index():
    # Функция render_template() ищет файл index.html в папке templates/,
    # отображает его и возвращает как HTML-страницу пользователю.
    return render_template("index.html")


# Декоратор. URL-адрес '/one'.
@app.route('/one') 
def my_one():
    return render_template("page.html")


# Декоратор. Можно передавать параметры через URL.
# В угловых скобках < > указываются параметры, которые будут извлекаться из URL.
# Можно задавать тип параметра (например, string, int, float, path).
# Формат: <тип:имя_переменной>
@app.route('/user/<string:username>/<int:id>') 
# Функция принимает параметры из URL (username и id).
def get_parameter_from_url(username, id):
    # Возвращаем f-строку с подставленными значениями.
    return f"Получение параметра из url. Имя: {username}; id: {id}"
    # При переходе по адресу http://127.0.0.1:5000/user/alex/123:
    # Получение параметра из url. Имя: alex; id: 123


# Проверяем, запущен ли скрипт напрямую (а не импортирован как модуль).
if __name__ == "__main__":    
    app.run(debug=True) # Запускаем веб-сервер Flask.