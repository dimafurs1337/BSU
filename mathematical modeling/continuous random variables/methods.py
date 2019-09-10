import random
from math import tan, pi, log, floor, atan, exp, erf, atan, sqrt

# --------------------------------------- Sample Mean, Sample Variance ---------------------------------------- #

def SampleMean(seq):
    return sum(seq)/len(seq)

def SampleVariance(seq):
    n = len(seq)
    return sum(map(lambda x : pow((x - SampleMean(seq)),2), seq))/(n-1)

# ---- Normal distribution N(m,s) where m = Mean, s**2 = Variance ---- #

def NormFunc(x,m,s):
    return 0.5*(1+erf((x-m)/(sqrt(2)*s)))

def generateNormSeq(n,m,s):
    seq = [0]*n
    k1, k2 = sqrt(12/n), n/2
    for i in range(n):
        seq[i] = m + s*k1*(sum([random.uniform(0,1) for _ in range(n)])-k2)
    return seq

# ---- Cauchy distribution C(a,b), Mean - undefined , Variance - undefined ---- #

def CauchyFunc(x,a,b):
    return 0.5 + atan((x-a)/b)/pi

def generateCauchySeq(n,a,b):
    seq = [0]*n
    for i in range(n):
        seq[i]= a + b*tan(2*pi*random.uniform(0,1))
    return seq

# ---- Laplace distribution L(a,b), Mean - b , Variance - 2/a**2 ---- #

def LaplaceFunc(x,a,b):
    if x<=a:
        return 0.5*exp(b*(x-a))
    return 1 - 0.5*exp(-b*(x-a))

def generateLaplaceSeq(n,a,b):
    seq = [0]*n
    k = random.uniform(0,1)
    for i in range(n):
        r = random.uniform(0,1)
        seq[i] = a + (1/b)*log(k/r)
        k = r
    return seq

# -------------------- Criterias -------------------- #

def Kolmogorov(seq,func,*args):
    sortedSeq = sorted(seq)
    n = len(seq)
    D = 0
    for i in range(n):
        if D < abs((i + 1) / n - func(sortedSeq[i],*args)):
            D = abs((i + 1) / n - func(sortedSeq[i],*args))
    return sqrt(n)*D

def Pirson(seq,n,func, *args):
    begin, end = min(seq), max(seq)
    dist = end-begin
    freq = [0]*(n+1)
    prob = [0]*(n+1)
    res = 0
    diff = dist/n
    
    for i in range(len(seq)):
	    freq[int((abs(seq[i]-begin)/dist)*n)]+=1
    
    for i in range(n+1):
        prob[i]= func(begin+diff*(i+1),*args) - func(begin+diff*i,*args)
        res += pow(freq[i]-len(seq)*prob[i],2)/(len(seq)*prob[i])
    return res
    
