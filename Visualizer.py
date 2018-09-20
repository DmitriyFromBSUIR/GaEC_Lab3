
#
import matplotlib.pyplot as plt
#
import PopulationCreator as pc
from GeneticAndEvoLib import GeneticAlgorithm as ga


class Visualizer:

    def __init__(self):
        pass

    def geneticAlgorithmPlot(self, population, popSize, eliteSize, mutationRate, generations):
        populationCreator = pc.PopulationCreator()
        pop = populationCreator.initialPopulation(popSize, population)
        progress = []
        genAlgo = ga.GeneticAlgorithm()
        progress.append(1 / genAlgo.rankRoutes(pop)[0][1])

        for i in range(0, generations):
            pop = genAlgo.nextGeneration(pop, eliteSize, mutationRate)
            progress.append(1 / genAlgo.rankRoutes(pop)[0][1])

        plt.plot(progress)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show()

        plt.savefig("./Plots/plot.png")
        #plt.imsave("./Plots/plot2.png")