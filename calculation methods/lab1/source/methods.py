import random as rand
from copy import deepcopy
import time
from math import sqrt

def generate_matrix(n, _range):
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(0,n):
        for j in range(i+1,n):
            matrix[i][j] = rand.uniform(-pow(2,_range/4),pow(2,_range/4))
            matrix[j][i] = matrix[i][j]
        matrix[i][i] = sum(abs(matrix[i][j]) for j in range(n))
    return matrix
    
def generate_vector(n, _range):
    return [rand.uniform(-pow(2,_range/4),pow(2,_range/4)) for _ in range(n)]

def l_norm(matrix):
    return max(sum(abs(matrix[i][j]) for j in range(len(matrix))) for i in range(len(matrix)))

def square_norm(vector):
    return sqrt(sum(elem**2 for elem in vector)) 

def max_norm(vector):
    return max(abs(elem) for elem in vector)

def multiplication(matrix, vector):
    return [sum(matrix[i][j]*vector[j] for j in range(len(vector))) for i in range(len(matrix))]

def matrix_multiplication(matrix1, matrix2):
    n = len(matrix1)
    m = len(matrix1[0])
    p = len(matrix2[0])
    return [[sum(x * y for x, y in zip(matrix1_r, matrix2_c)) for matrix2_c in zip(*matrix2)] for matrix1_r in matrix1]

def sign(x): return 1 if x > 0 else -1

def substract_vectors(a,b):
    return [a[i]-b[i] for i in range(len(a))]

def gauss_jordan(matrix):
    h, w = len(matrix), len(matrix[0])
    for y in range(0,h):
        maxrow = y
        for y2 in range(y+1, h):
            if abs(matrix[y2][y]) > abs(matrix[maxrow][y]):
                maxrow = y2
        matrix[y], matrix[maxrow] = matrix[maxrow], matrix[y]
        for y2 in range(y+1, h): 
            c = matrix[y2][y] / matrix[y][y]
            for x in range(y, w):
                matrix[y2][x] -= matrix[y][x] * c
    for y in range(h-1, 0-1, -1):
        c  = matrix[y][y]
        for y2 in range(0,y):
            for x in range(w-1, y-1, -1):
                matrix[y2][x] -=  matrix[y][x] * matrix[y2][y] / c
        matrix[y][y] /= c
        for x in range(h, w):     
            matrix[y][x] /= c
    return matrix

def inv(matrix):
    m2 = [row[:]+[float(int(i==j)) for j in range(len(matrix))] for i,row in enumerate(matrix)]
    m2 = gauss_jordan(m2)
    return [row[len(matrix[0]):] for row in m2]

def condition_number(matrix):
    return l_norm(matrix) * l_norm(inv(matrix))

def gauss(matrix, vector):
    m2 = [row[:]+ [vector[i]] for i,row in enumerate(matrix)]
    m2 = gauss_jordan(m2)
    return [row[len(vector)] for row in m2]

def gauss_max_element(matrix, vector):
    n = len(vector)
    m2 = [row[:]+ [vector[i]] for i,row in enumerate(matrix)]
    permutation = [i for i in range(n)]
    maxrow = 0
    maxcolumn = 0
    for k in range(n-1):
        maxrow = k
        maxcolumn = k
        for i in range(k,n):
            for j in range(k,n):
                if abs(m2[i][j]) > abs(m2[maxrow][maxcolumn]): 
                    maxrow = i 
                    maxcolumn = j
        permutation[maxcolumn], permutation[k] = permutation[k], permutation[maxcolumn]
        m2[maxrow], m2[k] = m2[k], m2[maxrow]
        for l in range(n):
            m2[l][k], m2[l][maxcolumn] = m2[l][maxcolumn], m2[l][k]
        for _i in range(k+1,n):
            b = m2[_i][n] - (m2[_i][k]/m2[k][k])*m2[k][n]
            m2[_i] = [0 for _ in range(k+1)] + [m2[_i][p] - (m2[_i][k]/m2[k][k])*m2[k][p] for p in range(k+1,n)]
            m2[_i] += [b]
    res = [0]*n
    res[n-1] = m2[n-1][n] / m2[n-1][n-1]
    for i_ in range(n-2,-1,-1):
        res[i_] = (1/m2[i_][i_])*(m2[i_][n] - sum(m2[i_][j]*res[j] for j in range(i_+1,n)))
    return [res[permutation.index(ind)] for ind in range(n)]

