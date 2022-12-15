import random

# Вернуть псевдослучайное дробное число в интервале [0.0, 1.0)
print(random.random())

# Вернуть целое число в диапазоне от <начала> до <конца>
print(random.randint(100, 999))
print(random.randrange(100, 999, 100))

# Перемешать последовательность (список)
numbers = list(range(10))
print(numbers)
random.shuffle(numbers)
print(numbers)

# Вернуть случайный элемент из последовотельности (строки, списка, ...) 
print(random.choices("ПРИВЕТ"))
print(random.choices("ПРИВЕТ", k=20))
print(random.choices(list(range(10)), k=20))

# HW:
# Добавить использование других методов из random 
# Примеры: https://python-scripts.com/random#seed
# (1)
random.seed(5)
print("Случайное число с семенем ", random.random())
random.seed(5)
print("Случайное число с семенем ", random.random())