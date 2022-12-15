# HW: создать двумерный массив, заполнить случайными значениями, 
# например, от 10 до 99, распечатать его и затем в цикле выбирать действие 
# (повернуть влево, вправо, отразить ...) и тоже распечатать
# -------------------------------------------------------------------------

class my_matrix:
    """ Класс методов для работы с матрицами """

    def init_matrix():
        """ 
        Инициализация матрицы \n 
        (српашиваем у пользователя ширину и высоту) 
        """
        import random
        _w = int(input("Укажите ширину матрицы: "))
        _h = int(input("Укажите высоту матрицы: "))
        new_matrix = [[random.randint(10, 99) for j in range(_w)] for i in range(_h)]
        return new_matrix

    def draw_matrix(in_matrix):
        """ Нарисовать матрицу в консоль """
        
        if my_matrix.matrix_is_invalid(in_matrix): return

        print()
        h, w = len(in_matrix), len(in_matrix[0])
        for y in range(h):
            for x in range(w):
                print(in_matrix[x][y], end=' ')
            print()

    def work_with_matrix(in_matrix):
        """ 
        Работа с матрицой \n 
        (спрашиваем у пользователя номер команды) \n 
        (1 - повернуть влево, 2 - вправо, 3 - отразить ...) 
        """
        
        if my_matrix.matrix_is_invalid(in_matrix): return

        print()
        commands_list = ["Повернуть влево ←", "Повернуть вправо →", "Отразить ↔"] 
        print("Список команд:")
        [print(f"{_index}: {_command}") for _index, _command in enumerate(commands_list)]
        print()

        select_command = int(input("Введите выбранный номер команды: "))
        if select_command == 0: return my_matrix.turn_left_matrix(in_matrix)
        if select_command == 1: return my_matrix.turn_right_matrix(in_matrix)
        if select_command == 2: return my_matrix.flip_matrix(in_matrix)

    def turn_left_matrix(in_matrix):
        ''' Повернуть матрицу влево ← '''
        
        if my_matrix.matrix_is_invalid(in_matrix): return

        h, w = len(in_matrix), len(in_matrix[0])
        new_array = [[None] * h for _ in range(w)]
        for c in range(w - 1, -1, -1):
            for r in range(h):
                new_array[c][h - r - 1] = in_matrix[r][c]
        return new_array.copy()


    def turn_right_matrix(in_matrix):
        ''' Повернуть матрицу вправо → '''
        
        if my_matrix.matrix_is_invalid(in_matrix): return

        h, w = len(in_matrix), len(in_matrix[0])
        new_array = [[None] * h for _ in range(w)]
        for c in range(w):
            for r in range(h - 1, -1, -1):
                new_array[w - c - 1][r] = in_matrix[r][c]
        return new_array.copy()


    def flip_matrix(in_matrix):
        ''' Отразить матрицу ↔ '''

        if my_matrix.matrix_is_invalid(in_matrix): return

        h, w = len(in_matrix), len(in_matrix[0])
        new_array = [[None] * h for _ in range(w)]
        for c in range(w):
            for r in range(h):
                new_array[r][c] = in_matrix[w - r - 1][c]
        return new_array.copy()

    def matrix_is_invalid(in_matrix):
        """ Проверяем матрицу на состояние работы """
        
        if in_matrix is None or len(in_matrix) == 0:
            print("!!!!! В матрице нет элементов !!!!!")
            return True
        return False

def main_loop(in_matrix):
    """ Цикл повтора """

    if my_matrix.matrix_is_invalid(in_matrix): return

    isAgain = True
    while isAgain:
        try:
            in_matrix = my_matrix.work_with_matrix(in_matrix)
            my_matrix.draw_matrix(in_matrix)
        except Exception as ex:
            print(ex)
        finally:
            print()
            in_val  = input("Повторить? [y/n] [1/0] - ").lower()
            isAgain = in_val == "y" or in_val == "1"

# Точка входа в программу
if __name__ == "__main__":   
    new_matrix = my_matrix.init_matrix()
    my_matrix.draw_matrix(new_matrix)
    main_loop(new_matrix)