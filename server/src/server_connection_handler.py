"""Server Connection Handler"""
from socket import socket, gethostname, gethostbyname, AF_INET, SOCK_STREAM
import threading
import ssl
import os
from connections import Connection

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
certfile = os.path.join("..", "config", "cert.pem")
keyfile = os.path.join("..", "config", "key.pem")
context.load_cert_chain(certfile=certfile, keyfile=keyfile)


class ConnectionHandler:
    """Class to handle incoming tcp connections."""

    def __init__(self, function):
        """
        Create base ConnectionHandler.

        :param function: callback function, called with arguments (addr, Conn)
        """
        self._function = function
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._threads = []
        self._stop_flag = False
        self._context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self._context.load_cert_chain(
            certfile=os.path.join("..", "config", "cert.pem"),
            keyfile=os.path.join("..", "config", "key.pem"))

    def start(self, port):
        """
        Start connection handler in new thread.

        :param port: port for connection handler to listen on
        """
        self._stop_flag = False
        print(gethostbyname(gethostname()))
        self._socket.bind((gethostbyname(gethostname()), port))
        self._socket.listen(10)
        thread = threading.Thread(name="handler", target=self.handler, args=())
        thread.start()
        self._threads.append(thread)

    def handler(self):
        """Handle incoming tcp connections passing to new thread."""
        while not self._stop_flag:
            try:
                self._socket.settimeout(0.2)
                conn, addr = self._socket.accept()
            except Exception:
                pass
            else:
                conn = self._context.wrap_socket(conn, server_side=True)
                client_conn = Connection(addr[0], addr[1], connection=conn)
                thread = threading.Thread(name="worker",
                                          target=self._function,
                                          args=(addr, client_conn))
                thread.start()
                self._threads.append(thread)

    def stop(self):
        """Stop connection handler and join all threads."""
        self._stop_flag = True
        for thread in self._threads:
            thread.join()
        self._socket.close()
        self._socket = socket(AF_INET, SOCK_STREAM)


def main():
    """Test function."""
    ser = ConnectionHandler(test)
    ser.start(10000)
    ser.stop()


def test(addr, connection):
    """Test handler function."""
    print(addr)
    print(connection.recv())


if __name__ == "__main__":
    main()