def lup(matrix, vector):
    n = len(matrix)
    m2 = deepcopy(matrix)
    y = [0]*n
    res = [0]*n
    maxrow = 0
    for k in range(n-1):
        for ind in range(k,n):
            if abs(m2[ind][k]) > abs(m2[maxrow][k]):
                maxrow = ind
        m2[maxrow], m2[k] = m2[k], m2[maxrow]
        vector[maxrow], vector[k] = vector[k], vector[maxrow]
        for i in range(k+1,n):
            m2[i][k] /= m2[k][k]
            for j in range(k+1,n):
                m2[i][j] -= m2[i][k]*m2[k][j]
    y[0] = vector[0]
    for i_ in range(1,n):
        y[i_] = (vector[i_] - sum(m2[i_][j]*y[j] for j in range(i_)))
    res[n-1] = y[n-1] / m2[n-1][n-1]
    for i_ in range(n-2,-1,-1):
        res[i_] = (1/m2[i_][i_])*(y[i_] - sum(m2[i_][j]*res[j] for j in range(i_+1,n)))
    return res

def cholesky_decomposition(matrix, vector):
    n = len(vector)
    x,y,d = [0]*n, [0]*n,[0]*n
    s = [[0 for _ in range(n)] for _ in range(n)]
    d[0] = sign(matrix[0][0])
    s[0][0] = sqrt(abs(matrix[0][0]))

    for j in range(1,n):
        s[0][j] = matrix[0][j] / (s[0][0] * d[0])
    for i in range(1,n):
        Sum = 0
        for k in range(i):
            Sum += s[k][i] * s[k][i] * d[k]
        d[i] = sign(matrix[i][i] - Sum)
        s[i][i] = (abs(matrix[i][i] - Sum))**0.5
        l = 1/(s[i][i]*d[i])
        
        for j in range(i+1,n):
            SDSsum = 0
            for k in range(i):
                SDSsum += s[k][i] * d[k] * s[k][j]
            s[i][j] = l * (matrix[i][j] - SDSsum)
    
    y[0] = vector[0] / (s[0][0]*d[0])
    for i in range(1,n):
        ssum = 0
        for j in range(i):
            ssum += s[j][i] *d[j] * y[j]
        y[i] = (vector[i] -ssum) / (s[i][i]* d[i])
  
    x[n-1] = y[n-1] / s[n-1][n-1]
    for i in range(n-2,-1,-1):
        Ssum = 0
        for k in range(i+1,n):
            Ssum += s[i][k]*x[k]
        x[i] = (y[i]-Ssum)/s[i][i]
    return x

def relaxation(matrix, vector, w=1.5, e = 10**(-12)):
    f = vector[:]
    n = len(vector)
    while True:
        fprev = f[:]
        for i in range(n):
            delta = 0
            for j in range(n):
                if i != j :
                    delta = delta + matrix[i][j]*f[j]
            f[i] = (1-w)*f[i] + (w/matrix[i][i])*(vector[i]-delta)
        if max_norm(substract_vectors(fprev,f)) < e: break
    return f

def qr_decomposition(matrix,b):
    n = len(b)
    a = deepcopy(matrix)
    d = [0]*n
    y = b[:]
    for j in range(n):
        s=0
        for i in range(j,n):
            s = s + pow(a[i][j],2)
        s = sqrt(s)
        d[j] = s
        a[j][j] = a[j][j] - d[j]
        s=0
        for i in range(j,n):
            s = s+pow(a[i][j],2)
        s = sqrt(s)
        for k in range(j,n):
            a[k][j] = a[k][j] / s
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
    
    for j in range(n):
        s = 0
        for k in range(j,n):
            s = s + a[k][j] * y[k]
        for k in range(j,n):
            y[k] = y[k] - 2*s*a[k][j]
    res = [0]*n
    res[n-1] = y[n-1] / R[n-1][n-1]
    for i in range(n-2,-1,-1):
        res[i] = (1/R[i][i])*(y[i] - sum(R[i][j]*res[j] for j in range(i+1,n)))
    return res
    
