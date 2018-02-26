"""Civilisation representation."""

from unit import Worker, Swordsman, Unit
from city import City
from building import Building
from currency import CurrencyType


class Civilisation(object):
    """Civilisation class."""

    def __init__(self, identifier, grid):
        """
        Initialise Civilisation attributes.

        :param grid: hex grid that game is using
        """
        self._id = identifier
        self._grid = grid
        self._units = {}
        self._cities = {}
        self._gold = 100
        self._food = 100
        self._science = 100

    def __repr__(self):
        """Return string representation of Civilisation."""
        string = "Cities: %i, Units: %i, Gold: %i, Food: %i, Science: %i" \
                 % (len(self.cities), len(self.units), self._gold, self._food,
                    self._science)
        return string

    @property
    def id(self):
        """Return civilisation unique ID."""
        return self._id

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

    def set_up(self, start_tile, city_id, worker_id):
        """
        Start civilisation.

        Build city on start hex. Create Worker.
        """
        city = City(city_id, start_tile)
        tiles = self.grid.spiral_ring(start_tile, City.RANGE)
        city.tiles = tiles
        self.cities[city.id] = city
        worker = Worker(worker_id, 1, city.no_unit_tile(), self)
        worker.position.unit = worker
        self.units[worker_id] = worker

    def build_city_on_tile(self, identifier, tile):
        """
        Build city on given tile.

        :param tile: hex tile to build city on
        """
        cost_of_city = 25
        if not tile.claimed and isinstance(tile.unit, Worker)\
                and self.gold >= cost_of_city:
            self.gold -= cost_of_city
            city = City(identifier, tile)
            tiles = self.grid.spiral_ring(tile, City.RANGE)
            city.tiles = tiles
            self.cities[city.id] = city
        else:
            print("Unable to build city.")

    def build_structure(self, identifier, tile, building_type):
        """
        Build building at tiles position.

        :param tile: hex object
        """
        if tile.building is None and isinstance(tile.unit, Worker) \
                and tile.claimed is True:
            # TODO Need to check if tile is claimed by your civilisation
            building = Building(identifier, building_type, tile)
            if self.gold >= building.buy_cost:
                self.gold -= building.buy_cost
                tile.building = building
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
                unit.movement -= movement_cost
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

    def attack_unit(self, soldier, enemy):
        """
        Attack enemy unit with Archer or Swordsman.

        :param soldier: Soldier unit of player
        :param enemy: enemy unit of opponent
        """
        distance = self.grid.hex_distance(soldier.position, enemy.position)
        if soldier.attack_range >= distance:
            damage = soldier.attack_power()
            enemy.receive_damage(damage)
            self.is_dead(enemy)
            if distance == 1 and isinstance(enemy, Swordsman):
                damage = enemy.attack_power()
                soldier.receive_damage(damage)
                self.is_dead(soldier)

    def is_dead(self, unit):
        """Check if unit is dead and remove references if True."""
        if unit.health == 0:
            unit.position.unit = None
            del unit.civilisation.units[unit.id]

    def buy_unit(self, identifier, level, city, unit_type):
        """
        Buy unit.

        Unit will be placed on first tile near city that has no unit.

        :param level: int level of unit
        :param city: city to spawn worker at
        :param unit_type: Worker, Archer, or Swordsman class
        """
        if issubclass(unit_type, Unit):
            position = city.no_unit_tile()
            unit = unit_type(identifier, level, position, self)
            if self.gold >= unit.buy_cost and position is not None:
                self.gold -= unit.buy_cost
                position.unit = unit
                self.units[unit.id] = unit
            else:
                print("Unable to purchase worker.")
        else:
            print("Unable to purchase worker.")

    def currency_per_turn(self):
        """Update Gold, Food, and Science per turn."""
        currency = self.currency_of_buildings()
        cost = self.cost_of_units()
        self.gold += currency['gold'] - cost['gold']
        self.food += currency['food'] - cost['food']
        self.science += currency['science'] - cost['science']

    def cost_of_units(self):
        """
        Cost of all units per turn.

        :return: dict of costs
        """
        cost = {'gold': 0, 'food': 0, 'science': 0}
        for unit_id in self.units:
            unit = self.units[unit_id]
            cost['gold'] += unit.cost['gold']
            cost['food'] += unit.cost['food']
            cost['science'] += unit.cost['science']
        return cost

    def currency_of_buildings(self):
        """
        Currency generated by buildings eac turn.

        :return: dict of currency
        """
        currency = {'gold': 0, 'food': 0, 'science': 0}
        for city_id in self.cities:
            buildings = self.cities[city_id].buildings
            for building in buildings:
                if building._type is not False:
                    currency['gold'] += building.currency[CurrencyType.GOLD]
                    currency['food'] += building.currency[CurrencyType.FOOD]
                    currency['science'] += \
                        building.currency[CurrencyType.SCIENCE]
        return currency
