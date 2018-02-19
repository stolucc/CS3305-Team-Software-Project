"""Server Connection Handler Test."""
from socket import socket, gethostname, gethostbyname, AF_INET, SOCK_STREAM
import threading
import ssl
import os
from connections import Connection
import json
from server_connection_handler import ConnectionHandler, test
import unittest


class ServerConnectionHandlerTests(unittest.TestCase):
    """Tests for the Server Connection Handler class."""

    def testHandlerFunctionMatchesPassedInFunction(self):
        handler = ConnectionHandler(test)
        self.assertEqual(handler._function, test)
        handler._socket.close()

    def testHandlerPortMatchesPassedInPortInStart(self):
        handler = ConnectionHandler(test)
        handler.start(80)
        currentport = handler._socket.getsockname()[1]
        self.assertEqual(80, currentport)
        handler._socket.close()
        
        
if __name__ == '__main__':
    unittest.main()
