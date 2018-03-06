"""Civilisation representation."""

from unit import Worker, Swordsman, Unit
from city import City
from building import Building
from currency import CurrencyType
from researchtree import ResearchTree
from mapresource import ResourceType


class Civilisation(object):
    """Civilisation class."""

    def __init__(self, identifier, grid, logger):
        """
        Initialise Civilisation attributes.

        :param grid: hex grid that game is using
        """
        self._id = identifier
        self._grid = grid
        self._units = {}
        self._cities = {}
        self._tiles = {}
        self._gold = 100
        self._food = 100
        self._science = 0
        self._tree = ResearchTree(self)
        self._logger = logger
        self._vision = []

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
    def resources(self):
        """Getter for all resources available to civ."""
        values = {}
        for resource in list(ResourceType):
            values[resource] = 0
        for key, city in self._cities.items():
            for resource in list(ResourceType):
                values[resource] += city.resources
        return values

    @property
    def grid(self):
        """
        Grid that game is using.

        :return: grid object.
        """
        return self._grid

    @property
    def vision(self):
        """
        List of tiles that the civ can see.

        :return: list of hex object
        """
        return self._vision

    @property
    def tiles(self):
        """
        List of tiles that the civ owns.

        :return: list of hex object
        """
        return self._tiles

    def set_up(self, tile, worker_id):
        """
        Start civilisation.

        Create Worker.
        """
        worker = Worker(worker_id, 1, tile, self._id)
        worker.actions = 2
        tile.unit = worker
        self.units[worker_id] = worker

    def build_city_on_tile(self, worker, city_id):
        """
        Build city on given tile.

        :param tile: hex tile to build city on
        """
        cost_of_city = 25
        tile = worker.position
        if tile.civ_id is None and isinstance(worker, Worker)\
                and self.gold >= cost_of_city:
            city = City(city_id, tile, self._id)
            tiles = self.grid.spiral_ring(tile, City.RANGE)
            city.tiles = tiles
            self.gold -= cost_of_city
            worker.actions -= 1
            for tile in tiles:
                self.tiles[tile] = self._id
            self.cities[city.id] = city
        else:
            self._logger.debug("Unable to build city.")

    def build_structure(self, worker, building_type, building_id):
        """
        Build building at tiles position.

        :param tile: hex object
        """
        tile = worker.position
        if tile.building is None and isinstance(worker, Worker)\
                and tile.civ_id == worker.civ_id\
                and self.gold >= Building.buy_cost(building_type)\
                and worker.actions > 0:
            city_id = tile.city_id
            building = Building(building_id, building_type, tile,
                                worker.civ_id, city_id)
            self.gold -= Building.buy_cost(building_type)
            tile.building = building
            self.cities[city_id].buildings[building_id] = building
            worker.actions -= 1
        else:
            self._logger.debug("Unable to build structure.")

    def unlock_research(self, node_id):
        """
        Unlock node on research tree.

        Nodes ID go from 0-9.
        :param node_id: int ID of research node
        """
        node = self._tree._nodes[node_id]
        if node.unlock_cost <= self.science and self._tree.unlockable(node_id):
            self.science -= node.unlock_cost
            self._tree.unlock_node(node_id)
        else:
            self._logger.debug("Unable to unlock research node.")

    def upgrade_unit(self, unit):
        """
        Upgrade unit.

        :param unit: Unit object that is to be levelled up
        """
        if unit.level < self.tree.tier[unit.get_string()]:
            cost = unit.level * 10
            if self.gold >= cost and unit.actions > 0:
                unit.level_up()
                unit.actions -= 1
            else:
                self._logger.debug("Unable to upgrade unit.")
        else:
            self._logger.debug("Unable to upgrade unit.")

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
            if unit.movement_range >= movement_cost and unit.actions > 0:
                pos = unit.position
                unit.movement -= movement_cost
                unit.position.unit = None
                unit.position = tile
                tile.unit = unit
                pos.unit = None
                unit.actions -= 1
            else:
                self._logger.debug("Unable to move unit.")
        else:
            self._logger.debug("Tile already has unit.")

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
        if soldier.attack_range >= distance and soldier.actions > 0:
            damage = soldier.attack_power()
            enemy.receive_damage(damage)
            self.is_dead(enemy)
            soldier.actions -= 1
            if distance == 1 and isinstance(enemy, Swordsman):
                damage = enemy.attack_power()
                soldier.receive_damage(damage)
                self.is_dead(soldier)

    def is_dead(self, unit):
        """Check if unit is dead and remove references if True."""
        if unit.health == 0:
            unit.position.unit = None
            del unit.civilisation.units[unit.id]

    def buy_unit(self, city, unit_type, level, unit_id):
        """
        Buy unit.

        Unit will be placed on first tile near city that has no unit.

        :param level: int level of unit
        :param city: city to spawn worker at
        :param unit_type: Worker, Archer, or Swordsman class
        """
        position = city.no_unit_tile()
        if issubclass(unit_type, Unit) and self.gold >= \
                unit_type.gold_cost(level) and position is not None:
            unit = unit_type(unit_id, level, position, self)
            self.gold -= unit.gold_cost(level)
            position.unit = unit
            self.units[unit_id] = unit
            return unit
        else:
            self._logger.debug("Unable to purchase unit.")

    def per_turn(self):
        """Amount of actions to be taken per turn."""
        self.reset_unit_actions_and_movement()
        self.currency_per_turn()

    def reset_unit_actions_and_movement(self):
        """Reset the actions units can take per turn."""
        actions_per_turn = 2
        for unit in self._units:
            unit = self._units[unit]
            unit.actions = actions_per_turn
            unit.movement = unit.movement_range

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
                building = buildings[building]
                if building._type is not False:
                    currency['gold'] += building.currency[CurrencyType.GOLD]
                    currency['food'] += building.currency[CurrencyType.FOOD]
                    currency['science'] += \
                        building.currency[CurrencyType.SCIENCE]
        return currency

    def calculate_vision(self):
        """Determine the tiles visible to the civilisation."""
        vision = set()
        for unit_id in self._units:
            unit = self._units[unit_id]
            vision_range = 5  # TODO: Replace with unit vision range
            tile = unit.position
            unit_vision = self._grid.vision(tile, vision_range)
            vision |= set(unit_vision)

        for city_id in self.cities:
            buildings = self.cities[city_id].buildings
            for building in buildings:
                vision_range = 2
                tile = buildings[building].position
                building_vision = self._grid.vision(tile, vision_range)
                vision |= set(building_vision)
        self._vision = vision
