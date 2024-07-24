import random
from Crypto.Util import number

def encrypt(message, public_key):
    e, n = public_key
    cipher_text = pow(message, e, n)
    return cipher_text

def decrypt(cipher_text, private_key):
    d, n = private_key
    decrypted_message = pow(cipher_text, d, n)
    return decrypted_message

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



p = number.getPrime(1024)
q = number.getPrime(1024)
print(f"The value of P: {p}\n\nThe value of Q: {q}")
n = p * q
phi_n = (p - 1) * (q - 1)
# e = int(input(f"Enter the value of E (Make sure E is between (1, {phi_n})): "))
e = 65537
d = mod_inverse(e, phi_n)
print(f"d: {d}")

# Public and private keys
public_key = (e, n)
private_key = (d, n)

# Encryption and Decryption
message = int(input(f"Enter the message: "))
cipher_text = encrypt(message, public_key)
decrypted_message = decrypt(cipher_text, private_key)

# Display results
# print("Public key:", public_key)
# print("Private key:", private_key)
print("\nOriginal Message:", message)
print("\nEncrypted Message (Cipher Text):", cipher_text)
print("\n\nDecrypted Message:", decrypted_message)


