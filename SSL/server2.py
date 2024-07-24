#server
import socket
import ssl

HOST = "localhost"
PORT = 1227

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("ssl.pem","private.key")

with socket.socket(socket.AF_INET,socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST,PORT))
    print('Server is ready.....')
    sock.listen(3)
    with context.wrap_socket(sock,server_side=True) as ssock:
        conn,addr = ssock.accept()
        print(f"Server is connected to {addr}")
        conn.send(bytes("\n\nWelcome to server!!\nKATHIRESH 21BCE6083","utf-8"))
        ssock.close()