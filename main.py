from src import arg_mng
from src.MobSimulator import MobSimulator
from src.Terrain import Terrain
import pickle,click
import datetime
import timeit,copy
import psutil
import time
from src.GLOBAL_CONSTANTS import * 

if __name__ == '__main__':
    parser = arg_mng.createParser()
    args = parser.parse_args()

    if args.l is None :
        print("Generating Terrain")
        terrain = Terrain.RandomTerrain(n_people=args.p)
        print("Terrain Generated")
        FileNameOut = "GeneratedTerrains/GeneratedTerrain_NP_"+str(args.p)+"___"+str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".dat"
        pickleOut= open(FileNameOut , "wb+")
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
        RealTime = []
        CPU_TIME = []
        for i in range(5):
            print("Running Simulation " , i+1)
            simulator = MobSimulator(copy.deepcopy(terrain))
            t_REAL = time.time()
            t_CPU = time.process_time()

            #
            # RT= timeit.Timer(simulator.run_single_threaded).repeat(repeat=1,number=1)[0]
            simulator.run_one_thread_per_person()
            elapsed_time_CPU = time.process_time() - t_CPU
            elapsed_time_REAL =  time.time() - t_REAL 
            RealTime.append(elapsed_time_REAL)
            CPU_TIME.append(elapsed_time_CPU)
            print("Simulation", i+1 ,"Finished ")
            print(simulator.terrain.persons_exited, "People Exited")
    elif args.t == 2:
        RealTime = []
        CPU_TIME = []
        #Quandrant Exits for quadrant 1 

        QuadrantExits[0] = DEFAULT_EXITS
        
        #Quandrant Exits for quadrant 2
        for i in range(0,1):
            QuadrantExits[1].append(Point(i,64))
       
        #Quandrant Exits for quadrant 3
        for i in range(0,1):
            QuadrantExits[2].append(Point(256,i))
        
        #Quandrant Exits for quadrant 4
        for i in range(64,65):
            QuadrantExits[3].append(Point(256,i))
            

        for inx in range(5):
            print("Running Simulation " , inx+1)

            quadrants = []
            sum = 0 
            for i in range(1,5):
                newQuadrant = copy.deepcopy(terrain)
                newQuadrant.keepOnlyPeopleOfQuadrant(i)
                quadrants.append(newQuadrant)
                sum += len(newQuadrant.people)
                
            t_REAL = time.time()
            t_CPU = time.process_time()
            simulator.run_one_thread_per_quadrant_multiprocessing(quadrants)
            elapsed_time_CPU = time.process_time() - t_CPU
            elapsed_time_REAL =  time.time() - t_REAL 
            RealTime.append(elapsed_time_REAL)
            CPU_TIME.append(elapsed_time_CPU)
            print("Simulation", inx+1 ,"Finished ")
            print(simulator.persons_exited, "People Exited")
    if args.m is True :
        RealTime.sort()
        CPU_TIME.sort()
        print("#######################################################################")

        print("Intermediate Real Times Taken to run the simulation", RealTime[1:4])
        print("Intermediate CPU Times Taken to run the simulation", CPU_TIME[1:4])
        avgCPUTime = avgRealTime = 0
        for i in range (1 , 4):
            avgRealTime += RealTime[i]
            avgCPUTime += CPU_TIME[i]
        avgRealTime = avgRealTime / 3
        print("Average REAL Time Taken to run the simulation : ", avgRealTime )
        avgCPUTime = avgCPUTime / 3
        print("Average CPU Time Taken to run the simulation  : ", avgCPUTime )
