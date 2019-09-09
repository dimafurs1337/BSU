from rsa import *

s = "message "*100
k = generate_keys(generate_pq(200))
enc = encrypt_str(s,k[0])
dec = decrypt_str(enc,k[1])
print("decrypted msg: ", dec)