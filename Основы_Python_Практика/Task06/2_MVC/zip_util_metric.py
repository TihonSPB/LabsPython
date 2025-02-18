# -*- coding: utf-8 -*-

#Адаптер
#Оболочка на zip_util

import zip_util as zu

#-------------------------------------------------------------------------------------- 

MI_TO_KM = 1.60934 #Мили в километры 
UNITS = 'км'

def mi_to_km(val_mi):
    return MI_TO_KM * val_mi

def calculate_distance(location1, location2): 
    return mi_to_km(zu.calculate_distance(location1, location2)) # Преобразуем ответ из zip_core в километры через функцию mi_to_km
