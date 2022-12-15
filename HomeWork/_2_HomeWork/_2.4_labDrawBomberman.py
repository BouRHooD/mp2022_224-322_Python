# HW: вывести в консоль карту для игры Bomberman (стены, деревянные стены в случайных местах, пустоты)
# Картинка с примером: http://gamefabrique.com/storage/screenshots/gba/bomberman-jetters-game-collection-03.png
# -------------------------------------------------------------------------

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

block_wall = "██"
def create_wall(matrix):
    res = matrix
    if len(matrix) == 0:
        return res

    row_begin = 0
    row_end   = len(matrix) - 1
    col_begin = 0
    col_end   = len(matrix[0]) - 1

    select_block = block_wall
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
                res[row_end][i] = select_block
        row_end -= 1

        # Идем вверх
        if col_begin <= col_end:
            for i in range(row_end, row_begin - 1, -1):
                res[i][col_begin] = select_block
        col_begin += 1
        break

    return res

def create_clear_map():
    # Создаем матрицу HxW
    new_matrix = create_matrix(25, 11)

    # Делаем стены
    wall_matrix = create_wall(new_matrix)

    row_end = len(wall_matrix) - 1
    col_end = len(wall_matrix[0]) - 1
    for row in range(row_end):
        for col in range(col_end):
            select_value_cell = wall_matrix[row][col]

            # Если уже есть блок, пропускаем ячейку
            if (select_value_cell == block_wall):
                continue
            # Если строка нечетная, то пропускаем, столбы в четных должны быть
            if row % 2 == 1: 
                continue
            # Если колонка нечетная, то пропускаем, столбы в четных должны быть
            if col % 2 == 1:
                continue
            # Ставим столб
            wall_matrix[row][col] = block_wall
    return wall_matrix

block_destroyed_wall = "░░"
def random_destroyed_wall(matrix):
    import random
    row_end = len(matrix) - 1
    col_end = len(matrix[0]) - 1
    for row in range(row_end):
        for col in range(col_end):
            select_value_cell = matrix[row][col]

            # Если уже есть блок, пропускаем ячейку
            if (select_value_cell == block_wall) or (select_value_cell == block_destroyed_wall):
                continue
            # Если рандом выбрал поставить разрушаемую стену, то ставим блок разрушаемой стены
            if random.choice([True, False]):
                matrix[row][col] = block_destroyed_wall
    return matrix

def create_matrix(in_w: 0, in_h: 0):
    new_matrix = [[f"  " for j in range(in_w)] for i in range(in_h)]
    return new_matrix

def draw_bomberman_map():
    # Делаем чистую карту с стенами и столбами внутри
    matrix_clear_map = create_clear_map()
    
    # Создаем разрушаемые стены внутри карты (на данный момент просто другой формат стен)
    final_map = random_destroyed_wall(matrix_clear_map)

    # Выводим карту
    draw_matrix(final_map)

def main_loop():
    """ Цикл повтора """
    isAgain = True
    while isAgain:
        try:
            draw_bomberman_map()
        except Exception as ex:
            print(ex)
        finally:
            print()
            isAgain = input("Повторить? [y/n] [1/0] - ").lower() in ["1", "y"]

# Точка входа в программу
if __name__ == "__main__":   
    main_loop()