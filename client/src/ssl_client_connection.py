import socket
import ssl
import os

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations(os.path.join("..", "config", "ca-bundle.crt"))

conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="Team 7")
conn.connect(("127.0.0.1", 10023))
cert = conn.getpeercert()
print(cert)

conn.sendall(b"Hi there!")
print(conn.recv(1024))
