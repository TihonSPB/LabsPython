# -*- coding: utf-8 -*-

import random
from datetime import datetime, timedelta

class Review: 
    
    def __init__(self, rev_id, user_id, market_id):
        self.rev_id = rev_id
        self.user_id = user_id
        self.market_id = market_id
        self.date_time = self.random_date()
        self.score = random.randint(1, 5)
        self.review = self.get_farm_market_review(self.score)
    
    def random_date(self):
        # Генерация случайной даты между start_year и end_year
        start_year=2000
        end_year=2024
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        
        random_days = random.randint(0, (end_date - start_date).days)
        return (start_date + timedelta(days=random_days)).date()
    
    def get_farm_market_review(self, rating):
        # Словарь с отзывами для каждой оценки
        reviews = {
            1: [
                "Ужасное качество продуктов!",
                "Никогда больше не приду сюда.",
                "Очень разочарован.",
                ""
            ],
            2: [
                "Не понравилось, много недостатков.",
                "Могло бы быть и лучше.",
                "Не советую.",
                ""
            ],
            3: [
                "Неплохо, но есть куда расти.",
                "Средненько, ничего особенного.",
                "Обычный фермерский рынок.",
                ""
            ],
            4: [
                "Хороший выбор продуктов!",
                "Понравилось, буду приходить еще.",
                "Качество на уровне.",
                ""
            ],
            5: [
                "Отличный рынок! Все свежее и вкусное!",
                "Лучший фермерский рынок в городе!",
                "Супер! Рекомендую всем!",
                ""
            ]
        }
        
        # Проверка корректности оценки
        if rating not in reviews:
            return ''
        
        # Случайный выбор отзыва
        return random.choice(reviews[rating])
    
    def print_review(self):
        print(f"id = {self.rev_id}, user id = {self.user_id}, market id = {self.market_id}, date = {self.date_time}, score = {self.score}, review = {self.review}")
    
    def to_tuple(self):
        return (self.rev_id, self.user_id, self.market_id, self.date_time, self.score, self.review)
    
def generate_reviews(user_ids, market_ids):
    """
    Генерирует список отзывов в виде кортежей
    :param user_ids: список ID пользователей
    :param market_ids: список ID магазинов
    :return: список кортежей с отзывами
    """
    reviews = []
    rev_id = 1
    
    for user_id in user_ids:
        # Каждый пользователь оставляет от 1 до 6 отзывов
        num_reviews = random.randint(1, 6)
        # Выбираем случайные магазины для отзывов
        selected_markets = random.sample(market_ids, min(num_reviews, len(market_ids)))
        
        for market_id in selected_markets:
            review = Review(rev_id, user_id, market_id)
            reviews.append(review.to_tuple())
            rev_id += 1
    
    return reviews
            
if __name__ == "__main__":
    
    import tabulate
    
    # Тестовые данные
    user_ids = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116]
    market_ids = [1, 2, 3, 4, 5, 6, 7, 8]
    
    # Создание одну рецензию
    new_review = Review(0, 0, 0)
    new_review.print_review()
    
    # Создаем список рецензий
    reviews = generate_reviews(user_ids, market_ids)
    print(tabulate.tabulate(reviews))
    
    input("нажать клавишу")