# -*- coding: utf-8 -*-
#Модель (Model)
#Работа с данными. Ответ на запросы от основного приложения

#-------------------------------------------------------------------------------------- 
import psycopg # модуль для работы с DB postgreSQL (pip install psycopg[binary])

#--------------------------------------------------------------------------------------
# установка подключения к БД
conn = psycopg.connect(dbname="zip",
                       host="localhost",
                       user="",
                       password="",
                       port="5432")
#--------------------------------------------------------------------------------------
# создаем курсор
cur = conn.cursor()
#--------------------------------------------------------------------------------------
def zip_by_location(location): # Принимает: location - список локации (город, штат) пример ("Anchorage", "AK")
    city, state = location
    zips = [] # список кодов
    cur.execute("""SELECT zip_code FROM zip_codes z WHERE lower(z.city) = %s AND lower(z.state) = %s;""", (city.lower(), state.lower()))
    res = cur.fetchall()
    for record in res:
        #print(res)
        zips.append(record[0]) # добавляем индекс в список кодов    
    return zips # возвращает список кодов
#-------------------------------------------------------------------------------------    
def location_by_zip(zipcode): # Принимает: zip_code - код
    cur.execute("""SELECT * FROM zip_codes z WHERE z.zip_code = %s;""", (zipcode, )) # ищем строчку по индексу
    res = cur.fetchone() # Берем первый результат
    if res is not None and len(res) > 0: #если результат не None и длина более 0
        #print(res)
        return res[1:] # возвращаем кортеж данных по локации с элемента [1]
    return () # возвращаем пустой кортеж
    
#location_by_zip('12180') #тест
#zip_by_location(('miami','fl')) #тест