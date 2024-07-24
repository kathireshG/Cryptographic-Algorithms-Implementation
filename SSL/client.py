import socket
import ssl
import threading

# Server configuration
HOST = 'localhost'
PORT = 12345

# Function to handle receiving messages from the server
def receive_messages(ssl_socket):
    while True:
        data = ssl_socket.recv(1024)
        if not data:
            break
        print(f"Received from server: {data.decode()}")

# Wrap the socket with SSL/TLS
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=HOST)

# Connect to the server
ssl_socket.connect((HOST, PORT))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(ssl_socket,))
receive_thread.start()

# Send messages to the server
while True:
    message = input("Enter your message: ")
    ssl_socket.sendall(message.encode())
