# HW: Нарисовать в консоли прямоугольную улитку с параметрами: ширина, высота

'''
Создаем матрицу HxW, проходимся по ней алгоритмом улитки 
(https://ourcodeworld.com/articles/read/827/how-to-format-a-given-array-matrix-in-spiral-form-snail-or-clockwise-spiral-sorting-in-python)
выставляем блоки и выводим матрицу в консоль
 
Пример (12x11)(HxW):
0:  0 1 2 3 4 5 6 7 8 9 10          * * * * * * * * * * *
1:  0 1 2 3 4 5 6 7 8 9 10                              *
2:  0 1 2 3 4 5 6 7 8 9 10          * * * * * * * * *   *
3:  0 1 2 3 4 5 6 7 8 9 10          *               *   *
4:  0 1 2 3 4 5 6 7 8 9 10          *   * * * * *   *   *
5:  0 1 2 3 4 5 6 7 8 9 10  ---->   *   *       *   *   *
6:  0 1 2 3 4 5 6 7 8 9 10          *   *   *   *   *   *
7:  0 1 2 3 4 5 6 7 8 9 10          *   *   * * *   *   *
8:  0 1 2 3 4 5 6 7 8 9 10          *   *           *   *
9:  0 1 2 3 4 5 6 7 8 9 10          *   * * * * * * *   *
10: 0 1 2 3 4 5 6 7 8 9 10          *                   *
11: 0 1 2 3 4 5 6 7 8 9 10          * * * * * * * * * * *
-----
'''
def draw_matrix(matrix):
    res = matrix
    if len(matrix) == 0:
        return res

    row_end = len(matrix)
    col_end = len(matrix[0])
    for row in range(row_end):
        for column in range(col_end):
            print(matrix[row][column], end="")
        print()

def spiral_traversal(matrix):
    res = matrix
    if len(matrix) == 0:
        return res

    row_begin = 0
    row_end   = len(matrix) - 1
    col_begin = 0
    col_end   = len(matrix[0]) - 1

    select_block = block
    while row_begin <= row_end and col_begin <= col_end:
        # Идем вправо
        for i in range(col_begin, col_end + 1):
            res[row_begin][i] = select_block
        row_begin += 1

        # Идем вниз
        for i in range(row_begin, row_end + 1):
            res[i][col_end] = select_block
        col_end -= 1

        # Идем влево
        if row_begin <= row_end:
            for i in range(col_end, col_begin - 1, -1):
                # Если спереди приграда - символ/блок, то меняем символ и пропускаем
                if i - 1 >= 0 and res[row_end][i - 1] == select_block:
                    if select_block == block:
                        select_block = "  "
                    else:
                        select_block = block 
                res[row_end][i] = select_block
        row_end -= 1

        # Идем вверх
        if col_begin <= col_end:
            for i in range(row_end, row_begin - 1, -1):
                # Если спереди приграда - символ/блок, то меняем символ и пропускаем
                if i - 1 >= 0 and res[i - 1][col_begin] == select_block: 
                    if select_block == block:
                        select_block = "  "
                    else:
                        select_block = block
                res[i][col_begin] = select_block
        col_begin += 1

    return res

def create_matrix(in_w: 0, in_h: 0):
    new_matrix = [[f"{i}:{j}" for j in range(in_w)] for i in range(in_h)]
    return new_matrix


block = "██"
def draw_snail(): 
    # Входные данные пользователя
    in_w = int(input("Ширина? - "))
    in_h = int(input("Высота? - "))

    # Создаем матрицу HxW
    new_matrix = create_matrix(in_w, in_h)

    # Делаем из матрицы улитку
    spiral_matrix = spiral_traversal(new_matrix)

    # Рисуем улитку
    draw_matrix(spiral_matrix)
    
            

# Цикл повтора
isAgain = True
while isAgain:
    try:
        draw_snail()
    except Exception as ex:
        print(ex)
    finally:
        isAgain = input("Повторить? [y/n] - ").lower() == "y"