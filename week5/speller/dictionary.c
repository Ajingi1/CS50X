// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// words count
int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // get hash index
    int hash_index = hash(word);

    // new node to store current word
    node *current = table[hash_index];

    // while current is not NULL
    while (current != NULL)
    {
        if (strcasecmp(current->word, word) == 0)
        {
            // when word found
            return true;
        }
        current = current->next;
    }
    // when word not found
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;
    const char *ptr = word;
    while (*ptr != '\0')
    {
        hash_value += toupper(*ptr) - 'A';
        ptr++;
    }
    hash_value += strlen(word);
    hash_value %= 26;
    return hash_value;

    // // TODO: Improve this hash function
    // return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *myfile = fopen(dictionary, "r");

    // Read each word in the file
    if (myfile == NULL)
    {
        return false;
    }

    //
    char word[LENGTH + 1];

    // Add each word to the hash table
    while (fscanf(myfile, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(myfile);
            return false;
        }
        // copy word to node
        strcpy(new_node->word, word);
        new_node->next = NULL;

        // get index of hash
        int hash_index = hash(word);

        // insert the word to table
        if (table[hash_index] == NULL)
        {
            table[hash_index] = new_node;
        }
        else
        {
            new_node->next = table[hash_index];
            table[hash_index] = new_node;
        }
        word_count++;
    }
    // Close the dictionary file
    fclose(myfile);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    // done it when adding word
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // iterate over each node
    for (int i = 0; i < N; i++)
    {
        node *current = table[i];
        while (current != NULL)
        {
            node *temp = current;
            current = current->next;
            free(temp);
        }
        // when while complete reset table to NULL
        table[i] = NULL;
    }
    return true;
}
