#include <stdio.h>
#include <stdlib.h>

struct server_configuration {
	char Id[13];
	int UDP_port;
	int TCP_port;
} configuration;

struct server_configuration parse(char file[]) {
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
	printf("%s\n", configuration.Id);
	printf("%d\n", configuration.UDP_port);
	printf("%d\n", configuration.TCP_port);
	return configuration;
}