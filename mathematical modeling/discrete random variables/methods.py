import random
import math

def generatePoissonSeq(n ,l):
    seq = [0]*n
    for i in range(n):
        p, x, r = math.exp(-l), 0, random.uniform(0,1)
        r-=p
        while r >= 0:
            x+=1
            p*=l/x
            r-=p
        seq[i]= x
    return seq

def generateBinomialSeq(n, m0, p0):
    seq = [0]*n
    for i in range(n):
        m, p = m0, p0
        q =1-p
        c, r = p/q, random.uniform(0,1)
        p = pow(q,m)
        x=0
        r-=p
        while r >= 0:
            x+=1
            p *= c*(m+1-x)/x
            r-=p
        seq[i]=x
    return seq

def BinomialMean(m, p):
    return m*p

def BinomialVariance(m, p):
    return m*p*(1-p)

def SampleMean(seq,n):
    return sum(seq)/n

def SampleVariance(seq, n):
    return sum(map(lambda x : pow((x - SampleMean(seq,n)),2), seq))/(n-1)
        
def BinomialXi2(seq,n,m,p):
    freq = [0]*(m+1)
    prob = [0]*(m+1)
    for i in seq:
        freq[i]+=1
    for i in range(m+1):
        prob[i] = binomialCoefficient(m,i)*pow(p,i)*pow(1-p,m-i)
    s = 0
    for i in range(m+1):
        s += pow(freq[i]- n * prob[i],2)/(n*prob[i])
    return s

def PoissonXi2(seq,n,l):
    sortedSeq = sorted(seq)
    freq = [0]*(sortedSeq[n-1]+1)
    prob = [0]*(sortedSeq[n-1]+1)
    for i in seq:
       freq[i]+=1
    for i in range(sortedSeq[n-1]+1):
        prob[i] = pow(l,i)*math.exp(-l)/math.factorial(i)
    s = 0
    for i in range(sortedSeq[n-1]+1):
        s += pow(freq[i]-n*prob[i],2)/(n*prob[i])
    return s

def binomialCoefficient(n, k):
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)
    c = 1
    for i in range(k):
        c = c * (n - i) / (i + 1)
    return c
    
    
        


    
