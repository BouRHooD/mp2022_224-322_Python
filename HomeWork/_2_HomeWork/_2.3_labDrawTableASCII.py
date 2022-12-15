# HW: вывести в консоль таблицу из ascii-символов с параметрами: колонок, строк
# -------------------------------------------------------------------------

def draw_ansii_table(): 
    """ Вывести в консоль таблицу из ascii-символов с параметрами: колонок, строк """
    _w = int(input("Укажите кол-во колнок таблицы из ascii: "))
    _h = int(input("Укажите кол-во строк таблицы из ascii: "))

    max_index_char = _w * _h
    print("Всего элементов:" + str(max_index_char))

    ansii_char_tuple = [chr(i) for i in range(0, max_index_char)]
    for _index, _char in enumerate(ansii_char_tuple):
        # Если индекс уже больше кол-во элементов, которые вмещает матрица, то выходим из цикла
        if (_index + 1) > max_index_char:
            break

        # Некоторые символы в консоль выводятся с ошибкой, необходимо заменить их на пробел
        if _index in [0, 7, 8, 9, 10, 11, 12, 13, 14, 15, 27, 
        28, 29, 127, 128, 129, 130, 131, 132, 133, 134, 135, 
        136, 137, 142, 143, 144, 146, 147, 148, 149, 150, 151, 152, 154, 155, 156, 157, 158, 159]:
            _char = " "

        # Выводим символ в формате (Десятичное число = Символ)
        # r - чтобы могло вывестить \n
        print(rf"{_index} = {_char}".ljust(8, " "), end="|")
        
        # Переносим вывод на следующую строку, если в колонку больше выводить не можем
        if _index != 0 and (_index + 1) % _w == 0:
            print()

def main_loop():
    """ Цикл повтора """
    isAgain = True
    while isAgain:
        try:
            draw_ansii_table()
        except Exception as ex:
            print(ex)
        finally:
            print()
            in_val  = input("Повторить? [y/n] [1/0] - ").lower()
            isAgain = in_val == "y" or in_val == "1"
            
# Точка входа в программу
if __name__ == "__main__":   
    main_loop()