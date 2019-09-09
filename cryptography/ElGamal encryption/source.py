import hashlib
from math import sqrt, gcd
import random

def xgcd(a, b):
    x, old_x = 0, 1
    y, old_y = 1, 0
    while (b != 0):
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    return a, old_x, old_y

def find_hash(message):
    return hashlib.blake2b(message.encode(),digest_size=4).hexdigest()
    
def generate_possibly_prime(bits=33):
    end = 1 << bits
    sieve = AtkinSieve(200)
    q = sieve[random.randint(0,len(sieve)-1)]
    n = 2
    p = q*n + 1
    while p <= end and p.bit_length() != end.bit_length():
        q = p
        n = 2
        p = q*n +1
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

def generate_p(n_bits=33):
    p = generate_possibly_prime(n_bits)
    while (p.bit_length() != n_bits):
        p = generate_possibly_prime(n_bits)
    if not miller_rabin(p):
        generate_p(n_bits)
    return p
    
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

def find_primitive_root(p):
    p1 = 2
    p2 = (p-1)//p1
    while True:
        g = random.randint(2,p-1)
        if not pow(g, (p-1)//p1, p) == 1:
            if not pow(g,(p-1)//p2,p) == 1:
                return g

def find_k(p,module):
    k = random.randint(2,module-1)
    while gcd(k,module) != 1:
        k = random.randint(2,module-1)
    return k

def make_public_key(pgx):
    p,g,x = pgx
    y = pow(g,x,p)
    return (p,g,y)

def make_private_key():
    p = generate_p()
    g = find_primitive_root(p) 
    x = random.randint(2,p-2)
    return (p,g,x)

def make_sign(message, private_key, module,k):
    #int_m = int(find_hash(message),16)
    int_m = message
    p,g,x = private_key
    #k = find_k(p,module)
    r = pow(g,k,p)
    gcd_a, inverted_k, b_coeff = xgcd(k,module)
    s = ((int_m - x*r)*inverted_k)%(module)
    return (r,s)

def verify_sign(message,public_key,sign):
    p,g,y = public_key
    r,s = sign
    if (not (0 < r < p)) and (not (0 < s < p-1)):
        print("Invalid parameters")
        return False
    #int_m = int(find_hash(message),16)
    int_m = message
    if (pow(y,r,p)*pow(r,s,p))%p == pow(g,int_m,p):
        print("Verified")
        return True
    else:
        print("Not verified")
        return False


'''message = "hello"
private_k = make_private_key()
public_k = make_public_key(private_k)
sign = make_sign(message,private_k)
verify_sign(message,public_k,sign)'''
        


'''p = int(b'1be6817b78f650e924330e88e87eb8ceb34bd34f5e799b6878046c8d313ffc9db5e4523e1d5dcb129f51b235feef82ca7',16)
q = int(b'df340bdbc7b287492198744743f5c6759a5e9a7af3ccdb43c023646989ffe4edaf2291f0eaee5894fa8d91aff77c1653',16)
g = int(b'18b84ce7a6970c4acca5c874c394de03fcbb8f8d1e6e35da60d9f45734d1a94d0c5533bfde99188b88251579038bcf549',16)
m = int(b'661780d92f4a4dd7aa8e7490e129e0947a1fc1a09c4d68a9dbd87398358e535b381d9f9f96a767f547a55e859b030e89',16)
y = int(b'62ef7d618c879e67b79573be87066edaf5c7a3414be9630b74bb63925df44c199af31cbb06c9b89f3ae1c9df9fe2442e',16)
r = int(b'a8284e75ed112b0ff663bc7d008b7701329324891eb67e6232f635e9b89f3a16c8611bdf49b6f157be540b2521be46d6',16)
s = int(b'742f8e001cc640dd73cbc45b2b5b3f936d56f227fa3844b1c70145f18a9feeee42811b904772e49fe6707ef3743ebebc',16)'''

'''sign = (r,s)
pgy = (p,g,y)
verify_sign(m,pgy,sign)'''

# 1 - нет
# 2 - да 
# 3 - да 
# 4 -

'''
p = int(b'3f780bb568ff38af4d67cb4273c0563ea76f3d1331d710b863cfb808f4bd26b1c75553d2d67ca93089d9ad3797146ea9ea4020136ac0bb901b0ccc27ae9a4f75e34f53f93ebd9181d7868b35494aaa9ee39529f05f09c4b08b1276e74154d0a5c4c75bc3831f579bc25b5fc7e02dc087bb180fca36dbea9ed6f346808c84da98ba06f11f6afc0034f83aeaa6bbfbe65fe8c8ff00bd6fede64e8e65bdccd36fb82f58fe65',16)
q = int(b'551df10647e4f6e59e13b88b49bc3bcbcb7a05a85c8357fa1',16)
g = int(b'1c1541e4fad5e972932686429429e82991fd8d6f96882fdace0999481b9be129137ce0fe16dbae724d86d5d4e07a0ddf31d73e33dd3ea7bb77563c9af4e620d813d6375dcd768ed4cc81b76c478bad8a9a576f899dac2288f7c4d009bacc3b402be1233dc864a93f03299d1a763149797668800bee2c40681135250def42d72eba3c298a773d06a2eab650d887f48c54ed50eddfa938f3ae6409ab60668d77b6325b1b16',16)
m = int(b'35f42ac2c91f3bd0d479c4b33b8310cbf7ec9f7df62b617b8',16)
y = int(b'1883c237f99fe3ea94cc2111a18e0ac95589529147637c74a820ac9f00c794c54d6b4921e13de6c4d06a860c36202c62e0ab4eedc077a4f12eb015363c9789baa5c740761ae770e04c33f5bb13d3cfbd5d0b1fa30ba5aff461497df8773ee2d9df0e46af7ef59106f034e37924351d3caa7b4faab5fc00ad1d6083a072781f7dac8a10a047f84d13fd75e03cb44b090cbafe1407853dbf912b7f50573016f7a29358051f',16)
r = int(b'33eace592a534c1afbe5370054756b9983e807ae8e011ae785f18f841c83788663c18bfd282da805c246fded58e1f2a3969b80d97ce77e709cd417567242636f6e2f46fe38d7ad48061510007de6cdd0b0ec7a9e3c26cebe041d3ab48540e4adc588942c6957d96896e57c61fbae30a175c3554b052ef30872eea2bde08d56ec630738cd0e3ac7de90f2cc5d446f07ba126ef28554a772dc360b9ae93184ae3982cbc36b',16)
s = int(b'3cd9a118c88ac39091f9091f8555be14949769abadac4d7a7',16)

sign = (r,s)
pgy = (p,g,y)
verify_sign(m,pgy,sign)'''


'''p = int(b'3fa56c30e17380b914311610ba49b534541bdc553b705c0ba9fa3d6a010f09f60b39bfe4dc024c06207d792a2b931db16c7e617bb66c678d2129f8e792ef42c82e923c36850f3afce330d57e3a2bbf7c996dafba241c270e04b9474883566e32a288aeef2de0998b45b0850a0aa6ed2dfdebeb42dda90a1e3ce44de7bc3814aabcfaa5bc0882b3469a6bb7bf23e0dc04f286a98c17d2ba36f161e8739deafec1a0a28585',16)
q = int(b'7f2f27e03f7759465ad794dd78e6e7dd972da515c3c805b29',16)
g = int(b'36d4c1d76f7dd4f0e1c535de62492dc9faef1fe4dce81c5b92e7c6bcd6550c318c4c6c3f0b15be5a85d543a5efa816aafa7812c156109655e890660499039e73b5f05e030770fb578f16f6becb9e5451819fa8e8434f965fb8440a7a3ba8b2e7874351fb96c8bf0ccfb354cac6b06a95e04efb2da1621b8f183b01042568de7b62333fc3286748252a83e81c49b585f6388ca3c2577946ddad7b73643052fa73ab1710af',16)
m = int(b'6463c01b362eefdc6af44add21c0a34d91e7c96dea146704d',16)
y = int(b'1babfddda960d21ad37cdfff4dd08756a4294c2b8d202d54abf01c777d8c7c70be050d543d46e49bd82c0a7367a7c549ed1855f3e7075bfff9182aa3e178d0785620e4a03ace3fa91d236904fef75275fd33e387428e7d350c38001a4d956e4ce925159529f2d445311c2838e389b23f7d12261fe4d4c84ba840c07e70d1403a238fe39917c63cf569c38db88da6cc1532d6235140644d6ddd40195e5abb15a2f9ba9924',16)
r = int(b'94e619f0e3da8dbc7d2866528ca93cddf4d1de971279867b28b857de495b8a6f175025fc96d94317d3d1842975ab6cadf71d7ecc960fa2e82a4a4780a83711f50ee4df1b6d730208e743299d47c5eb28c4a6699a8f2abd58aa455e13f9730d472f2f563f03f13658c950576416df7b0b10059f8185295c68f3d25c7c4b82e548096e9f834c9998e3f04cb9a77b602f0e73cb6420e4233a229040055a87cffa25d4ee36',16)
s = int(b'2bc0c443eb69f395abe9e14e3774087bc19c73ea15634587a',16)

sign = (r,s)
pgy = (p,g,y)
verify_sign(m,pgy,sign)'''


p = int(b'2a23f8981dad2d735317ade6369b601455d8183ffe43b76aebaec2eec1a13d0608b9ef009b50f725de63e9419b6afa099c995be79e4f9b84100150f5a88d3c447cb8b6be4b9f930323da2fe00492c30c12f451b73132d2a80a78850ecb262d50c689a2f8e22c5778e02a3ecfc3f52bfd41190570949ba08edb274ddc45af78169c8d9a274bc681ff244eadd85f4e9268eb825f051bf1206d96b09164a123cffb13b623a7',16)
q = int(b'503785568f0489f6e2ac2188af5d6f560689848ba404fd53f',16)
g = int(b'164acb0c59999a9803a64553bcea558ae9f20bebebb505685d4c0882bb223475d387848a78b190ca798a9b482f1e25ff2e8c25176c59025ce934a244776a84e28933492fb068e02a5c6dd712f2a3f40edf6b7bf5291e0cd7b90172b929eb2b54d7ddc27dbf156cff6bc342ba968b8487da1d439cd5158c4241c772006858b1a2dc935dd433bdc0c0fa2d781910a50feaf6a916ab2333b8f2899a73624427edf187b6db3f',16)
m = int(b'5b261d76eebd4aa2cc805d4514aaae732414e2db63bcf444',16)

x = int(b'13aacf80282179f083f1b05d51be89e326ad463d2321b1e38',16)
k = int(b'1f6ac1ca74d82c372ed0bdd72d77a6636a0fe23fc4429bd00',16)

pgx = p,g,x
sign = make_sign(m,pgx,q,k)
print(sign[0])


