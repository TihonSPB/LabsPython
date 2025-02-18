# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------- 
# чтение нормализация csv файла
def read_zip_all():
    header = [] #для заголовка
    zip_codes = [] #список списков всех индексов
    zip_data = [] #список данных одной строки (одного индекса)

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
    return(zip_codes)
#-------------------------------------------------------------------------------------- 
# Функционал
import math
 
EARTH_RADIUS_MI = 3959.191 # радиус земли в милях


def zip_by_location(codes, location): # Принимает: codes - список списков, location - список локации (город, штат) пример ("Anchorage", "AK")
    zips = [] # список кодов
    for code in codes: # Проходим по всему списку списков 
        # Сравниваем город из списка локации со спипком списков И штат из списка локации со спипком списков (все в нижнем регистре lower())
        if location[0].lower() == code[3].lower() and location[1].lower() == code[4].lower():
            zips.append(code[0]) # добавляем индекс в список кодов
    return zips # возвращает список кодов zip_code

def location_by_zip(codes, zipcode): # Принимает: codes - список списков, zip_code - код
    for code in codes: # Проходим по всему списку списков
        if code[0] == zipcode: # сравнивает код с кодом из списка
            return tuple(code[1:]) # возвращаем кортеж данных по локации с элемента [1]
    return() # возвращаем пустой кортеж
    
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
#--------------------------------------------------------------------------------------
# Взаимодействие с пользователем

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

def process_loc(codes):
    zipcode = input('Введите почтовый индекс для поиска => ') # запрос индекса
    print(zipcode)
    location = location_by_zip(codes, zipcode) 
    if len(location) > 0:
        print('Почтовый индекс {} находится в {}, {}, округ {},\nкоординаты: {}'.
              format(zipcode, location[2], location[3], location[4], 
                     format_location((location[0], location[1]))))
    else:
        print('Неверный или неизвестный почтовый индекс')

def process_zip(codes):
    city = input('Введите название города для поиска => ')
    print(city)
    city = city.strip().title()
    state = input('Введите название штата для поиска => ')
    print(state)
    state = state.strip().upper()
    zipcodes = zip_by_location(codes, (city, state))
    if len(zipcodes) > 0:
        print('Следующий(ие) почтовый(ые) индекс(ы) найден(ы) для {}, {}: {}'.
              format(city, state, ", ".join(zipcodes)))
    else:
        print('Не найдено ни одного почтового индекса для {}, {}'.format(city, state))

def process_dist(codes):
    pass

    zip1 = input('Введите первый почтовый индекс => ')
    print(zip1)
    # logging.info(f'Received the first ZIP {zip1}')
    # logger_main.info(f'Получили первый почтовый индекс {zip1}')
    zip2 = input('Введите второй почтовый индекс => ')
    print(zip2)
    # logging.info(f'Received the second ZIP {zip2}')
    # logger_main.info(f'Получил второй почтовый индекс {zip2}')

    location1 = location_by_zip(codes, zip1)
    location2 = location_by_zip(codes, zip2)
    if len(location1) == 0 or len(location2) == 0:
        print('Расстояние между {} и {} не может быть определено'.
              format(zip1, zip2))
    else:
        dist = calculate_distance(location1, location2)
        print('Расстояние между {} и {} составляет {:.2f} миль.'.
              format(zip1, zip2, dist))

#--------------------------------------------------------------------------------------
# Основная часть программы 
if __name__ == "__main__": 
    
    #ТЕСТИРОВАНИЕ
    EPSILON_MI = 0.1 # погрешность в милях
    EPSILON_COORD = 0.00001 # погрешность в градусах
    # счетчик тестов
    passed = 0
    failed = 0
    codes = read_zip_all() #список списков
    
    # тест 1 Проверка данных на корректность при переносе с csv
    if codes[568] == ["01970",42.512946,-70.904237,"Salem","MA","Essex"]:
        passed += 1
    else:
        print("ОШИБКА тест 1.")
        failed += 1        
    # тест 2 Проверка расчета дистанции 
    location1 = (codes[568][1],codes[568][2])
    location2 = (codes[581][1],codes[581][2])
    if abs(calculate_distance(location1, location2) - 27.20) < EPSILON_MI :
        passed += 1
    else:
        print("ОШИБКА тест 2.")
        failed += 1
    # тест 3 Проверка города по нескольким индексам
    # if zip_by_location(codes, ("Anchorage", "AK")) == ["99501","99502","99503","99504","99507","99508","99509","99510","99511","99512","99513","99514","99515","99516","99517","99518","99519","99520","99521","99522","99523","99524","99599","99695"]:
    # без учета порядка записей списка индексов. Приводим список ко множеству set([]) => {}
    if set(zip_by_location(codes, ("Anchorage", "AK"))) == set(["99501","99502","99503","99504","99507","99508","99509","99510","99511","99512","99513","99514","99515","99516","99517","99518","99519","99520","99521","99522","99523","99524","99599","99695"]):
        passed += 1
    else:
        print("ОШИБКА тест 3.")
        failed += 1
    # тест 4 Проверка города по одному индексу
    if zip_by_location(codes, ("Clarkston","WA")) == ["99403"]:
        passed += 1
    else:
        print("ОШИБКА тест 4.")
        failed += 1
    # тест 5 Проверка поиска локации по индексу
    loc = location_by_zip(codes, "99173")
    48.002188, -117.828964, 
    if loc[2:] == ("Springdale", "WA", "Stevens") and abs(loc[0] - 48.002188) < EPSILON_COORD and abs(loc[1] - -117.828964) < EPSILON_COORD:
        passed += 1
    else:
        print("ОШИБКА тест 5.")
        failed += 1
    # Итог тестирования
    if failed == 0:
        print(f'Все тесты ({passed}) успешно пройдены')
    else:
        print(f'Провалено {failed} тестов.{passed} успешно пройдены') 
        
    #print(read_zip_all())
#--------------------------------------------------------------------------------------    
    #Интерфейс пользователя
    zip_codes = read_zip_all()
    command = ""
    
    while command != "end":
        command = input("Команды ('loc', 'zip', 'dist', 'end') => ") # запрос команды и ввод
        
        '''
        # logging.info(f'Received command {command}')
        logger_main.debug('Debugging...')
        #logger.log(logging.CRITICAL, 'Critical error detected!')
        logger_main.info(f'Received command {command}')
        logger_aux.info(f'Received command {command}')
        '''
        
        print(command)
        command = command.strip().lower() #удаляются пробелы с обоих сторон, приводим к нижнему регистру
        # Выполнение выбранной команды
        if command == 'loc':
            process_loc(zip_codes)
        elif command == 'zip':
            process_zip(zip_codes)
        elif command == 'dist':
            process_dist(zip_codes)
        elif command != 'end':
            print("Неверная команнда")
        print()
    print("Выход")
    '''
    for handler in logger_main.handlers:
        logger_main.removeHandler(handler)
        handler.close()
    logging.shutdown()
    '''