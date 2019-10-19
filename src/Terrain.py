from src.Point import Point
from src.Person import Person

class Terrain:
    @staticmethod
    def RandomTerrain(n_people):
        return Terrain(size=(512, 128), obstacles=[], exits=[Point(0,0), Point(0, 1), Point(1, 0)], people=[Person(0, Point(510, 120)), Person(1, Point(0, 120))])

    def __init__(self, size, obstacles, exits, people):
        self.size = size
        self.obstacles = obstacles
        self.exits = exits
        self.people = people

        self._map = [[0 for _ in range(size[1])] for _ in range(size[0])]
        for obstacle in self.obstacles:
            for x in range(obstacle.top_left.x, obstacle.bottom_right.x):
                for y in range(obstacle.top_left.y, obstacle.bottom_right.y):
                    self._map[x][y] = 1
        for exit in exits:
            self._map[exit.x][exit.y] = -1
        for person in people:
            self._map[person.position.x][person.position.y] = 2

    def is_position_blocked(self, position):
        return self._map[position.x][position.y] > 0

    def is_exit(self, position):
        return self._map[position.x][position.y] < 0

    def update_person_position(self, position_update):
        self._map[position_update[0].x][position_update[0].y] = 0
        self._map[position_update[1].x][position_update[0].y] = 2

class Obstacle:
    def __init__(self, bounds):
        self.top_left = Point(bounds[0], bounds[2])
        self.bottom_right = Point(bounds[1], bounds[3])
