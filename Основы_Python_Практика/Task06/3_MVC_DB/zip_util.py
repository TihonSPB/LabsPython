# -*- coding: utf-8 -*-


import math
 
EARTH_RADIUS_MI = 3959.191 # радиус земли в милях
UNITS = 'миль'
    
def calculate_distance(location1, location2): # Принимает: координаты
    """
    This function returns the great-circle distance between location1 and
    location2.
    
    (iterable, iterable) -> float

    Parameters:
    location1 (iterable): The geographic coordinates
    of the first location. The first element of the iterable is latitude,
    the second one is longitude.

    location2 (iterable): The geographic coordinates
    of the second location. The first element of the iterable is latitude,
    the second one is longitude.

    Returns:
    float: Value of the distance in U.S. miles between two locations computed using
    the haversine formula
    """
    lat1 = math.radians(location1[0]) # преобразуем в радианы
    lat2 = math.radians(location2[0]) # преобразуем в радианы
    long1 = math.radians(location1[1]) # преобразуем в радианы
    long2 = math.radians(location2[1]) # преобразуем в радианы
    # вычисление расстояния по формуле Хаверсина
    del_lat = (lat1 - lat2) / 2
    del_long = (long1 - long2) / 2
    angle = math.sin(del_lat)**2 + math.cos(lat1) * math.cos(lat2) * \
        math.sin(del_long)**2
    distance = 2 * EARTH_RADIUS_MI * math.asin(math.sqrt(angle))
    return distance # возвращает растояние междк координатами