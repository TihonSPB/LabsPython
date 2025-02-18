# -*- coding: utf-8 -*-
# Контроллер (Controller)
# Взаимодействует с пользователем (Принимает ввод от пользователя). Соединяет модель и представление
# Основная часть программы
 
import zip_view as view
import zip_util_metric as zu #Импортируем функционал из файла zip_util или zip_util_metric, как zu
import zip_model as model

def process_loc():
    view.print_request_single_zip()
    zipcode = input()
    view.print_zip(zipcode)
    location = model.location_by_zip(zipcode)
    if len(location) > 0:
        view.print_location(zipcode, location)
    else:
        view.print_invalid_zip()

def process_zip():
    view.print_request_city()
    city = input()
    view.print_city(city)
    city = city.strip().title()
    view.print_request_state()
    state = input()
    view.print_state(state)
    state = state.strip().upper()
    zipcodes = model.zip_by_location((city, state))
    if len(zipcodes) > 0:
        view.print_zip_found(city, state, zipcodes)
    else:
        view.print_zip_not_found(city, state)

def process_dist():
    view.print_request_zip(1)
    zip1 = input()
    view.print_zip(zip1)
    view.print_request_zip(2)
    zip2 = input()
    view.print_zip(zip2)

    location1 = model.location_by_zip(zip1)
    location2 = model.location_by_zip(zip2)
    if len(location1) == 0 or len(location2) == 0:
        view.print_invalid_distance(zip1, zip2)
    else:
        dist = zu.calculate_distance(location1, location2)
        view.print_distance(zip1, zip2, dist, zu.UNITS)
#--------------------------------------------------------------------------------------        

command = ""
while command != 'end':
    view.print_prompt()
    command = input()
    view.print_command(command)
    command = command.strip().lower()
    if command == 'loc':
        process_loc()
    elif command == 'zip':
        process_zip()
    elif command == 'dist':
        process_dist()
    elif command != 'end':
        view.print_invalid_command()
    view.print_newline()
view.print_exit()