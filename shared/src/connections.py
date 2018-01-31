"""Network API."""
from socket import socket, gethostbyname, AF_INET, SOCK_STREAM
import ssl
import os
import json

with open(os.path.join("..", "config", "config.json")) as config_file:
    config = json.load(config_file)


class Connection:
    """Class the represent a TCP connection."""

    def __init__(self, host, port, connection=None):
        """
        Create base Connection object.

        :param host: location of other party
        :param port: port number of other party
        :param connection: default new connection, can be passed existing tcp
        """
        self._host = gethostbyname(host)
        self._port = port
        if connection is None:
            self._context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            self._context.verify_mode = ssl.CERT_REQUIRED
            self._context.check_hostname = True
            self._context.load_verify_locations(
                config["paths"]["ca-bundle"])
            self._socket = self._context.wrap_socket(
                socket(AF_INET, SOCK_STREAM),
                server_hostname=config["server"]["hostname"])
            self._open_status = False
        else:
            self._socket = connection
            self._open_status = True

    def send(self, message, wait_response=False):
        """
        Send message to other party over TCP.

        :param message: Message (String) to be sent
        :param wait_response: (bool) default False, set True to return response
        :return: response to message else None
        """
        if self._open_status:
            try:
                msglen = "{:16}".format(len(message))  # create padded string
                message = msglen + message  # add the message length
                self._socket.sendall(message.encode())  # send encoded message
                if wait_response:
                    return self.recv()  # recv message in response
                return None
            except Exception:
                raise
        else:
            raise NetworkException("Connection currently closed.")

    def recv(self):
        """
        Send message to other party over TCP.

        :return: response to message else None
        """
        if self._open_status:
            try:
                amount_expected = int(self._socket.recv(16).decode())
                amount_received = 0
                message = ""
                while amount_received < amount_expected:
                    data = self._socket.recv(16).decode()  # get 16 bytes
                    message += data
                    amount_received += len(data)
                return message
            except Exception:
                raise
        else:
            raise NetworkException("Connection currently closed.")

    def open(self):
        """Open tcp connection with other party."""
        if not self._open_status:
            try:
                self._socket.connect((self._host, self._port))
                self._open_status = True
            except Exception:
                raise
        else:
            raise NetworkException("Connection is already open.")

    def close(self):
        """Close tcp connection."""
        if self._open_status:
            try:
                self._socket.close()
                self._open_status = False
                self._socket = self._context.wrap_socket(
                    socket(AF_INET, SOCK_STREAM),
                    server_hostname=config["server"]["hostname"])
            except Exception:
                raise
        else:
            raise NetworkException("Connection currently closed.")


class NetworkException(Exception):
    """Custom Exception for networkapi."""

    pass


def main():
    """Test function."""
    con = Connection(config["server"]["ip"], config["server"]["port"])
    con.open()
    con.send("Can you hear me?")
    con.close()
    con.open()
    con.send("Can you hear me now?")
    con.close()


if __name__ == "__main__":
    main()
