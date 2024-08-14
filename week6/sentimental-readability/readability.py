# import libraries
from cs50 import get_string


def main():
    # collect the text here
    text = get_string("Text: ")

    l, w, s = return_f(text)

    coleman = compute_coleman(l, w, s)

    # grade checking algth
    grade = round(coleman)
    if grade < 1:
        print("Before Grade 1")
    elif grade > 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


def return_f(text):

    letter_count = 0
    word_count = 0
    sentence_count = 0

    # count number of letters in the text
    for i in text:
        if i.isalpha():
            letter_count += 1
    # print(letter_count)

    # count number of words in the text
    word = text.split()
    word_count = len(word)
    # print(word_count)

    # count number of sentences in the text
    for i in text:
        if i in [".", "!", "?"]:
            sentence_count += 1
    # print(sentence_count)
    return letter_count, word_count, sentence_count


def compute_coleman(l, w, s):
    # L average number of letters, the number of letters divided by the number of words, all multiplied by 100.
    l_average = (l / w) * 100
    # S average number of sentences, the number of sentences divided by the number of words, all multiplied by 100.
    s_average = (s / w) * 100
    coleman_index = (0.0588 * l_average) - (0.296 * s_average) - 15.8
    return coleman_index


if __name__ == "__main__":
    main()
