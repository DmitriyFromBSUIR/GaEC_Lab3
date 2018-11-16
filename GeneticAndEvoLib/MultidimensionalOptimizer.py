#!/usr/bin/python
''' Simple Differential Evolution implementation: Scheme DE1- de/rand/1

@article{storn1997differential,
title={{Differential evolution--a simple and efficient heuristic for global optimization over continuous spaces}},
author={Storn, R. and Price, K.},
journal={Journal of global optimization},
volume={11},
number={4},
pages={341--359},
year={1997},
publisher={Springer}
}

Also refer: http://www.icsi.berkeley.edu/~storn/code.html

CONTACT
-------

Please contact for bug reports/patches or anything else via electronic mail:
Amit Saha <amitsaha.in@gmail.com>, http://amitksaha.wordpress.com


README
-------

Verson 0.1 - 16/03/2010

Its probably going to remain a hobby code. However, feel free to use it to improve it
for your works, and i would really get that warm fuzzy feeling to know if my code has helped
you in some way. Drop me an email about your improvements.

Gotchas:
1. No constraint handling, except boundary constraints
2. Limited testing (Since simulated evolution almost works everytime, this code also works)
3. All the data structure are Globals (FIXME)
4. Not much thought have been given to the code quality


Usage:

1. Define your objective function in func()
2. Create a input file in the following form:

   Number of generations
   dimension of the problem
   lower variable1 bound
   upper variable2 bound
   .
   .
   .

$ python de.py < input.inp


TODOS
-----
- User interaction?
- Simple Constraint Handling

DATA STRUCTURE
--------------

pop: The population is represented as a list of lists
fvals: List containing the objective function values
NP: population size

Xu: List of the upper bounds of the variables
Xl: List of the lower bounds of the variables
dim: number of variables

'''

import random
import math

import numpy as np
from mpl_toolkits.mplot3d import Axes3D # This import has side effects required for the kwarg projection='3d' in the call to fig.add_subplot
import matplotlib.pyplot as plt
import random

# math functions & constants
sin = math.sin
cos = math.cos
sqrt = math.sqrt
pi = math.pi
fabs = math.fabs

# FIX (no globals)
dim = 0
Xu = []
Xl = []
pop = []
fvals = []
num_fe = 0  # count the total number of function evaluations
max_gen = 0  # number of generations
NP = 0
cr = 0.90  # crossover probability
F = 0.90  # Scaling factor
U = []  # trial vector

f_best = -1

f_best_list = []

xy = list()
z = 0


# util function- return a random real in (0.0,1.0)
def urand():
    return random.random()

'''
# objective function
def func(X):
    global num_fe
    sum = 0

    # Rastrigin function (2 variables)
    # for i in xrange(0,dim):
    #     sum = sum + 10*cos(2*pi*X[i]*X[i])

    # Schwefel function (20 variables)
    for i in range(0, dim):
        sum = sum + X[i] * sin(sqrt(fabs(X[i])))
    sum = 418.9828872724337998 * (dim * 1.0) - sum

    # First De Jong function (Sphere)
    # [-5.12,5.12]
    # for i in xrange(0,dim):
    #     sum = sum + X[i]*X[i];

    # Second De Jong function (Rosenbrock's Function)
    # [-2.048,2.048]
    # sum = 100.0*((X[0]**2 - X[1])**2) + (1.0-X[0])**2

    num_fe = num_fe + 1

    return sum
'''

def func(X):
    global num_fe
    res = 0

    soq = X[0]*X[0] + X[1]*X[1]
    # 6th Schaffer function (2 variables)
    # 0.5 + ( ( sin( sqrt(x*x +y*y) ))^2 - 0.5 ) / ( (1 + 0.001*(x*x +y*y))^2 )
    #res = 0.5 + ( pow( sin( sqrt(soq) ), 2) - 0.5 ) / ( pow(1 + 0.001*(soq), 2) )
    # 2nd Yong's function (2 variables)
    # 100 * ( x^2 - y )^2 + (1-x)^2
    res = 100*pow((X[0]*X[0] - X[1]), 2) + pow(1-X[0], 2)

    return res

# Control parameters
def setup():
    global max_gen, dim, Xu, Xl, NP, f_best

    #max_gen = input("Enter the max. number of generations:: ")
    #max_gen = int(max_gen)
    max_gen = 1000
    #dim = input("Enter the dimension of the problem:: ")
    #dim = int(dim)
    dim = 2

    for i in range(0, dim):
        #print("Enter the lower and upper bound of %d th variable" % i)
        #Xl.insert(i, int(input()))
        #Xu.insert(i, int(input()))

        #Xl.insert(i, -100)
        #Xu.insert(i, 100)
        Xl.insert(i, -2.048)
        Xu.insert(i, 2.048)

    NP = 20 * dim  # population size

    # Open the file to store the best individual of every generation
    f_best = open("best_pop.out", "w")


