from socket import *

class Connection:
    def __init__(self, host, port, connection = None):
        self._host = socket.gethostbyname(host) #resolve hostnames
        self._port = port
        if connection == None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            except Exeption:
                raise
        else:
            raise NetworkExeption("Connection currently closed.")

    def recv(self):
        if self._OPEN_STATUS:
            try:
                amount_expected = int(self._socket.recv(16).decode()) #get length of incoming message
                message = ""
                while amount_received < amount_expected:
                    data = self._socket.recv(16).decode() #get 16 bytes of message and decode
                    message += data
                    amount_received += len(data)
                return message
            except Exeption:
                raise
        else:
            raise NetworkExeption("Connection currently closed.")

    def open(self):
        if not self._OPEN_STATUS:
            try:
                self._socket.connect((self._host, self._port))
                self._OPEN_STATUS = True
            except Exeption:
                raise
        else:
            raise NetworkExeption("Connection is already open.")

    def close(self):
        if self._OPEN_STATUS:
            try:
                self._socket.close()
                self._OPEN_STATUS = False
            except Exeption:
                raise
        else:
            raise NetworkExeption("Connection currently closed.")    

class NetworkExeption(Exeption):
    pass

if __name__ == "__main__":
    main()

def main():
    con = Connection("localhost", 10000)
