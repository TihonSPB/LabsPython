# -*- coding: utf-8 -*-

#               d2
#             ◁───▷
#    △┌───────┬───┐😱
#    ││       │l2╱│
#    ││       │ ╱ │      x=d1*tan(o1)
#    ││       │╱o2│      l1=sqrt(x^2 +d1^2)
#   h│├───────┼───┤      l2=sqrt((h-x)^2+d2^2)
#    ││   o1 ╱│△  │      t=1/v_sand * (l1+n*l2)
#    ││     ╱ ││  │
#    ││    ╱  ││  │      1 ярд = 0,9144 м
#    ││   ╱   ││x │      1 фут = 0,3048 м
#    ││  ╱ l1 ││  │      1 миля = 1,60934 км
#    ││ ╱     ││  │      1 градус = пи/180 рад
#    ││╱      ││  │
#    ▽└───────┴───┘
#   🙂◁──────▷
#        d1

import math

# Преобразование в тип с плавающей точкой
# Ярды в метры
def yards_to_meters (yard):
    return yard * 0.9144
# Футы в метры
def feet_to_meters (feet):
    return feet * 0.3048
# Мили в метры
def miles_to_meters (miles):
    return miles * 1609.34

# Преобразование градусов в радианы
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)

# Преобразование часов в минуты секунды
def hours_to_minutes_seconds(hours):
    minutes = int(hours * 60)
    seconds = (hours * 60 - minutes) * 60
    return minutes, seconds

# Основная часть программы
if __name__ == "__main__":
    d1 = 8 #Кратчайшее расстояние от спасателя до кромки воды (в ярдах)
    d2 = 10 #Кратчайшее расстояние от утопающего до берега (в футах)
    h = 50 #Боковое смещение между спасателем и утопающим (в ярдах)
    v_sand = 5 #Скорость движения спасателя по песку (в милях в час)
    n = 2 #Коэффициент замедления спасателя при движении в воде
    o1 = 39.413 #Направление движения спасателя по песку (в градусах)

    # Преобразование переменных  
    d1 = yards_to_meters(d1)
    d2 = feet_to_meters(d2)
    h = yards_to_meters(h)
    v_sand = miles_to_meters(v_sand)
    o1 = degrees_to_radians(o1)
   
    x = d1*math.tan(o1)
   
    l1 = math.sqrt(x**2+d1**2)
    l2 = math.sqrt((h-x)**2 + d1**2)
               
    t = 1/v_sand * (l1+n*l2)
   
    minutes, seconds = hours_to_minutes_seconds(t)
    print(t)
       
    print(f"Время, затраченное на спасение: {minutes} минут и {seconds:.2f} секунд")