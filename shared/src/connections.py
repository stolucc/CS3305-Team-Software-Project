from socket import socket, gethostname, gethostbyname, AF_INET, SOCK_STREAM
import threading

class Connection:
    """
    Class the represent a TCP connection
    """
    def __init__(self, host, port, connection=None):
        """
        Create base Connection object

        :param host: location of other party
        :param port: port number of other party
        :param connection: default new connection, can be passed existing tcp socket
        """
        self._host = gethostbyname(host) #resolve hostnames
        self._port = port
        if connection is None:
            self._socket = socket(AF_INET, SOCK_STREAM)
            self._open_status = False
        else:
            self._socket = connection
            self._open_status = True

    def send(self, message, wait_response=False):
        """
        Send message to other party over TCP

        :param message: Message (String) to be sent
        :param wait_response: (bool) default False, set True to return message response
        :return: response to message else None
        """
        if self._open_status:
            try:
                msglen = "{:16}".format(len(message)) #create padded string
                message = msglen + message #add the message length to the begining of the message
                self._socket.sendall(message.encode()) #send encoded message over TCP
                if wait_response:
                    return self.recv() #recv message in response
                return None
            except Exception:
                raise
        else:
            raise NetworkException("Connection currently closed.")

    def recv(self):
        """
        Send message to other party over TCP

        :return: response to message else None
        """
        if self._open_status:
            try:
                amount_expected = int(self._socket.recv(16).decode()) #get message length
                amount_received = 0
                message = ""
                while amount_received < amount_expected:
                    data = self._socket.recv(16).decode() #get 16 bytes of message and decode
                    message += data
                    amount_received += len(data)
                return message
            except Exception:
                raise
        else:
            raise NetworkException("Connection currently closed.")

    def open(self):
        """
        Open tcp connection with other party
        """
        if not self._open_status:
            try:
                self._socket.connect((self._host, self._port))
                self._open_status = True
            except Exception:
                raise
        else:
            raise NetworkException("Connection is already open.")

    def close(self):
        """
        Close tcp connection
        """
        if self._open_status:
            try:
                self._socket.close()
                self._open_status = False
                self._socket = socket(AF_INET, SOCK_STREAM)
            except Exception:
                raise
        else:
            raise NetworkException("Connection currently closed.")

class ConnectionHandler:
    """
    Class to handle incoming tcp connections
    """
    def __init__(self, function):
        """
        Create base ConnectionHandler

        :param function: callback function, called with arguments ((ip, host), Connection)
        """
        self._function = function
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._threads = []
        self._stop_flag = False

    def start(self, port):
        self._stop_flag = False
        self._socket.bind((gethostbyname(gethostname()), port))
        self._socket.listen(10)
        thread = threading.Thread(name="handler", target=self.handler, args=())
        thread.start()
        self._threads.append(thread)

    def handler(self):
        while not self._stop_flag:
            try:
                self._socket.settimeout(0.2)
                conn, addr = self._socket.accept()
            except socket.timeout:
                pass
            except:
                raise
            else:
                client_connection = Connection(addr[0], addr[1], connection=conn)
                thread = threading.Thread(name="worker",
                                          target=self._function,
                                          args=(addr, client_connection))
                thread.start()
                self._threads.append(thread)

    def stop(self):
        self._stop_flag = True
        for thread in self._threads:
            thread.join()
        self._socket.close()
        self._socket = socket(AF_INET, SOCK_STREAM)

class NetworkException(Exception):
    pass

def main():
    con = Connection("127.0.1.1", 10000)
    ser = ConnectionHandler(test)
    ser.start(10000)
    con.open()
    con.send("Can you hear me?")
    con.close()
    con.open()
    con.send("Can you hear me now?")
    con.close()
    ser.stop()

def test(addr, connection):
    print(addr)
    print(connection.recv())

if __name__ == "__main__":
    main()
