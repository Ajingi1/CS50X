#include <cs50.h>
#include <stdio.h>

void row(int leng);

int main(void)
{
    int wall_height;
    do
    {
        wall_height = get_int("Enter the height: ");
    }
   while (wall_height < 1 || wall_height  > 8);

    row(wall_height);
}

void row(int leng)
{
    for (int i = 1; i <= leng; i++)
    {
        for (int j = leng; j > i; j--)
        {
            printf(" ");
        }
        for (int n = 1; n <= i; n++)
        {
            printf("#");
        }
        for (int k = 0; k <= 1; k++)
        {
            printf(" ");
        }
        for (int m = 1; m <= i; m++)
        {
            printf("#");
        }
        printf("\n");
    }
}
