#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>

#define FILE_NAME_SIZE 100

void parse(char file[]);

struct server_configuration {
	char Id[13];
	int UDP_port;
	int TCP_port;
} configuration;

bool debug = false;

int main(int argc, char const *argv[]) {
	char file[FILE_NAME_SIZE];

	if (argc == 2) {
		if (!strcmp(argv[1], "-d")) {
			debug = true;
		} else {
			strcpy(file, argv[1]);
		}
	}

	parse(file);

	printf("%s\n", configuration.Id);
	printf("%d\n", configuration.UDP_port);
	printf("%d\n", configuration.TCP_port);

	return 0;
}

void parse(char file[]) {
	char *tocken;
	FILE *f = fopen(file, "r");

	if (f == NULL) {
		perror("Error al abrir fichero");
		exit(-1);

	} else {
		char line[20];

		while (fgets(line, 100, f) != NULL) {
			fputs(line, f);
			tocken = strtok(line, " ");

			if (!strcmp(tocken, "Id")) {
				while (tocken != NULL) {
					strcpy(configuration.Id, tocken);
					tocken = strtok(NULL, " \n\r");
				}
				
			} else if (!strcmp(tocken, "UDP-port")) {
				char aux[20];
				while (tocken != NULL) {
					strcpy(aux, tocken);
					configuration.UDP_port = atoi(aux);
					tocken = strtok(NULL, " ");
				}

			} else if (!strcmp(tocken, "TCP-port")) {
				char aux[20];
				while (tocken != NULL) {
					strcpy(aux, tocken);
					configuration.TCP_port = atoi(aux);
					tocken = strtok(NULL, " ");
				}

			}
			
		}
	}
}