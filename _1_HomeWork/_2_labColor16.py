# HW: вывести в коносль все доступные цвета и фоны

# ***** Пример (example) https://stackabuse.com/how-to-print-colored-text-in-python/
# Использовать ANSI коды просто, для этого нужно знать базовый синтаксис и сами коды. Разбор на примере кода «\033[0;31;40m\033[0;0m»:
# 1) \033[ — обозначение того, что дальше идет какой-то управляющий цветом код;
# 2) 0;    — обозначет стиль текста (0 - normal, 1 - bold, 2 - light, 3 - italicized, 4 - underlined, 5 - blink); 
# 3) 31;   — цвет текста (красный) (диапозон от 30 до 37);
# 4) 40m   — цвет фона (черный) (диапозон от 40 до 47) (m является разделителем);
# 5) \033[0;0m — возвращает терминалу исходную цветовую схему. Для того, чтобы текст не перетекал на следующую строку, нужно закрыть ТЕГ.
_text = "Привет BouRHooD!"
print(f'\033[0;31;40m {_text} \033[0;0m') 
print("\033[2;31;44mПривет\033[0m")

# ***** (1)
"""<Вывод 16 цветов (8 фоновых + 8 передних)>"""
# Выводим цвета текста 
print("-" * 5)
for select_color_text_value in range(30, 38):
    print(f"\033[0;{select_color_text_value};40m {select_color_text_value} \033[0;0m", end="")
print()

# Выводим цвета текста и фона
print("-" * 5)
for select_color_text_value in range(30, 38):
    for select_color_background_value in range(40, 48):
        print(f"\033[0;{select_color_text_value};{select_color_background_value}m {select_color_text_value}:{select_color_background_value} \033[0;0m", end="")
    print()

# Выводим цвета фона
print("-" * 5)
for select_color_background_value in range(40, 48):
    print(f"\033[0;30;{select_color_background_value}m {select_color_background_value} \033[0;0m", end="")
print()