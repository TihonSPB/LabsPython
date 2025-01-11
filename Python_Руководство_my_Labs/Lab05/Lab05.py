from random import randint
import time

NUMBERS_OF_PLAYERS = 2
NUMBER_OF_THROW = 5
MIN_POINTS = 1
MAX_POINTS = 6
DELAY_BETWEEN_THROWS = 2

#Ввод имен играющих
def entering_names ():
    igroki=[]
    
    for i in range(NUMBERS_OF_PLAYERS):
        while True:
            igrok = input(f'Введите имя {i+1}-го играющего: ')
            if igrok in igroki:
                print("Игрок с таким именем уже существует. Пожалуйста, введите новое имя.")
            else:
                igroki.append(igrok)
                break
    
    return igroki

#Моделирование бросания кубика
def throw (igrok):
    print('Кубик бросает', igrok)
    time.sleep(DELAY_BETWEEN_THROWS)
    n = randint(MIN_POINTS, MAX_POINTS)
    print('Выпало:', n)
    
    return n

#Ядро игры
def core_game (igroki):
    data_gamers = {key: [] for key in igroki} # Пустой словарь для хранения данных
    
    for _ in range(NUMBER_OF_THROW):
        for igrok in igroki:
            result = throw(igrok)
            data_gamers[igrok].append(result) 
            
    return data_gamers

#Определение и вывод результата
def determine_winner(results):    
    max_sum = 0
    winner = None
    
    print("Результаты игроков:")
    for igrok, throws in results.items():
        sum_throws = sum(throws)
        print(f"{igrok}: {sum_throws} очков")
        if sum_throws > max_sum:
            max_sum = sum_throws
            winner = igrok
    
    print("Победитель игры:", winner)
    return winner

# Основная часть программы
if __name__ == "__main__":
    gamers = entering_names()
    results = core_game(gamers)   
    winner = determine_winner(results)

 
