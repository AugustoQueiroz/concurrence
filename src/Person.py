from src.Point import Point

class Person:
    def __init__(self, identifier, position):
        self.identifier = identifier
        self.position = position

    def move_towards(self, goal, terrain, locking=False):
        if locking:
            terrain.lock_positions_for_person(self.position)
            #print('Locked positions')
        best_movement = (self.position, self.position.distance_to(goal))

        for dx in range(-1, 1):
            for dy in range(-1, 1):
                new_position = self.position.moved_by(dx, dy)
                if terrain.is_position_blocked(new_position):
                    #print("Cannot move there", terrain._map[new_position.x][new_position.y])
                    continue
                new_distance = new_position.distance_to(goal)

                if new_distance < best_movement[1]:
                    best_movement = (new_position, new_distance)
                #else:
                    #print("Wont move there")
        
        old_position = self.position
        self.position = best_movement[0]

        terrain.update_person_position((old_position, self.position))

        if locking:
            terrain.unlock_positions_for_person(old_position)
            #print('Unlocked positions')

        return (old_position, self.position)

    def closest_exit(self, exits):
        closest = (exits[0], self.position.distance_to(exits[0]))

        for exit in exits[1:]:
            distance_from_person = self.position.distance_to(exit)
            if distance_from_person < closest[1]:
                closest = (exit, distance_from_person)

        return closest[0]

    def loop(self, terrain):
        while not terrain.is_exit(self.position):
            position_update = self.move_towards(self.closest_exit(terrain.exits), terrain=terrain, locking=True)
            if person_update[0].x == person_update[1].x and person_update[0].x == person_update[1].x:
                print('Person', self.identifier, 'is not moving')
            #terrain.update_person_position(position_update)
            #print("Person", self.identifier, "moved to", self.position.x, self.position.y)
    
    def __str__(self):
        return "Person {} : {} ".format(self.identifier,self.position)
