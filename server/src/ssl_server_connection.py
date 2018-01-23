import socket
import ssl
import os

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
certfile = os.path.join("..", "config", "cert.pem")
keyfile = os.path.join("..", "config", "key.pem")
context.load_cert_chain(certfile=certfile, keyfile=keyfile)

bindsocket = socket.socket()
bindsocket.bind(("127.0.0.1", 10023))
bindsocket.listen(5)


def do_something(connstream, data):
    connstream.sendall(data)
    print(data)
    return False


def deal_with_client(connstream):
    data = connstream.recv(1024)
    # empty data means the client is finished with us
    while data:
        if not do_something(connstream, data):
            # we'll assume do_something returns False
            # when we're finished with client
            break
        data = connstream.recv(1024)
    # finished with client


while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket, server_side=True)
    try:
        deal_with_client(connstream)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
