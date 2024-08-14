#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int player_score(string player);
void score_calc(int player_one_score, int player_two_score);

int main(void)
{
    string player1 = get_string("Player 1: ");
    string player2 = get_string("Player 2: ");

    int player_one_score = player_score(player1);
    int player_two_score = player_score(player2);

    score_calc(player_one_score, player_two_score);
}

int player_score(string player)
{
    int score = 0;
    int leng = strlen(player);
    for (int i = 0; i < leng; i++)
    {
        switch (toupper(player[i]))
        {
            // A E I L N O R S T U = 1
            case 'A':
            case 'E':
            case 'I':
            case 'L':
            case 'N':
            case 'O':
            case 'R':
            case 'S':
            case 'T':
            case 'U':
                score++;
                break;
            // D G = 2
            case 'D':
            case 'G':
                score += 2;
                break;
            // B C M P = 3
            case 'B':
            case 'C':
            case 'M':
            case 'P':
                score += 3;
                break;
            // F H V W Y = 4
            case 'F':
            case 'H':
            case 'V':
            case 'W':
            case 'Y':
                score += 4;
                break;
            // K = 5
            case 'K':
                score += 5;
                break;
            // J X = 8
            case 'J':
            case 'X':
                score += 8;
                break;
            // Q Z = 10
            case 'Q':
            case 'Z':
                score += 10;
                break;
        }
    }
    return score;
}

void score_calc(int score_one, int score_two)
{
    if (score_one == score_two)
    {
        printf("Tie!\n");
    }
    else if (score_one > score_two)
    {
        printf("Player 1 wins!\n");
    }
    else if (score_one < score_two)
    {
        printf("Player 2 wins!\n");
    }
}
