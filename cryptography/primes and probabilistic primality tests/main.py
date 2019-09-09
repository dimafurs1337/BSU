from source import *
from random import randint

sieve = AtkinSieve(200)

def generatePrime(bits=256):
        end = 1 << bits
        q = sieve[random.randint(0,len(sieve))]
        n = 2
        p = q*n + 1
        while p <= end:
                q = p
                n = 2
                p= q*n +1
                while p >= pow(2*q+1,2) or pow(2,q*n,p)!=1 or pow(2,n,p)==1:
                        n += 2
                        p = q*n + 1
        return q


num = probably_prime_num(256)

print("Generated number : ", num)
print("Fermat test           : ", ferma(num))
print("Solovoy-Strassen test : ", solovoy_strassen(num))
print("Miller-Rabin test     : ", miller_rabin(num))

m = generatePrime()
print("\nGenerated number : ", m)
print("Fermat test           : ", ferma(m))
print("Solovoy-Strassen test : ", solovoy_strassen(m))
print("Miller-Rabin test     : ", miller_rabin(m))













