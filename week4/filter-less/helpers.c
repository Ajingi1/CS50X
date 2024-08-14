#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //
    for (int l = 0; l < height; l++)
    {
        for (int k = 0; k < width; k++)
        {
            int red = image[l][k].rgbtRed;
            int green = image[l][k].rgbtGreen;
            int blue = image[l][k].rgbtBlue;

            int average_color = round((red + green + blue) / 3.0);

            image[l][k].rgbtRed = average_color;
            image[l][k].rgbtGreen = average_color;
            image[l][k].rgbtBlue = average_color;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //
    for (int l = 0; l < height; l++)
    {
        for (int k = 0; k < width; k++)
        {
            int red = image[l][k].rgbtRed;
            int green = image[l][k].rgbtGreen;
            int blue = image[l][k].rgbtBlue;

            int sepiaR = round((0.393 * red) + (0.769 * green) + (0.189 * blue));
            int sepiaG = round((0.349 * red) + (0.686 * green) + (0.168 * blue));
            int sepiaB = round((0.272 * red) + (0.534 * green) + (0.131 * blue));

            if (sepiaR > 255)
            {
                sepiaR = 255;
            }

            if (sepiaG > 255)
            {
                sepiaG = 255;
            }

            if (sepiaB > 255)
            {
                sepiaB = 255;
            }

            image[l][k].rgbtRed = sepiaR;
            image[l][k].rgbtGreen = sepiaG;
            image[l][k].rgbtBlue = sepiaB;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //
    for (int i = 0; i < height; i++)
    {
        for (int j = width - 1, n = 0, half = (width / 2); j >= half; j-- , n++)
        {
            int tempRe = image[i][j].rgbtRed;
            int tempGe = image[i][j].rgbtGreen;
            int tempBe = image[i][j].rgbtBlue;

            int tempRs = image[i][n].rgbtRed;
            int tempGs = image[i][n].rgbtGreen;
            int tempBs = image[i][n].rgbtBlue;

            image[i][n].rgbtRed = tempRe;
            image[i][n].rgbtGreen = tempGe;
            image[i][n].rgbtBlue = tempBe;

            image[i][j].rgbtRed = tempRs;
            image[i][j].rgbtGreen = tempGs;
            image[i][j].rgbtBlue = tempBs;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // copy a image in tempImage
    RGBTRIPLE tempImage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            tempImage[i][j] = image[i][j];
        }
    }



    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumR = 0, sumG = 0, sumB = 0;
            int counting = 0;

            // Iterate over every 3 by 3 grid center around current block
            for (int r = i - 1; r <= i + 1; r++)
            {
                for (int c = j - 1; c <= j + 1; c++)
                {

                    if (r >= 0 && r < height && c >= 0 && c < width)
                    {
                        // Add color values of current block to the sum[R or G or B]
                        sumR += tempImage[r][c].rgbtRed;
                        sumG += tempImage[r][c].rgbtGreen;
                        sumB += tempImage[r][c].rgbtBlue;
                        counting++;
                    }
                }
            }

            // Calculate the average RGB values
            int blurR = round(sumR / (float) counting);
            int blurG = round(sumG / (float) counting);
            int blurB = round(sumB / (float) counting);

            // Set the RGB values of the current  to the average values
            image[i][j].rgbtRed = blurR;
            image[i][j].rgbtGreen = blurG;
            image[i][j].rgbtBlue = blurB;
        }
    }

    return;
}
