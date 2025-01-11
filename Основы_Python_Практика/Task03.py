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

#######################################################
def RAMKA (string):
    n = len(string)+4
    return "#"*n
        
def INFO_VARIABLE (a):
    name = list(globals().keys())[list(globals().values()).index(a)]
    string = f"ПРОВЕРКА Имя: {name}; Значение: {a}; Тип: {type(a)}; ID: {id(a)}"
    cellWidth = RAMKA(string)
    print(f"""
{cellWidth}
# {string} #
{cellWidth}
""")
####################################################### 

import math

# Константы для преобразования единиц измерения
YARDS_TO_METERS = 0.9144
FEET_TO_METERS = 0.3048
MILES_TO_METERS = 1609.34

# Ввод данных
def entering_data (massage):
    while True:
        try:
            data = float(input(massage))
            return data
        except ValueError:
            print("Ошибка ввода. Пожалуйста, введите число.")

# Преобразование в метры
# Ярды в метры
def yards_to_meters (yard):
    return yard * YARDS_TO_METERS
# Футы в метры
def feet_to_meters (feet):
    return feet * FEET_TO_METERS
# Мили в метры
def miles_to_meters (miles):
    return miles * MILES_TO_METERS

# Преобразование градусов в радианы
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)

# Преобразование часов в минуты секунды
def hours_to_minutes_seconds(hours):
    minutes = int(hours * 60)
    seconds = (hours * 60 - minutes) * 60
    return minutes, seconds

# Расчет
def calculation (d1, d2, h, v_sand, n, o1):
    d1 = yards_to_meters(d1)
    d2 = feet_to_meters(d2)
    h = yards_to_meters(h)
    v_sand = miles_to_meters(v_sand)
    o1 = degrees_to_radians(o1)
    
    x = d1*math.tan(o1)
    
    l1 = math.sqrt(x**2+d1**2)
    l2 = math.sqrt((h-x)**2 + d1**2)
                
    t = 1/v_sand * (l1+n*l2)
    
    return t
    
# Расчет времени при заданном угле
def time_at_a_given_angle (d1, d2, h, v_sand, n, o1):
    t = calculation(d1, d2, h, v_sand, n, o1)
    minutes, seconds = hours_to_minutes_seconds(t)
    return minutes, seconds

# Перебор углов и поиск оптимального времени
def find_optimal_angle (d1, d2, h, v_sand, n):
    min_time = float('inf')
    best_o1 = None
    for o1_test in range(0, 91, 1):  # Проверяем углы от 0 до 90 градусов с шагом 1
        total_time = calculation(d1, d2, h, v_sand, n, o1_test)
        if total_time < min_time:
            min_time = total_time
            best_o1 = o1_test
                            
    minutes, seconds = hours_to_minutes_seconds(min_time)
   
    return minutes, seconds, best_o1

# Основная часть программы
if __name__ == "__main__":
        
    d1 = entering_data("Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды):")
    d2 = entering_data("Введите кратчайшее расстояние от утопающего до берега, d2 (футы):")
    h = entering_data("Введите боковое смещение между спасателем и утопающим, h (ярды):")
    v_sand = entering_data("Введите скорость движения спасателя по песку, v_sand (мили в час):")
    n = entering_data("Введите коэффициент замедления спасателя при движении в воде, n:")
    o1 = entering_data("Введите направление движения спасателя по песку, theta1 (градусы):")
          
    minutes, seconds = time_at_a_given_angle(d1, d2, h, v_sand, n, o1)
    
    print(f"Если спасатель начнёт движение под углом theta1, равным {o1:.0f} градусам, \
он достигнет утопающего через {minutes} минут, {seconds:.1f} секунды")
    
    minutes, seconds, best_o1 = find_optimal_angle(d1, d2, h, v_sand, n)
    
    print(f"Оптимальное значение угла theta1, под которым необходимо начать движение: {best_o1:.0f} градусов. \
Спасатель достигнет утопающего через {minutes} минут, {seconds:.1f} секунды")