# Initialize population
def initpop():
    global pop, fvals, num_fe

    pop = []
    fvals = []

    for i in range(0, NP):
        X = []
        for j in range(0, dim):
            # fill up X and just add it to the pop
            X.insert(j, (Xl[j] + (Xu[j] - Xl[j]) * urand()))

        # bounds check
        for j in range(0, dim):
            while X[j] < Xl[j] or X[j] > Xu[j]:
                if X[j] < Xl[j]:
                    X[j] = 2 * Xl[j] - X[j]
                if X[j] > Xu[j]:
                    X[j] = 2 * Xu[j] - X[j]

        pop.insert(i, X)
        fvals.insert(i, func(X))  # function evaluation


# DE/rand/1
def evolve_de_rand_1():
    global pop, fvals

    for i in range(0, max_gen):
        # Write the best individual of this generation into a file
        # best_pop.out
        write_best()
        for j in range(0, NP):

            ''' Mutation '''
            # select r1,r2,r3 in [0,NP) such that r1 != j != r2 != r3
            while True:
                r1 = random.randint(0, NP - 1)
                if r1 != j:
                    break

            while True:
                r2 = random.randint(0, NP - 1)
                if r2 != r1 and r2 != j:
                    break

            while True:
                r3 = random.randint(0, NP - 1)
                if r3 != r2 and r3 != r1 and r3 != j:
                    break

            U = []
            for k in range(0, dim):
                # if urand() <= cr and k == dim_rand:
                U.insert(k, (pop[r3])[k] + F * ((pop[r1])[k] - (pop[r2])[k]))
                # else:
                #    U.insert(k,(pop[j])[k])

            ''' Crossover '''
            n = int(urand() * dim)
            L = 0
            while 1:
                L = L + 1
                if urand() > cr or L > dim:
                    break

            for k in range(0, dim):
                for kk in (n, n + L):
                    if k != (kk % dim):
                        U.insert(k, (pop[j])[k])

            # bounds check
            for k in range(0, dim):
                while U[k] < Xl[k] or U[k] > Xu[k]:
                    if U[k] < Xl[k]:
                        U[k] = 2 * Xl[k] - U[k]
                    if U[k] > Xu[k]:
                        U[k] = 2 * Xu[k] - U[k]

            U.insert(dim, func(U))  # the last value in the list is the function value

            ''' Selection'''
            # Comparing the trial vector, 'U' and the old individual
            if U[dim] <= fvals[j]:
                for k in range(0, dim):
                    (pop[j])[k] = U[k]
                fvals.insert(j, func(pop[j]))


# Find the best obj. fn. value and write it to the file
# called every generation
def write_best():
    best_val = fvals[0]
    best_index = 0
    for i in range(0, NP):
        if fvals[i] < best_val:
            best_index = i
            best_val = fvals[i]

    # for i in xrange(0,dim):
    #     f_best.write(str((pop[best_index])[i]) + '\t')
    print("best val: " + str(best_val))
    # f_best_list.append(fvals[best_index])
    f_best.write(str(best_val))
    f_best.write('\n')


#xy = None
#z = None

# Report the best pop and save the population
# statistics
def report():
    #global xy, z

    # Save the final population to the file
    f = open("final_pop.out", "w")
    f.write("Final population Data: Variable values || Objective function values\n")
    for i in range(0, NP):
        for j in range(0, dim):
            f.write(str((pop[i])[j]) + '\t')
        f.write('\t\t|| ')
        f.write(str(fvals[i]))
        f.write('\n')
    f.close()

    # Find the best individual and report
    best_val = fvals[0]
    best_index = 0
    for i in range(0, NP):
        if fvals[i] < best_val:
            best_index = i
            best_val = fvals[i]

    xy.append(pop[best_index][0])
    xy.append(pop[best_index][1])
    z = fvals[best_index]
    print("The best indvidual (x,y) is", xy, "::  z = ", z)
    print("Total number of function evaluations:: ", num_fe)
    #return [xy[0], xy[1], z]


def viz():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #x = y = np.arange(-100.0, 100.0, 0.05)
    x = y = np.arange(-2.048, 2.048, 0.05)
    X, Y = np.meshgrid(x, y)
    zs = np.array([func([x,y]) for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)

    ax.plot_surface(X, Y, Z)

    # draw best point
    ax.scatter(np.array([xy[0]]),
               np.array([xy[1]]),
               np.array([z]),
               color='red',
               s=40
               )

    '''
    for val in f_best_list:
        print("val ", val)
        ax.scatter(np.array([val[0]]),
                   np.array([val[1]]),
                   np.array([val[2]]),
                   color='yellow',
                   s=20
                   )
    '''

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()


if __name__ == '__main__':
    print("****************************************")
    print("Simple Differential Evolution  - Scheme DE1")
    print("*****************************************")
    setup()
    initpop()
    print("Evolution in progress..")
    evolve_de_rand_1()
    print("---------------------------------------")
    #print(X)
    #print("xy ", xy, " z ", z)

    print("Evolution Summary")
    print("*****************")
    report()

    viz()
