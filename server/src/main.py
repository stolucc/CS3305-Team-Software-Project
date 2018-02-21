from server_connection_handler import ConnectionHandler
from database_logger import Logger
import database_API
import os
import json
from message import Message

class Server():

    def __init__(self):
        with open(os.path.join("..", "config", "config.json")) as config_file:
            config = json.load(config_file)
        db_connection = database_API.Connection(config["postgres"]["user"],
                                                config["postgres"]["password"],
                                                config["postgres"]["database"])
        session = db_connection.get_session()
        logger = Logger(session, "Server Connection Handler",
                        config["logging"]["log_level"])
        self._log = logger.get_logger()
        self._connection_handler = ConnectionHandler(self.handle_message, self._log)
        self._connection_handler.start(config["server"]["port"])

    def handle_message(self, connection):
        info = connection.recv()
        message = Message.deserialise(info)
        print(message)

if __name__=="__main__":
    s = Server()

"""
def test(addr, connection, log):
    info = connection.recv()
    message = Message.deserialise(info)
    print(message)
    log.debug(str(message))
    bytestream = message.serialise()
    connection.send(bytestream)
"""
