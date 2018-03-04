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
                                  args=(server_api,), daemon=True)
        thread.start()
        sleep(3)
        civ = server_api._game_state._civs[server_api.id]
        unit = None
        for key in civ._units:
            unit = civ._units[key]
        print(unit)
        unit_coords = unit.position.coords
        move_back = server_api._game_state._grid.get_hextile(unit_coords)
        move_coords = (unit_coords[0] + 1, unit_coords[1] - 1, unit_coords[2])
        hex_to_move = server_api._game_state._grid.get_hextile(move_coords)
        input("send move")
        print(hex_to_move)
        server_api.move_unit(unit, hex_to_move)
        server_api.end_turn()
        input("send move2")
        print(move_back)
        server_api.move_unit(unit, move_back)
        server_api.end_turn()
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
