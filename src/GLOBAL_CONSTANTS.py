from src.Point import Point
#GLOBAL CONSTANTS
OBSTACLE_IDENTIFIER = 1
EXIT_IDENTIFIER = -2
EMPTY_IDENTIFIER = 0
PERSON_IDENTIFIER = 2

MAX_OBSTACLE_HEIGHT = 10
MAX_OBSTACLE_WIDTH  = 10

MAX_NUMBER_OF_PEOPLE = 512

DEFAULT_SIZE = [512,128]
DEFAULT_EXITS= [Point(0,0),Point(1,0),Point(0,1)]

rangeQ = [ [Point(0,0),Point(256,64)],  [Point(0,64),Point(256,128)] ,  [Point(256,0),Point(512,64)] , [Point(256,64),Point(512,128)] ]

QuadrantExits = [list(),list(),list(),list()]