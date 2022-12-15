# HW: Нарисовать в консоли прямоугольник с параметрами: ширина, высота, закрасить и в конце вопрос "Повторить?" 

# В windows можно запустить приложение "Таблица символов"
char = "▓▓"
isAgain = True
while isAgain:
    try:
        # Входные данные пользователя
        in_w = int(input("Ширина? - "))
        in_h = int(input("Длина? - "))
        in_f = input("Закрасить? [y/n] - ")

        is_fill = in_f.lower() == "y"
        char_fill = char if is_fill else "  "

        # Рисуем
        for r in range(in_h):
            for c in range(in_w):
                # Рисуем границы прямоугольника
                if r == 0 or c == 0 or r == in_h-1 or c == in_w-1:
                    print(char, end="")
                # Заполняем прямоугольник
                else:
                    print(char_fill, end="")
            print()

    except Exception as ex:
        print(ex)
    finally:
        isAgain = input("Повторить? [y/n] - ").lower() == "y"