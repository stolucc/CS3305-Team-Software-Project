"""Server Message API."""
from connections import Connection
import os
import json
import action
from message import Message


class ServerAPI:
    """Server API class to send and receive messages from the server."""

    def __init__(self, player_id):
        """Create ServerAPI object."""
        with open(os.path.join("..", "config", "config.json")) as config_file:
            config = json.load(config_file)
        self.con = Connection(config["server"]["ip"], config["server"]["port"])
        self.id = player_id

    def send_action(self, action):
        """Create a Message which contains action and send it to the server."""
        self.con.open()
        message = Message(action, self.id)
        self.con.send(message.serialise())
        reply = self.con.recv()
        self.con.close()
        reply_message = Message.deserialise(reply)
        return reply_message

    def move_unit(self, unit, hexagon):
        """Create and send an action causing a unit to move."""
        upgrade_action = action.MovementAction(unit, hexagon)
        # TODO Add code to handle response
        return self.send_action(upgrade_action)

    def attack(self, attacker, defender):
        """Create and send an action causing one unit to attack another."""
        combat_action = action.CombatAction(attacker, defender)
        # TODO Add code to handle response
        return self.send_action(combat_action)

    def upgrade(self, unit):
        """Create and send an action which upgrades a unit."""
        upgrade_action = action.UpgradeAction(unit)
        # TODO Add code to handle response
        return self.send_action(upgrade_action)

    def build(self, unit, building_type):
        """Create and send an action which constructs a new building."""
        build_action = action.BuildAction(unit, building_type)
        # TODO Add code to handle response
        return self.send_action(build_action)

    def purchase(self, city, unit_type, level):
        """Create and send an action which purchases a new unit."""
        purchase_action = action.PurchaseAction(city, unit_type, level)
        # TODO Add code to handle response
        return self.send_action(purchase_action)
