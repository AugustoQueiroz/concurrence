import threading

class MobSimulator:
    def __init__(self, terrain):
        self.terrain = terrain

    def run_single_threaded(self):
        while len(self.terrain.people):
            mob = self.terrain.people

            for person in mob:
                position_update = person.move_towards(person.closest_exit(self.terrain.exits), terrain=self.terrain)
                print(person.position.x, person.position.y)
                if self.terrain.is_exit(person.position):
                    self.terrain.people.remove(person)

    def run_one_thread_per_person(self):
        for person in self.terrain.people:
            x = threading.Thread(target=person.loop, args=(self.terrain,))
            x.start()

    def run_one_thread_per_quadrant(self):
        pass
