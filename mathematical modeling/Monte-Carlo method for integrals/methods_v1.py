from math import exp,pi
from random import uniform
import scipy.integrate as integrate
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def func(x):
    return exp(-x**4) * (1 + x**2)**0.5

def generateSequence(n=1000):
    return [sum([uniform(0,1) for _ in range(12)])-6 for i in range(n)]

def integralEvaluate(n, seq, func):
    return (pow(2*pi,0.5)/n)*sum([func(seq[i])*exp(0.5* seq[i]**2) for i in range(n)])

def steps():
    return (2**x for x in range(0, 16))

def test(func):
    return [integralEvaluate(n,generateSequence(n),func) for n in steps()]

def draw(calculated, approximate):
    matplotlib.rc('ytick', labelsize=10)
    matplotlib.rc('xtick', labelsize=10)
    plt.figure(figsize=(10, 5))
    x = list(steps())
    plt.plot(x, [approximate]*len(x), label='Approximate',color="c")
    plt.plot(x, calculated, label='Calculated',color="m")
    plt.xscale('log')
    plt.xticks(x, x)
    plt.xlabel('Number of iterations(n)', fontsize=10)
    plt.ylabel('Integral value', fontsize=10)
    plt.legend()
    plt.show()

realValue = integrate.quad(func,-np.inf, np.inf)[0]
draw(test(func),realValue)