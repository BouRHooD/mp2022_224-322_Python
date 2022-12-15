# HW: Нарисовать в консоли прямоугольную змейку с параметрами: ширина, высота

'''
Каждую 4 строчку происходит повторение змейки:
    1) в каждой четной - хвост;
    2) в каждой 1 строке - тело;
    3) в каждой 3 строке - тело. 

Пример:
0: -----
1:     -
2: -----
3: -
'''
block = "██"
def draw_sneak(): 
    # Входные данные пользователя
    in_w = int(input("Ширина? - "))
    in_h = int(input("Высота? - "))

    # Рисование змейки 
    for row in range(in_h):
        for column in range(in_w):
            is_digit_parity = row % 2 == 0                      # Если строка четная, то там блок змейки - хвост
            is_val_1 = (column == in_w - 1 and row % 4 == 1)    # Если колонка последняя и строка в которой должно быть тело, то там блок змейки
            is_val_2 = (column == 0 and row % 4 == 3)           # Если колонка первая и строка в которой должно быть тело, то там блок змейки 
            if (is_digit_parity or is_val_1 or is_val_2):
                print(block, end="")
            else:
                print(" ", end=" ")
        print()

# Цикл повтора
isAgain = True
while isAgain:
    try:
        draw_sneak()
    except Exception as ex:
        print(ex)
    finally:
        isAgain = input("Повторить? [y/n] - ").lower() == "y"
