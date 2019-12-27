import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, goal):
        return math.hypot(self.x - goal.x, self.y - goal.y)
    
    def isInside(self, listOfPoints):
        if( self.x >= listOfPoints[0].x and self.x < listOfPoints[1].x and self.y >= listOfPoints[0].y and self.y < listOfPoints[1].y ):
            return True
        else:
            return False
    def moved_by(self, dx, dy):
        return Point(self.x + dx, self.y + dy)
    def __str__(self):
        return "({:>3},{:>3})".format(self.x,self.y)

    def __eq__(self, obj):
        return isinstance(obj, Point) and obj.x == self.x and  obj.y == self.y
