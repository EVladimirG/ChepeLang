#include <stdio.h>
#include <stdlib.h>


int main(int argc, char *argv[]) {    
     if (argc == 2) {
        if (strcmp(argv[1], "-v") == 0) {
            printf("\nVersion 1.0\nProgramado en C por EVladimirG\n");
            return 0;
        }
        if (strcmp(argv[1], "-h") == 0) {
            printf("\n -h Obtener ayuda\n -r --> Requisitos de funcionamiento\n -v --> Obtener version\n ");
            return 0;
        }
        if (strcmp(argv[1], "-r") == 0) {
            printf("\n Necesario tener instalado gcc a través de MinGW/n/n https://sourceforge.net/projects/mingw/");
            return 0;
        }
    }

    if (argc < 2) {
        fprintf(stderr, "Uso: Chepe <Codigo.chepe>\n\nArgumento -h para obtener ayuda\n\n", argv[0]);
        system("pause");
        return 1;
    }

    const char *inputFile = argv[1];
    const char *tempFile = "..\\Temp\\temp.c";
    const char *executable = "..\\Temp\\temp";

    char compileCommand[256];
    sprintf(compileCommand, "gcc %s -o %s", tempFile, executable);

    char runCommand[256];
    sprintf(runCommand, "%s", executable);

    FILE *file = fopen(inputFile, "r");
    if (!file) {
        perror("Error al abrir el archivo");
        return 1;
    }

    FILE *temp = fopen(tempFile, "w");
    if (!temp) {
        perror("Error al crear el archivo temporal");
        fclose(file);
        return 1;
    }

    fprintf(temp, "#include \"\\Chepe.h\"\n");

    char ch;
    while ((ch = fgetc(file)) != EOF) {
        fputc(ch, temp);
    }

    fclose(file);
    fclose(temp);

    if (system(compileCommand) != 0) {
        fprintf(stderr, "Error al compilar el codigo\n");
        return 1;
    }

    if (system(runCommand) != 0) {
        fprintf(stderr, "Error al ejecutar el codigo\n");
        return 1;
    }

    remove(tempFile);
    remove(executable);

    return 0;
}
