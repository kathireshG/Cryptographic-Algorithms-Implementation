#client
import socket
import hashlib
    
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

# Initialize socket
host = 'localhost'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Receive parameters from the server
data = client_socket.recv(1024).decode()
p, q, g, y, r_, s_ = map(int, data.split(','))
Message_ = client_socket.recv(1024).decode()

print("\nReceived from Server: p,q,g,y,r,s,Message")
print(f"Message: {Message_}\n")


h_m_ = hashlib.sha1(Message_.encode())
h_m_ = int(h_m_.hexdigest(),16)

print("\nVerification: ")
w = mod_inverse(s_,q)
print(f"w: {w}")
u1 = (h_m_*w)%q
print(f"u1: {u1}")
u2 = (r_*w)%q
print(f"u2: {u2}")
v = (((g**u1)*(y**u2))%p)%q
print(f"v: {v}\n")

print(f"r' (from Sender):{r_}")
print(f"v  (Calculated):{v}\n")
if(r_ == v): print("Successful Verified Signature")
else: print("\nIncorrect Signature !!! ")

# Close the connection
client_socket.close()
