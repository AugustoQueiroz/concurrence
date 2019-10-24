from src import arg_mng
from src.MobSimulator import MobSimulator
from src.Terrain import Terrain
import pickle,click
import datetime

parser = arg_mng.createParser()
args = parser.parse_args()

if args.l is None :
    print("Generating Terrain")
    terrain = Terrain.RandomTerrain(n_people=args.p)
    print("Terrain Generated")
    FileNameOut = "GeneratedTerrain_NP_"+str(args.p)+"___"+str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".dat"
    pickleOut= open(FileNameOut , "wb")
    pickle.dump(terrain,pickleOut)
    pickleOut.close()
else:
    print("Loading Existing Terrain...")
    FileNameIn = args.l
    try:
        pickleIn = open ( FileNameIn,"rb")
        terrain = pickle.load(pickleIn)
        print("LOADED Existing Terrain!")
    except :
        print("No such file at the path given : ",FileNameIn)
        if click.confirm('Do you want to generate a new terrain and continue?', default=True):
            print("Generating Terrain")
            terrain = Terrain.RandomTerrain(n_people=args.p)
            print("Terrain Generated")
            FileNameOut = "GeneratedTerrain_NP_"+str(args.p)+"___"+str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".dat"
            pickleOut= open(FileNameOut , "wb")
            pickle.dump(terrain,pickleOut)
            pickleOut.close()
        else:
            print("Programmed Terminated!")
            exit()
    

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
