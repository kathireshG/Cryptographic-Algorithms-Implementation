# Server

import socket
import threading

ENCODING = "utf8"
def key_gen(p, q, k):
    alice = (p**k) % q
    return alice

class Server(threading.Thread):
    def run(self):
        count = 0
        spacing = "\t\t\t"
        serverHost = "127.0.0.1"
        serverPort = 12346
        serverAddress = (serverHost, serverPort)

        # open connection
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connection.bind(serverAddress)

        # print("open")
        print("\n")

        while 1:
            # get request from client
            bob_key, clientAddress = connection.recvfrom(1024)
            print("Public key exchange for Key Generation: \n")
            print("Received Public Key of Bob(YD2 - from Attacker): ", bob_key.decode(ENCODING))


            # send response to client
            print("Sending Public key of Alice(YA) to Bob: ", alice_key)
            connection.sendto(alice_key.encode(ENCODING), clientAddress)

            break

        bob_public = int(bob_key)
        K_from_bob = key_gen(bob_public, q, alice_private_key)
        print(f"The Key Calculated by Alice(K2): {K_from_bob}")

        alice_answer, clientAddress = connection.recvfrom(1024)
        print("Calculated K by Bob: ", alice_answer.decode(ENCODING))

        if K_from_bob == int(alice_answer):
            print("Keys generated are Same")


        connection.close()
        print("\nConnection closed")

if __name__ == "__main__":
    p = 23
    print("Prime number P: ", p)
    q = 31
    print("Prime number Q: ", q)
    alice_private_key = int(input("Enter the private key of Alice (XA): "))
    print(f"\nPrivate key of Alice (XA): {alice_private_key}")
    alice = key_gen(p, q, alice_private_key)
    alice_key = str(alice)
    print("Calculated Public key of Alice (YA): ", alice_key)
    server_thread = Server()
    server_thread.start()
