
import numpy as np, \
    random, operator, \
    pandas as pd, \
    matplotlib.pyplot as plt
#
import MetricsEstimator as me
import PopulationCreator as pc

class GeneticAlgorithm:

    def __init__(self):
        pass

    def rankRoutes(self, population):
        fitnessResults = {}
        for i in range(0, len(population)):
            fitnessResults[i] = me.Fitness(population[i]).routeFitness()
        return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)

    def selection(self, popRanked, eliteSize):
        selectionResults = []
        df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

        for i in range(0, eliteSize):
            selectionResults.append(popRanked[i][0])
        for i in range(0, len(popRanked) - eliteSize):
            pick = 100 * random.random()
            for i in range(0, len(popRanked)):
                if pick <= df.iat[i, 3]:
                    selectionResults.append(popRanked[i][0])
                    break
        return selectionResults

    def matingPool(self, population, selectionResults):
        matingpool = []
        for i in range(0, len(selectionResults)):
            index = selectionResults[i]
            matingpool.append(population[index])
        return matingpool

    def breed(self, parent1, parent2):
        child = []
        childP1 = []
        childP2 = []

        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(startGene, endGene):
            childP1.append(parent1[i])

        childP2 = [item for item in parent2 if item not in childP1]

        child = childP1 + childP2
        return child

    def breedPopulation(self, matingpool, eliteSize):
        children = []
        length = len(matingpool) - eliteSize
        pool = random.sample(matingpool, len(matingpool))

        for i in range(0, eliteSize):
            children.append(matingpool[i])

        for i in range(0, length):
            child = self.breed(pool[i], pool[len(matingpool) - i - 1])
            children.append(child)
        return children

    def mutate(self, individual, mutationRate):
        for swapped in range(len(individual)):
            if (random.random() < mutationRate):
                swapWith = int(random.random() * len(individual))

                city1 = individual[swapped]
                city2 = individual[swapWith]

                individual[swapped] = city2
                individual[swapWith] = city1
        return individual

    def mutatePopulation(self, population, mutationRate):
        mutatedPop = []

        for ind in range(0, len(population)):
            mutatedInd = self.mutate(population[ind], mutationRate)
            mutatedPop.append(mutatedInd)
        return mutatedPop

    def nextGeneration(self, currentGen, eliteSize, mutationRate):
        popRanked = self.rankRoutes(currentGen)
        selectionResults = self.selection(popRanked, eliteSize)
        matingpool = self.matingPool(currentGen, selectionResults)
        children = self.breedPopulation(matingpool, eliteSize)
        nextGeneration = self.mutatePopulation(children, mutationRate)
        return nextGeneration

    def launchGeneticAlgorithm(self, population, popSize, eliteSize, mutationRate, generations):
        populationCreator = pc.PopulationCreator()
        pop = populationCreator.initialPopulation(popSize, population)
        print("Initial distance: " + str(1 / self.rankRoutes(pop)[0][1]))

        for i in range(0, generations):
            pop = self.nextGeneration(pop, eliteSize, mutationRate)

        print("Final distance: " + str(1 / self.rankRoutes(pop)[0][1]))
        bestRouteIndex = self.rankRoutes(pop)[0][0]
        bestRoute = pop[bestRouteIndex]
        return bestRoute

