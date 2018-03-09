"""Civilisation representation."""

from unit import Worker, Swordsman, Soldier, Unit
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
        self._vision = {}

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
    def tree(self):
        """
        Getter for tree.

        :return: Research Tree.
        """
        return self._tree

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
        unit_cost = self.unit_resource_cost()
        for key, city in self._cities.items():
            for resource in list(ResourceType):
                values[resource] += city.resources[resource]
                values[resource] -= unit_cost[resource]
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
    def visions(self):
        """
        List of tiles that the civ can see.

        :return: list of hex object
        """
        return self._visions

    @property
    def tiles(self):
        """
        List of tiles that the civ owns.

        :return: list of hex object
        """
        return self._tiles

    @property
    def buildings(self):
        """
        Research Tree of civilisation.

        :return: Research tree
        """

    def set_up(self, tile, worker_id):
        """
        Start civilisation.

        Create Worker.
        """
        worker = Worker(worker_id, 1, tile, self._id)
        worker.actions = 2
        tile.unit = worker
        self.units[worker_id] = worker

    def get_building(self, bld_id):
        """Get building from building ID."""
        for city_id in self._cities:
            city = self._cities[city_id]
            if bld_id in city._buildings:
                return city._buildings[bld_id]

    def build_city_on_tile(self, worker, city_id):
        """
        Build city on given tile.

        :param tile: hex tile to build city on
        """
        cost_of_city = 25
        tile = worker.position
        if tile.civ_id is None and isinstance(worker, Worker)\
                and self.gold >= cost_of_city and worker.actions > 0:
            city = City(city_id, tile, self._id)
            tiles = self.grid.spiral_ring(tile, City.RANGE)
            city.tiles = tiles
            self.gold -= cost_of_city
            worker.actions -= 1
            for tile in tiles:
                self.tiles[tile] = self._id
            self.cities[city.id] = city
            return tiles
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
                and self.gold >= Building.buy_cost(building_type)[CurrencyType.
                                                                  GOLD]\
                and self.resources[ResourceType.GEMS] >=\
                Building.buy_cost(building_type)[ResourceType.GEMS]\
                and worker.actions > 0:
            city_id = tile.city_id
            building = Building(building_id, building_type, tile,
                                worker.civ_id, city_id)
            self.gold -= Building.buy_cost(building_type)[CurrencyType.GOLD]
            tile.building = building
            self.cities[city_id].buildings[building_id] = building
            worker.actions -= 1
            return True
        else:
            self._logger.debug("Unable to build structure.")
        return False

    def unlock_research(self, branch):
        """
        Unlock node on research tree.

        Nodes ID go from 0-9.
        :param node_id: int ID of research node
        """
        node = self._tree.get_next_unlockable()
        if node is not None and node.unlock_cost <= self.science:
            self.science -= node.unlock_cost
            self._tree.unlock_node(branch, node)
        else:
            self._logger.debug("Unable to unlock research node.")

    def upgrade_unit(self, unit):
        """
        Upgrade unit.

        :param unit: Unit object that is to be levelled up
        """
        if unit.level < self.tree._tier[unit.get_string()]:
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
                if tile.city_id is not None and isinstance(unit, Soldier)\
                        and tile.civ_id != unit._civ_id and\
                        isinstance(tile.building, City):
                    return self.destroy_city(tile)
            else:
                self._logger.debug("Unable to move unit.")
        else:
            self._logger.debug("Tile already has unit.")

    def destroy_building(self, tile):
        """Remove references for buildings."""
        tile._building = None
        tile._city_id = None
        tile._civ_id = None

    def destroy_city(self, tile):
        """Remove all references for the city and its buildings."""
        city_tiles = self._grid.spiral_ring(tile, 4)
        for city_tile in city_tiles:
            if city_tile.city_id == tile.city_id:
                self.destroy_building(city_tile)
            if city_tile.terrain.resource is not None:
                city_tile.terrain.resource.stop_work()
        self.destroy_building(tile)
        return city_tiles

    def destroy_civilisation(self):
        """Remove all references for this civilisation."""
        for unit_id in self._units:
            unit = self._units[unit_id]
            unit.position.unit = None
            unit.position = None
        for city_id in self._cities:
            city_tile = self._cities[city_id].position
            self.destroy_city(city_tile)

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
        if soldier.attack_range >= distance and soldier.actions > 0\
                and soldier.civ_id != enemy.civ_id:
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
            if unit.id in self.units:
                del self.units[unit.id]

    def buy_unit(self, city, unit_type, level, unit_id):
        """
        Buy unit.

        Unit will be placed on first tile near city that has no unit.

        :param level: int level of unit
        :param city: city to spawn worker at
        :param unit_type: Worker, Archer, or Swordsman class
        """
        position = city.position
        if issubclass(unit_type, Unit) and self.gold >= \
                unit_type.gold_cost(level) and position is not None:
            unit = unit_type(unit_id, level, position, self._id)
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

    def unit_resource_cost(self):
        """Calculate resource cost of higher level units."""
        cost = {}
        for resource in list(ResourceType):
            cost[resource] = 0
        for unit in self._units:
            if self._units[unit].level > 1:
                cost[self._units[unit].resource_cost()] += 1
        return cost

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
        Currency generated by buildings each turn.

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
        self._vision = {}
        for unit_id in self._units:
            unit = self._units[unit_id]
            vision_range = 3  # TODO: Replace with unit vision range
            tile = unit.position
            unit_vision = self._grid.vision(tile, vision_range)
            vision |= set(unit_vision)

        for city_id in self.cities:
            city = self.cities[city_id]
            buildings = city.buildings
            vision |= set(self._grid.vision(city.position, 3))
            for building in buildings:
                vision_range = 2
                tile = buildings[building].position
                building_vision = self._grid.vision(tile, vision_range)
                vision |= set(building_vision)
        for tile in vision:
            self._vision[tile] = tile
