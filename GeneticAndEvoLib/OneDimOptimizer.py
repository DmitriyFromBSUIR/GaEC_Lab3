
#
import math
import random
from math import sin, cos
#
import numpy as np
import matplotlib.pyplot as plt
#
from gaft.components import BinaryIndividual
from gaft.components import Population
from gaft.operators import TournamentSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitMutation
# Import an on-the-fly analysis plugin to output info to console
from gaft.analysis import ConsoleOutput
from gaft import GAEngine
# Analysis plugin base class.
from gaft.plugin_interfaces.analysis import OnTheFlyAnalysis


# Find the global maxima of function F(t) = (a*t + b)*sin(c*PI*t + d)   t [0;5]
# Find the global minima of function F(t) = (a*t + b)*cos(c*PI*t + d)   t [-6;6]

def func1(t, a=1.5, b=0.9, c=1, d=1.1):
    return (a*t + b)*math.sin(c*math.pi*t + d)

def func2(t, a=1.3, b=1.9, c=1.1, d=-1.5):
    return (a*t + b)*math.cos(c*math.pi*t + d)

'''
@engine.fitness_register
@engine.minimize
def fitness(indv):
    x, = indv.solution
    return x + 10*sin(5*x) + 7*cos(4*x)

'''


if __name__ == '__main__':
    # Create individual (use binary encoding)
    indv = BinaryIndividual(ranges=[(0, 10)], eps=0.001)
    # Create a population with 50 individuals
    population = Population(indv_template=indv, size=50).init()
    # Create genetic operators: selection, crossover, mutation
    # 1. Tournament selection
    selection = TournamentSelection()
    # 2. Uniform crossover
    # pc is the probabililty of crossover operation
    # pe is the exchange probabiltiy for each possible gene bit in chromsome
    crossover = UniformCrossover(pc=0.8, pe=0.5)
    # 3. Flip bit mutation
    # pm is the probability of mutation
    mutation = FlipBitMutation(pm=0.1)
    # Create an engine to run
    engine1 = GAEngine(population=population, selection=selection,
                      crossover=crossover, mutation=mutation,
                      analysis=[ConsoleOutput])
    engine2 = GAEngine(population=population, selection=selection,
                      crossover=crossover, mutation=mutation,
                      analysis=[ConsoleOutput])
    # Define target function to optimize
    # here we try to find the global minima of func2 and maxima of func1
    # GA engine find the maxima of the fitness function, here we use the engine.minimize decorator to tell GA engine to find the minima.
    fitnessFunc1 = None
    fitnessFunc2 = None

    @engine2.fitness_register
    @engine2.minimize
    def fitness2(indv):
        x, = indv.solution
        return func2(x)

    @engine1.fitness_register
    @engine1.minimize
    def fitness1(indv):
        x, = indv.solution
        return -func1(x)

    fitnessFunc1 = fitness1
    fitnessFunc2 = fitness2

    # Run the engine 1
    engine1.run(ng=50)
    # Run the engine 2
    engine2.run(ng=50)

    # After engine running, we can do something more...
    # Get the best individual
    best_indv = engine1.population.best_indv(engine1.fitness)
    # Get the solution
    print("========================")
    print("Function for Alex:")
    print("========================")
    print("t = ", best_indv.solution)
    # And the fitness value
    print("F(t) = ", fitnessFunc1(best_indv))

    best_indv = engine2.population.best_indv(engine2.fitness)
    # Get the solution
    print("========================")
    print("Function for Me:")
    print("========================")
    print("t = ", best_indv.solution)
    # And the fitness value
    print("F(t) = ", fitnessFunc2(best_indv))


    @engine1.analysis_register
    class ConsoleOutput(OnTheFlyAnalysis):
        master_only = True
        interval = 1
        def register_step(self, g, population, engine):
            best_indv = population.best_indv(engine.fitness)
            msg = 'Generation: {}, best fitness: {:.3f}'.format(g, engine.fmax)
            engine.logger.info(msg)