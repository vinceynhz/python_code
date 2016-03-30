#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define FALSE 0
#define TRUE 1

char * toLower(char * str){
    int i;
    int len;
    static char buffer[10];
    
    memset(buffer, 0x00, 10);
    len = strlen(str);

    for(i=0; i<len; i++){
        if(str[i] > 0x40 && str[i] < 0x5B){
            buffer[i] = str[i] + 0x20;
        }else{
            buffer[i] = str[i];
        }
    }

    return buffer;
}

int main(int argc, char ** argv){    
    const size_t linesize = 100;
    FILE * textfile = NULL;
    
    char * filename = NULL;
    char * line = (char *) malloc(linesize);
    char * token = NULL;
    char * comma = NULL;

    int config_counter = 1;
    int restarts = 0;
    char restarting = FALSE;

    if(argc < 1)
        return 0;

    filename = argv[1];

    textfile = fopen(filename, "r");

    if(textfile == NULL){
        printf("Error opening file: %s\n", filename);
        return 0;
    }

    // start the json
    printf("{");

    // Let's read line by line
    while( fgets(line, linesize, textfile) != NULL ){
        
        // if there is an empty string, we skip it
        if(strlen(line) == 0){
            continue;
        }

        // if we have a configuration line
        if( strstr(line, ">>>") ){
            
            // if there is a previous configuration open
            if(config_counter > 1){
                printf("}}, ");
            }

            // start the configuration
            printf("\"%d\": {\"lr\": ", config_counter++);

            token = strstr(line, "lr");
            token += 3;
            while(token[0] != ','){
                printf("%c", token[0]);
                token++;
            }

            printf(", \"wr\": ");

            token = strstr(line, "wr");
            token += 3;
            while(token[0] != ' '){
                printf("%c", token[0]);
                token++;
            }

            printf(", \"samples\": {");
        }

        // if we have a sample line
        else if(strstr(line, "<<<") ){
            // <<< 0 max epochs reached, restarting
            // <<< 99 = epochs: 161 extrapolation: False
            // LINE INDICATOR
            token = strtok(line, " "); // <<<
 
            // SAMPLE ID
            token = strtok(NULL, " "); // sample id
            
            // open sample object
            if(!restarting){
                // if this is not the first sample, add the comma for the previous one
                if(strcmp(token, "0") != 0){
                    printf(", ");
                }
                printf("\"%s\": {", token);
            }

            // MAX INDICATOR
            token = strtok(NULL, " "); // max | =

            // if this is a restart
            if( strcmp(token, "max") == 0 ){
                token = strtok(NULL, " "); // epochs | restarts

                if( strcmp(token, "epochs") == 0 ){
                    restarts++;
                    restarting = TRUE;
                }
                else if(strcmp(token, "restarts") == 0){
                    printf("\"restarts\": 5, \"epochs\": -1, \"extrapolation\": false}");
                    restarts = 0;
                    restarting = FALSE;
                }   
            }
            else{
                token = strtok(NULL, " "); // epochs:
                token = strtok(NULL, " ");
                printf("\"restarts\": %d, \"epochs\": %s", restarts, token);
                token = strtok(NULL, " "); // extrapolation:
                token = strtok(NULL, " \n");
                printf(", \"extrapolation\": %s}", toLower(token));
                restarts = 0;
                restarting = FALSE;
            }
        }
    }

    // Somehow the test ended in the middle of a restart or something
    if(restarts != 0){
        printf("\"restarts\": 5, \"epochs\": -1, \"extrapolation\": false}");
    }

    // the closing of the last sample, the last configuration and the file
    printf("}}}");

    free(line);
    fclose(textfile);
}

