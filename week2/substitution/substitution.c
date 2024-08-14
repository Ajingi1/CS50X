#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int validate(string key);
void encryp(string text, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (argc == 2)
    {
        int validation_result = validate(argv[1]);
        if (validation_result == 1)
        {
            return 1;
        }
        else
        {
            string message = get_string("plaintext: ");
            encryp(message, argv[1]);
            // printf("correct1\n");
        }
    }
}

int validate(string key)
{
    int len = strlen(key);
    if (len != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < len; i++)
        {
            if (!isalpha(key[i]))
            {
                printf("Key must contain only characters\n");
                return 1;
            }
            else
            {
                for (int j = i + 1; j < len; j++)
                {
                    if (tolower(key[i]) == tolower(key[j]))
                    {
                        printf("Key must not contain any duplicate\n");
                        return 1;
                    }
                }
            }
        }
        return 0;
    }
}

void encryp(string text, string key)
{
    int text_len = strlen(text);
    int key_len = strlen(key);
    printf("ciphertext: ");

    for (int i = 0; i < text_len; i++)
    {
        if (isalpha(text[i]))
        {
            // if (isupper(key[i]))
            // {
            if (isupper(text[i]))
            {
                int sub_int = (text[i] - 65);
                printf("%c", toupper(key[sub_int]));
            }
            else
            {
                int sub_int = (text[i] - 97);
                printf("%c", tolower((key[sub_int])));
            }
            // }
            // else if (islower(key[i]))
            // {
            //     if (isupper(text[i]))
            //     {
            //         int sub_int = (text[i] - 65);
            //         printf("%c", (key[sub_int]));
            //     }
            //     else
            //     {
            //         int sub_int = (text[i] - 97);
            //         printf("%c", (key[sub_int]));
            //     }
            // }
        }
        else
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
}
