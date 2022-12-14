#include <stdio.h>
#include <stdlib.h>

#define CHARS_TO_FIND 14

int found[26];
int total_since_clear = 0;

void clear() {
    for (int i = 0; i < 26; i++) {
        found[i] = 0;
    }
    total_since_clear = 0;
}

int readFile(char *fileName) {
    FILE *file = fopen(fileName, "r");
    if (file == NULL) {
        printf("Error opening file\n");
        return -1;
    }
    clear();
    fseek(file, 0, SEEK_SET);

    int i, index;
    char c;
    while ((i = fgetc(file)) != EOF) {
        c = (char)i;
        index = c - 'a';

        if(found[index]) {
            unsigned long go_back_to = found[index] * sizeof(char);

            clear();
            fseek(file, go_back_to, SEEK_SET);
        } else {
            found[index] = ftell(file)/sizeof(char);
            total_since_clear++;
        }

        if (total_since_clear == CHARS_TO_FIND) {
            break;
        }
    }

    return ftell(file)/sizeof(char);
}


int main(int argc, char *argv[]) {
   int result = readFile(argv[1]);
   printf("%d\n", result);
   return 0;
}