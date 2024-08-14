#include <stdio.h>
#include <cs50.h>

int checking(long card_no);
int first_two_no(long card_no);
int validity(long card_no, int len);

int main(void)
{
    long card_no = get_long("Enter Your card Number: ");
    int card_len = checking(card_no);
    int first_2_no = first_two_no(card_no);
    int card_validity_number = validity(card_no, card_len);
    // printf("%i\n", card_len);
    if((card_len != 13) && (card_len != 15) && (card_len != 16))
    {
        printf("INVALID\n");
    }
    else if(card_validity_number != 0)
    {
        printf("INVALID\n");
    }
    else if (card_validity_number == 0)
    {
        if((card_len == 15) && ((first_2_no == 34) || (first_2_no == 37)))
        {
            printf("AMEX\n");
        }
        else if((card_len == 16) && ((first_2_no == 51) || (first_2_no == 52) || (first_2_no == 53) || (first_2_no == 54) || (first_2_no == 55)))
        {
            printf("MASTERCARD\n");
        }
        else if(((card_len == 13) || (card_len == 16)) && (first_2_no / 10 == 4))
        {
            printf("VISA\n");
        }
        else
        {
        printf("INVALID\n");
        }
    }

}

// checking card len and returning len of card number
int checking(long card_no)
{
    int counter = 0;
    while(card_no > 0)
    {
        counter ++;
        card_no /= 10;
    }
    return counter;
}

// checking first to numbers and returning them
int first_two_no(long card_no)
{
    int first_two_no;
    while(card_no > 30)
    {
        if(card_no < 100 && card_no > 30){
            first_two_no = card_no;
        }
        card_no /= 10;
    }
    return first_two_no;
}

// checking card is valid or invalid

int validity(long card_no, int len)
{
    int card_no_array[len];
    int card_added_even_no = 0;
    int card_added_odd_no = 0;
    for (int i = 0; i < len; i++)
    {
        card_no_array[i] = card_no % 10;
        card_no /= 10;
    }

    for (int j = 1; j <= len; j += 2) {
        // printf("%d\n", card_no_array[j]);
        int temp = card_no_array[j] * 2;
        if(temp > 0)
        {
            while(temp > 0)
            {
                card_added_even_no += temp % 10;
                temp /= 10;
            }
        }

    }
    for (int k = 0; k < len; k += 2)
    {
        card_added_odd_no += card_no_array[k];
    }
    int final = card_added_even_no + card_added_odd_no;
    return final % 10;
}
