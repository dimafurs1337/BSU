from math import sqrt, floor, gcd
import random

def generate_prime(bits=256):
    end = 1 << bits
    sieve = AtkinSieve(200)
    q = sieve[random.randint(0,len(sieve)-1)]
    n = 2
    p = q*n + 1
    while p <= end and p.bit_length() != end.bit_length():
        q = p
        n = 2
        p= q*n +1
        while p >= pow(2*q+1,2) or pow(2,q*n,p)!=1 or pow(2,n,p)==1:
            n += 2
            p = q*n + 1
    return q

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

def generate_primes_file(filename,power):
    l = AtkinSieve(2**(power+1))
    j=0
    with open(filename,"w") as fout:
        for i in l:
            if i > 2**power:
                j+=1
                fout.write(str(i)+"\n")
    return j

def choose_pq_from_file(primes_file,size):
    indP = random.randint(0,size-1)
    indQ = random.randint(0,indP-1) if indP > int(size/2) else random.randint(indP+1, size-1)
    with open(primes_file,"r") as fin:
        primes = fin.readlines()
        p = int(primes[indP].rstrip("\n"))
        q = int(primes[indQ].rstrip("\n"))
    return (p,q)

def generate_pq(n_bits):
    p = generate_prime(n_bits)
    while p.bit_length() != n_bits and (not miller_rabin(p)) :
        p = generate_prime(n_bits)
    q = generate_prime(n_bits)
    while q.bit_length() != n_bits and (not miller_rabin(q)):
        q = generate_prime(n_bits)
    return (p,q)

def miller_rabin(num, k=200):
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

def xgcd(a, b):
    x, old_x = 0, 1
    y, old_y = 1, 0
    while (b != 0):
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    return a, old_x, old_y

def generate_keys(pq):
    (p,q) = pq
    n = p*q
    phi = (p-1)*(q-1)
    while True:
        e = random.randint(2,phi)
        if gcd(e,phi) == 1: break
    _gcd, d, y = xgcd(e,phi)
    if d < 0: d+=phi
    return ((e,n),(d,n))
    
def encrypt_by_symbol(message,public_key):
    (e,n) = public_key
    return [(ord(ch)**e)%n for ch in message]

def decrypt_by_symbol(message,private_key):
    (d,n) = private_key
    return "".join([chr((ch**d)%n) for ch in message])

def encrypt(num, public_key):
    (e,n) = public_key
    return pow(num,e,n)

def decrypt(num, private_key):
    (d,n) = private_key
    return pow(num,d,n)

def string_to_bits(_str):
    return "".join((bin(ord(c))[2:]).zfill(8) for c in _str)

def string_from_bits(bin_str):
    return "".join(chr(int(bin_str[i:i+8],2)) for i in range(0, len(bin_str)-7, 8))

def encrypt_str(message, public_key):
    (e,n) = public_key
    res = ""
    bin_str = string_to_bits(message)
    bin_str += "1"
    while len(bin_str) % (n.bit_length()-1) != 0:
        bin_str += "0"
    for i in range(0,len(bin_str),n.bit_length()-1):
        enc_i = pow(int(bin_str[i:i+n.bit_length()-1],2),e,n)
        bin_i = format(enc_i, 'b').zfill(n.bit_length())
        res += bin_i
    return res

def decrypt_str(message, private_key):
    (d,n) = private_key
    bin_str = ""    
    for i in range(0,len(message),n.bit_length()):
        num = int(message[i:i+n.bit_length()],2)
        dec_num = pow(num,d,n)
        bin_str += format(dec_num, 'b').zfill(n.bit_length()-1)  
    return string_from_bits(bin_str[:bin_str.rfind("1")])

def is_prime(n):
    if n % 2 == 0:
        return False
    d = 3
    while d*d <= n and n%d != 0:
        d+=2
    return d*d>n

    

 