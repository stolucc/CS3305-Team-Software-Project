"""Game state representation."""


class GameState:
    """Game state class."""

    def __init__(self, game_id, seed, grid, logger):
        """
        Initialise GameState attributes.

        :param game_id: hex grid that game is using
        :param seed: hex grid that game is using
        :param grid: hex grid that game is using
        """
        self._logger = logger
        self._game_id = game_id
        self._seed = seed
        self._grid = grid
        self._civs = {}
        self._my_id = None
        self._turn_count = 1
        self._current_player = None
        self._game_started = False
        self._orphaned_buildings = []

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

    @property
    def civs(self):
        """
        Getter for civs.

        :return: civs
        """
        return self._civs

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

    def set_player_turn(self, current_player):
        """Update the person whose turn it is."""
        self._current_player = current_player

    @property
    def current_player(self):
        """Who holds current turn."""
        return self._current_player

    @property
    def my_turn(self):
        """Getter True if this is my turn."""
        return self._my_id == self._current_player

    def removed_orphaned_buildings(self, civ):
        """Remove orphaned buildings."""
        for building in self._orphaned_buildings:
            if building._civ_id == civ:
                building._hex._building = None
