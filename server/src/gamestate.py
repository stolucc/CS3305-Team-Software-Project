"""Game state representation."""

import database_API
from civilisation import Civilisation
from action import ServerError, GAME_FULL_ERROR, UNKNOWN_ACTION, \
    StartTurnUpdate
from unit import Worker
import random
from queue import Queue


class GameState:
    """Game state class."""

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
        self._turn_count = 1
        self._current_player = None
        self._game_started = False
        self._queues = {}

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

    def handle_action(self, message):
        """
        Handle an action sent by a client.

        :param messag: The message object received from the client
        :return: The value to be sent back to the client
        """
        civ_actions = ["MovementAction", "CombatAction", "UpgradeAction",
                       "BuildAction", "PurchaseAction"]

        if message.type == "CheckForUpdates":
            return self.update_player(message)

        if message.id == self._current_player:
            self._logger.debug(message)
            if message.type == "JoinGameAction":
                return self.add_player(message)
            elif message.type == "LeaveGameAction":
                return self.remove_player(message)
            elif message.type == "EndTurnAction":
                return self.end_turn(message)
            elif message.type in civ_actions:
                result_set = self._civs[message.id].handle_action(message.obj)
        err = ServerError(UNKNOWN_ACTION)
        self._logger.error(err)
        return err

    def add_player(self, message):
        """
        Add a new player to the game.

        :param message: The message object sent from the client.
        :return: The id of the new player
        """
        start_locations = [(0, 0, 0), (50, -25, -25),
                           (-50, 25, 25), (25, -50, 25)]
        if len(self._civs) < 4:
            user_id = database_API.User.insert(self._session,
                                               self._game_id,
                                               active=True, gold=100,
                                               food=100, science=0,
                                               production=0)
            self.add_civ(Civilisation(user_id, self._grid, self._logger,
                         self._session))
            self._logger.info("New Civilisation joined with id " +
                              str(user_id))
            # NOTE: Not needed when loading from db
            location = random.choice(start_locations)
            del start_locations[start_locations.index(location)]
            unit_id = database_API.Unit.insert(self._session, user_id, 1,
                                               0, Worker.get_health(1),
                                               *location)
            self._civs[user_id].set_up(self._grid.get_hextile(location),
                                       unit_id)
            self._queues[user_id] = Queue()
            # TODO: Inform client of worker

            if(len(self._civs) == 4):
                self._game_started = True
                self._turn_count = 1
                self._current_player = list(self._civs.keys())[0]
                start_turn_update = StartTurnUpdate(self._current_player,
                                                    self._turn_count)
                for key in self._queues:
                    self._queues[key].put(start_turn_update)
                # TODO: Tell Clients game has begun and who's turn it is

            return self.game_id, user_id
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
        next_civ_index = (current_civ_index + 1) % 4
        next_civ = civs[next_civ_index]
        self._current_player = next_civ
        if next_civ_index == 0:
            self._turn_count += 1
        start_turn_update = StartTurnUpdate(self._current_player,
                                            self._turn_count)
        for key in self._queues:
            self._queues[key].put(start_turn_update)

    def set_player_turn(self, current_player):
        """Update the person whose turn it is."""
        self._current_player = current_player

    def handle_action(self, civ, action):
        """
        Handle incoming client-actions and update game state accordingly.

        :param action: The action to be processed.
        """
        # NOTE: Assume validation has already ocurred
        if action.type == "MovementAction":
            self.move_unit_to_hex(action.unit, action.destination)
            return [action.unit.location, action.destination]
        elif action.type == "CombatAction":
            self.attack_unit(action.attacker, action.defender)
            return [action.attacker, action.defender]
        elif action.type == "UpgradeAction":
            self.upgrade_unit(action.unit)
            return [action.unit]
        elif action.type == "BuildAction":
            self.build_structure(action.unit, action.building_type)
            return [action.unit.location]
        elif action.type == "PurchaseAction":
            return [self.buy_unit(action.building,
                                  action.unit_type, action.level)]