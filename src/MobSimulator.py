import threading

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
            

    def run_one_thread_per_quadrant(self):
        pass
