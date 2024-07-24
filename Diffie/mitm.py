# Attacker

import socket
import threading
import random

ENCODING = "utf8"

def key_gen(p, q, k):
    ans = (p**k) % q
    return ans

class Attacker(threading.Thread):
    def run(self):
        spacing = "            "
        clientHost = "127.0.0.1"
        clientPort = 12345
        clientAddress = (clientHost, clientPort)

        # open connection
        clientConnection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientConnection.bind(clientAddress)

        serverHost = "127.0.0.1"
        serverPort = 12346
        serverAddress = (serverHost, serverPort)

        # open connection
        serverConnection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print("open")

        while 1:
            # get request from bob
            clientRequestData, clientAddress = clientConnection.recvfrom(1024)
            print("Receiving from Bob YB:", clientRequestData.decode(ENCODING))
            public_key_bob = int(clientRequestData.decode(ENCODING))
            # print("YB", public_key_bob)

            # modify request 
            serverRequestData = str(key_gen(p, q, xd_bob))
            K_from_bob = str(key_gen(public_key_bob, q, xd_alice))

            #p = 23; q = 31; xd_alice = 40
            #p = 23; q = 31; xd_bob = 50

            # send request to alice
            print("Sending to Alice YD2:", serverRequestData)
            serverConnection.sendto(serverRequestData.encode(ENCODING), serverAddress)

            # get response from alice
            serverResponseData, serverAddress = serverConnection.recvfrom(1024)
            print("Receiving from Alice YA:", serverResponseData.decode(ENCODING))
            public_key_alice = int(serverResponseData.decode(ENCODING))
            # print("YA", public_key_alice)


            # modify response 
            clientResponseData = str(key_gen(p, q, xd_alice))

            K_from_alice = str(key_gen(public_key_alice, q, xd_bob))

            # send response to bob
            print("Sending to Bob YD1:", clientResponseData)
            clientConnection.sendto(clientResponseData.encode(ENCODING), clientAddress)

            # send request to alice
            print("Sending the calculated K to Alice:", K_from_alice)
            serverConnection.sendto(K_from_alice.encode(ENCODING), serverAddress)

            # send response to bob
            print("Sending the calculated K to Bob:", K_from_bob)
            clientConnection.sendto(K_from_bob.encode(ENCODING), clientAddress)


            # if clientResponseData.decode(ENCODING) == "1":
            break
            

        # close connection
        serverConnection.close()
        clientConnection.close()
        print("close")

# Create and start the attacker thread
if __name__ == "__main__":
    p = 23
    print("Prime number P: ", p)
    q = 31
    print("Prime number Q: ", q)


    #Assumed private key of attacker
    xd_alice = random.randint(1000, 100000)
    print("Random private key of Alice XD1: ", xd_alice)

    xd_bob = random.randint(1000, 100000)
    print("Random private key of Bob XD2: ", xd_bob)
    attacker_thread = Attacker()
    attacker_thread.start()
