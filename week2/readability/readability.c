#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
float compute_coleman(int letters, int words, int sentences);

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");

    // Count the number of letters
    int letters = count_letters(text);

    //Count the number of words
    int words = count_words(text);

    // Count the number of sentences in the text
    int sentences = count_sentences(text);
    // printf("%i\n", sentences);

    // Compute the Coleman-Liau index
     float coleman_liau = compute_coleman(letters, words, sentences);

     // Print the grade level
     int grade = round(coleman_liau);
     if (grade < 1)
     {
        printf("Before Grade 1\n");
     }
     else if (grade > 16)
     {
        printf("Grade 16+\n");
     }
     else
     {
        printf("Grade %i\n", grade);
     }
}


int count_letters(string text)
{
    int count = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 1;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == ' ')
        {
            count++;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if ((text[i] == '.') || (text[i] == '!') || (text[i] == '?'))
        {
            count++;
        }
    }
    return count;
}

float compute_coleman(int letters, int words, int sentences)
{
    // L average number of letters, the number of letters divided by the number of words, all multiplied by 100.
    float l_average = ((float) letters / words) * 100.0;
    // S average number of sentences, the number of sentences divided by the number of words, all multiplied by 100.
    float s_average = ((float) sentences / words) * 100.0;
    float coleman_index = 0.0588 * l_average - 0.296 * s_average - 15.8;
    return coleman_index;
}

