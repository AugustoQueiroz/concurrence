import argparse

def createParser():
    parser = argparse.ArgumentParser(description="Simulate the movement of people in a room")
    parser.add_argument("-p", type=int, help="An int in the range [0,9] that codes the number of people in the terrain\nThe number of people = 2^p", required=True)
    parser.add_argument("-t", type=int, help="Mode in which the program should be run.\n0 - Single Thread,\n1 - One thread for each person,\n2 - One thread for each quadrant of the terrain", required=True)
    parser.add_argument("-m", action='store_true')
    parser.add_argument("-l", type=str, help="Load pre-existing terrain, (specify path after -l)", required=False)

    return parser

if __name__ == "__main__":
    parser = createParser()
    args = parser.parse_args()
    print(args)
