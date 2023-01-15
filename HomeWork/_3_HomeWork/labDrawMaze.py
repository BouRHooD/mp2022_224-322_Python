# HW: labDrawMaze - Нарисовать в консоли сгенерированный лабиринт с параметрами: ширина, высота
# Как генерировать лабиринт: https://github.com/Yan-Minotskiy/labyrinth_generating/blob/master/README.md 
# Как генерировать лабиринт 2: https://habr.com/ru/post/262345/
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

block_wall  = "██"
block_floor = "  "
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

def create_maze_wall(matrix):
    res = matrix
    if len(matrix) == 0:
        return res

    UNVISITED_CELLS = []

    row_end = len(matrix)
    col_end = len(matrix[0])
    for row in range(row_end):
        for column in range(col_end):
            # Если ячейка нечетная по x и y
            if row % 2 != 0 and column % 2 != 0:
                # И при этом находится в пределах стен лабиринта
                if row < row_end - 1 and column < col_end - 1:
                    # То это КЛЕТКА - пол
                    res[row][column] = block_floor
                    UNVISITED_CELLS.append([row, column])
            # В остальных случаях это СТЕНА
            else:
                # То это КЛЕТКА - стена
                res[row][column] = block_wall
    return res, UNVISITED_CELLS

def create_maze_startfinish(matrix):
    res = matrix
    if len(matrix) == 0:
        return res

    in_w = len(matrix)
    in_h = len(matrix[0])

    # Делаем проходы начала и конца лабиринта
    start_point = start_point_generate(in_w, in_h) 
    finish_point = finish_point_generate(start_point, in_w, in_h)

    # Ставим проход начала
    _x_start = start_point[0]
    _y_start = start_point[1]
    res[_x_start][_y_start] = block_floor

    # Ставим проход конца
    _x_finish = finish_point[0]
    _y_finish = finish_point[1]
    res[_x_finish][_y_finish] = block_floor
    
    return res, start_point, finish_point

def get_neighbours_points(matrix, in_point, distance, UNVISITED_CELLS):
    res = matrix
    if len(matrix) == 0:
        return res

    _x = in_point[0]
    _y = in_point[1]
    _up = [_x, _y - distance]
    _rt = [_x + distance, _y]
    _dw = [_x, _y + distance]
    _lt = [_x - distance, _y]
    _d = [_dw, _rt, _up, _lt]

    _cells = []

    _in_w = len(matrix)
    _in_h = len(matrix[0])

    # Для каждого направления d
    for i in range(4):
        _d_x = _d[i][0]
        _d_y = _d[i][1]
        # Если не выходит за границы лабиринта
        if _d_x > 0 and _d_x < _in_w and _d_y > 0 and _d_y < _in_h:
            mazeCellCurrent = matrix[_d_x][_d_y]
            cellCurrent = _d[i]
            if mazeCellCurrent != block_wall and cellCurrent in UNVISITED_CELLS:
                _cells.append(cellCurrent)
        pass
        
    return _cells

def remove_wall(first_cell, second_cell, matrix, UNVISITED_CELLS):
    res = matrix
    if len(matrix) == 0:
        return res
    
    x_diff = second_cell[0] - first_cell[0]
    y_diff = second_cell[1] - first_cell[1]
    addX = x_diff / abs(x_diff) if x_diff != 0 else 0
    addY = y_diff / abs(y_diff) if y_diff != 0 else 0
    target = [first_cell[0] + addX, first_cell[1] + addY]

    if UNVISITED_CELLS.count(target) > 0:
        UNVISITED_CELLS.remove(target)

    matrix[target[0]][target[1]] = block_floor
    return matrix

def create_clear_map(in_w: 0, in_h: 0):
    # Создаем матрицу HxW
    new_matrix = create_matrix(in_w, in_h)

    # Делаем границы с стенами
    wall_matrix = create_wall(new_matrix)

    # Делаем стены лабиринта (сырой вариант)
    maze_matrix, UNVISITED_CELLS = create_maze_wall(wall_matrix)

    # Делаем прохода начала и конца
    # maze_startfinish, start_point, finish_point = create_maze_startfinish(maze_matrix)

    # Генерируем лабиринт
    current_point = [1, 1]
    neighbour_point = None
    
    # Если у клетки есть непосещенные соседи
    stack_points = []
    neighbours_points = get_neighbours_points(maze_matrix, current_point, 2, UNVISITED_CELLS)
    if len(neighbours_points) != 0:
        import random
        randNum = random.randint(0, len(neighbours_points) - 1)
        neighbourCell = neighbours_points[randNum]; # Выбираем случайного соседа
        stack_points.append(current_point)          # Заносим текущую точку в стек
        # Убираем стену между текущей и сосендней точками
        maze_matrix, UNVISITED_CELLS = remove_wall(maze_matrix)  
        # Делаем соседнюю точку текущей и отмечаем ее посещенной
        current_point = neighbourCell
        if UNVISITED_CELLS.count(current_point) > 0:
            UNVISITED_CELLS.remove(current_point)
    elif len(neighbours_points) == 0:
        pass
    else:
        pass

    return maze_matrix

def start_point_generate(n, m):
    """Функция выбора точки начала лабиринта"""
    import random
    # Определяем с какой стороны
    if random.choice([True, False]):
        # Определяем вторую координату
        if random.choice([True, False]):
            start = (0, random.randint(0, m - 1))
        else:
            start = (n - 1, random.randint(0, m - 1))
    else:
        if random.choice([True, False]):
            start = (random.randint(0, n - 1), 0)
        else:
            start = (random.randint(0, n - 1), m - 1)
    return start


def finish_point_generate(start, n, m):
    """Выбор точки конца лабиринта"""
    return n - 1 - start[0], m - 1 - start[1]

def create_matrix(in_w: 0, in_h: 0):
    new_matrix = [[f"  " for j in range(in_w)] for i in range(in_h)]
    return new_matrix

def draw_maze_map():
    _w = int(input("Укажите ширину лабиринта: "))
    _h = int(input("Укажите высоту лабиринта: "))

    # Делаем чистую карту лабиринта
    matrix_clear_map = create_clear_map(_w, _h)

    # Выводим карту
    draw_matrix(matrix_clear_map)

def main_loop():
    """ Цикл повтора """
    isAgain = True
    while isAgain:
        try:
            draw_maze_map()
        except Exception as ex:
            print(ex)
        finally:
            print()
            isAgain = input("Повторить? [y/n] [1/0] - ").lower() in ["1", "y"]

# Точка входа в программу
if __name__ == "__main__":   
    main_loop()