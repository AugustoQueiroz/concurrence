from src import arg_mng
from src.MobSimulator import MobSimulator
from src.Terrain import Terrain

parser = arg_mng.createParser()
args = parser.parse_args()

terrain = Terrain.RandomTerrain(n_people=2**args.p)
simulator = MobSimulator(terrain)

if args.t == 0:
    simulator.run_single_threaded()
elif args.t == 1:
    simulator.run_one_thread_per_person()
elif args.t == 2:
    simulator.run_one_thread_per_quadrant()
