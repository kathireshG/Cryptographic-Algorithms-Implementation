import socket
import ssl

HOST = '127.0.0.1'
PORT = 12345
CERTFILE = 'cert.pem'

def echo_client():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(CERTFILE)

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            message = "Hello, server!"
            ssock.sendall(message.encode())
            data = ssock.recv(1024)
            print('Received:', data.decode())

if __name__ == "__main__":
    echo_client()
