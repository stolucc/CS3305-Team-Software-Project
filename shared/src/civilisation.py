import unit
from city import City
from currency import Currency
from mapresource import ResourceType
from hexgrid import Hex, Grid
from building import Building, BuildingType


class Civilisation(object):
    """Civilisation class."""

    def __init__(self, grid):
        """
        Initialise Civilisation attributes.

        :param grid: hex grid that game is using
        """
        self._grid = grid
        self._units = []
        self._cities = []
        self._gold = 100
        self._food = 100
        self._science = 0

    def __repr__(self):
        """String representation of Civilisation."""
        string = "Cities: %i, Units: %i, Gold: %i, Food: %i, Science: %i" \
                 % (len(self.cities), len(self.units), self._gold, self._food,
                    self._science)
        return string

    @property
    def units(self):
        """
        List of units owned by civilisation.

        :return: list of all units.
        """
        return self._units

    @units.setter
    def units(self, units):
        """
        Add unit to list of units.

        :param unit: Unit object to add
        """
        self._units = units

    @property
    def cities(self):
        """
        List of cities owned by civilisation.

        :return: list of all cities.
        """
        return self._cities

    @cities.setter
    def cities(self, cities):
        """
        Add city to list of cities.

        :param city: City object to add
        """
        self._cities = cities

    @property
    def gold(self):
        """
        Gold of civilisation.

        :return: int.
        """
        return self._gold

    @gold.setter
    def gold(self, gold):
        """
        Set Gold of civilisation.

        :param gold: int.
        """
        self._gold = gold

    @property
    def food(self):
        """
        Food of civilisation.

        :return: int.
        """
        return self._food

    @food.setter
    def food(self, food):
        """
        Set Food of civilisation.

        :param food: int.
        """
        self._food = food

    @property
    def science(self):
        """
        Science of civilisation.

        :return: int.
        """
        return self._science

    @science.setter
    def science(self, science):
        """
        Set Science of civilisation.

        :param science: int.
        """
        self._science = science

    @property
    def grid(self):
        """
        Grid that game is using.

        :return: grid object.
        """
        return self._grid

    def build_city_on_tile(self, tile, worker):
        """
        Build city on given tile.

        :param tile: hex tile to build city on
        :param grid: grid that is being used
        """
        if not tile.claimed and isinstance(worker, unit.Worker):
            city = City(tile)
            tiles = self.grid.spiral_ring(tile, City.RANGE)
            city.tiles = tiles
            self.cities += [city]
        else:
            print("Tile is claimed, unable to build city.")

    def start_civlisation(self, start_hex):
        """
        Create city, worker, archer, swordsman.

        :param start_hex: where to start Civilisation
        """
        worker = unit.Worker(1, start_hex)
        archer = unit.Archer(1, self.grid.get_neighbour_in_direction
                             (start_hex, 5))
        swordsman = unit.Swordsman(1, self.grid.get_neighbour_in_direction
                                   (start_hex, 4))
        self.units += [worker, archer, swordsman]
        self.build_city_on_tile(start_hex, worker)

    def build_farm(self, worker):
        """
        Build farm at workers position.

        :param worker: worker unit
        """
        tile = worker.position
        if tile.building is None and tile.claimed is True:
            # Need to check if tile is claimed by your civilisation
            cost_of_farm = 10
            if self.gold >= cost_of_farm:
                self.gold -= cost_of_farm
                farm = Building(BuildingType.FARM, tile)
                tile.building = farm
            else:
                print("Not enough money.")
        else:
            print("Cannot build here.")

    def move_unit_to_hex(self, unit, tile):
        """
        Move unit to tile.

        :param unit: unit to move
        :param tile: tile to move to
        """
        if tile.unit is None:
            path = self.grid.shortest_path(unit.position, tile,
                                           unit.movement_range)
            movement_cost = self.movement_cost_of_path(path)
            if unit.movement_range >= movement_cost:
                unit.position = tile
                tile.unit = unit
            else:
                print("Units movement range is not enough.")
        else:
            print("Tile already has unit.")

    def movement_cost_of_path(self, path):
        """Calculate movement cost of list of hex tiles."""
        movement_cost = 0
        for hex in path:
            movement_cost += hex.terrain.calculate_movement_cost()
        return movement_cost

    def update_currency(self):
        """Update currency based on units and buildings."""
        unit_costs = self.get_cost_of_units()
        if self._gold < 0:
            self._gold = 0
        if self._food < 0:
            self._food = 0
        if self._science < 0:
            self._science = 0

    def get_currency_of_cities(self):
        city_currency = {'food': 0, 'gold': 0, 'science': 0}
        for city in self.cities:
            print(city)
            print(city.currency)

    def get_cost_of_units(self):
        """
        Get costs of all units in civilisation.

        :return: dict of costs
        """
        unit_costs = {'food': 0, 'gold': 0, 'science': 0}
        for unit in self.units:
            unit_costs['gold'] += unit.cost['gold']
            unit_costs['food'] += unit.cost['food']
            unit_costs['science'] += unit.cost['science']
        return unit_costs
