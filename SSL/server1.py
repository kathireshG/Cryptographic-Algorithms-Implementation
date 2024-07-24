import socket
import ssl

HOST = '127.0.0.1'
PORT = 12345
CERTFILE = 'cert.pem'
KEYFILE = 'key.pem'

def echo_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable outdated protocols

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)

        with context.wrap_socket(sock, server_side=True) as ssock:
            print("Server listening on {}:{}".format(HOST, PORT))
            conn, addr = ssock.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

if __name__ == "__main__":
    echo_server()
