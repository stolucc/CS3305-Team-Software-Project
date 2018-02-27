"""Game state representation."""

import database_API
from civilisation import Civilisation
from action import ServerError, GAME_FULL_ERROR, UNKNOWN_ACTION

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
        self._logger.debug(message)
        if message.type == "JoinGameAction":
            if len(self._civs) < 4:
                user_id = database_API.User.insert(self._session,
                                                   self._game_id,
                                                   active=True, gold=100,
                                                   food=100, science=0,
                                                   production=0)
                self.add_civ(Civilisation(user_id, self._grid))
                self._logger.info("New Civilisation joined with id " +
                                  str(user_id))
                return user_id
            else:
                err = ServerError(GAME_FULL_ERROR)
                self._logger.error(err)
                return err
        err = ServerError(UNKNOWN_ACTION)
        self._logger.error(err)
        return err
