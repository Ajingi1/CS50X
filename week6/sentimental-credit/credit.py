# from CS50 import get_string, import re lib , import sys
from cs50 import get_string
import re
import sys


def main():
    number = get_string("Number: ")
    if validate(number) and calculate_card_number_validity(number):
        if (number[:2] in ["51", "52", "53", "55"]) and len(number) == 16:
            print("MASTERCARD")
        elif (number[:2] in ["34", "37"]) and len(number) == 15:
            print("AMEX")
        elif (number[:1] == "4") and ((len(number) == 13) or len(number) == 16):
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")


def validate(number):
    while True:
        matche = re.search(r"^(34)|^(37)|^(51)|^(52)|^(53)|^(55)|^4", number)
        leng = len(number)
        if ((leng == 13) or (leng == 16) or (leng == 15)):
            if matche:
                return True
            else:
                sys.exit("INVALID")
        else:
            sys.exit("INVALID")


def calculate_card_number_validity(number):
    # store even index of the card number from 0 index to the end skip odd index
    even_index = []

    # store odd index of the card number from 0 index to the end skip even index
    odd_index = []

    # add all result to this variable
    result = 0

    # loop throught the card numbers from the second number to the end index then append it to even_index list
    for i in range(len(number) - 2, -1, -2):
        even_index.append(number[i])

    for i in range(len(even_index)):
        temp = int(even_index[i]) * 2

        # if temp is >= 10 add the numbers as separate number not as
        # if 6 * 2 = 12 you will ad 1 + 2 to the result
        if temp >= 10:
            temp2 = temp
            for n in str(temp2):
                result += int(n)
        elif temp < 10:
            result += temp

    # loop throught the card numbers from the end skip by 1 index then append it to odd_index list
    # I can skip the appending and add numbers to the result but storing it in the separate list is good
    for i in range(len(number) - 1, -1, -2):
        odd_index.append(number[i])

    for k in range(len(odd_index)):
        result += int(odd_index[k])

    # check if card number is valid
    # else exit with INVALID message
    print(result % 10)
    if result % 10 == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    main()
