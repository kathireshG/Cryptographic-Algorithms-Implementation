import socket
import ssl
import threading

# Server configuration
HOST = 'localhost'
PORT = 12345
CERTFILE = 'server.crt'
KEYFILE = 'server.key'

# Function to handle client connections
def handle_client(conn):
    while True:
        # Receive data from the client
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received from client: {data.decode()}")

        # Send a response back to the client
        response = input("Enter your response: ")
        conn.sendall(response.encode())

    # Close the connection
    conn.close()

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the socket with SSL/TLS
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
server_socket_ssl = context.wrap_socket(server_socket, server_side=True)

# Bind the socket to the address and start listening
server_socket_ssl.bind((HOST, PORT))
server_socket_ssl.listen(5)

print(f"Server listening on {HOST}:{PORT}")

while True:
    # Wait for a connection
    conn, addr = server_socket_ssl.accept()
    print(f"Connection from {addr}")

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(conn,))
    client_thread.start()
