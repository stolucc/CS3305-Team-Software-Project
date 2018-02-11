import unittest
from connections import Connection
from server_connection_handler import ConnectionHandler


class SimpleNetworkTest():

    def setUp(self):
        """Call before every test case."""
        self._ser = ConnectionHandler(test)
        self._ser.start(10000)

    def tearDown(self):
        """Call after every test case."""
        self._ser.stop()

    def testA(self):
        """Note that all test method names must begin with 'test.'"""
        con = Connection("127.0.0.1", 10000)
        con.open()
        con.send("Can you hear me?")
        con.close()
        con.open()
        con.send("Can you hear me now?")
        con.close()
        assert 5 == 5, "bar() not calculating values correctly"


def test(addr, connection):
    """Test handler function."""
    print(addr)
    print(connection.recv())
