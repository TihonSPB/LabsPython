# -*- coding: utf-8 -*-
"""
Модульное тестирование модели пользователей

Для запуска в cmd:
    python tests.py
    # или с более подробным выводом
    python tests.py -v
"""

# Модуль os для работы с переменными окружения
import os
# Устанавливаем переменную окружения DATABASE_URL для использования SQLite в памяти
# Это гарантирует, что тесты будут использовать отдельную тестовую БД, а не основную
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta # Для работы с датами и временем
import unittest # Встроенный модуль Python для написания тестов
from app import app, db # Импортируем приложение и базу данных
from app.models import User, Post # Импортируем модели


class UserModelCase(unittest.TestCase):
    """
    ТЕСТОВЫЙ КЛАСС
    Наследуется от unittest.TestCase для создания набора тестов модели User
    """
    # Создаем контекст приложения (нужен для работы с БД)
    def setUp(self):
        """
        МЕТОД НАСТРОЙКИ (выполняется ПЕРЕД каждым тестом)
        Создает контекст приложения и все таблицы в тестовой БД
        """
        self.app_context = app.app_context()
        self.app_context.push() # Активируем контекст
        db.create_all() # Создаем все таблицы в тестовой базе данных

    def tearDown(self):
        """
        МЕТОД ОЧИСТКИ (выполняется ПОСЛЕ каждого теста)
        Удаляет все данные и закрывает соединение с БД
        """
        db.session.remove() # Удаляем сессию БД
        db.drop_all() # Удаляем все таблицы
        self.app_context.pop() # Удаляем контекст приложения

    def test_password_hashing(self):
        """
        ТЕСТ 1: Проверка хеширования паролей
        Проверяет, что пароли правильно хешируются и проверяются
        """
        # Создаем тестового пользователя
        u = User(username='susan', email='susan@example.com')
        # Устанавливаем пароль 'cat'
        u.set_password('cat')
        # Проверяем: пароль 'dog' НЕ должен подходить
        self.assertFalse(u.check_password('dog'))
        # Проверяем: пароль 'cat' ДОЛЖЕН подходить
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        """
        ТЕСТ 2: Проверка генерации аватарок
        Проверяет, что URL аватарки генерируется правильно
        """
        u = User(username='john', email='john@example.com')
        # Сравниваем сгенерированный URL с ожидаемым
        # MD5 хеш от 'john@example.com' должен быть 'd4c74594d841139328695756648b6bd6'
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        """
        ТЕСТ 3: Проверка функциональности подписок
        Тестирует подписку, отписку и связанные методы
        """
        # Создаем двух пользователей
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        # Добавляем в БД и сохраняем
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        # Проверяем начальное состояние (нет подписок)
        following = db.session.scalars(u1.following.select()).all() # На кого подписан u1
        followers = db.session.scalars(u2.followers.select()).all() # Кто подписан на u2
        self.assertEqual(following, []) # u1 ни на кого не подписан
        self.assertEqual(followers, []) # На u2 никто не подписан
        
        # ТЕСТ ПОДПИСКИ: u1 подписывается на u2
        u1.follow(u2)
        db.session.commit()
        # Проверяем результаты подписки
        self.assertTrue(u1.is_following(u2))  # u1 должен быть подписан на u2
        self.assertEqual(u1.following_count(), 1) # У u1 должна быть 1 подписка
        self.assertEqual(u2.followers_count(), 1) # У u2 должен быть 1 подписчик
        # Проверяем конкретные связи
        u1_following = db.session.scalars(u1.following.select()).all() # Получаем список подписок u1
        u2_followers = db.session.scalars(u2.followers.select()).all() # Получаем список подписчиков u2
        self.assertEqual(u1_following[0].username, 'susan') # u1 подписан на susan
        self.assertEqual(u2_followers[0].username, 'john') # На susan подписан john
        
        # ТЕСТ ОТПИСКИ: u1 отписывается от u2
        u1.unfollow(u2)
        db.session.commit()
        # Проверяем результаты отписки
        self.assertFalse(u1.is_following(u2)) # u1 больше не подписан на u2
        self.assertEqual(u1.following_count(), 0) # У u1 нет подписок
        self.assertEqual(u2.followers_count(), 0) # У u2 нет подписчиков

    def test_follow_posts(self):
        """
        ТЕСТ 4: Проверка ленты постов
        Тестирует метод following_posts() для получения ленты новостей
        Создает сложную структуру подписок и проверяет правильность ленты
        """
        # СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4]) # Добавляем всех сразу
        
        # СОЗДАНИЕ ПОСТОВ с разным временем публикации
        now = datetime.now(timezone.utc) # Текущее время как база
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1)) # +1 сек
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4)) # +4 сек (самый новый)
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3)) # +3 сек
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2)) # +2 сек
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()
        
        # НАСТРОЙКА ПОДПИСОК (создаем сеть отношений)
        u1.follow(u2) # john подписывается на susan
        u1.follow(u4) # john подписывается на david
        u2.follow(u3) # susan подписывается на mary
        u3.follow(u4) # mary подписывается на david
        db.session.commit()
        
        # ПОЛУЧЕНИЕ ЛЕНТ ДЛЯ КАЖДОГО ПОЛЬЗОВАТЕЛЯ
        f1 = db.session.scalars(u1.following_posts()).all() # Лента john
        f2 = db.session.scalars(u2.following_posts()).all() # Лента susan
        f3 = db.session.scalars(u3.following_posts()).all() # Лента mary
        f4 = db.session.scalars(u4.following_posts()).all() # Лента david
        # ПРОВЕРКА ЛЕНТ (должны быть отсортированы по времени, новые сверху)
        # Для john: подписан на susan и david (+ свои посты)
        # Посты: p2 (susan, +4сек), p4 (david, +2сек), p1 (john, +1сек)
        self.assertEqual(f1, [p2, p4, p1])
        # Для susan: подписана на mary (+ свои посты)
        # Посты: p2 (susan, +4сек), p3 (mary, +3сек)
        self.assertEqual(f2, [p2, p3])
        # Для mary: подписана на david (+ свои посты)
        # Посты: p3 (mary, +3сек), p4 (david, +2сек)
        self.assertEqual(f3, [p3, p4])
        # Для david: только свои посты (ни на кого не подписан)
        # Посты: p4 (david, +2сек)
        self.assertEqual(f4, [p4])


# ТОЧКА ВХОДА
if __name__ == '__main__':
    # Запускаем все тесты с подробным выводом (verbosity=2)
    unittest.main(verbosity=2)
