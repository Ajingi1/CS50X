# from cs50 library import get_float
from cs50 import get_float

# set of coin available
coin = (25, 10, 5, 1)

# use while to reprompt if user negative or non numeric
while True:
    change = get_float("Change: ")
    if 0.00 < change:
        break
# convert the change to number
change = change * 100
# print(change)

# store how many coin where used
count = 0

# change calculation
while True:
    for i in coin:
        while change >= i:
            change = change - i
            count += 1
    if change == 0:
        break

print(count)
