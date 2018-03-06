"""A module for launching a server instance."""

from server_connection_handler import ConnectionHandler
from database_logger import Logger
from hexgrid import Grid
from gamestate import GameState
import traceback
import database_API
import os
import sys
import json
from message import Message


class Server():
    """A class encapsulating all server implementation."""

    def __init__(self):
        """Initialise a new Server object."""
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
        grid = Grid(20)
        grid.create_grid()
        game_id = database_API.Game.insert(self._session, 1, True)
        self._gamestate = GameState(game_id, 1, grid, self._log, self._session)
        try:
            self._connection_handler.start(config["server"]["port"])
        except KeyboardInterrupt:
            print("I happened")
            self._connection_handler.stop()
            sys.exit()

    def handle_message(self, connection):
        """
        Handle an incoming message sent to the server.

        :param connection: The initiated connection
        """
        try:
            info = connection.recv()
            message = Message.deserialise(info)
            result = self._gamestate.handle_message(message)
            msg = Message(result, -1)
            connection.send(msg.serialise())
        except TypeError as t:
            self._log.error(traceback.format_exc(t))


if __name__ == "__main__":
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
