from socket import *
import threading

class Connection:
    def __init__(self, host, port, connection = None):
        self._host = gethostbyname(host) #resolve hostnames
        self._port = port
        if connection == None:
            self._socket = socket(AF_INET, SOCK_STREAM)
            self._OPEN_STATUS = False
        else:
            self._socket = connection
            self._OPEN_STATUS = True

    def send(self, message, wait_response = False):
        if self._OPEN_STATUS:
            try:
                msglen = "{:16}".format(len(message)) #create padded string of length 16 containing the length of the message to be sent
                message = msglen + message #add the message length to the begining of the message
                self._socket.sendall(message.encode()) #send encoded message over TCP
                if wait_response:
                    return recv() #recv message in response
                else:
                    return None
            except Exception:
                raise
        else:
            raise NetworkException("Connection currently closed.")

    def recv(self):
        if self._OPEN_STATUS:
            try:
                amount_expected = int(self._socket.recv(16).decode()) #get length of incoming message
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
        if not self._OPEN_STATUS:
            try:
                self._socket.connect((self._host, self._port))
                self._OPEN_STATUS = True
            except Exception:
                raise
        else:
            raise NetworkException("Connection is already open.")

    def close(self):
        if self._OPEN_STATUS:
            try:
                self._socket.close()
                self._OPEN_STATUS = False
                self._socket = socket(AF_INET, SOCK_STREAM)
            except Exception:
                raise
        else:
            raise NetworkException("Connection currently closed.")

class ConnectionHandler:
    def __init__(self, function):
        self._function = function
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._threads = []
        self._stop_flag = False

    def start(self, port):
        self._stop_flag = False
        self._socket.bind((gethostbyname(gethostname()), port))
        self._socket.listen(10)
        t = threading.Thread(name="handler", target=self.handler, args=())
        t.start()
        self._threads.append(t)

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
                t = threading.Thread(name="worker", target=self._function, args=(addr,client_connection))
                t.start()
                self._threads.append(t)

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
