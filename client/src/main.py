"""Main client program."""

from connections import Connection
import os
import json
from server_API import ServerAPI
import action
import sys


class Client:
    """Client object."""

    def __init__(self):
        """Create a new Class object."""
        with open(os.path.join("..", "config", "config.json")) as config_file:
            config = json.load(config_file)
        self._con = Connection(config["server"]["ip"],
                               config["server"]["port"])
        self._server_API = ServerAPI(None)

    def join_game(self):
        """Ask the server to join a game."""
        self._server_API.join_game()

    def leave_game(self):
        """Ask the server to leave a game."""
        self._server_API.leave_game()


def main():
    """Start main program."""
    client = Client()
    try:
        client.join_game()
        # client.leave_game()
    except action.ServerError as e:
        print("Server error occurred with error code " + str(e.error_code))
        sys.exit(1)


if __name__ == "__main__":
    main()
