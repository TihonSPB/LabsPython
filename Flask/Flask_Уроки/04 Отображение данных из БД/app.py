# -*- coding: utf-8 -*-
# Импорт основных компонентов Flask
from flask import (
    Flask,          # Основной класс Flask - ядро приложения
    render_template, # Функция для рендеринга HTML-шаблонов
    url_for,        # Генератор URL для маршрутов и статических файлов, используется в шаблоне html
    request,       # Объект для работы с входящими HTTP-запросами
    redirect       # Функция для перенаправления на другие URL
)

# Импорт главного класса SQLAlchemy из расширения flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
"""
SQLAlchemy - это ORM (Object-Relational Mapping), который позволяет:
- Работать с базой данных через Python-объекты
- Автоматизировать создание/изменение таблиц
- Строить сложные запросы на Python (без чистого SQL)

Основные возможности:
- Создание моделей данных (Python-классы → таблицы БД)
- Управление сессиями и подключениями
- Миграции (с дополнительными расширениями)
- Поддержка разных СУБД: SQLite, PostgreSQL, MySQL и др.
"""
from datetime import datetime


# Создаём объект app на основе класса Flask
app = Flask(__name__)

# Конфигурация подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
"""
Ключ 'SQLALCHEMY_DATABASE_URI' - это стандартное имя настройки Flask-SQLAlchemy
- 'sqlite:///' - указание на использование SQLite (легковесная файловая БД)
- 'site.db' - имя файла базы данных (будет создан в рабочей директории)
Варианты для других СУБД:
- PostgreSQL: 'postgresql://user:password@localhost/mydb'
- MySQL: 'mysql://user:password@localhost/mydb'
- Oracle: 'oracle://user:password@127.0.0.1:1521/sidname'
"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Создание экземпляра SQLAlchemy и привязка к Flask-приложению (app)
db = SQLAlchemy(app)  # db - это главный объект для работы с базой данных


'''
Создаем класс таблицы DB
SQL-эквивалент:
    
CREATE TABLE article (
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    intro VARCHAR(300),
    text TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);
'''
class Article(db.Model):
    # Каждый экземпляр класса запись в таблице articles
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300))
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Специальный метод для строкового представления объекта
    def __repr__(self):
        # При выборе объекта на основе класса Article будет выдаваться объект и его id
        return f'<Article {self.id}>'
        # return '<Article %r>' % self.id


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

# Отправка данных в БД
# Декоратор. URL-адрес '/create-article'.
# methods=['POST', 'GET'] - разрешает GET (отображение формы) и POST (отправка данных)
@app.route('/create-article', methods=['POST', 'GET']) 
def create_article():
    # Проверяем метод запроса
    if request.method == "POST":
        title = request.form['title'] # Получаем заголовок из формы
        intro = request.form['intro'] # Получаем анонс из формы
        text = request.form['text'] # Получаем текст статьи из формы
        
        # Создаем новый объект Article с полученными данными
        article = Article(title=title, intro=intro, text=text)
        
        try:
            db.session.add(article) # Добавляем статью в сессию
            db.session.commit() # Сохраняем изменения в БД
            return redirect('/articles') # Перенаправляем на другую страницу
        except:
            print("Произошла ошибка!")
    else:
        # Если метод GET - просто отображаем форму
        return render_template("create-article.html")


# Отображение данных из БД
# Декоратор. URL-адрес '/articles'.
@app.route('/articles') 
def articles():
    # articles_list = Article.query.first() # Получает только первую статью
    
    '''
    Article.query - создает базовый запрос к таблице Article
    .order_by(Article.date.desc()) - сортировка по дате (новые сначала)
    .all() - выполняет запрос и возвращает все результаты
    '''
    articles_list = Article.query.order_by(Article.date.desc()).all()
    
    # Рендерим шаблон articles.html и передаем в него список статей
    # articles_list=articles_list - передача переменной в шаблон
    return render_template("articles.html", articles_list = articles_list)


# Декоратор. URL-адрес '/articles/<id статьи>'.
# <int:id> - динамический параметр URL, преобразуется в целое число
@app.route('/articles/<int:id>') 
def article_detail(id):
    # Получаем статью из базы данных:
    # Article.query.get(id) - ищет запись по первичному ключу (id)
    # Возвращает:
    # - объект Article, если статья найдена
    # - None, если статьи с таким id нет
    article = Article.query.get(id)
    # Рендерим шаблон и передаем в него найденную статью
    # Если article=None, шаблон получит None (нужна дополнительная обработка)
    return render_template("article_detail.html", article = article)


# Декоратор. URL-адрес '/about'.
@app.route('/about') 
def about():
    return render_template("about.html")


# Проверяем, запущен ли скрипт напрямую (а не импортирован как модуль).
if __name__ == "__main__":    
    app.run(debug=True) # Запускаем веб-сервер Flask.