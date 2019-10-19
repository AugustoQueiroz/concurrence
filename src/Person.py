from Point import Point

class Person:
    def __init__(self, identifier, position):
        self.identifier = identifier
        self.position = position

    def move_towards(self, goal, blocked_positions=[]):
        best_movement = (self.position, self.position.distance_to(goal))

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx, dy) in blocked_positions:
                    continue

                new_position = self.position.moved_by(dx, dy)
                new_distance = new_position.distance_to(goal)

                if new_distance < best_movement[1]:
                    best_movement = (new_position, new_distance)
        
        self.position = best_movement[0]

    def closest_exit(self, exits):
        closest = (exits[0], self.position.distance_to(exits[0]))

        for exit in exits[1:]:
            distance_from_person = self.position.distance_to(exit)
            if distance_from_person < closest[1]:
                closest = (exit, distance_from_person)

        return closest[0]
    
    def __str__(self):
        return "Person {} : {} ".format(self.identifier,self.position)


