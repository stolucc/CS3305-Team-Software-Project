"""Game state representation."""

import database_API
from civilisation import Civilisation
from action import ServerError, GAME_FULL_ERROR, UNKNOWN_ACTION
from unit import Worker
import random


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
        civ_actions = ["MovementAction", "CombatAction", "UpgradeAction",
                       "BuildAction", "PurchaseAction"]
        self._logger.debug(message)
        if message.type == "JoinGameAction":
            return self.add_player(message)
        elif message.type == "LeaveGameAction":
            return self.remove_player(message)
        elif message.type in civ_actions:
            self._civs[message.id].handle_action(message.obj)
        err = ServerError(UNKNOWN_ACTION)
        self._logger.error(err)
        return err

    def add_player(self, message):
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
            # TODO: Inform client of worker
            return user_id
        else:
            err = ServerError(GAME_FULL_ERROR)
            self._logger.error(err)
            return err

    def remove_player(self, message):
        user_id = message.id
        del self._civs[user_id]
        database_API.User.update(self._session, user_id, active=False)
        return True
