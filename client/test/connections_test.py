"""Connections Tests."""
from socket import socket, AF_INET, SOCK_STREAM
import ssl
import os
import json
from connections import Connection, NetworkException
import unittest

with open(os.path.join("..", "config", "config.json")) as config_file:
    config = json.load(config_file)


class ConnectionTests(unittest.TestCase):
    """Tests for the Connections class."""

    def testHostMatchesPassedInHost(self):
        con = Connection(config["server"]["ip"], config["server"]["port"])
        self.assertEqual(con._host, config["server"]["ip"])

    def testPortMatchesPassedInPort(self):
        con = Connection(config["server"]["ip"], config["server"]["port"])
        self.assertEqual(con._port, config["server"]["port"])

    def testConnectionMatchesPassedInConnection(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        mysocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM),
                                       server_hostname=config["server"]["hostname"])
        con = Connection(config["server"]["ip"], config["server"]["port"], mysocket)
        self.assertEqual(con._socket, mysocket)

    def testSendingOverClosedConnectionRaisesNetworkException(self):
        con = Connection(config["server"]["ip"], config["server"]["port"])
        with self.assertRaises(NetworkException):
            con.send("Hello world")

    def testRecvOverClosedConnectionRaisesNetworkException(self):
        con = Connection(config["server"]["ip"], config["server"]["port"])
        with self.assertRaises(NetworkException):
            con.recv()

    def testOpenRaisesNetworkExceptionOnAlreadyOpenConnection(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        mysocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM),
                                       server_hostname=config["server"]["hostname"])
        con = Connection(config["server"]["ip"], config["server"]["port"], mysocket)
        with self.assertRaises(NetworkException):
            con.open()

    def testCloseRaisesNetworkExceptionOnAlreadyClosedConnection(self):
        con = Connection(config["server"]["ip"], config["server"]["port"])
        with self.assertRaises(NetworkException):
            con.close()


if __name__ == '__main__':
    unittest.main()
