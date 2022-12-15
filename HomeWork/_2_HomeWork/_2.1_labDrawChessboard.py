# HW: Нарисовать в консоли шахматную доску

def draw_chessboard():
    cell_black = "■"
    cell_white = "□"
    print("{blocks}".format(blocks="  | abcdefgh |  "))
    for row in range(1, 8 + 1):
        if row % 2 == 1:
            print("{index:<1} | {blocks:^8} | {index:>1}".format(index=row, blocks=(cell_black+cell_white)*4))
        else:
            print("{index:<1} | {blocks:^8} | {index:>1}".format(index=row, blocks=(cell_white+cell_black)*4))
    print("{blocks}".format(blocks="  | abcdefgh |  "))

def draw_chessboard_2():
    cell_black = "⬛"
    cell_white = "⬜"
    print("{blocks}".format(blocks="  |  a b c d e f g h |  "))
    for row in range(1, 8 + 1):
        if row % 2 == 1:
            print("{index:<1} | {blocks:^8} | {index:>1}".format(index=row, blocks=(cell_black+cell_white)*4))
        else:
            print("{index:<1} | {blocks:^8} | {index:>1}".format(index=row, blocks=(cell_white+cell_black)*4))
    print("{blocks}".format(blocks="  |  a b c d e f g h |  "))
    
'''Если запуск происходит из данного файла, то выполняем код ниже, иначе если происходит import, то данный код не выполняется'''
if __name__ == "__main__":            
    draw_chessboard()
    print()
    draw_chessboard_2()