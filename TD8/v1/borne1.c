// #include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/shm.h>
#include <sys/sem.h>

#include "def.h"


int* get_shmadr() {
	key_t cle = ftok(SHM_CHEMIN, SHM_ID);
	size_t taille = sizeof(int);
	int shmid = shmget(cle, taille, 0666);
	int* shmadr = (int*)shmat(shmid, NULL, 0);
	return shmadr;
}

int get_semid() {
	key_t cle = ftok(SHM_CHEMIN, SHM_ID);
	int semid = semget(cle, 1, 0);
	return semid;
}

void acquire_semaphore() {
	int semid = get_semid();

	struct sembuf acquire = {0, -1, 0};
	struct sembuf ops[] = {acquire};

	semop(semid, ops, 1);
}

void release_sempahore() {
	int semid = get_semid();

	struct sembuf release = {0, 1, 0};
	struct sembuf ops[] = {release};

	semop(semid, ops, 1);
}

int nombre_de_places() {
	int* shmadr = get_shmadr();
	return *shmadr;
}

void decrement_nombre_de_places() {
	int* shmadr = get_shmadr();
	--(*shmadr);
}

int main() {
	//int fd = open(SHM_CHEMIN, O_WRONLY);
	//printf("%d\n", fd);
	//struct flock lock;
	//memset(&lock, 0, sizeof(lock));
	//lock.l_type = F_WRLCK;
	
	while (1) {
		//flock(lock, LOCK_EX);
		//lock.l_type = F_WRLCK;
		//fcntl(fd, F_SETLKW, &lock);
		acquire_semaphore();

		if (nombre_de_places() > 0) {
			printf("Demande acceptée\n");
			sleep(2);

			decrement_nombre_de_places();
			printf("Impression ticket\n");
			printf("%d\n", nombre_de_places());
			//flock(lock, LOCK_UN);
		} else {
			printf("Pas de place\n");
			sleep(1);
		}

		//lock.l_type = F_UNLCK;
		//fcntl(fd, F_SETLKW, &lock);
		release_sempahore();
	}

	//fclose(fd);
}
