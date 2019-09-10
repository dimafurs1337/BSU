from math import exp,pi,sqrt
from random import uniform
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import integrate

G = lambda x,y,r1,r2: (True if r1 <= x**2 + y**2 < r2 else False)

def func(x,y):
    return (x**3 + exp(y))/(x**2 +2*y**2)

def MonteCarlo_integrate(f,x0, x1, y0, y1, n, r1, r2):
	x = np.random.uniform(x0, x1, n)
	y = np.random.uniform(y0, y1, n)
	func_sum = 0         
	for i in range(n):
		if G(x[i], y[i], r1, r2):
			func_sum += f(x[i], y[i])
	area = ((x1-x0)*(y1-y0))/n
	return area*func_sum

def get_limits(d):
	def limit(x):
		y = (d - x**2)**0.5
		return [-y,y]
	return limit

def library_integrate(f, r1, r2):
	e = 0.001
	i_1 = integrate.nquad(f, [get_limits(r2**2), [-r2, -e]])[0]
	i_2 = integrate.nquad(f, [get_limits(r2**2), [e, r2]])[0]
	i_3 = integrate.nquad(f, [get_limits(r1**2), [-r1, -e]])[0]
	i_4 = integrate.nquad(f, [get_limits(r1**2), [e, r1]])[0]
	return i_1 + i_2 - (i_3 + i_4)

def steps():
    return (2**x for x in range(0, 16))

def test(f,x0, x1, y0, y1,r1, r2):
    return [MonteCarlo_integrate(f,x0, x1, y0, y1, n, r1, r2) for n in steps()]

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

realValue = library_integrate(func,1,7**0.5)
draw(test(func,-7**0.5,7**0.5,-7**0.5,7**0.5,1,7),realValue)
