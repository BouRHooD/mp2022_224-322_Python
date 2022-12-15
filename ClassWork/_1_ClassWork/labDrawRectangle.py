# HW: нарисовать 

# В windows можно запустить приложение "Таблица символов"
char = "▓"
in_w = int(input("Ширина?"))
in_h = int(input("Длина?"))
in_f = input("Закрасить? [y/n]")

is_fill = in_f.lower() == "y"
char_fill = char if is_fill else " "

for r in range(in_h):
    print(char * in_w)
    # TODO HW 
