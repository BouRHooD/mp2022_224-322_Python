# HW: вывести в коносль все доступные цвета и фоны

# ***** Пример (example) https://egorovegor.ru/python-color-printing/
# Color Builder for Terminal: http://terminal-color-builder.mudasobwa.ru/
# Работа с 256 цветами немного отличается от работы с 16-цветовой схемой:
# 1) \033[     — обозначение того, что дальше идет какой-то управляющий цветом код;
# 2) 01;       — обозначет стиль текста (00 - normal, 01 - bold, 02 - light, 03 - italicized, 04 - underlined, 05 - blink, 07 - reverse text and background settings);
# 3) 38;       — выбор между цветом для текста (38) или фона (48); 
# 4) 05;       — указатель, что будет использоваться следующим значение в RGB;
# 5) 222;      — цвет текста (оранжевый) (значение в RGB [0, 255]);
# 3) 48;       — выбор между цветом для текста (38) или фона (48); 
# 3) 05;       — указатель, что будет использоваться следующим значение в RGB;
# 4) 232m      — цвет фона (черный) (значение в RGB [0, 255]);
# 5) \033[0;0m — возвращает терминалу исходную цветовую схему. Для того, чтобы текст не перетекал на следующую строку, нужно закрыть ТЕГ.
_text = "Привет BouRHooD!"
print(f"\033[00;38;05;222;48;05;232m {_text} \033[0;0m")
print("\033[01;38;05;50;48;05;232mПривет\033[0;0m")

# ***** (1)
"""<Вывод 256 цветов>"""
# Выбираем рандомно цвета для текста
import random
print("Random text colors:")
list_color_text = random.choices(range(0, 256), k=16)
for select_color_text_value in list_color_text:
    text_values   = f"{select_color_text_value}".center(5, ' ')
    to_print_text = f"\033[00;38;05;{select_color_text_value};48;05;232m{text_values}\033[0;0m"
    print(to_print_text, end="")
print()

# Выбираем рандомно цвета для фона
print("Random background colors:")
list_color_background = random.choices(range(0, 256), k=16)
for select_color_background_value in list_color_background:
    text_values   = f"{select_color_background_value}".center(5, ' ')
    to_print_text = f"\033[00;38;05;232;48;05;{select_color_background_value}m{text_values}\033[0;0m"
    print(to_print_text, end="")
print()

# Выводим цвета текста и фона (матрицу 16х16)
print("-" * 5)
for select_color_text_value in list_color_text:
    for select_color_background_value in list_color_background:
        text_values   = f"{select_color_text_value}:{select_color_background_value}".center(9, ' ')
        to_print_text = f"\033[00;38;05;{select_color_text_value};48;05;{select_color_background_value}m{text_values}\033[0;0m"
        print(to_print_text, end="")
    print()
