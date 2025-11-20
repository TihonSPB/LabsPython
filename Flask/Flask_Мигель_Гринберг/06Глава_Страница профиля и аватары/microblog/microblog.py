# -*- coding: utf-8 -*-
"""
Основной модуль приложения
"""

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post

# Декоратор регистрирует функцию как контекстную функцию оболочки.
# Когда команда flask shell выполняется, она вызывает эту функцию и регистрирует элементы, возвращаемые ею, в сеансе оболочки.
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}