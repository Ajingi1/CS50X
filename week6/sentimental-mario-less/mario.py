# import cs50 get_int
from cs50 import get_int


# ask for pyramid height non negative interger and not greater than 8
while True:
    height = get_int("Heiht: ")
    if 0 < height <= 8:
        break

for i in range(1, height + 1):
    space = height - i
    print(" " * space + "#" * i)
