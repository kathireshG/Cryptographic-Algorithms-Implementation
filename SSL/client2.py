#client
import socket
import ssl

domain = "localhost"
port = 1227

def get_message():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations("ssl.pem")
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM, 0)
    c_soc = context.wrap_socket(soc,server_hostname=domain)
    c_soc.connect((domain,port))
    print("Connection Successful")
    msg = c_soc.recv(1024)
    print(msg.decode("utf-8"))
    c_soc.close()

get_message()


# Commands to run in OpenSSL:
# 1. openssl genrsa -aes256 -out private.key 2048
# 2. openssl rsa -in private.key -out private.key
# 3. openssl req -new -x509 -nodes -sha1 -key private.key -out certificate.crt -days 36500
# 4. openssl req -x509 -new -nodes -key private.key -sha1 -days 36500 -out new.pem