
#
#
import Globals as glb
import FileWorker as fw
import City as spacePoint
from GeneticAndEvoLib import GeneticAlgorithm as ga
import Visualizer as vis




if __name__ == "__main__":
    #

    #
    fileWorker = fw.FileWorker(citiesFilepath=glb.CITIES_FILEPATH, optTourFilepath=glb.OPTIMAL_TOUR_FILEPATH)
    citiesFileMetadata, optTourFileMetadata, \
    citiesCoordsList, optTourPointIdList = fileWorker.run()
    print()
    print("Cities File Metadata: ")
    print(citiesFileMetadata)
    print()
    print("Opt Tour File Metadata: ")
    print(optTourFileMetadata)
    print()
    print("Cities Coords List: ")
    print(citiesCoordsList)
    print()
    print("Opt Tour Point Id List: ")
    print(optTourPointIdList)
    #
    cityList = []
    #for i in range(0, 25):
    #    cityList.append(spacePoint.City(x=int(random.random() * 200), y=int(random.random() * 200)))
    for rec in citiesCoordsList:
        cityList.append(spacePoint.City(x=rec.x, y=rec.y))

    genAlgo = ga.GeneticAlgorithm()
    genAlgo.launchGeneticAlgorithm(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)

    visualizer = vis.Visualizer()
    visualizer.geneticAlgorithmPlot(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)

