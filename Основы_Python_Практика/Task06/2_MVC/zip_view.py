# -*- coding: utf-8 -*-
# Вью (View)
# Представление. Отвечает за вывод пользователю 

import math

def ordinal(x):
    ordinals = [
        "first", "second", "third", "fourth", "fifth",
        "sixth", "seventh", "eighth", "ninth", "tenth",
        "eleventh", "twelfth"]
    return ordinals[x-1]

MINS_IN_HOUR = 60
SECS_IN_MIN = 60

def degree_minutes_seconds(location): # Разбивка локации на градусы, минуты, секунды
    minutes, degrees = math.modf(location)
    degrees = int(degrees)
    minutes *= MINS_IN_HOUR
    seconds, minutes = math.modf(minutes)
    minutes = int(minutes)
    seconds = SECS_IN_MIN * seconds
    return degrees, minutes, seconds # Кортеж

def format_location(location): # Вывод градусов в формате (025°44'16.00"N,080°13'29.17"W)
    # Определяем полушарие 
    ns = ""
    if location[0] < 0:
        ns = 'S'
    elif location[0] > 0:
        ns = 'N'

    ew = ""
    if location[1] < 0:
        ew = 'W'
    elif location[0] > 0:
        ew = 'E'

    format_string = '{:03d}\xb0{:0d}\'{:.2f}"' # Градусы{:03d}-(03-3 знака; d-целое число); \xb0-символ "°"; Минуты{:0d}\'-0 будет сохраннен; Секунды{:.2f}"-Дробное с двумя знаками после запятой.
    latdegree, latmin, latsecs = degree_minutes_seconds(abs(location[0]))
    latitude = format_string.format(latdegree, latmin, latsecs)
    longdegree, longmin, longsecs = degree_minutes_seconds(abs(location[1]))
    longitude = format_string.format(longdegree, longmin, longsecs)
    return '(' + latitude + ns + ',' + longitude + ew + ')'

def print_prompt():
    print("Команды ('loc', 'zip', 'dist', 'end') => ", end='')

def print_command(command):
    print(command)

def print_invalid_command():
    print("Неверная команнда")

def print_newline():
    print()

def print_exit():
    print("Выход")

def print_request_single_zip():
    print('Введите почтовый индекс для поиска => ', end='')

def print_zip(zipcode):
    print(zipcode)

def print_location(zipcode, location):
    print('Почтовый индекс {} находится в {}, {}, округ {},\nкоординаты: {}'.
      format(zipcode, location[2], location[3], location[4],
             format_location((location[0], location[1]))))

def print_invalid_zip():
    print('Неверный или неизвестный почтовый индекс')
    
def print_request_city():
    print('Введите название города для поиска => ', end='')

def print_city(city):
    print(city)

def print_request_state():
    print('Введите название штата для поиска => ', end='')

def print_state(state):
    print(state)

def print_zip_found(city, state, zipcodes):
    print('Следующий(ие) почтовый(ые) индекс(ы) найден(ы) для {}, {}: {}'.
              format(city, state, ", ".join(zipcodes)))

def print_zip_not_found(city, state):
    print('Не найдено ни одного почтового индекса для {}, {}'.format(city, state))

def print_request_zip(ord):
    assert ord <= 12
    print(f'Введите {ordinal(ord)} почтовый индекс => ', end='')

def print_invalid_distance(zip1, zip2):
    print('Расстояние между {} и {} не может быть определен'.
              format(zip1, zip2))

def print_distance(zip1, zip2, dist, units):
    print('Расстояние между {} и {} составляет {:.2f} {}'.
              format(zip1, zip2, dist, units))