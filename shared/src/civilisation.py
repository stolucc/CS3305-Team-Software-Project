"""Civilisation representation."""

from unit import Worker, Archer, Swordsman
from city import City
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
        """Return string representation of Civilisation."""
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
        if not tile.claimed and isinstance(worker, Worker):
            city = City(tile)
            tiles = self.grid.spiral_ring(tile, City.RANGE)
            city.tiles = tiles
            self.cities += [city]
        else:
            print("Unable to build city.")

    def start_civlisation(self, start_hex):
        """
        Create city, worker, archer, swordsman.

        City placed on start hex.Worker is placed on start_hex, Archer placed
        bottom right, Swordsman placed bottom left.

        :param start_hex: where to start Civilisation
        """
        worker = Worker(1, start_hex)
        archer = Archer(1, self.grid.get_neighbour_in_direction
                        (start_hex, 5))
        swordsman = Swordsman(1, self.grid.get_neighbour_in_direction
                              (start_hex, 4))
        self.units += [worker, archer, swordsman]
        self.build_city_on_tile(start_hex, worker)

    def build_structure(self, worker, building_type):
        """
        Build building at workers position.

        :param worker: worker unit
        """
        tile = worker.position
        if tile.building is None and tile.claimed is True:
            # Need to check if tile is claimed by your civilisation
            cost_of_building = 10
            if self.gold >= cost_of_building:
                self.gold -= cost_of_building
                building = Building(building_type, tile)
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
            self.units.remove(unit)

    def buy_worker(self, level, city):
        """
        Buy Worker.

        Worker will be placed on first tile near city that has no unit.

        :param level: int level of unit
        :param city: city to spawn worker at
        """
        cost_of_worker = 10 * level
        position = city.no_unit_tile()
        if self.gold >= cost_of_worker and position is not None:
            self.gold -= cost_of_worker
            worker = Worker(level, position)
            position.unit = worker
            self.units += [worker]
        else:
            print("Unable to purchase worker.")

    def buy_swordsman(self, level, city):
        """
        Buy Swordsman.

        Swordsman will be placed on first tile near city that has no unit.

        :param level: int level of unit
        :param city: city to spawn swordsman at
        """
        cost_of_swordsman = 20 * level
        position = city.no_unit_tile()
        if self.gold >= cost_of_swordsman and position is not None:
            self.gold -= cost_of_swordsman
            swordsman = Swordsman(level, position)
            position.unit = swordsman
            self.units += [swordsman]
        else:
            print("Unable to purchase swordsman.")

    def buy_archer(self, level, city):
        """
        Buy Archer.

        Archer will be placed on first tile near city that has no unit.

        :param level: int level of unit
        :param city: city to spawn archer at
        """
        cost_of_archer = 15 * level
        position = city.no_unit_tile()
        if self.gold >= cost_of_archer and position is not None:
            self.gold -= cost_of_archer
            archer = Archer(level, position)
            position.unit = archer
            self.units += [archer]
        else:
            print("Unable to purchase archer.")

    def cost_of_units(self):
        """
        Cost of all units per turn.

        :return: dict of costs
        """
        cost = {'gold': 0, 'food': 0, 'science': 0}
        for unit in self.units:
            cost['gold'] += unit.cost['gold']
            cost['food'] += unit.cost['food']
            cost['science'] += unit.cost['science']
        return cost

    def currency_of_buildings(self):
        """
        Currency generated by buildings eac turn.

        :return:
        """
        currency = {'gold': 0, 'food': 0, 'science': 0}
        for city in self.cities:
            for building in city.buildings:
                if building._type != BuildingType.CITY:
                    print(building)
                    print(building.currency)
