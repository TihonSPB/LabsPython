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

MINS_IN_HOUR = 60
SECS_IN_MIN = 60
ROW_COUNT = 25

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
# !!!\\\|||/// Формат координат \\\|||///!!!

def degree_minutes_seconds(location): # Разбивка локации на градусы, минуты, секунды

    minutes, degrees = math.modf(location)
    degrees = int(degrees)
    minutes *= MINS_IN_HOUR
    seconds, minutes = math.modf(minutes)
    minutes = int(minutes)
    seconds = SECS_IN_MIN * seconds
    return degrees, minutes, seconds # Кортеж


def format_location(location): # Вывод градусов в формате (025°44'16.00"N,080°13'29.17"W)
    
    # Если location пустой (None или пустой список/кортеж), возвращаем пустую строку
    if not location[0] or not location[1] or len(location) < 2:
        return "отсутствуют"
    
    # Определяем полушарие 
    ns = ""
    if location[0] < 0:
        ns = 'S'
    elif location[0] > 0:
        ns = 'N'

    ew = ""
    if location[1] < 0:
        ew = 'W'
    elif location[1] > 0:
        ew = 'E'

    format_string = '{:03d}\xb0{:0d}\'{:.2f}"' # Градусы{:03d}-(03-3 знака; d-целое число); \xb0-символ "°"; Минуты{:0d}\'-0 будет сохраннен; Секунды{:.2f}"-Дробное с двумя знаками после запятой.
    latdegree, latmin, latsecs = degree_minutes_seconds(abs(location[0]))
    latitude = format_string.format(latdegree, latmin, latsecs)
    longdegree, longmin, longsecs = degree_minutes_seconds(abs(location[1]))
    longitude = format_string.format(longdegree, longmin, longsecs)
    return '(' + latitude + ns + ',' + longitude + ew + ')'

# _______________________________________
# !!!\\\|||/// Маршрутизация \\\|||///!!!

# Декоратор. '/' - связывает функцию с URL-адресом '/' (главная страница).
@app.route('/')
@app.route('/home/<int:page>/<sort_by>/<order>')
# Пользователь заходит на главную страницу, Flask вызывает эту функцию.
def index(page=1, sort_by='market_name', order='asc'): # Параметры по умолчанию
    
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
        
    # Добавляем пагинацию (25 записей на страницу)
    per_page = ROW_COUNT
    markets_data = markets_query.paginate(page=page, per_page=per_page, error_out=False)
    
    if not markets_data.items and page != 1:
        abort(404)

    return render_template(
        "index.html", 
        markets=markets_data, 
        sort_by=sort_by, 
        order=order
        )


@app.route('/<int:id>') 
def market_detail(id):
    
    # Основная информация о рынке по ID и связанные данные через joins
    market_info = db.session.query(
        Market.market_id,
        Market.market_name,
        Market.street,
        Market.zip,
        Market.lat,
        Market.lon,
        City.city,
        State.state_full,
        State.state_abbr
    ).filter(Market.market_id == id)\
     .join(City, Market.city == City.city_id)\
     .join(State, Market.state == State.state_id)\
     .first()
    
    if not market_info:
        abort(404) # Возвращаем 404 если рынок не найден
    
    # Категории рынка
    categories = db.session.query(Category.category)\
        .join(markets_categories, Category.category_id == markets_categories.c.category_id)\
        .filter(markets_categories.c.market_id == id)\
        .all()
    
    # Преобразуем список кортежей в список строк
    categories = [category[0] for category in categories]
    
    location = format_location((market_info.lat, market_info.lon)) 
    
    # Получаем все отзывы для этого рынка с информацией о пользователях
    reviews = db.session.query(
        Review.date_time,
        Review.score,
        Review.review,
        User.fname,
        User.lname,
        User.username
    ).join(
        User, Review.user_id == User.user_id
    ).filter(
        Review.market_id == id
    ).order_by(
        Review.date_time.desc()
    ).all()
    
    # Рассчитываем средний рейтинг
    avg_rating = db.session.query(
        db.func.avg(Review.score)
    ).filter(
        Review.market_id == id
    ).scalar()
    
    # Округляем средний рейтинг до 1 знака после запятой
    avg_rating = round(avg_rating, 1) if avg_rating else None
    
    # Проверяем, есть ли валидные координаты у текущего рынка
    if (market_info.lat is None or market_info.lon is None or 
        market_info.lat == '' or market_info.lon == ''):
        current_location = None
    else:
        try:
            # Дополнительная проверка, что координаты можно преобразовать в float
            lat = float(market_info.lat)
            lon = float(market_info.lon)
            current_location = (lat, lon)
        except (ValueError, TypeError):
            current_location = None
    
    # Получаем все рынки (кроме текущего) с валидными координатами
    all_markets = db.session.query(
        Market.market_id,
        Market.market_name,
        City.city,
        State.state_abbr,
        Market.zip,
        Market.lat,
        Market.lon,
        func.avg(Review.score).label('avg_score')
    ).join(
        City, Market.city == City.city_id
    ).join(
        State, Market.state == State.state_id
    ).outerjoin(
        Review, Market.market_id == Review.market_id
    ).filter(
        Market.market_id != id,
        Market.lat.isnot(None),
        Market.lon.isnot(None),
        Market.lat != '',
        Market.lon != ''
    ).group_by(
        Market.market_id,
        Market.market_name,
        City.city,
        State.state_abbr,
        Market.zip,
        Market.lat,
        Market.lon
    ).all()
            
    # Фильтруем рынки по расстоянию (только если у текущего рынка есть валидные координаты)
    nearby_markets = []
    if current_location:
        for market in all_markets:
            # Проверяем координаты рынка
            if (market.lat is None or market.lon is None or 
                market.lat == '' or market.lon == ''):
                continue                
            try:
                market_lat = float(market.lat)
                market_lon = float(market.lon)
                market_location = (market_lat, market_lon)
                distance = calculate_distance(current_location, market_location)
                if distance <= 30:
                    nearby_markets.append({
                        'market_id': market.market_id,
                        'market_name': market.market_name,
                        'city': market.city,
                        'state_abbr': market.state_abbr,
                        'zip': market.zip,
                        'avg_score': round(float(market.avg_score), 1) if market.avg_score else None,
                        'distance': round(distance, 1)
                    })
            except (ValueError, TypeError):
                continue
        
        # Сортируем по расстоянию
        nearby_markets.sort(key=lambda x: x['distance'])
        
    return render_template(
        "market_detail.html", 
        market=market_info,
        categories=categories,
        location=location,
        reviews=reviews,
        avg_rating=avg_rating,
        nearby_markets=nearby_markets,
        has_coordinates=current_location is not None  # Добавляем флаг наличия координат
    )


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
    
    # запуск внутри сети. В cmd запустить flask run --host=0.0.0.0

