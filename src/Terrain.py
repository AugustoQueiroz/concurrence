from Point import Point
from Person import Person
from GLOBAL_CONSTANTS import *
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Terrain:
    
    @staticmethod
    def RandomTerrain(n_people,size=DEFAULT_SIZE,exits = DEFAULT_EXITS):
        dimRows,dimCols = size
        _map = [[0 for _ in range(dimCols)] for _ in range(dimRows)]

        # 1) to make sure at least MAX_NUMBER_OF_PEOPLE places are free
        totalPlaces = dimCols * dimRows
        totalPlaces-= MAX_NUMBER_OF_PEOPLE 
        totalPlaces-= len(DEFAULT_EXITS)
        
        #GENERATING OBSTACLES
        obstaclesList = []
        stopGeneratingObstacles = False
        for i in range( dimRows ) : 
            if stopGeneratingObstacles : 
                break
            for j in range( dimCols ) :
                # 2) to make sure at least MAX_NUMBER_OF_PEOPLE places are free
                if totalPlaces - MAX_OBSTACLE_HEIGHT * MAX_OBSTACLE_WIDTH <= MAX_NUMBER_OF_PEOPLE :
                    stopGeneratingObstacles = True
                    break
                
                if Terrain.__isPlaceOk(_map,i,j) and Terrain.__isThereObstacleSurrounding(_map,i,j) == False:
                    makeANewObstacleProbability =  random.random()
                    
                    if makeANewObstacleProbability > 0.90 :
                        sizeRow  = random.randint(1,MAX_OBSTACLE_HEIGHT)
                        sizeCols = random.randint(1,MAX_OBSTACLE_WIDTH)
                        
                        for r in range (i , min(i+sizeRow , dimRows)): 
                            for c in range (j , min(j+sizeCols , dimCols)):
                                
                                if Terrain.__isPlaceOk(_map,r,c):
                                    entryRow,entryCol = i,j
                                    if r == i and Terrain.__isThereObstacleUp(_map,r,c):
                                        sizeCols = abs( c-j )
                                        break
                                    if Terrain.__isThereObstacleRight(_map,r,c):
                                        sizeCols = abs( c-j )
                                        break
                                    _map[r][c]= OBSTACLE_IDENTIFIER
                                    totalPlaces-=1
                                    leaveRow,leaveCol = r,c
                        #print(entryRow,entryCol , leaveRow , leaveCol)
                        obstaclesList.append(Obstacle(entryRow,entryCol , leaveRow ,leaveCol))
        #for obstacle in obstaclesList :
        #    print (obstacle)
        
        #Generating People
        totalNumberOfPeople = 2**n_people
        PeopleSpawned = 0
        emptyPlaces = []
        peopleList = []
        for i in range(dimRows):
            for j in range(dimCols):
                if _map[i][j] == EMPTY_IDENTIFIER :
                    emptyPlaces.append(Point(i,j))
        
        while PeopleSpawned < totalNumberOfPeople :
            randomEmptyPlaceIndex = random.randint(0, len(emptyPlaces)-1)
            if _map[emptyPlaces[randomEmptyPlaceIndex].x][emptyPlaces[randomEmptyPlaceIndex].y] == 0:
                #PeopleSpawned +1 represents the id of the person
                _map[emptyPlaces[randomEmptyPlaceIndex].x][emptyPlaces[randomEmptyPlaceIndex].y] = PeopleSpawned + 1 
                PeopleSpawned+=1
                peopleList.append(Person(PeopleSpawned+1, emptyPlaces[randomEmptyPlaceIndex]))
        
        #for p in peopleList:
        #    print(p)
        
        #now we have SIZE, list of obstacles, list of exists, list of people, and the map
        return Terrain(obstaclesList, peopleList, _map , size,exits)        
                   
#        a = np.array(_map)
        '''fig, ax = plt.subplots()
        im = ax.imshow(a)
        ax.set_xticks(np.arange(128))
        ax.set_yticks(np.arange(512))
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
        
        for i in range(50):
            for j in range(50):
                text = ax.text(j, i, a[i, j],
                            ha="center", va="center", color="w")
        
        ax.set_title("Harvest of local farmers (in tons/year)")
        fig.tight_layout()
        plt.show()'''
        
        
            
                    

    def __init__(self, obstacles, people, map=None, size=DEFAULT_SIZE,exits = DEFAULT_EXITS):
        self.size = size
        self.obstacles = obstacles
        self.exits = exits
        self.people = people

       
        if map is not None : 
            self._map = map
        else : 
             #initialize map to zeros
            self._map = [[0 for _ in range(size[1])] for _ in range(size[0])]
        
            #fill Map with KNOWN obstacles
            for obstacle in self.obstacles:
                for x in range(obstacle.top_left.x, obstacle.bottom_right.x):
                    for y in range(obstacle.top_left.y, obstacle.bottom_right.y):
                        self._map[x][y] = OBSTACLE_IDENTIFIER
            
            #fill Map with KNOWN exits
            for exit in exits:
                self._map[exit.x][exit.y] = EXIT_IDENTIFIER

            #fill Map with KNOWN People
            for person in people:
                self._map[person.position.x][person.position.y] = 2

    def is_position_blocked(self, position):
        return self._map[position.x][position.y] > OBSTACLE_IDENTIFIER

    def is_exit(self, position):
        return self._map[position.x][position.y] == EXIT_IDENTIFIER

    @staticmethod
    def __isPlaceOk(_map, i: int , j: int,size=DEFAULT_SIZE) -> bool:
            dimRows,dimColumns = size
            if i == 0 or i == dimRows - 1 :
                return False
            if j == 0 or j == dimColumns - 1:
                return False
            #if it's an obstacle
            if _map[i][j] == OBSTACLE_IDENTIFIER :
                return False
            return True

    @staticmethod
    def __isThereObstacleUp(_map, i: int , j: int) -> bool:
        return _map[i-1][j] == OBSTACLE_IDENTIFIER
    @staticmethod
    def __isThereObstacleDown(_map, i: int , j: int) -> bool:
        return _map[i+1][j] == OBSTACLE_IDENTIFIER
    @staticmethod
    def __isThereObstacleLeft(_map, i: int , j: int) -> bool:
        return _map[i][j-1] == OBSTACLE_IDENTIFIER
    @staticmethod
    def __isThereObstacleRight(_map, i: int , j: int) -> bool:
        return _map[i][j+1] == OBSTACLE_IDENTIFIER
    @staticmethod
    def __isThereObstacleSurrounding(_map, i: int , j: int) -> bool:
        flag = Terrain.__isThereObstacleUp(_map,i,j)
        flag|= Terrain.__isThereObstacleDown(_map,i,j)
        flag|= Terrain.__isThereObstacleLeft(_map,i,j)
        flag|= Terrain.__isThereObstacleRight(_map,i,j)
        return flag

    def update_person_position(self, position_update):
        self._map[position_update[0].x][position_update[0].y] = 0
        self._map[position_update[1].x][position_update[0].y] = 2

class Obstacle:
    def __init__(self, x1,y1 , x2,y2 ):
        self.top_left = Point(x1, y1)
        self.bottom_right = Point(x2 , y2)
    def __str__(self):
        return "Obstacle from {} to {} ".format(self.top_left, self.bottom_right)

