from random import randint
import time

NUMBER_OF_THROW = 5

#Ввод имен играющих
igrok1 = input('Введите имя 1-го играющего ')
igrok2 = input('Введите имя 2-го играющего ')

pointsP1 = 0
pointsP2 = 0
for i in range(NUMBER_OF_THROW):
    #Моделирование бросания кубика первым играющим
    print('Кубик бросает', igrok1)
    time.sleep(2)
    n1 = randint(1, 6)
    print('Выпало:', n1)
    pointsP1 += n1
    #Моделирование бросания кубика вторым играющим
    print('Кубик бросает', igrok2)
    time.sleep(2)
    n2 = randint(1, 6)
    print('Выпало:', n2)
    pointsP2 += n2

#Определение результата (3 возможных варианта)
print(f"""Общее количество очков: 
      {igrok1} = {pointsP1}
      {igrok2} = {pointsP2}""")
if pointsP1 > pointsP2:
    print('Выиграл', igrok1)
elif pointsP1 < pointsP2:
    print('Выиграл', igrok2)
else:
    print('Ничья')