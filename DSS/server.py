#server.py
import socket
import random
from Crypto.Util import number
import hashlib

def nth_prime_divisor(p, n):
    count = 0
    num = 2
    while True:
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

# Generate keys and parameters
print("\nGlobal Public key Components: ")
p = number.getPrime(random.randint(512 // 64, 1024 // 64) * 64)
print(f"P (Randomly Generated): {p}")
q = nth_prime_divisor(p,4)
print(f"Q (Randomly Generated): {q}")
g = find_generator(p, q)
print(f"G (Randomly Generated): {g}")


Message = input(str("\nEnter the message : "))
# Message = "Hello"
h_m = hashlib.sha1(Message.encode())
print(f"Hash Value of Message (SHA-I): {h_m.hexdigest()}")
h_m = int(h_m.hexdigest(),16)

#User's private key
x = random.randint(1, q) 
print(f"\nUser's Private Key (X): {x}")

#User's public key
y = (g**x) % p
print(f"User's Public Key (Y): {y}")

#User's Per-Message Secret Number
k = random.randint(1, q) 
print(f"User's Per-Message Secret Number (K): {k}\n")

#Signing
r = ((g**k)%p)%q
k_inverse = mod_inverse(k,q)
s = (k_inverse*(h_m + x*r))%q
print(f"Signature: [r:{r},s:{s}]\n")


#Socket Programming
host = 'localhost'
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print("Server listening...")

conn, addr = server_socket.accept()
print("Connection from:", addr)

# Send parameters to the client
print("Sending to Client: p,q,g,y,r,s,Message")
conn.sendall(f"{p},{q},{g},{y},{r},{s}".encode())

ans=input("\nDo you want to send the correct message? (y/n)")
if(ans == "y"): conn.sendall(Message.encode())
else: conn.sendall((Message+"A").encode())

print("Sent Successfully")
conn.close()
server_socket.close()