def least_squares(full_matrix, b, N, coeff=1, begin=0):
    columns = 20*N
    columns = int(columns/coeff)
    A = [row[begin:columns] for row in full_matrix]
    transponeA = [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
    aTa = matrix_multiplication(transponeA,A)
    aTb = multiplication(transponeA,b)
    return gauss_max_element(aTa,aTb)

def gmres(a,b):
    n = len(b)
    K = [[0 for _ in range(n)] for _ in range(n)] 
    for i in range(n):
        K[i][0] = b[i]
    numIter = 1
    while numIter < n:
        for i in range(n):
            s = 0
            for j in range(n):
                s += a[i][j] * K[j][numIter-1]
            K[i][numIter] = s
        numIter += 1 
        y = least_squares(K,b,numIter,coeff=20,begin=1)
        x = [0]*n
        for i in range(n):
            s = 0
            for j in range(numIter-1):
                s += K[i][j] * y[j]
            x[i] = s
        if square_norm(substract_vectors(multiplication(a,x),b)) < 10**(-2): break
    return x

def gmres_arnoldi(a,b):
    n = len(b)
    Q = [[0 for _ in range(n)] for _ in range(n)] 
    AQ  =[[0 for _ in range(n)] for _ in range(n)]
    h = [[0 for _ in range(n)] for _ in range(n)]

    b_norm = square_norm(b)
    for i in range(n):
        Q[i][0] = b[i]/b_norm
    numIter = 1

    while numIter < n:
        for i in range(n):
            s = 0
            for j in range(n):
                s += a[i][j] * Q[j][numIter-1]
            AQ[i][numIter-1] = s
        
        y = least_squares(AQ, b, numIter,coeff=20,begin=0)
        x = [0]*n
        for i in range(n):
            s = 0
            for j in range(numIter):
                s += Q[i][j] * y[j]
            x[i] = s
    
        if square_norm(substract_vectors(multiplication(a,x),b)) < 10**(-10): break 
        z = [0]*n
        for i in range(n):
            s=0
            for j in range(n):
                s += a[i][j]*Q[j][numIter-1]
            z[i] = s

        for i in range(numIter):
            h[i][numIter-1] = sum(z[t]*Q[t][i] for t in range(n))
            z = substract_vectors(z,[h[i][numIter-1]*Q[t][i] for t in range(n)])
        h[numIter][numIter-1] = square_norm(z)
        if h[numIter][numIter-1] == 0: return x
        
        
        for i in range(n):
            Q[i][numIter] = z[i] / h[numIter][numIter-1]
        numIter += 1 
    return x

def lup_build(matrix, vector):
    n = len(matrix)
    m2 = deepcopy(matrix)
    maxrow = 0
    for k in range(n-1):
        for ind in range(k,n):
            if abs(m2[ind][k]) > abs(m2[maxrow][k]):
                maxrow = ind
        m2[maxrow], m2[k] = m2[k], m2[maxrow]
        vector[maxrow], vector[k] = vector[k], vector[maxrow]
        for i in range(k+1,n):
            m2[i][k] /= m2[k][k]
            for j in range(k+1,n):
                m2[i][j] -= m2[i][k]*m2[k][j]
    return (m2, vector)

def lup_solve(params):
    m2, vector = params[0], params[1]
    n= len(vector)
    y = [0]*n
    res = [0]*n
    y[0] = vector[0]
    for i_ in range(1,n):
        y[i_] = (vector[i_] - sum(m2[i_][j]*y[j] for j in range(i_)))
    res[n-1] = y[n-1] / m2[n-1][n-1]
    for i_ in range(n-2,-1,-1):
        res[i_] = (1/m2[i_][i_])*(y[i_] - sum(m2[i_][j]*res[j] for j in range(i_+1,n)))
    return res

def least_sq_tuple(full_matrix, b, N, coeff=1, begin=0):
    columns = 20*N
    columns = int(columns/coeff)
    A = [row[begin:columns] for row in full_matrix]
    transponeA = [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
    aTa = matrix_multiplication(transponeA,A)
    aTb = multiplication(transponeA,b)
    return (gauss_max_element(aTa,aTb),A,b)

def least_sq_custom(params):
    y,A,b = params[0],params[1],params[2]
    return square_norm(substract_vectors(multiplication(A,y),b))
    
def least_squares_arnoldi(full_matrix, b, rows, columns):
    A = [full_matrix[i][:columns] for i in range(rows)]
    b = b[:columns]
    transponeA = [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
    aTa = matrix_multiplication(transponeA,A)
    aTb = multiplication(transponeA,b)
    return gauss_max_element(aTa,aTb)

def arnoldi_multiplication(matrix, vector, rows, columns):
    return [sum(matrix[i][j]*vector[j] for j in range(columns)) for i in range(rows)]

def gmres_arnoldi_modified(a,b):
    n = len(b)
    Q = [[0 for _ in range(n)] for _ in range(n)] 
    AQ  =[[0 for _ in range(n)] for _ in range(n)]
    h = [[0 for _ in range(n)] for _ in range(n)]

    b_norm = square_norm(b)
    for i in range(n):
        Q[i][0] = b[i]/b_norm
    numIter = 1
    d = [0]*n
    d[0] = b_norm

    while numIter < n:

        z = [0]*n
        for i in range(n):
            s=0
            for j in range(n):
                s += a[i][j]*Q[j][numIter-1]
            z[i] = s

        for i in range(numIter):
            h[i][numIter-1] = sum(z[t]*Q[t][i] for t in range(n))
            z = substract_vectors(z,[h[i][numIter-1]*Q[t][i] for t in range(n)])
        h[numIter][numIter-1] = square_norm(z)
        if h[numIter][numIter-1] < 10**(-10): break

        for i in range(n):
            Q[i][numIter] = z[i] / h[numIter][numIter-1]
        
        y = least_squares_arnoldi(h, d, numIter+1, numIter)
        if square_norm(substract_vectors(arnoldi_multiplication(h,y,numIter+1,numIter),d)) < 10**(-10):break
        
        numIter += 1 
    return arnoldi_multiplication(Q, y, n,numIter)
