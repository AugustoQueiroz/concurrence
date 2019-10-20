from src import arg_mng
from src.MobSimulator import MobSimulator
from src.Terrain import Terrain

parser = arg_mng.createParser()
args = parser.parse_args()

print("Generating Terrain")
terrain = Terrain.RandomTerrain(n_people=args.p)
print("Terrain Generated")
print("Instantiating Simulator")
simulator = MobSimulator(terrain)
print("Simulator Instantiated")

if args.t == 0:
    print("Running Simulation")
    simulator.run_single_threaded()
    print("Simulation Finished")
elif args.t == 1:
    simulator.run_one_thread_per_person()
elif args.t == 2:
    simulator.run_one_thread_per_quadrant()
