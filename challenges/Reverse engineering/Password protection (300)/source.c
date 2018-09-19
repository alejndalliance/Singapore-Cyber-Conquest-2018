
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char** argv[])
{

    const char xorKey[] = {}; // redacted - run the binary!
    const char password[] = {0x90, 0x9d, 0x27, 0x24, 0x4f, 0x77, 0xb3, 0xea, 0x9a, 0x26};
    char input[11] = {0};
    char plainTextPassword[10] = {0};

    
    printf( "Enter the key: " );
    fgets( input, sizeof(input), stdin );

    unsigned int i;
    for ( i = 0; i < sizeof(password); i++)
    {
        plainTextPassword[i] = password[i] ^ xorKey[i];
    }
    
    if ( memcmp(input, plainTextPassword, sizeof(plainTextPassword)) == 0 )
    {
        setresuid(geteuid(),geteuid(),geteuid());
        printf("WIN!\n");
        system("/bin/sh");
    }
    else
    {
        printf( "Better luck next time!\r\n" );
    }
    
    return 0;
}

