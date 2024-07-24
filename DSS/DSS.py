import binascii
import random
from Crypto.Util import number
# from sympy import primefactors
# from sympy import mod_inverse
import hashlib

def nth_prime_divisor(p, n):
    count = 0
    num = 2
    while True:
        # if is_prime(num):
        if number.isPrime(num):
            if (p - 1) % num == 0:
                count += 1
                if count == n:
                    return num
        num += 1

def find_generator(p, q):
    h = number.getRandomRange(2, p - 1)    
    exp = (p - 1) // q
    g = pow(h, exp, p)
    if g > 1:
        return g
    else:
        return None
    
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b, a % b)
        return d, y, x - (a // b) * y

def mod_inverse(a, m):
    d, x, y = extended_gcd(a, m)
    if d != 1:
        raise ValueError("The modular inverse does not exist")
    return x % m


p = number.getPrime(random.randint(512 // 64, 1024 // 64) * 64)
print(f"P (random): {p}")
q = nth_prime_divisor(p,4)
print(f"Q (random): {q}")
g = find_generator(p, q)
print(f"G (random): {g}")

# Message = input(str("Enter the message : "))
Message = "Hello"
h_m = hashlib.sha1(Message.encode())
h_m = int(h_m.hexdigest(),16)

#User's private key
x = random.randint(1, q) 
print(f"User's Private Key (X): {x}")

#User's public key
y = (g**x) % p
print(f"User's Public Key (Y): {y}")

#User's Per-Message Secret Number
k = random.randint(1, q) 
print(f"User's Per-Message Secret Number (K): {k}")

#Signing
r = ((g**k)%p)%q
k_inverse = mod_inverse(k,q)
s = (k_inverse*(h_m + x*r))%q

print(f"Signature: [{r},{s}]")

#Receiver Side
r_ = r
s_ = s
Message_ = Message
h_m_ = hashlib.sha1(Message_.encode())
h_m_ = int(h_m_.hexdigest(),16)

w = mod_inverse(s_,q)
u1 = (h_m_*w)%q
u2 = (r_*w)%q
v = (((g**u1)*(y**u2))%p)%q


if(r_ == v): print("Successful Verified Signature")



