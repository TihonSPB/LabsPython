﻿## Последовательность выполнения работы  
1. Создали виртуальную среду venv через консоль  
2. Зашли в виртуальную среду  
3. Установили Flask через консоль pip install flask  
4. Установили библиотеку, для работы с базами данных (вместо SQL-запросов используем Python-классы).через консоль pip install flask-sqlalchemy  
5. Создали файл app.py в корне проекта. Главный файл (Controller + настройки Flask)  
6. Создали папку templates в корне проекта, в ней хранятся HTML-шаблоны (View в MVC)  
7. Создали общий шаблон base.html в папке  templates.  
8. Для быстрого заполнения базовой структуры html, в VSCode или PyCharm ныбираем «!» и Tab  
9. Создали папку static. Статические файлы в папке такие как, CSS/JS/Картинки.  
10. Создали папку css в папке static  
11. Создали файл стилей main.css в папке css (не используем, в этом уроке)  
12. Подключаем стиль bootstrap к общему шаблону  base.html  
  - если через удаленный сервер https://www.bootstrapcdn.com/ , прописываем url удаленного сервера в link.  
  - если скачен с сайта https://getbootstrap.com/ помещаем  в папку css, прописываем путь в link через функцию url_for()  
13. В основной шаблон base.html копируем шапку и футтер из примеров https://getbootstrap.com/docs/5.3/examples/  
14. Создали шаблоны наследники, файлы index.html, about.html и one.html в папке  templates  
15. Перешли в браузере по адресам (проверили работу приложения):  
  - http://127.0.0.1:5000  
  - http://127.0.0.1:5000/one  
  - http://127.0.0.1:5000/home  
  - http://127.0.0.1:5000/about  
---  
16. В файле app.py импортируем класс SQLAlchemy из библиотеки flask_sqlalchemy  
17. Импортируем функции request, redirect из библиотеки flask  
18. Импортируем datetime  
19. Пишем конфигурацию подключения к БД SQLite (site.db)  
20. Создаем класс Article, эквивалент SQL таблицы.  
21. Создаем базу данных через консоль:  
```   
flask shell  
```  
```  
>>>from app import db  
```  
```  
>>>db.create_all()  
```  
22. В файле app.py создаем функцию для отслеживания адреса /create-article  
23. В декораторе указываем какие методы мы принимаем  
24. Создали шаблон create-article.html в папке templates. Для отправки данных методом post  
25. В файле app.py в функции дописываем создание статьи, добавления в сессию и сохранения в базе данных.  
26. Проверяем работу отправив форму с адреса http://127.0.0.1:5000/create-article  
---  
27. В файле app.py создаем функцию для отслеживания адреса /articles  
28. Создаем шаблон articles.html в папке templates.  
29. В файле app.py создаем функцию для отслеживания адреса /articles/<id статьи>  
30. Создаем шаблон article_detail.html в папке templates.  
31. Перешли в браузере по адресу(проверили вывод всех данных): http://127.0.0.1:5000/articles  
32. Перешли по кнопке «Читать статью», проверили вывод  
---  
33. В шаблоне article_detail.html добавили кнопки, на редактирование и удаление.  
34. В файле app.py создаем функцию для отслеживания адреса /articles/<id статьи>/delete  
35. Создаем функцию для внесения изменения в статью /articles/<id статьи>/update  
## Структура:  
```   
папка проекта/
│
├── app.py                # Основной файл приложения (Controller)
│                         # Содержит:
│                         # - Создание Flask-приложения
│                         # - Маршруты (роуты)
│                         # - Настройки
│                         # - Обработчики запросов
│
├── requirements.txt      # Файл зависимостей Python
│                         # Список всех пакетов (Flask, SQLAlchemy и др.)
│                         # Для установки: pip install -r requirements.txt
│
├── README.md             # Документация проекта
│
├── static/               # Папка для статических файлов
│   └── css/              # Каскадные таблицы стилей (CSS)
│       └── main.css
├── templates/            # View (HTML-шаблоны)
│   ├── base.html         # Базовый шаблон (родительский для других)
│   ├── index.html        # Шаблон главной страницы (наследует base.html)
│   ├── page.html
│   ├── articles.html
│   ├── create-article.html
│   ├── article_detail.html
│   ├── post_update.html
│   └── about.html
└── instance/             # Папка для файлов экземпляра приложения
    └── site.db           # Файл базы данных SQLite
```   
