#include <cs50.h>
#include <stdio.h>

void calc_chaneg(int);
int main(void)
{
    int change;
    do
    {
        change = get_int("Change owed: ");
    }
    while (change < 0);

    calc_chaneg(change);
}

void calc_chaneg(int change)
{
    int count = 0;
    while (change >= 25)
    {
        // while change is greater than quarters subtract quarters and add counter
        // every subtraction will add how many quarters I gave to customer
        change -= 25;
        count++;
    }
    while (change >= 10)
    {
        // while change is greater than dimes subtract dimes and add counter
        // every subtraction will add how many dimes I gave to customer
        change -= 10;
        count++;
    }
    while (change >= 5)
    {
        // while change is greater than nickels subtract nickels and add counter
        // every subtraction will add how many nickels I gave to customer
        change -= 5;
        count++;
    }
    while (change >= 1)
    {
        // while change is greater than pennies subtract pennies and add counter
        // every subtraction will add how many pennies I gave to customer
        change -= 1;
        count++;
    }
    // funtion will print the total number of coins I gave
    printf("%i\n", count);
}
