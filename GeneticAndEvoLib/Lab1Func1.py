'''
Find the global maximum for function: F(t) = (a*t + b)*sin(c*PI*t + d)   t [0;5]
'''

import math
from math import sin, cos

from gaft import GAEngine
from gaft.components import BinaryIndividual
from gaft.components import Population
from gaft.operators import TournamentSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitMutation

# Analysis plugin base class.
from gaft.plugin_interfaces.analysis import OnTheFlyAnalysis

# Built-in best fitness analysis.
from gaft.analysis.fitness_store import FitnessStore

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

point = list()

# Define population.
indv_template = BinaryIndividual(ranges=[(0, 10)], eps=0.001)
population = Population(indv_template=indv_template, size=30).init()

# Create genetic operators.
selection = TournamentSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitMutation(pm=0.1)

# Create genetic algorithm engine.
engine = GAEngine(population=population, selection=selection,
                  crossover=crossover, mutation=mutation,
                  analysis=[FitnessStore])

def func1(t, a=1.5, b=0.9, c=1, d=1.1):
    return (a*t + b)*math.sin(c*math.pi*t + d)

# Define fitness function.
@engine.fitness_register
def fitness(indv):
    x, = indv.solution
    return func1(x)

# Define on-the-fly analysis.
@engine.analysis_register
class ConsoleOutputAnalysis(OnTheFlyAnalysis):
    interval = 1
    master_only = True

    def register_step(self, g, population, engine):
        best_indv = population.best_indv(engine.fitness)
        msg = 'Generation: {}, best fitness: {:.3f}'.format(g, engine.ori_fmax)
        self.logger.info(msg)

    def finalize(self, population, engine):
        best_indv = population.best_indv(engine.fitness)
        x = best_indv.solution
        y = engine.ori_fmax
        point.append(x)
        point.append(y)
        msg = 'Optimal solution: ({}, {})'.format(x, y)
        self.logger.info(msg)

if '__main__' == __name__:
    # Run the GA engine.
    engine.run(ng=150)
    #
    #x = y = np.arange(-2.048, 2.048, 0.05)
    #X, Y = np.meshgrid(x, y)
    X = np.arange(0, 11, 0.05)
    y = np.array([func1(x) for x in X])
    #Z = zs.reshape(X.shape)
    sns.set_style("darkgrid")
    plt.plot(X, y)
    plt.scatter(np.array([point[0]]),
               np.array([point[1]]),
               color='red',
               s=40
               )
    plt.show()