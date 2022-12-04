char = "+"

print("Длина?")
w = int(input())

# (1)
print(char * w)

# (2)
for i in range(w):
    print(char, end="")