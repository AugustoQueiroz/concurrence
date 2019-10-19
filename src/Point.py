import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, goal):
        return math.hypot(self.x - goal.x, self.y - goal.y)

    def moved_by(self, dx, dy):
        return Point(self.x + dx, self.y + dy)
    def __str__(self):
        return "({:>3},{:>3})".format(self.x,self.y)

