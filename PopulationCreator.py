
#
import random as rnd

class PopulationCreator:

    def __init__(self):
        pass

    def createRoute(self, cityList):
        route = rnd.sample(cityList, len(cityList))
        return route

    def initialPopulation(self, popSize, cityList):
        population = []
        for i in range(0, popSize):
            population.append(self.createRoute(cityList))
        return population