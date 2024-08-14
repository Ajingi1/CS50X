#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void encrypt(string message_text, string key);

int main(int argc, string argv[])
{
    // check argv len if not equal to 2 print error and return 1
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // check argv len if is equal to 2 and if is not digit print error message
    else if (argc == 2)
    {
        int argv_len = strlen(argv[1]);
        for (int i = 0; i < argv_len; i++)
        {
            if (!isdigit(argv[1][i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }

    // if all program is correctly entered get message from user
    string message = get_string("Enter Your Message: ");

    // call the function that will encrypt the message. message and the key are input
    // print encrypted message
    encrypt(message, argv[1]);
}

void encrypt(string message_text, string key_str)
{
    int key = atoi(key_str);
    int msg_len = strlen(message_text);
    printf("ciphertext: ");

    for (int i = 0; i < msg_len; i++)
    {
        if (isupper(message_text[i]))
        {
            printf("%c", ((((int) message_text[i] - 65) + key) % 26) + 65);
        }
        else if (islower(message_text[i]))
        {
            printf("%c", ((((int) message_text[i] - 97) + key) % 26) + 97);
        }
        else
        {
            printf("%c", message_text[i]);
        }
    }
    printf("\n");
}
