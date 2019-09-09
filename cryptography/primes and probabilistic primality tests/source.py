import random
import sys
from eulerlib import numtheory as nt
from eulerlib import prime_numbers as pn
from math import gcd, sqrt

# ------------------------------- GENERATORS and ADDITIONAL FUNCTIONS ------------------------------- #

def is_prime_obvious(n):
    if n % 2 == 0:
        return False
    d = 3
    while d*d <= n and n%d != 0:
        d+=2
    return d*d>n

def set_bit(n, num):
    mask = 1 << num
    return (n | mask)

def rand_num_gen(n):
    x = random.getrandbits(n)
    if x & 1:  
        return set_bit(x, n-1)
    else:
        return set_bit(x+1, n-1)

def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True

def prime_num_generator(bits, k=100):
    n = rand_num_gen(bits)
    primes = AtkinSieve(k)
    for i in primes:
        if n % i == 0:
            return
    while not (miller_rabin(n)):
        n+=2
    return n

def probably_prime_num(n):
    num = prime_num_generator(n)
    while num == None:
        num = prime_num_generator(n)
    return num

# ------------------------------- TESTS ------------------------------- #

def ferma(n,k=100):
    if n==2 or n==3:
        return True
    if not n&1:
        return False
        
    for _ in range(k):
        a = random.randint(2,n-1) 
        if not gcd(a,n):
            return False
        if not pow(a,n-1,n):
            return False
    return True

def miller_rabin(num, k=50):
    if num < 2: 
        return False
    if num == 2 or num == 3:
        return True
    if not num&1: 
        return False
    d = num - 1
    s = 0
    while d % 2 == 0:
        d = d // 2
        s += 1

    for _ in range(k):
        a = random.randint(2, num - 2)
        v = pow(a, d, num)
        if v != 1: 
            i = 0
            while v != (num - 1):
                if i == s - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

def jacobi(a, n): 
    j=1
    while a:
        while a%2==0:
            a = a//2
            if n%8==3 or n%8==5: j=-j
        a,n = n,a
        if a%4==3 and n%4==3: j=-j
        a = a%n
    if n==1:
        return j
    else:
        return 0

def solovoy_strassen(n,k=50):
    for _ in range(k):
        a = random.randint(2,n-1)
        if gcd(a,n) != 1:
            return False
        elif (jacobi(a,n)%n) != pow(a,(n-1)//2,n):
            return False
    return True

def AtkinSieve(nmax):
    is_prime = dict([(i, False) for i in range(5, nmax+1)])
    for x in range(1, int(sqrt(nmax))+1):

        for y in range(1, int(sqrt(nmax))+1):
            n = 4*x**2 + y**2
            if (n <= nmax) and ((n % 12 == 1) or (n % 12 == 5)):
                is_prime[n] = not is_prime[n]
            n = 3*x**2 + y**2

            if (n <= nmax) and (n % 12 == 7):
                is_prime[n] = not is_prime[n]
            n = 3*x**2 - y**2

            if (x > y) and (n <= nmax) and (n % 12 == 11):
                is_prime[n] = not is_prime[n]

    for n in range(5, int(sqrt(nmax))+1):

        if is_prime[n]:
            ik = 1
            while (ik * n**2 <= nmax):
                is_prime[ik * n**2] = False
                ik += 1
    primes = []
    for i in range(nmax + 1):

        if i in [0, 1, 4]: pass
        elif i in [2,3] or is_prime[i]: primes.append(i)
        else: pass
    return primes












   


