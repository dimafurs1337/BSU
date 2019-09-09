import random as rand
from copy import deepcopy
import time
from math import sqrt, cos, sin, log, exp, pi, fabs
import time
from matplotlib import pyplot as plt
import cmath

def sign(x): return 1 if x >= 0 else -1

def generate_matrix(n, _range):
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = rand.uniform(-pow(2,_range/4),pow(2,_range/4))
    return matrix

def multiplication(matrix, vector):
    return [sum(matrix[i][j]*vector[j] for j in range(len(vector))) for i in range(len(matrix))]
    
def square_norm(vector):
    return sqrt(sum(elem**2 for elem in vector)) 

def scalar_vector_multiplication(scalar,vector):
	return [scalar*x for x in vector]

def substract_vectors(a,b):
    return [a[i]-b[i] for i in range(len(a))]

def dot_product(a,b):
	return sum(a[i]*b[i] for i in range(len(a)))

def power_iteration(matrix):
    u = [0]*len(matrix)
    u[0] = 1
    l = 0
    i=0
    while square_norm(substract_vectors(multiplication(matrix,u),scalar_vector_multiplication(l,u))) > 10**(-14):
        y = multiplication(matrix,u)
        u = scalar_vector_multiplication(1/square_norm(y),y)
        l = dot_product(u,multiplication(matrix,u))
    return [l,u]

def substract_diag(matrix, diag):
	m = deepcopy(matrix)
	for i in range(len(diag)):
		m[i][i] -= diag[i]
	return m

def find_another_eig(matrix,l1):
	b = substract_diag(matrix,[l1 for i in range(len(matrix))])
	v = power_iteration(b)
	v[0] += l1
	return v 

def find_different_eigs(matrix):
    st = time.time()
    v1 = power_iteration(matrix)
    st = time.time()
    v2 = find_another_eig(matrix,v1[0])
    return v1,v2

def matrix_multiplication(matrix1, matrix2):
    n = len(matrix1)
    m = len(matrix1[0])
    p = len(matrix2[0])
    return [[sum(x * y for x, y in zip(matrix1_r, matrix2_c)) for matrix2_c in zip(*matrix2)] for matrix1_r in matrix1]

def qr_decomposition(matrix):
    n = len(matrix)
    a = deepcopy(matrix)
    d = [0]*n
    for j in range(n):
        s=0
        for i in range(j,n):
            s = s + pow(a[i][j],2)
        s = sqrt(s)
        d[j] = -sign(a[j][j])*s
        a[j][j] = a[j][j] - d[j]
        s=0
        for i in range(j,n):
            s = s+pow(a[i][j],2)
        s = sqrt(s)
        for k in range(j,n):
            a[k][j] = a[k][j]*10000 / (s*10000)
        for i in range(j+1,n):
            s=0
            for k in range(j,n):
                s = s+a[k][j]*a[k][i]
            for k in range(j,n):
                a[k][i] = a[k][i] - 2*s*a[k][j]
    R = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        R[i][i] = d[i]
    for i in range(n-1):
        for j in range(i+1,n):
            R[i][j] = a[i][j]
    
    Q = [[0 for _ in range(n)] for _ in range(n)]
    for _y in range(n):
        y = [1 if i ==_y else 0 for i in range(n)]
        for j in range(n):
            s = 0
            for k in range(j,n):
                s = s + a[k][j] * y[k]
            for k in range(j,n):
                y[k] = y[k] - 2*s*a[k][j]
        Q[_y] = y
    return Q, R
    
def qr_algorithm(A,max_iter=100):
    Ak = deepcopy(A)
    n = len(A[0])
    QQ = [[1 if i==j else 0 for i in range(n)] for j in range(n)]
    for k in range(max_iter):
        Q, R = qr_decomposition(Ak)
        Ak = matrix_multiplication(R,Q)
        QQ = matrix_multiplication(QQ,Q)
    return Ak, QQ

