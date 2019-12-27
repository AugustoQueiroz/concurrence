import threading
import multiprocessing
import time
import queue 
from src.Person import *
from src.GLOBAL_CONSTANTS import *

class MobSimulator:
    def __init__(self, terrain):
        self.terrain = terrain

    def run_single_threaded(self):
        while len(self.terrain.people):
            mob = self.terrain.people

            for person in mob:
                position_update = person.move_towards(person.closest_exit(self.terrain.exits), terrain=self.terrain)
                #self.terrain.update_person_position(position_update)
                #if position_update[0].x == position_update[1].x and position_update[0].y == position_update[1].y:
                    #print("Person", person.identifier, "didn't move")
                    #for dx in range(-1, 2):
                        #line = ''
                        #for dy in range(-1, 2):
                            #position = person.position.moved_by(dx, dy)
                            #if position.x < 0 or position.y < 0 or position.x >= len(self.terrain._map) or position.y >=len(self.terrain._map[0]): continue
                            #if self.terrain._map[position.x][position.y] == 0: line += ' '
                            #elif self.terrain._map[position.x][position.y] == 1: line += '█'
                            #elif self.terrain._map[position.x][position.y] == -2: line += 'E'
                            #elif self.terrain._map == 2: line += 'A'
                        #print(line)

                if self.terrain.is_exit(person.position):
                    #print("Person", person.identifier, "successfully exited")
                    self.terrain.people.remove(person)

    def run_one_thread_per_person(self):
        person_threads = []
        for person in self.terrain.people:
            x = threading.Thread(target=person.loop, args=(self.terrain,))
            x.start()
            person_threads.append(x)

        for thread in person_threads:
            thread.join()
    
    def is_exit(self, position,QuadrantExits):
        for exit in QuadrantExits:
            if position == exit:
                return True
        return False


    def runQuadrant(self,quandrant,queues_Quandrant,id_quadrant,QuadrantExits,queue_final):
        cnt = 0 
        switchQuadrantPeople = []
        id = id_quadrant -1
        id1,id2,id3,id4 = 0,1,2,3
        flag =[False,False,False,False] 
        ok = True
        originalSize = len(quandrant.people)
        if id == id4:
            ok = False
            
        
        while ok or len(quandrant.people):
            # print(ok,id_quadrant,  len(quandrant.people))
            # if(id_quadrant != 1 ) :
            #     for person in quandrant.people:
            #         print(person.identifier," Quadrant: ", id_quadrant, " Position : ",  person.position.x,person.position.y)
            try:
                Message = queues_Quandrant[id].get(False)
            except queue.Empty:
                pass
            else:
                if Message.blockingMessage == id4   :
                    flag[id4]=True
                elif Message.blockingMessage == id3   :
                    flag[id3]=True
                elif Message.blockingMessage == id2   :
                    flag[id2]=True
                else:
                    quandrant._map[Message.position.x][Message.position.y] = PERSON_IDENTIFIER
                    quandrant.people.append(Message)
            mob = quandrant.people
            for person in mob:
                position_update = person.move_towards(person.closest_exit(QuadrantExits[id_quadrant-1]), terrain=quandrant)
                # print(person.identifier, person.position)
                if self.is_exit(person.position, QuadrantExits[id_quadrant-1]):
                    cnt+=1
                    # print("##################################################")
                    # print(originalSize," || ", " cnt :",cnt , " || " , person.position.x,person.position.y,"Quadrant :", id_quadrant , " Person", person.identifier, "successfully exited")
                    quandrant.people.remove(person)
                    quandrant._map[person.position.x][person.position.y] = EMPTY_IDENTIFIER
                    if( id_quadrant == 2 or id_quadrant == 3 ):
                        queues_Quandrant[id1].put(person)

                    if( id_quadrant == 4 ):
                        if(person.position.x == 256): 
                            queues_Quandrant[id2].put(person)
                        elif (person.position.y == 64):
                            queues_Quandrant[id3].put(person)
                        else:
                            print("Attention!! Quadrant 4 ???")
                            
            if( len(quandrant.people) == 0 ) : 
                if( id_quadrant == 1 and flag[id2]==True and flag[id3]==True and flag[id4] == True):
                    ok = False
                if( id_quadrant == 2 and flag[id4]==True ):
                    queues_Quandrant[id1].put(Person(None,None,id2))
                    ok = False
                if( id_quadrant == 3 and flag[id4]==True ):
                    queues_Quandrant[id1].put(Person(None,None,id3))
                    ok = False
                if( id_quadrant == 4 ):
                    queues_Quandrant[id1].put(Person(None,None,id4))
                    queues_Quandrant[id2].put(Person(None,None,id4))
                    queues_Quandrant[id3].put(Person(None,None,id4))
                    ok = False
        if id_quadrant==1 :
            queue_final.put(quandrant.persons_exited)
                            
                        
                        


    def run_one_thread_per_quadrant(self,quadrants):
        queue_final = multiprocessing.Queue()
        queues_Quandrant=  [multiprocessing.Queue(),multiprocessing.Queue(),multiprocessing.Queue(),multiprocessing.Queue()]
        process_list = []
        t_REAL = time.time()
        t_CPU = time.process_time()
        for i in range(1, 5):
            p = multiprocessing.Process(target=self.runQuadrant, args=(quadrants[i-1],queues_Quandrant,i,QuadrantExits,queue_final))
            process_list.append(p)

        for proc in process_list:
            proc.start()

        for proc in process_list:
            proc.join()

        
        # print("CPU TIME : ", elapsed_time_CPU)
        # print("REAL TIME : ", elapsed_time_REAL)
        sum = 0 
        
        sum+= queue_final.get()
        self.persons_exited = sum
        return 
            
    
        # while len(self.terrain.people):
        #     mob = self.terrain.people
        #     for person in mob:
        #         position_update = person.move_towards(person.closest_exit(self.terrain.exits), terrain=self.terrain)
        #         if self.terrain.is_exit(person.position):
        #             #print("Person", person.identifier, "successfully exited")
        #             self.terrain.people.remove(person)
