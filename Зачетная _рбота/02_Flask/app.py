# -*- coding: utf-8 -*-

# Устанавливается через консоль pip install flask
from flask import (
    Flask,          # Основной класс Flask - ядро приложения
    render_template, # Функция для рендеринга HTML-шаблонов
    url_for,        # Генератор URL для маршрутов и статических файлов, используется в шаблоне html
    request,       # Объект для работы с входящими HTTP-запросами
    redirect,       # Функция для перенаправления на другие URL
    abort
)
# Импорт главного класса SQLAlchemy из расширения flask_sqlalchemy
# Устанавливается через консоль pip install flask-sqlalchemy
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

from sqlalchemy import func

# Создаём объект app на основе класса Flask
# В конструктор передаём название основного файла. (__name__)
# __name__ нужен, чтобы Flask знал, где искать шаблоны (templates) и статические файлы (static).
app = Flask(__name__)

# __________________________________________
# !!!\\\|||/// Подключение к DB \\\|||///!!!
# Конфигурация подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmersmarkets.db'
"""
Ключ 'SQLALCHEMY_DATABASE_URI' - это стандартное имя настройки Flask-SQLAlchemy
- 'sqlite:///' - указание на использование SQLite
- 'farmersmarkets.db' - имя файла базы данных (будет создан в рабочей директории)
Варианты для других СУБД:
- PostgreSQL: 'postgresql://user:password@localhost/mydb'
- MySQL: 'mysql://user:password@localhost/mydb'
- Oracle: 'oracle://user:password@127.0.0.1:1521/sidname'
"""

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создание экземпляра SQLAlchemy и привязка к Flask-приложению (app)
db = SQLAlchemy(app)  # db - это главный объект для работы с базой данных

# ____________________________________
# !!!\\\|||/// Таблицы DB \\\|||///!!!

class Category(db.Model):
    __tablename__ = 'categories' # __tablename__ - название таблицы в базе данных
    
    category_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    

class State(db.Model):
    __tablename__ = 'states'
    
    state_id = db.Column(db.Integer, primary_key=True)
    state_full = db.Column(db.String(255))
    state_abbr = db.Column(db.String(2), nullable=False)


class City(db.Model):
    __tablename__ = 'cities'
    
    city_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(255), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.state_id'), nullable=False)


class Market(db.Model):
    __tablename__ = 'markets'
    
    market_id = db.Column(db.Integer, primary_key=True)
    market_name = db.Column(db.String(255))
    street = db.Column(db.String(255))
    city = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    state = db.Column(db.Integer, db.ForeignKey('states.state_id'))
    zip = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)


# Таблица связи многие-ко-многим (не требует отдельного класса)
markets_categories = db.Table('markets_categories',
    db.Column('market_category_id', db.Integer, nullable=False),
    db.Column('market_id', db.Integer, db.ForeignKey('markets.market_id'), nullable=False),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
)

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255))
    lname = db.Column(db.String(255))
    username = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)


class Review(db.Model):
    __tablename__ = 'reviews'
    
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    market_id = db.Column(db.Integer, db.ForeignKey('markets.market_id'), nullable=False)
    date_time = db.Column(db.Date, nullable=False)
    score = db.Column(db.SmallInteger, nullable=False)
    review = db.Column(db.Text)

# _______________________________________
# !!!\\\|||/// Утилита (Util) Универсальная программа для расчета расстояния на поверхности земли \\\|||///!!!

import math

EARTH_RADIUS_MI = 3958.8
def calculate_distance(location1, location2):
    
    lat1 = math.radians(location1[0])
    lat2 = math.radians(location2[0])
    long1 = math.radians(location1[1])
    long2 = math.radians(location2[1])
    del_lat = (lat1 - lat2) / 2
    del_long = (long1 - long2) / 2
    angle = math.sin(del_lat)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(del_long)**2
    distance = 2 * EARTH_RADIUS_MI * math.asin(math.sqrt(angle))
    return distance

# _______________________________________
# !!!\\\|||/// Маршрутизация \\\|||///!!!

# Декоратор. '/' - связывает функцию с URL-адресом '/' (главная страница).
@app.route('/')
@app.route('/home')
# Пользователь заходит на главную страницу, Flask вызывает эту функцию.
def index():
    # Получаем параметр сортировки из URL (по умолчанию - по названию)
    sort_by = request.args.get('sort', 'market_name')
    order = request.args.get('order', 'asc')  # asc▼ или desc▲
    
    # !!!new
    page = request.args.get('page', 1, type=int)  # Добавляем параметр страницы
    # !!!new

    # Определяем поле для сортировки
    sort_field = {
        'market_name': func.lower(Market.market_name), # func.lower() - # Приводим к нижнему регистру
        'city': func.lower(City.city),
        'state': func.lower(State.state_abbr),
        'rating': func.avg(Review.score),
        'zip': Market.zip
    }.get(sort_by, Market.market_name)  # по умолчанию сортируем по названию

    # Определяем направление сортировки
    if order == 'desc':
        sort_field = sort_field.desc()
       
    # Запрос с объединением таблиц и вычислением среднего рейтинга
    markets_query = db.session.query(
        Market.market_id,
        Market.market_name,
        City.city,
        State.state_abbr,
        Market.zip,
        func.avg(Review.score).label('avg_rating')
    ).join(
        City, Market.city == City.city_id
    ).join(
        State, Market.state == State.state_id
    ).outerjoin(  # Используем outerjoin, чтобы включить рынки без отзывов
        Review, Market.market_id == Review.market_id
    ).group_by(
        Market.market_id,
        Market.market_name,
        City.city,
        State.state_abbr,
        Market.zip
    ).order_by(sort_field)
        
    # markets_data = markets_query.all()
    
    # !!!new
    # Добавляем пагинацию (25 записей на страницу)
    per_page = 25
    markets_data = markets_query.paginate(page=page, per_page=per_page, error_out=False)
    
    if not markets_data.items and page != 1:
        abort(404)
    # !!!new

    return render_template(
        "index.html", 
        markets=markets_data, 
        sort_by=sort_by, 
        order=order
        )

@app.route('/home/<int:id>') 
def market_detail(id):
    market = Market.query.get(id)
    return render_template("market_detail.html", market = market)

@app.route('/test')
def test():
    markets = Market.query.first()
    return render_template("test.html",markets=markets)


# Проверяем, запущен ли скрипт напрямую (а не импортирован как модуль).
if __name__ == "__main__":
    # app.run() - Запускаем веб-сервер Flask.
    # Параметр debug=True включает:
    # 1) Автоперезагрузку сервера при изменении кода.
    # 2) Подробные ошибки в браузере (удобно для разработки).
    # При перебросе на сервер отключить отображение ошибок в браузере
    app.run(debug=True)