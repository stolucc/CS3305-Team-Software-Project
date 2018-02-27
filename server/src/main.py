from server_connection_handler import ConnectionHandler
from database_logger import Logger
from hexgrid import Grid
from gamestate import GameState
import database_API
import os
import sys
import json
from message import Message


class Server():

    def __init__(self):
        with open(os.path.join("..", "config", "config.json")) as config_file:
            config = json.load(config_file)
        db_connection = database_API.Connection(config["postgres"]["user"],
                                                config["postgres"]["password"],
                                                config["postgres"]["database"])
        self._session = db_connection.get_session()
        logger = Logger(self._session, "Server Connection Handler",
                        config["logging"]["log_level"])

        self._log = logger.get_logger()
        self._connection_handler = ConnectionHandler(self.handle_message,
                                                     self._log)
        grid = Grid(100)
        game_id = database_API.Game.insert(self._session, 1, True)
        self._gamestate = GameState(game_id, 1, grid, self._log, self._session)
        try:
            self._connection_handler.start(config["server"]["port"])
        except KeyboardInterrupt:
            self._connection_handler.stop()
            sys.exit()

    def handle_message(self, connection):
        try:
            info = connection.recv()
            message = Message.deserialise(info)
            result = self._gamestate.handle_action(message)
            msg = Message(result, -1)
            connection.send(msg.serialise())
        except TypeError as t:
            self._log.error(str(t))

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
