#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>

#include "def.h"

int shmid;
int semid;
int *shmadr;

union semun {
	int		val;
	struct semid_ds *buf;
	unsigned short *array;
	struct seminfo *__buf;
};

void traitant_sigint(int numero_signal) {
	shmdt(shmadr);
	shmctl(shmid, IPC_RMID, NULL);
	exit(0);
}

int shm_creation(char* chemin_fichier, int identificateur, int taille) {
	int fd, shmid;
	key_t cle;

	fd = open(chemin_fichier, O_CREAT|O_WRONLY, 0644);
	close(fd);

	cle = ftok(chemin_fichier, identificateur);

	shmid = shmget(cle, taille, IPC_CREAT|0666);

	return shmid;
}

int sem_creation(char* chemin_fichier, int identificateur) {
	int semid;
	key_t cle;

	cle = ftok(chemin_fichier, identificateur);

	semid = semget(cle, 1, IPC_CREAT|IPC_EXCL|0666);
	union semun arg;
	arg.val = 1;
	semctl(semid, 0, SETVAL, arg);

	return semid;
}

int main() {
	shmid = shm_creation(SHM_CHEMIN, SHM_ID, sizeof(int));
	semid = sem_creation(SHM_CHEMIN, SHM_ID);

	shmadr = (int*) shmat(shmid, NULL, 0);

	*shmadr = 20;
	printf("parking : identificateur=%d, places=%d.\n", shmid, *shmadr);

	signal(SIGINT, traitant_sigint);
	pause();

	return 0;
}
