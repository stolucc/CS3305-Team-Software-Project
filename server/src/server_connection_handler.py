"""Server Connection Handler."""
from socket import socket, AF_INET, SOCK_STREAM, \
    timeout
import threading
import ssl
import os
from connections import Connection
import json


class ConnectionHandler:
    """Class to handle incoming tcp connections."""

    def __init__(self, function, log):
        """
        Create base ConnectionHandler.

        :param function: callback function, called with arguments (addr, Conn)
        """
        with open(os.path.join("..", "config", "config.json")) as config_file:
            config = json.load(config_file)
        self._log = log
        self._ip = config["server"]["ip_address"]
        self._config = config
        self._function = function
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._threads = []
        self._stop_flag = False
        self._context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self._context.load_cert_chain(
            certfile=config["paths"]["cert"],
            keyfile=config["paths"]["key"])

    def start(self, port):
        """
        Start connection handler in new thread.

        :param port: port for connection handler to listen on
        """
        self._stop_flag = False
        print(self._ip)
        self._socket.bind((self._ip, port))
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
                conn = self._context.wrap_socket(conn, server_side=True)
            except ssl.SSLEOFError as e:
                self._log.error("Run-time error: %s" % e)
                pass
            except timeout:
                pass
            except Exception as e:
                self._log.error("Run-time error: %s" % e)
                pass
            else:
                client_conn = Connection(addr[0], addr[1], connection=conn)
                thread = threading.Thread(name="worker",
                                          target=self._function,
                                          args=(client_conn,))
                thread.start()
                self._threads.append(thread)

    def stop(self):
        """Stop connection handler and join all threads."""
        self._stop_flag = True
        for thread in self._threads:
            thread.join()
        self._socket.close()
        self._socket = socket(AF_INET, SOCK_STREAM)
