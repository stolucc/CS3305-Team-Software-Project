"""Main client program."""
from server_API import ServerAPI
import action
import sys


def main():
    """Start main program."""
    server_api = ServerAPI()
    try:
        server_api.join_game()
        # server_api.leave_game()
    except action.ServerError as e:
        print("Server error occurred with error code " + str(e.error_code))
        sys.exit(1)


if __name__ == "__main__":
    main()