def solve_equation(t1,t2,t3,t4):
    a = 1
    b = -(t4+t1)
    c = t4*t1-t2*t3
    d = (b**2) - (4*a*c)
    sol1 = (-b-cmath.sqrt(d))/(2*a)
    sol2 = (-b+cmath.sqrt(d))/(2*a)
    return sol1,sol2

def get_tridiag_form(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if abs(matrix[i][j])< 10**(-10):
                matrix[i][j] = 0
    return matrix

def extract_eigvals(matrix):
    res = []
    n=len(matrix)
    i=0
    while i < n:
        if i == n-1:
            res.append(matrix[i][i])
            i+=1
        elif matrix[i+1][i] != 0.0:
            res.append(solve_equation(matrix[i][i],matrix[i][i+1],matrix[i+1][i],matrix[i+1][i+1]))
            i+=2
        else:
            res.append(matrix[i][i])
            i+=1
    return res

def arnoldi_hessenberg(a):
    n = len(a)
    Q = [[0 for _ in range(n+1)] for _ in range(n)] 
    h = [[0 for _ in range(n)] for _ in range(n+1)]
    
    q1 = [0]*n
    q1[0] = 1
    for i in range(n):
        Q[i][0] = q1[i]
    
    for numIter in range(n):
        z = [0]*n
        for i in range(n):
            s=0
            for j in range(n):
                s += a[i][j]*Q[j][numIter]
            z[i] = s
        
        for j in range(numIter+1):
            h[j][numIter] = sum(z[t]*Q[t][j] for t in range(n))
            z = substract_vectors(z,[h[j][numIter]*Q[t][j] for t in range(n)])
        h[numIter+1][numIter] = square_norm(z)
        if h[numIter+1][numIter] == 0: return h
        for i in range(n):
            Q[i][numIter+1] = z[i] / h[numIter+1][numIter]
        
    return h[:-1]

def find_all_eigvals(matrix,max_iter=100):
    Q,R = qr_algorithm(arnoldi_hessenberg(matrix),max_iter)
    Q = get_tridiag_form(Q)
    return extract_eigvals(Q)

scales  = ((-2, -1.6), (-1.4, -1), (1.6, 2))

def func(x):
    return ((pow(x,9) + pi)*cos(log(pow(x,2) +1)))/exp(pow(x,2)) - x/2018
    
def derivative(x):
    return x * exp(-x**2)*(cos(log(x**2 +1))*(9*x**7 - 2*(x**9 + pi)) - 2*(x**9 + pi)*sin(log(x**2 +1)) * (x**2 +1)**(-1)) - 1/2018

def draw_function(f, a, b, step):
    x, y = [], []
    i = a
    while i <= b:
        x.append(i)
        y.append(f(i))
        i += step
    x_ticks = []
    i = a
    while i <= b:
        x_ticks.append(i)
        i += 1
    plt.plot(x, y)
    plt.grid(True)
    plt.xticks(x_ticks)
    plt.show()

def bisection(func, scales, eps = 10e-4):
    res = [list(pair) for pair in scales]
    for pair in res:
        while pair[1]-pair[0] > eps:
            mid = (pair[1]+pair[0]) / 2
            if sign(func(mid)) != sign(func(pair[0])): pair[1] = mid
            else: pair[0] = mid
    return res

def discrete_newton(func=func,scales=scales, h = 10e-5, eps = 10e-15):
    res = []
    for pair in scales:
        x0 = pair[1]
        x1 = x0 - (h * func(x0))/(func(h+x0) - func(x0))
        while abs(x1-x0) > eps:
            x0 = x1
            x1 = x0 - (h * func(x0))/(func(h+x0) - func(x0))     
        res.append(x1)
    return res

def improved_newton(roots, func=func, derivative=derivative, eps = 10e-16):
    res=[]    
    for root in roots:
        x, x_prev = root, root + 2*eps
        while abs(x-x_prev) > eps:
            x, x_prev = x-func(x)/derivative(x), x
        res.append(x)
    return res 

























 



