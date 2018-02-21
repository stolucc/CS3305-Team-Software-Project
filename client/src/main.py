"""Main client program."""

from connections import Connection
import os
import json
from message import Message
from action import JoinGameAction


class Client:
    """Client object."""

    def __init__(self):
        """Create a new Class object."""
        with open(os.path.join("..", "config", "config.json")) as config_file:
            config = json.load(config_file)
        self._con = Connection(config["server"]["ip"],
                               config["server"]["port"])
        self._player_id = None

    def join_game(self):
        """Ask the server to join a game."""
        self._con.open()
        join_game_action = JoinGameAction()
        message = Message(join_game_action, None)
        self._con.send(message.serialise())
        message = Message.deserialise(self._con.recv())
        print(str(message))
        self._con.close()


def main():
    """Start main program."""
    client = Client()
    client.join_game()


if __name__ == "__main__":
    main()
