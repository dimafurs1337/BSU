import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt


def get_B(matrix):
    n = len(matrix)
    for i in range(n):
        matrix[i][i] -= 1
        for j in range(n):
            matrix[i][j] *= -1
    return matrix

def get_rand():
    rd = random.uniform(0,1)
    if rd < (1.)/3: return 0
    elif rd < (2.)/3: return 1
    else: return 2
                        
def monte_carlo(matrix,b,N,L):
    a = get_B(matrix)
    n = len(matrix)
    p = [[0 for _ in range(n)] for _ in range(n)]
    res = [0]*n
    for i in range(n):
        l = sum(element != 0 for element in a[i])
        elem = 1 / l
        for j in range(n):
            p[i][j] = elem
    
    for j in range(n):
        Q, ksi = 0,0
        for i in range(L):
            x_ind = j
            Q_pr = 1
            for l in range(1,N):
                ind = get_rand()
                if p[x_ind][ind] > 0: Q = Q_pr*a[x_ind][ind]/p[x_ind][ind]
                else: Q = 0
                ksi += Q*b[ind]
                Q_pr = Q
                x_ind = ind
        res[j] = b[j] + ksi/L
    return res

def max_norm(vector):
    return max(abs(elem) for elem in vector)

def substract_vectors(a,b):
    return [a[i]-b[i] for i in range(len(a))]

def steps():
    return (2**x for x in range(0, 16))

def test(matrix,b,realValue):
    return [max_norm(substract_vectors(monte_carlo(matrix,b,10,n),realValue)) for n in steps()]

def draw(calculated):
    matplotlib.rc('ytick', labelsize=10)
    matplotlib.rc('xtick', labelsize=10)
    plt.figure(figsize=(10, 5))
    x = list(steps())
    plt.plot(x, calculated, label='Calculated',color="m")
    plt.xscale('log')
    plt.xticks(x, x)
    plt.xlabel('N', fontsize=10)
    plt.ylabel('Max norm', fontsize=10)
    plt.legend()
    plt.show()
        