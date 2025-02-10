# -*- coding: utf-8 -*-

header = [] #для заголовка
zip_codes = [] #список для индексов
zip_data = [] #структура данных одной строки (индекса)

i = 0 #счетчик строк

path = r'..\zip_codes_states.csv' #путь к файлу

for line in open(path).read().split("\n"): # читаем одной строкой весь файл и разбиваем построчно по символу переноса методом split("\n")
    #rint(line) #... "99950",55.542007,"-131.432682","Ketchikan","AK","Ketchikan Gateway"
    m = line.strip().replace('"', '').split(",") # Удаляем пробелы с обеих сторон, удаляем '"' из строки, разделяем строку по ','
    #print(m) #... ['99950', '55.542007', '-131.432682', 'Ketchikan', 'AK', 'Ketchikan Gateway']
    
    # формирование списка
    i += 1 #счетчик строк
    skip_line = False #не пропускаем строки
    if i == 1: # записываем шапку в список header, если счетчик = 1(первая строка)
        for val in m:
            header.append(val)            
        #print(header) # ['zip_code', 'latitude', 'longitude', 'city', 'state', 'county']
        
    else:
        zip_data = []
        for idx in range(0, len(m)): # читаем каждую строку по индексу в списке от 0 до 5
            
            if m[idx]=='':  # пропускаем всю строку без записи, если присутствует пустое поле в строке 
                skip_line = True
                break
            
            if header[idx] == "latitude" or header[idx] == "longitude": # если индекс совпадает с наименованием в header 
                val = float(m[idx]) # то преобразуем поле во float
            else:
                val = m[idx] # оставляем поле как есть.
            zip_data.append(val) # добавляем очищенное поле в индекс
            
        if not skip_line: # добавляем список данных индекса в список списков если skip_line = False
            zip_codes.append(zip_data) 
            #print(zip_data) #... ['99950', 55.542007, -131.432682, 'Ketchikan', 'AK', 'Ketchikan Gateway']
            
# print(header) # шапка ['zip_code', 'latitude', 'longitude', 'city', 'state', 'county']
# print(zip_codes[2]) # строка 2 ['00601', 18.165273, -66.722583, 'Adjuntas', 'PR', 'Adjuntas']

