# -*- coding: utf-8 -*-
"""
модуль forms.py для хранения классов веб-форм
"""

from flask_wtf import FlaskForm # FlaskForm - базовый класс для всех форм в Flask-WTF
from wtforms import StringField, PasswordField, BooleanField, SubmitField # - Поля формы
from wtforms.validators import DataRequired # Валидатор - проверяет, что поле не пустое

'''
Класс формы
LoginForm наследуется от FlaskForm
'''
class LoginForm(FlaskForm): 
    username = StringField('Имя пользователя', validators=[DataRequired()])
    '''
    Поле имени пользователя:
    StringField - текстовое поле ввода
    Метка 'Username' будет отображаться в форме
    validators=[DataRequired()] - требует, чтобы поле было заполнено
    '''
    
    password = PasswordField('Пароль', validators=[DataRequired()])
    '''
    Поле пароля:
    PasswordField - поле для ввода пароля (ввод маскируется)
    Метка 'Пароль'
    Также обязательное для заполнения
    '''
    
    remember_me = BooleanField('Запомнить меня')
    '''
    Флажок "Запомнить меня":
    BooleanField - чекбокс (флажок)
    Позволяет пользователю выбрать, запомнить ли его данные для будущих входов
    '''
    
    submit = SubmitField('Отправить')
    '''
    Кнопка отправки:
    SubmitField - кнопка для отправки формы
    Будет отображаться с текстом 'Отправить'
    '''