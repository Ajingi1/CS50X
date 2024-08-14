#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

const int BYTE = 512;

typedef uint8_t buffer[BYTE];

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("usage: ./recover file\n ");
        return 1;
    }
    // open memory
    FILE *memory = fopen(argv[1], "r");

    if (memory == NULL)
    {
        printf(" file couldn't be opened\n ");
        return 2;
    }
    buffer buff;
    int f_counter = 0;
    FILE *img = NULL;

    while (fread(buff, 1, BYTE, memory) == BYTE)
    {
        if (buff[0] == 0xff && buff[1] == 0xd8 && buff[2] == 0xff)
        {
            if (img != NULL)
            {
                fclose(img);
            }
            char nfile[8];
            sprintf(nfile, "%03i.jpg", f_counter);
            img = fopen(nfile, "w");
            f_counter++;
        }
        if (img != NULL)
        {
            fwrite(buff, 1, BYTE, img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }
    fclose(memory);
}
