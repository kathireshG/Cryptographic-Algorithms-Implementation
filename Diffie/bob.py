# Client

import socket
import threading
import random

ENCODING = "utf8"

def key_gen(p, q, k):
    bob = (p**k) % q
    return bob

class Client(threading.Thread):
    def run(self):
        clientHost = "127.0.0.1"
        clientPort = 12345
        clientAddress = (clientHost, clientPort)

        # open connection
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print("open")



        # send request to server
        print("Sending the Public Key of Bob YB:", bob_key)
        connection.sendto(bob_key.encode(ENCODING), clientAddress)

        # get response from server
        alice_key, clientAddress = connection.recvfrom(1024)
        print("Received the Public Key of Alice Yd1:", alice_key.decode(ENCODING))

        alice_public = int(alice_key)
        K_from_alice = key_gen(alice_public, q, bob_private_key)
        K_from_alice = str(K_from_alice)

        print(f"The Key generated from Alice: {K_from_alice}")

        bob_answer, clientAddress = connection.recvfrom(1024)
        print("Calculated K by Alice: ", bob_answer.decode(ENCODING))

        if int(K_from_alice) == int(bob_answer):
            print("Success")
        # connection.sendto(K_from_alice.encode(ENCODING), clientAddress)

        # close connection
        connection.close()
        print("close")

# Create and start the client thread
if __name__ == "__main__":
    p = 23
    print("Prime number P: ", p)
    q = 31
    print("Prime number Q: ", q)
    bob_private_key = random.randint(1000, 100000)
    print(f"Private key of Bob XB: {bob_private_key}")
    bob = key_gen(p, q, bob_private_key)
    bob_key = str(bob)
    print("Public key of Bob YB: ", bob_key)
    client_thread = Client()
    client_thread.start()
