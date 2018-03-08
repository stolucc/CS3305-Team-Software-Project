"""Civilisation unit testing"""

import unittest

from building import BuildingType
from civilisation import *
from file_logger import Logger
from hexgrid import Grid, Hex
from terrain import Terrain, TerrainType, BiomeType
from unit import Archer

grid = Grid(10)
logger = Logger("log.txt", "logger", "1")


class CivilisationTest(unittest.TestCase):
    """Unittest class for civilisation"""

    def test_civilisation_constructor(self):
        """Test the constructor for the civilisation class."""

        civ = Civilisation("myCiv", grid, logger)
        tree = civ._tree

        self.assertEqual(civ._id, "myCiv")
        self.assertEqual(civ._grid, grid)
        self.assertEqual(civ._logger, logger)
        self.assertEqual(civ._units, {})
        self.assertEqual(civ._cities, {})
        self.assertEqual(civ._tiles, {})
        self.assertEqual(civ._food, 100)
        self.assertEqual(civ._gold, 100)
        self.assertEqual(civ._science, 0)
        self.assertEqual(civ._tree, tree)
        self.assertEqual(civ._vision, {})

    def test_set_up(self):
        """Test the set_up function."""

        hextile = Hex(0, 0, 0)
        civ = Civilisation("myCiv", grid, logger)

        civ.set_up(hextile, "worker")
        worker = civ.units["worker"]

        self.assertEqual(worker.actions, 2)
        self.assertEqual(hextile.unit, worker)
        self.assertEqual(civ.units["worker"], worker)

    def test_build_city_on_tile(self):
        """Test the build_city_on_tile function."""

        hextile = Hex(0, 0, 0)
        civ = Civilisation("myCiv", grid, logger)
        worker = Worker("worker", 1, hextile, 1)

        grid.create_grid()

        gold = civ.gold
        actions = worker.actions

        civ.build_city_on_tile(worker, 1)

        city = civ.cities[1]

        self.assertEqual(civ.gold, gold - 25)
        self.assertEqual(worker.actions, actions - 1)
        self.assertEqual(civ.cities[1], city)
        self.assertEqual(civ.tiles[worker.position], civ._id)

    def test_build_structure(self):
        """Test the build_structure function."""
        grid.create_grid()
        hextile = Hex(0, 0, 0)
        civ = Civilisation("myCiv", grid, logger)
        worker = Worker("worker", 1, hextile, "myCiv")
        worker.actions = 2

        grid.create_grid()
        gold = civ.gold
        actions = worker.actions

        civ.build_city_on_tile(worker, 1)
        hextile2 = grid.get_neighbour_in_direction(hextile, 2)
        worker.position = hextile2

        civ.build_structure(worker, BuildingType.UNIVERSITY, 1)
        building = civ.cities[hextile.city_id].buildings[1]

        # a city had to be built before the university so both costs
        # must be deducted from the total gold and actions
        self.assertEqual(civ.gold, gold - 35)
        self.assertEqual(worker.actions, actions - 2)
        self.assertEqual(worker.position.building, building)

    def test_unlock_research(self):
        """Test the unlock_research function."""
        hextile = Hex(0, 0, 0)
        civ = Civilisation("myCiv", grid, logger)
        civ.science = 50
        civ.unlock_research(1)

        self.assertEqual(civ._tree._nodes[1].unlocked, True)

    def test_upgrade_unit(self):
        """Test the upgrade_unit method."""
        civ = Civilisation("myCiv", grid, logger)
        civ.unlock_research(3) #archer upgrade
        hextile = Hex(0, 0, 0)
        archer = Archer(1, 1, "myCiv", hextile)
        archer.actions = 2
        civ.upgrade_unit(archer)

        self.assertEqual(archer.level, 2)
        self.assertEqual(archer.actions, 1)

    def test_move_unit_to_hex(self):
        """Test the move_unit_to_hex method"""
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        hextile2 = Hex(1, 0, -1)
        archer = Archer(1, 1, hextile, "myCiv")
        archer.actions = 2
        civ.move_unit_to_hex(archer, hextile2)

        self.assertEqual(archer.position, hextile2)
        self.assertEqual(archer.actions, 1)

    def test_movement_cost_of_path(self):
        """Tests the movement_cost_of_path function"""
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        hextile2 = Hex(1, 0, -1)
        hextile3 = Hex(1, 1, -2)
        hextile._terrain = Terrain(TerrainType.FLAT, BiomeType.GRASSLAND)
        hextile2._terrain = Terrain(TerrainType.HILL, BiomeType.GRASSLAND)
        hextile3._terrain = Terrain(TerrainType.HILL, BiomeType.DESERT)
        # costs are 1, 2 and 3 respectively
        hexes = [hextile, hextile2, hextile3]
        archer = Archer(1, 1, hextile, "myCiv")
        archer.actions = 2
        cost = civ.movement_cost_of_path(hexes)

        self.assertEqual(cost, 6)

    def test_attack_unit(self):
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        archer = Archer(1, 1, hextile, "myCiv")
        hextile2 = Hex(1, 0, -1)
        archer.actions = 2
        swordsman = Swordsman(1, 1, hextile2, "notMyCiv")
        civ.attack_unit(archer, swordsman)

        self.assertEqual(swordsman.health, 110)
        self.assertEqual(round(archer.health), 85)
        self.assertEqual(archer.actions, 1)

    def test_is_dead(self):
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        archer = Archer(1, 1, hextile, "myCiv")
        archer.health = 0
        civ.units[archer.id] = archer
        archer._civilisation = civ
        civ.is_dead(archer)

        self.assertEqual(archer.health, 0)
        self.assertNotIn(archer, civ.units)

    def test_buy_unit(self):
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        worker = Worker("worker", 1, hextile, "myCiv")
        worker.actions = 5
        civ.units[worker.id] = worker

        grid.create_grid()
        civ.build_city_on_tile(worker, 1)
        city = civ.cities[1]
        unit = civ.buy_unit(city, Archer, 1, 1)

        self.assertEqual(civ.units[1], unit)
        self.assertEqual(unit._civilisation, civ)
        self.assertEqual(civ.gold, 65)

    def test_per_turn(self): # tbc
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        worker = Worker("worker", 1, hextile, "myCiv")
        civ.units[worker.id] = worker
        archer = Archer(1, 1, hextile, "myCiv")
        civ.units[archer.id] = archer
        civ.reset_unit_actions_and_movement()

        grid.create_grid()
        civ.build_city_on_tile(worker, 1)
        hextile2 = grid.get_neighbour_in_direction(hextile, 2)
        worker.position = hextile2
        civ.build_structure(worker, BuildingType.UNIVERSITY, 1)

        civ.reset_unit_actions_and_movement()

        hextile3 = grid.get_neighbour_in_direction(hextile, 4)
        worker.position = hextile3
        civ.build_structure(worker, BuildingType.FARM, 2)

        civ.reset_unit_actions_and_movement()
        civ.currency_per_turn()

        self.assertEqual(archer.actions, 2)
        self.assertEqual(worker.actions, 2)
        self.assertEqual(archer.movement, 5)
        self.assertEqual(worker.movement, 4)

        self.assertEqual(civ.food, 99)
        self.assertEqual(civ.gold, 51)
        self.assertEqual(civ.science, 5)

    def test_reset_unit_actions_and_movement(self):
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        worker = Worker("worker", 1, hextile, "myCiv")
        civ.units[worker.id] = worker
        archer = Archer(1, 1, hextile, "myCiv")
        civ.units[archer.id] = archer

        civ.reset_unit_actions_and_movement()

        self.assertEqual(archer.actions, 2)
        self.assertEqual(worker.actions, 2)
        self.assertEqual(archer.movement, 5)
        self.assertEqual(worker.movement, 4)

    def test_currency_per_turn(self):
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        worker = Worker("worker", 1, hextile, "myCiv")
        worker.actions = 5
        civ.units[worker.id] = worker
        archer = Archer(1, 1, hextile, "myCiv")
        civ.units[archer.id] = archer

        grid.create_grid()
        civ.build_city_on_tile(worker, 1)
        hextile2 = grid.get_neighbour_in_direction(hextile, 2)
        worker.position = hextile2
        civ.build_structure(worker, BuildingType.UNIVERSITY, 1)

        hextile3 = grid.get_neighbour_in_direction(hextile, 4)
        worker.position = hextile3
        civ.build_structure(worker, BuildingType.FARM, 2)
        curr = civ.currency_of_buildings()
        cost = civ.cost_of_units()

        civ.currency_per_turn()
        self.assertEqual(civ.food, 99)
        self.assertEqual(civ.gold, 51)
        self.assertEqual(civ.science, 5)

    def test_cost_of_units(self):
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        worker = Worker("worker", 1, hextile, "myCiv")
        civ.units[worker.id] = worker

        archer = Archer(1, 1, hextile, "myCiv")
        civ.units[archer.id] = archer

        cost = civ.cost_of_units()
        self.assertEqual(cost["food"], 3)
        self.assertEqual(cost["gold"], 0)
        self.assertEqual(cost["science"], 0)


    def test_currency_of_buildings(self):
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        worker = Worker("worker", 1, hextile, "myCiv")
        worker.actions = 5
        civ.units[worker.id] = worker

        grid.create_grid()
        civ.build_city_on_tile(worker, 1)
        hextile2 = grid.get_neighbour_in_direction(hextile, 2)
        worker.position = hextile2
        civ.build_structure(worker, BuildingType.UNIVERSITY, 1)

        hextile3 = grid.get_neighbour_in_direction(hextile, 4)
        worker.position = hextile3
        civ.build_structure(worker, BuildingType.FARM, 2)
        curr = civ.currency_of_buildings()

        self.assertEqual(curr["food"], 2)
        self.assertEqual(curr["gold"], -4)
        self.assertEqual(curr["science"], 5)

    def test_calculate_vision(self):
        civ = Civilisation("myCiv", grid, logger)
        hextile = Hex(0, 0, 0)
        worker = Worker("worker", 1, hextile, "myCiv")
        worker.actions = 2
        civ.units[worker.id] = worker

        grid.create_grid()
        civ.build_city_on_tile(worker, 1)
        hextile2 = grid.get_neighbour_in_direction(hextile, 2)
        worker.position = hextile2

        civ.build_structure(worker, BuildingType.UNIVERSITY, 1)
        civ.calculate_vision()

        self.assertEqual(len(civ._vision), 37)
