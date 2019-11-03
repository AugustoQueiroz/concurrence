from src import arg_mng
from src.MobSimulator import MobSimulator
from src.Terrain import Terrain
import pickle,click
import datetime
import timeit,copy
import psutil
import time

parser = arg_mng.createParser()
args = parser.parse_args()

if args.l is None :
    print("Generating Terrain")
    terrain = Terrain.RandomTerrain(n_people=args.p)
    print("Terrain Generated")
    FileNameOut = "GeneratedTerrains/GeneratedTerrain_NP_"+str(args.p)+"___"+str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".dat"
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
            FileNameOut = "GeneratedTerrains/GeneratedTerrain_NP_"+str(args.p)+"___"+str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".dat"
            pickleOut= open(FileNameOut , "wb")
            pickle.dump(terrain,pickleOut)
            pickleOut.close()
        else:
            print("Programmed Terminated!")
            exit()
    

print("Instantiating Simulator")
originalTerrain = terrain
simulator = MobSimulator(terrain)
print("Simulator Instantiated")

if args.t == 0:
    RealTime = []
    CPU_TIME = []
    for i in range(5):
        print("Running Simulation " , i+1)
        simulator = MobSimulator(copy.deepcopy(terrain))
        t_REAL = time.time()
        t_CPU = time.process_time()

        #
        # RT= timeit.Timer(simulator.run_single_threaded).repeat(repeat=1,number=1)[0]
        simulator.run_single_threaded()
        elapsed_time_CPU = time.process_time() - t_CPU
        elapsed_time_REAL =  time.time() - t_REAL 
        RealTime.append(elapsed_time_REAL)
        CPU_TIME.append(elapsed_time_CPU)
        print("Simulation", i+1 ,"Finished ")
elif args.t == 1:
    simulator.run_one_thread_per_person()
elif args.t == 2:
    simulator.run_one_thread_per_quadrant()
    
if args.m is True :
    RealTime.sort()
    CPU_TIME.sort()
    print("#######################################################################")

    print("Intermediate Real Times Taken to run the simulation", RealTime[1:4])
    print("Intermediate CPU Times Taken to run the simulation", CPU_TIME[1:4])
    avgRealTime = sum(RealTime[1:4]) / 3
    print("Average Time Taken to run the simulation : ", avgRealTime )
    avgCPUTime = sum(CPU_TIME[1:4]) / 3
    print("Average Time Taken to run the simulation : ", avgCPUTime )
