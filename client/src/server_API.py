"""Server Message API."""
from connections import Connection
import os
import json
import action
from message import Message
from hexgrid import Grid
from gamestate import GameState
from file_logger import Logger


class ServerAPI:
    """Server API class to send and receive messages from the server."""

    def __init__(self):
        """Create ServerAPI object."""
        with open(os.path.join("..", "config", "config.json")) as config_file:
            config = json.load(config_file)
        self.con = Connection(config["server"]["ip"], config["server"]["port"])
        logger = Logger("client.log", "Client",
                        config["logging"]["log_level"])
        self._log = logger.get_logger()
        self.id = None
        self._game_state = None

    def send_action(self, action):
        """
        Create a Message which contains action and send it to the server.

        :param action: Action object to be encapsulated and sent to the
        server.
        """
        self.con.open()
        message = Message(action, self.id)
        self.con.send(message.serialise())
        reply = self.con.recv()
        self.con.close()
        reply_message = Message.deserialise(reply)
        return reply_message

    def join_game(self):
        """Ask the server to join a game."""
        join_game_action = action.JoinGameAction()
        reply = self.send_action(join_game_action)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            raise action.ServerError(action.GAME_FULL_ERROR)
        else:
            self._log.info("Joined game player id = " + str(reply.obj))
            game_id, self.id = reply.obj
            grid = Grid(103)
            self._game_state = GameState(game_id, 1, grid, self._log,
                                         None)

    def leave_game(self):
        """Ask the server to leave a game."""
        leave_game_action = action.LeaveGameAction()
        reply = self.send_action(leave_game_action)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            raise action.ServerError(action.VALIDATION_ERROR)
        else:
            self._log.info("Left game = " + str(reply.obj))

    def check_for_updates(self):
        """Ask the server to update the game for a client."""
        check_for_updates_action = action.CheckForUpdates()
        reply = self.send_action(check_for_updates_action)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            raise action.ServerError(action.VALIDATION_ERROR)
        else:
            # TODO Add code to handle response
            pass

    def move_unit(self, unit, hexagon):
        """
        Create and send an action causing a unit to move.

        :param unit: unit to be moved.
        :param hexagon: the hex that the unit is to be moved to.
        """
        move_action = action.MovementAction(unit, hexagon)
        reply = self.send_action(move_action)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            raise action.ServerError(action.VALIDATION_ERROR)
        else:
            unit.position = hexagon

    def attack(self, attacker, defender):
        """
        Create and send an action causing one unit to attack another.

        :param attacker: unit that is doing the attacking.
        :param defender: unit that is being attacked.
        """
        combat_action = action.CombatAction(attacker, defender)
        reply = self.send_action(combat_action)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            raise action.ServerError(action.VALIDATION_ERROR)
        else:
            # TODO Add code to handle response
            pass

    def upgrade(self, unit):
        """
        Create and send an action which upgrades a unit.

        :param unit: unit that is being upgraded.
        """
        upgrade_action = action.UpgradeAction(unit)
        reply = self.send_action(upgrade_action)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            raise action.ServerError(action.VALIDATION_ERROR)
        else:
            # TODO Add code to handle response
            pass

    def build(self, unit, building_type):
        """
        Create and send an action which constructs a new building.

        :param unit: unit that is doing the building.
        :param building_type: the type of building that is being built.
        """
        build_action = action.BuildAction(unit, building_type)
        reply = self.send_action(build_action)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            raise action.ServerError(action.VALIDATION_ERROR)
        else:
            # TODO Add code to handle response
            pass

    def purchase(self, city, unit_type, level):
        """
        Create and send an action which purchases a new unit.

        :param city: the city where the unit is being bought.
        :param unit_type: the type of unit being bought.
        :param level: the level of unit being bought.
        """
        purchase_action = action.PurchaseAction(city, unit_type, level)
        reply = self.send_action(purchase_action)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            raise action.ServerError(action.VALIDATION_ERROR)
        else:
            # TODO Add code to handle response
            pass
