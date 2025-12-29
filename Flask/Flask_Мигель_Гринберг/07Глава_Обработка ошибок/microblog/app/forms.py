# -*- coding: utf-8 -*-
"""
модуль forms.py для хранения классов веб-форм
"""

from flask_wtf import FlaskForm # FlaskForm - базовый класс для всех форм в Flask-WTF
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField # Поля формы
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length # Валидатор - проверяет, что поле не пустое

import sqlalchemy as sa  # SQLAlchemy для запросов к БД
from app import db  # Объект базы данных
from app.models import User  # Модель пользователя

'''
Класс формы
LoginForm наследуется от FlaskForm
'''
class LoginForm(FlaskForm): 
    username = StringField('Имя пользователя', validators=[DataRequired()])
    '''
    Поле имени пользователя:
    StringField - текстовое поле ввода
    Метка 'Имя пользователя' будет отображаться в форме
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


'''
Класс формы
RegistrationForm наследуется от FlaskForm
'''
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    '''
    Поле имени пользователя:
    StringField - текстовое поле ввода
    Метка 'Имя пользователя' будет отображаться в форме
    validators=[DataRequired()] - требует, чтобы поле было заполнено
    '''
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    '''
    Поле почты пользователя:
    StringField - текстовое поле ввода
    Метка 'Email' будет отображаться в форме
    validators=[DataRequired()] - требует, чтобы поле было заполнено
    validators=[Email()] - проверка формата email
    '''
    
    password = PasswordField('Пароль', validators=[DataRequired()])
    '''
    Поле пароля:
    PasswordField - поле для ввода пароля (ввод маскируется)
    Метка 'Пароль'
    validators=[DataRequired()] - Обязательное для заполнения
    '''
    
    # Поле для повторения пароля с проверкой совпадения с первым паролем
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    '''
    Поле повтора пароля:
    PasswordField - поле для ввода пароля (ввод маскируется)
    Метка 'Повторите пароль'
    validators=[DataRequired()] - Обязательное для заполнения
    validators=[EqualTo('password')] - проверка совпадения с первым паролем
    '''
    
    submit = SubmitField('Зарегистрироваться')
    '''
    Кнопка отправки:
    SubmitField - кнопка для отправки формы
    Будет отображаться с текстом 'Зарегистрироваться'
    '''


    '''
    Методы validate_username() и validate_email(), 
    называются по специальному шаблону validate_<field_name>,
    WTForms автоматически вызывает методы, начинающиеся с validate_, для соответствующих полей
    '''
    # КАСТОМНАЯ ВАЛИДАЦИЯ: Проверка уникальности имени пользователя
    def validate_username(self, username):
        """Проверяет, не занято ли имя пользователя другим пользователем"""
        # Ищем пользователя с таким же именем в базе данных
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        
        # Если пользователь с таким именем уже существует
        if user is not None:
            # Выбрасываем ошибку валидации - имя уже занято
            raise ValidationError('Пожалуйста, используйте другое имя пользователя.')

    # КАСТОМНАЯ ВАЛИДАЦИЯ: Проверка уникальности email
    def validate_email(self, email):
        """Проверяет, не используется ли email другим пользователем"""
        # Ищем пользователя с таким же email в базе данных
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        
        # Если email уже зарегистрирован
        if user is not None:
            # Выбрасываем ошибку валидации - email уже используется
            raise ValidationError('Пожалуйста, используйте другой адрес электронной почты.')


'''
Класс формы
EditProfileForm наследуется от FlaskForm
'''
class EditProfileForm(FlaskForm):
    """
    Форма для редактирования профиля пользователя.
    Позволяет изменить имя пользователя и информацию 'О себе'.
    """
    
    # Поле для имени пользователя
    # StringField - стандартное текстовое поле (одна строка)
    # DataRequired() - проверяет, что поле не пустое
    username = StringField('Имя пользователя', validators=[DataRequired()])
    
    # Поле 'О себе' (многострочный текст)
    # TextAreaField - поле для ввода длинного текста (textarea в HTML)
    # Length(min=0, max=140) - проверяет длину текста (от 0 до 140 символов)
    # min=0 - поле может быть пустым (пользователь может не заполнять)
    # max=140 - ограничение как в Twitter (краткая информация)
    about_me = TextAreaField('О себе', validators=[Length(min=0, max=140)])
    
    # Кнопка отправки формы
    submit = SubmitField('Отправить')
    
    
    # СПЕЦИАЛЬНЫЙ КОНСТРУКТОР
    def __init__(self, original_username, *args, **kwargs):
        """
        original_username: текущее имя пользователя ДО редактирования
        Нужно для проверки, изменил ли пользователь свое имя
        """
        # Вызываем конструктор родительского класса (FlaskForm)
        super().__init__(*args, **kwargs)
        
        # Сохраняем оригинальное имя пользователя как атрибут формы
        self.original_username = original_username

    # КАСТОМНАЯ ВАЛИДАЦИЯ USERNAME
    def validate_username(self, username):
        """
        Проверяет, можно ли использовать новое имя пользователя.
        Вызывается автоматически WTForms (по правилу naming convention)
        """
        # 1. Сравниваем новое имя с оригинальным
        if username.data != self.original_username:
            # 2. Если имя изменилось - проверяем, не занято ли оно
            user = db.session.scalar(sa.select(User).where(
                User.username == self.username.data))
            
            # 3. Если пользователь с таким именем уже существует
            if user is not None:
                # 4. Выбрасываем ошибку валидации
                raise ValidationError('Пожалуйста, используйте другое имя пользователя.')