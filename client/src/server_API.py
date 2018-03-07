"""Server Message API."""
from connections import Connection
import os
import json
import action
from message import Message
from hexgrid import Grid
from client_gamestate import GameState
from file_logger import Logger
from civilisation import Civilisation
from city import City


class ServerAPI:
    """Server API class to send and receive messages from the server."""

    def __init__(self):
        """Create ServerAPI object."""
        with open(os.path.join("..", "config", "config.json")) as config_file:
            config = json.load(config_file)
        self.con = Connection(config["server"]["ip"], config["server"]["port"])
        self.con2 = Connection(config["server"]["ip"],
                               config["server"]["port"])
        logger = Logger("client.log", "Client",
                        config["logging"]["log_level"])
        self._log = logger.get_logger()
        self.id = None
        self._game_state = None

    def send_action(self, action, connection):
        """
        Create a Message which contains action and send it to the server.

        :param action: Action object to be encapsulated and sent to the
            server.
        """
        connection.open()
        message = Message(action, self.id)
        connection.send(message.serialise())
        reply = connection.recv()
        connection.close()
        reply_message = Message.deserialise(reply)
        return reply_message

    def join_game(self):
        """Ask the server to join a game."""
        join_game_action = action.JoinGameAction()
        reply = self.send_action(join_game_action, self.con)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            # raise action.ServerError(reply.obj)
        else:
            self._log.info("Joined game player id = " + str(reply.obj))
            game_id, self.id = reply.obj
            grid = Grid(20)
            self._game_state = GameState(game_id, 1, grid, self._log)
            self._game_state._grid.create_grid()
            self._game_state._grid.static_map()
            civ = Civilisation(self.id, self._game_state._grid, self._log)
            self._game_state.add_civ(civ)
            self._game_state._my_id = self.id

    def end_turn(self):
        """Ask the server to join a game."""
        end_turn_action = action.EndTurnAction()
        reply = self.send_action(end_turn_action, self.con)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            # raise action.ServerError(reply.obj)
        else:
            self._log.info("Turn ended")

    def leave_game(self):
        """Ask the server to leave a game."""
        leave_game_action = action.LeaveGameAction()
        reply = self.send_action(leave_game_action, self.con)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            # raise action.ServerError(reply.obj)
        else:
            self._log.info("Left game = " + str(reply.obj))

    def move_unit(self, unit, hexagon):
        """
        Create and send an action causing a unit to move.

        :param unit: unit to be moved.
        :param hexagon: the hex that the unit is to be moved to.
        """
        move_action = action.MovementAction(unit, hexagon)
        reply = self.send_action(move_action, self.con)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            # raise action.ServerError(reply.obj)
        else:
            tile_updates = reply.obj
            for tile in tile_updates._tiles:
                self.handle_tile_update(tile)
            self._game_state._civs[self.id].move_unit_to_hex(unit, hexagon)

    def attack(self, attacker, defender):
        """
        Create and send an action causing one unit to attack another.

        :param attacker: unit that is doing the attacking.
        :param defender: unit that is being attacked.
        """
        combat_action = action.CombatAction(attacker, defender)
        reply = self.send_action(combat_action, self.con)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            # raise action.ServerError(reply.obj)
        else:
            self._game_state._civs[self.id].attack_unit(attacker, defender)

    def upgrade(self, unit):
        """
        Create and send an action which upgrades a unit.

        :param unit: unit that is being upgraded.
        """
        upgrade_action = action.UpgradeAction(unit)
        reply = self.send_action(upgrade_action, self.con)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            # raise action.ServerError(reply.obj)
        else:
            self._game_state._civs[self.id].upgrade_unit(unit)

    def build(self, unit, building_type):
        """
        Create and send an action which constructs a new building.

        :param unit: unit that is doing the building.
        :param building_type: the type of building that is being built.
        """
        build_action = action.BuildAction(unit, building_type)
        reply = self.send_action(build_action, self.con)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            # raise action.ServerError(reply.obj)
        else:
            building_id = reply.obj
            self._game_state._civs[self.id].build_structure(unit,
                                                            building_type,
                                                            building_id)

    def build_city(self, unit):
        """
        Create and send an action which constructs a new city.

        :param unit: unit that is doing the building.
        """
        build_city_action = action.BuildCityAction(unit)
        reply = self.send_action(build_city_action, self.con)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            # raise action.ServerError(reply.obj)
        else:
            city_id = reply.obj
            self._game_state._civs[self.id].build_city_on_tile(unit,
                                                               city_id)

    def purchase(self, city, unit_type, level):
        """
        Create and send an action which purchases a new unit.

        :param city: the city where the unit is being bought.
        :param unit_type: the type of unit being bought.
        :param level: the level of unit being bought.
        """
        purchase_action = action.PurchaseAction(city, unit_type, level)
        reply = self.send_action(purchase_action, self.con)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            # raise action.ServerError(reply.obj)
        else:
            unit_id = reply.obj
            self._game_state._civs[self.id].buy_unit(city, unit_type, level,
                                                     unit_id)

    def check_for_updates(self):
        """Ask the server to update the game for a client."""
        check_for_updates_action = action.CheckForUpdates()
        reply = self.send_action(check_for_updates_action, self.con2)
        if reply.type == "ServerError":
            self._log.error(reply.obj)
            # raise action.ServerError(reply.obj)
        else:
            for update in reply.obj:
                self.handle_update(update)

    def handle_update(self, update):
        """Handle update reply that comes from the server."""
        if update.__class__.__name__ == "StartTurnUpdate":
            self.handle_start_turn_update(update)
        elif update.__class__.__name__ == "PlayerJoinedUpdate":
            self.handle_player_joined_update(update)
        elif update.__class__.__name__ == "UnitUpdate":
            self.handle_unit_update(update)
            self._game_state.get_civ(self._game_state.my_id).calculate_vision()
        elif update.__class__.__name__ == "TileUpdates":
            for tile in update._tiles:
                self.handle_tile_update(tile)
            self._game_state.get_civ(self._game_state.my_id).calculate_vision()

    def handle_start_turn_update(self, update):
        """Handle start turn update."""
        self._game_state.set_player_turn(update._current_player)
        self._game_state.turn_count = update._turn_count
        if update._current_player == self.id:
            self._game_state._civs[self.id].currency_per_turn()
            self._game_state._civs[self.id].reset_unit_actions_and_movement()

    def handle_player_joined_update(self, update):
        """Handle player joined update."""
        for id in update._players:
            if id not in self._game_state._civs:
                new_civ = Civilisation(id, self._game_state._grid, self._log)
                self._game_state._civs[id] = new_civ

    def handle_unit_update(self, update):
        """Handle unit update."""
        civ = self._game_state._civs[update._unit._civ_id]
        unit = update._unit
        if unit._id in civ._units:
            if unit._health <= 0:
                del civ._units[unit._id]
            else:
                if self._game_state._my_id == unit._civ_id:
                    while civ._units[unit._id]._level < unit._level:
                        civ.upgrade_unit(
                            civ._units[unit._id])
                else:
                    civ._units[unit._id]._level = unit._level
                civ._units[unit._id]._health = unit._health
        else:
            if unit._health > 0:
                civ._units[unit._id] = update._unit
                coords = unit.position.coords
                hex_tile = self._game_state._grid.get_hextile(coords)
                civ._units[unit._id].position = hex_tile
                hex_tile._unit = civ._units[unit._id]

    def handle_tile_update(self, tile):
        """Handle tile update."""
        old_tile = self._game_state._grid.get_hextile(tile.coords)
        unit = tile._unit
        building = tile._building
        if unit is not None:
            civ = self._game_state._civs[unit._civ_id]
            if unit._id in civ._units:
                civ._units[unit._id].position = old_tile
                old_tile._unit = civ._units[unit._id]
            else:
                civ._units[unit._id] = tile._unit
                coords = unit.position.coords
                hex_tile = self._game_state._grid.get_hextile(coords)
                civ._units[unit._id].position = hex_tile
                old_tile._unit = civ._units[unit._id]
        else:
            old_tile._unit = None
        if building is not None:
            if isinstance(building, City):
                civ_id = tile.civ_id
                civ = self._game_state._civs[civ_id]
                civ._cities[building.id] = building
                coords = building._hex.coords
                hex_tile = self._game_state._grid.get_hextile(coords)
                civ._cities[building.id]._hex = hex_tile
                old_tile._building = civ._cities[building.id]
            else:
                civ = self._game_state._civs[building._civ_id]
                if building._city_id in civ._cities:
                    city = civ._cities[building._city_id]
                    buildings = city._buildings
                    if building._id in buildings:
                        pass
                    else:
                        buildings[building._id] = building
                        coords = building._location.coords
                        hex_tile = self._game_state._grid.get_hextile(coords)
                        buildings[building._id].position = hex_tile
                        old_tile._building = buildings[building._id]
                else:
                    old_tile._building = building
                    old_tile._civ_id = building._civ_id
                    coords = building._hex.coords
                    hex_tile = self._game_state._grid.get_hextile(coords)
                    old_tile._building._hex = hex_tile

        else:
            old_tile._building = None
        old_tile._civ_id = tile._civ_id
        old_tile._city_id = tile._city_id
