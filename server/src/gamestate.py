"""Game state representation."""

import database_API
from civilisation import Civilisation
from building import Building
from unit import Unit
from action import ServerError, GAME_FULL_ERROR, UNKNOWN_ACTION, \
    StartTurnUpdate, TileUpdates, UnitUpdate, MovementAction, \
    CombatAction, UpgradeAction, BuildAction, PurchaseAction, \
    PlayerJoinedUpdate, ResearchAction, BuildCityAction
from unit import Worker
import random
from queue import Queue


class GameState:
    """Game state class."""

    NUM_PLAYERS = 2

    def __init__(self, game_id, seed, grid, logger, session):
        """
        Initialise GameState attributes.

        :param game_id: hex grid that game is using
        :param seed: hex grid that game is using
        :param grid: hex grid that game is using
        """
        self._logger = logger
        self._session = session
        self._game_id = game_id
        self._seed = seed
        self._grid = grid
        self._civs = {}
        self._my_id = None
        self._turn_count = 0
        self._current_player = None
        self._game_started = False
        self._queues = {}
        self._start_locations = [(4, -2, -2), (-3, -2, 5),
                                 (-2, 4, -2), (4, -5, 1)]

    @property
    def game_id(self):
        """
        Getter for game_id.

        :return: game_id
        """
        return self._game_id

    @property
    def seed(self):
        """
        Getter for seed.

        :return: seed
        """
        return self._seed

    @property
    def grid(self):
        """
        Getter for grid.

        :return: grid
        """
        return self._grid

    def get_civ(self, civ_id):
        """
        Return the civ with the id of civ_id.

        :return: Civilization
        """
        return self._civs[civ_id]

    def add_civ(self, civ):
        """Add the civ to the list of civs playing."""
        self._civs[civ.id] = civ

    @property
    def my_id(self):
        """
        Getter for my_id.

        :return: my_id
        """
        return self._my_id

    @my_id.setter
    def my_id(self, my_id):
        """Setter for my_id."""
        self._my_id = my_id

    @property
    def turn_count(self):
        """
        Getter for turn_count.

        :return: turn_count
        """
        return self._turn_count

    @turn_count.setter
    def turn_count(self, turn_count):
        """Setter for turn_count."""
        self._turn_count = turn_count

    def handle_message(self, message):
        """
        Handle an action sent by a client.

        :param messag: The message object received from the client
        :return: The value to be sent back to the client
        """
        civ_actions = ["MovementAction", "CombatAction", "UpgradeAction",
                       "BuildAction", "PurchaseAction", "BuildCityAction"]

        if message.type == "CheckForUpdates":
            return self.update_player(message)
        self._logger.debug(message)
        if message.type == "JoinGameAction":
            return self.add_player(message)
        elif message.type == "LeaveGameAction":
            return self.remove_player(message)

        if message.id == self._current_player:
            if message.type == "EndTurnAction":
                return self.end_turn(message)
            elif message.type in civ_actions:
                (result_set, return_value) = self.handle_action(message.id,
                                                                message.obj)
                self.populate_queues(result_set)
                return return_value
        err = ServerError(UNKNOWN_ACTION)
        self._logger.error(err)
        return err

    def populate_queues(self, result_set):
        """Add update information to relevant queues."""
        impacted_tiles = result_set
        is_tile = True
        if isinstance(result_set[0], Unit):
            impacted_tiles = [unit.position for unit in impacted_tiles]
            is_tile = False
        for civ in self._civs:
            self._civs[civ].calculate_vision()
            # vision = self._civs[civ].vision - this is never used
            relevant = []
            for tile in range(len(impacted_tiles)):
                # if impacted_tiles[tile] in vision:
                relevant += [tile]
            if is_tile:
                self._queues[civ].put(
                    TileUpdates([result_set[x] for x in relevant]))
            else:
                for index in relevant:
                    self._queues[civ].put(UnitUpdate(result_set[index]))

    def add_player(self, message):
        """
        Add a new player to the game.

        :param message: The message object sent from the client.
        :return: The id of the new player
        """
        if len(self._civs) < GameState.NUM_PLAYERS:
            user_id = database_API.User.insert(self._session,
                                               self._game_id,
                                               active=True, gold=100,
                                               food=100, science=0,
                                               production=0)
            self.add_civ(Civilisation(user_id, self._grid, self._logger))
            self._logger.info("New Civilisation joined with id " +
                              str(user_id))
            # NOTE: Not needed when loading from db
            location = random.choice(self._start_locations)
            del self._start_locations[self._start_locations.index(location)]
            unit_id = database_API.Unit.insert(self._session, user_id, 1,
                                               0, Worker.get_health(1),
                                               *location)
            self._civs[user_id].set_up(self._grid.get_hextile(location),
                                       unit_id)
            self._queues[user_id] = Queue()
            self._queues[user_id].put(UnitUpdate(
                self._civs[user_id].units[unit_id]))
            if(len(self._civs) == GameState.NUM_PLAYERS):
                self._game_started = True
                self._turn_count += 1
                player_ids = [x for x in self._civs]
                for civ in self._civs:
                    self._queues[civ].put(PlayerJoinedUpdate(player_ids))
                self._current_player = list(self._civs.keys())[0]
                start_turn_update = StartTurnUpdate(self._current_player,
                                                    self._turn_count)
                for key in self._queues:
                    self._queues[key].put(start_turn_update)
                    unit = self._civs[key].units[list(self._civs[key].units.
                                                      keys())[0]]
                    self.populate_queues([unit])

            return self._game_id, user_id
        else:
            err = ServerError(GAME_FULL_ERROR)
            self._logger.error(err)
            return err

    def remove_player(self, message):
        """
        Remove a player to the game.

        :param message: The message object sent from the client.
        :return: The boolean success value of the function
        """
        user_id = message.id
        del self._civs[user_id]
        del self._queues[user_id]
        database_API.User.update(self._session, user_id, active=False)
        return True

    def update_player(self, message):
        """
        Convert the updates available to the player to a list to be sent.

        :param message: The message object sent from the client.
        :return: The list of updates for that client.
        """
        user_id = message.id
        updates = []
        while not self._queues[user_id].empty():
            updates.append(self._queues[user_id].get())
        return updates

    def end_turn(self, message):
        """
        End a player's turn and move on to the next.

        :param message: The message object sent from the client.
        """
        civs = list(self._civs.keys())
        current_civ_index = civs.index(self._current_player)
        next_civ_index = (current_civ_index + 1) % GameState.NUM_PLAYERS
        next_civ = civs[next_civ_index]
        self._current_player = next_civ
        self._civs[self._current_player].reset_unit_actions_and_movement()
        if next_civ_index == 0:
            self._turn_count += 1
        start_turn_update = StartTurnUpdate(self._current_player,
                                            self._turn_count)
        for key in self._queues:
            self._queues[key].put(start_turn_update)

    def set_player_turn(self, current_player):
        """Update the person whose turn it is."""
        self._current_player = current_player

    def handle_movement_action(self, civ, action):
        """Handle incoming movement actions and update game state."""
        if self._civs[civ].id != action.unit._civ_id:
            return ([], ServerError(4))

        unit = self.validate_unit(civ, action.unit)
        tile = self.validate_tile(action.destination)

        city_destroyed_update = self._civs[civ].move_unit_to_hex(unit, tile)
        database_API.Unit.update(self._session, unit.id, x=tile.x,
                                 y=tile.y, z=tile.z)
        result_tiles = self._grid.vision(unit.position, 3)
        results = [action.unit.position, unit.position] + \
            (city_destroyed_update if
             city_destroyed_update is not None else [])
        return (results,
                TileUpdates(result_tiles))

    def handle_combat_action(self, civ, action):
        """Handle incoming combat actions and update game state."""
        if self._civs[civ].id != action.attacker._civ_id \
                or self._civs[civ].id == action.defender._civ_id:
            return ([], ServerError(4))
        attacker = self.validate_unit(civ, action.attacker)
        defender = self.validate_unit(self._civs[action.defender._civ_id],
                                      action.defender)
        self._civs[civ].attack_unit(attacker, defender)
        enemy = action.defender
        database_API.Unit.update(self._session, enemy.id,
                                 health=enemy.health)
        return ([attacker, defender], True)

    def handle_upgrade_action(self, civ, action):
        """Handle incoming upgrade actions and update game state."""
        if self._civs[civ].id != action.unit._civ_id:
            return ([], ServerError(4))
        self._civs[civ].upgrade_unit(action.unit)
        unit = self.validate_unit(civ, action.unit)
        database_API.Unit.update(self._session, unit._id,
                                 level=unit.level, health=unit.health)
        return [unit]

    def handle_build_action(self, civ, action):
        """Handle incoming build actions and update game state."""
        if self._civs[civ].id != action.unit._civ_id:
            return ([], ServerError(4))
        building_type = action.building_type
        tile = self.validate_tile(action.unit.position)
        bld_id = database_API.Building.insert(self._session,
                                              self._civs[civ]._id,
                                              True, Building.get_type
                                              (building_type),
                                              tile.x, tile.y, tile.z)
        self._civs[civ].build_structure(action.unit,
                                        action.building_type,
                                        bld_id)
        return ([action.unit.position], bld_id)

    def handle_purchase_action(self, civ, action):
        """Handle incoming purchase actions and update game state."""
        if self._civs[civ].id != action.unit._civ_id:
            return ([], ServerError(4))
        level = action.level
        unit_type = action.unit_type
        position = self.validate_tile(action.building.position)
        unit_id = database_API.Unit.insert(self._session,
                                           self._civs[civ]._id, level,
                                           unit_type.get_type(),
                                           unit_type.get_health(level),
                                           position.x, position.y,
                                           position.z)
        return ([self._civs[civ].buy_unit(unit_id, action.building,
                                          action.unit_type, action.level)],
                unit_id)

    def handle_build_city_action(self, civ, action):
        """Handle incoming city-building actions and update game state."""
        if self._civs[civ].id != action.unit._civ_id:
            return ([], ServerError(4))
        unit = self.validate_unit(civ, action.unit)
        tile = self.validate_tile(unit.position)
        city_id = database_API.Building.insert(self._session,
                                               self._civs[civ]._id,
                                               True, 3, tile.x, tile.y,
                                               tile.z)
        self._civs[civ].build_city_on_tile(unit, city_id)
        return ([tile], city_id)

    def handle_research_action(self, civ, action):
        """Handle incoming research actions and update game state."""
        node_id = action.node_id
        database_API.Technology.insert(self._session, self._civs[civ]._id,
                                       node_id)
        return [self._civs[civ].unlock_research(node_id)]

    def validate_unit(self, civ, unit):
        """Return valid unit."""
        return self._civs[civ].units[unit.id]

    def validate_tile(self, tile):
        """Return valid tile."""
        return self._grid.get_hextile(tile.coords)

    def handle_action(self, civ, action):
        """
        Handle incoming client-actions and update game state accordingly.

        :param action: The action to be processed.
        """
        # NOTE: Assume validation has already ocurred
        if isinstance(action, MovementAction):
            return self.handle_movement_action(civ, action)
        elif isinstance(action, CombatAction):
            return self.handle_combat_action(civ, action)
        elif isinstance(action, UpgradeAction):
            return self.handle_upgrade_action(civ, action)
        elif isinstance(action, BuildAction):
            return self.handle_build_action(civ, action)
        elif isinstance(action, PurchaseAction):
            return self.handle_purchase_action(civ, action)
        elif isinstance(action, BuildCityAction):
            return self.handle_build_city_action(civ, action)
        elif isinstance(action, ResearchAction):
            return self.handle_research_action(civ, action)
