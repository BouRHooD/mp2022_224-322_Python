import random

def game_convert():
    difficulty_level = input("Выберите уровень сложности (1 - детский, 2 - лёгкий, 3 - средний, 4 - сложный): ")
    questions_count = int(input("Введите количество вопросов: "))
    print()

    import time
    start_time = time.time()
    print("Переведите числа в указанную систему счисления:")

    stats = []

    for i in range(questions_count):
        correct_number = 0

        if difficulty_level == '1':
            correct_number = random.randint(0, 7)
        elif difficulty_level == '2':
            correct_number = random.randint(0, 15)
        elif difficulty_level == '3':
            correct_number = random.randint(0, 63)
        elif difficulty_level == '4':
            correct_number = random.randint(0, 255)

        mode = random.choice([10, 16])
        question = '{0:08b}'.format(correct_number)

        if mode == 10:
            question += " in dec = "
            answer = input(question)
            if int(answer) == correct_number:
                stats.append('Правильно')
            else:
                stats.append('Неправильно')

        elif mode == 16:
            question += " in hex = "
            answer = input(question)
            if int(answer, 16) == correct_number:
                stats.append('Правильно')
            else:
                stats.append('Неправильно')
    
    end_time = time.time()

    print(dict(enumerate(stats)))
    print(f"✅ Правильных ответов: {stats.count('Правильно')}")
    print(f"❌ Неправильных ответов: {stats.count('Неправильно')}")
    print(f"⌛ Общее время ответов: {round(end_time - start_time, 3)} секунд")

def main_loop():
    """ Цикл повтора """
    isAgain = True
    while isAgain:
        try:
            game_convert()
        except Exception as ex:
            print(ex)
        finally:
            print()
            isAgain = input("Повторить? [y/n] [1/0] - ").lower() in ["1", "y"]

# Точка входа в программу
if __name__ == "__main__":   
    main_loop()