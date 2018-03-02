"""Civilisation representation."""

from unit import Worker, Swordsman, Unit, Archer
from city import City
from building import Building
from currency import CurrencyType
from researchtree import ResearchTree
import database_API


class Civilisation(object):
    """Civilisation class."""

    def __init__(self, identifier, grid, logger, session):
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
        self._session = session

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

    @property
    def tiles(self):
        return self._tiles

    def set_up(self, tile, worker_id):
        """
        Start civilisation.

        Create Worker.
        """
        worker_id = database_API.Unit.insert(self._session, self._id, 1, 0,
                                             100, tile.x, tile.y, tile.z)
        worker = Worker(worker_id, 1, tile, self._id)
        worker.actions = 2
        tile.unit = worker
        self.units[worker_id] = worker

    def build_city_on_tile(self, tile):
        """
        Build city on given tile.

        :param tile: hex tile to build city on
        """
        cost_of_city = 25
        unit = tile.unit
        if not tile.claimed and isinstance(unit, Worker)\
                and self.gold >= cost_of_city:
            city_id = database_API.Building.insert(self._session, self._id,
                                                   True, 3, tile.x, tile.y,
                                                   tile.z)
            city = City(city_id, tile)
            tiles = self.grid.spiral_ring(tile, City.RANGE)
            city.tiles = tiles
            self.gold -= cost_of_city
            unit.actions -= 1
            for tile in tiles:
                self._tiles[tile]= self._id
            self.cities[city.id] = city
        else:
            self._logger.debug("Unable to build city.")

    def build_structure(self, worker, building_type):
        """
        Build building at tiles position.

        :param tile: hex object
        """
        tile = worker.position
        if tile.building is None and isinstance(worker, Worker)\
                and tile.civ_id == worker.civ_id\
                and self.gold >= building_type.buy_cost()\
                and worker.actions > 0:
            bld_id = database_API.Building.insert(self._session, self._id,
                                                  True, Building.get_type
                                                  (building_type),
                                                  tile.x, tile.y, tile.z)
            building = Building(bld_id, building_type, tile, worker.civ_id)
            self.gold -= building.buy_cost
            tile.building = building
            worker.actions -= 1
        else:
            self._logger.debug("Unable to build structure.")

    def unlock_research(self, branch):
        """
        Unlock next node on research branch.

        branches = 'worker', 'archer', 'swordsman'.
        """
        if branch in self.tree.branches:
            if self.tree.next_unlock_node(branch).unlock_cost <= self.science:
                self.tree.unlock_tier(branch)
            else:
                print("Not enough Science points.")
        else:
            self._logger.debug("Branch not in research tree.")

    def unlock_research_win(self):
        """Unlock last node of researchh to win game."""
        if self.tree.end_node_unlockable():
            if self.science >= self.tree.win_node._unlock_cost:
                self.tree.unlock_end_node()

    def upgrade_unit(self, unit):
        """Upgrade unit."""
        if unit.level < self.tree.tier[unit.get_string()]:
            cost = unit.level * 10
            if self.gold >= cost and unit.actions > 0:
                unit.level_up()
                unit.actions -= 1
                database_API.Unit.update(self._session, unit._id,
                                         level=unit.level, health=unit.health)
            else:
                self._logger.debug("Not enough gold.")
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
                unit.movement -= movement_cost
                unit.position.unit = None
                unit.position = tile
                tile.unit = unit
                unit.actions -= 1
                database_API.Unit.update(self._session, unit.id, x=tile.x,
                                         y=tile.y, z=tile.z)
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
            database_API.Unit.update(self._session, enemy.id,
                                     health=enemy.health)
            if distance == 1 and isinstance(enemy, Swordsman):
                damage = enemy.attack_power()
                soldier.receive_damage(damage)
                self.is_dead(soldier)
                database_API.Unit.update(self._session, soldier.id,
                                         health=soldier.health)

    def is_dead(self, unit):
        """Check if unit is dead and remove references if True."""
        if unit.health == 0:
            unit.position.unit = None
            del unit.civilisation.units[unit.id]


    def buy_unit(self, identifier, city, unit_type, level):
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
            unit_id = database_API.Unit.insert(self._session, self._id, level,
                                               unit_type.get_type(),
                                               unit_type.get_health(level),
                                               position.x, position.y,
                                               position.z)
            unit = unit_type(unit_id, level, position, self)
            self.gold -= unit.gold_cost(level)
            position.unit = unit
            self.units[unit_id] = unit
        else:
            self._logger.debug("Unable to purchase unit.")

    def reset_unit_actions(self):
        """Reset the actions units can take per turn."""
        actions_per_turn = 2
        for unit in self._units:
            self._units[unit].actions = actions_per_turn

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

    def handle_action(self, action):
        """
        Handle incoming client-actions and update game state accordingly.

        :param action: The action to be processed.
        """
        # NOTE: Assume validation has already ocurred
        if action.type == "MovementAction":
            self.move_unit_to_hex(action.unit, action.destination)
        elif action.type == "CombatAction":
            self.attack_unit(action.attacker, action.defender)
        elif action.type == "UpgradeAction":
            self.upgrade_unit(action.unit)
        elif action.type == "BuildAction":
            self.build_structure(action.unit, action.building_type)
        elif action.type == "PurchaseAction":
            self.buy_unit(action.building, action.unit_type, action.level)
