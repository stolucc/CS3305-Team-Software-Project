"""Main client program."""
from server_API import ServerAPI
import action
import sys
import threading
from time import sleep


def main():
    """Start main program."""
    server_api = ServerAPI()
    try:
        server_api.join_game()
        thread = threading.Thread(name="check_for_updates",
                                  target=check_for_updates,
                                  args=(server_api,))
        thread.start()
        # server_api.leave_game()
    except action.ServerError as e:
        print("Server error occurred with error code " + str(e.error_code))
        sys.exit(1)


def check_for_updates(server_api):
    """Check for updates from server."""
    while True:
        server_api.check_for_updates()
        sleep(1)


if __name__ == "__main__":
    main()
