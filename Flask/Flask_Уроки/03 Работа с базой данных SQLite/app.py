
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
            return redirect('/one') # Перенаправляем на другую страницу
        except:
            print("Произошла ошибка!")
    else:
        # Если метод GET - просто отображаем форму
        return render_template("create-article.html")


# Декоратор. URL-адрес '/about'.
@app.route('/about') 
def about():
    return render_template("about.html")


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