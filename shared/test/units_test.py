import unittest
from hexgrid import Hex, Grid
from unit import Unit, Worker, Soldier, Swordsman, Archer
from civilisation import Civilisation


class UnitTest(unittest.TestCase):
    """Test class for the units classes."""

    def test_unit_attributes(self):
        """Test that unit's attributes are initialised correctly."""
        hextile = Hex(0, 0, 0)
        grid = Grid(25)
        civ = Civilisation(1, grid)

        unit = Unit(1, 100, 1, 5, {'food': 2, 'gold': 1, 'science': 0}, 10, hextile, civ)
        self.assertEqual(unit._health, 100)
        self.assertEqual(unit._max_health, 100)
        self.assertEqual(unit._level, 1)
        self.assertEqual(unit._movement_range, 5)
        self.assertEqual(unit._cost, {'food': 2, 'gold': 1, 'science': 0})
        self.assertEqual(unit._buy_cost, 10)
        self.assertEqual(unit._position, hextile)
        self.assertEqual(unit._civilisation, civ)

    def test_cost_increase(self):
        """Test that the resource costs are increased by the correct amount."""
        hextile = Hex(0, 0, 0)
        grid = Grid(25)
        civ = Civilisation(1, grid)

        unit = Unit(1, 100, 1, 5, {'food': 2, 'gold': 1, 'science': 0}, 10, hextile, civ)
        unit.cost_increase(-1, 0, 2)

        self.assertEqual(unit._cost['food'], 1)
        self.assertEqual(unit._cost['gold'], 1)
        self.assertEqual(unit._cost['science'], 2)

    def test_unit_level_up(self):
        """Test that the units attributes are increased correctly."""
        hextile = Hex(0, 0, 0)
        grid = Grid(25)
        civ = Civilisation(1, grid)

        unit = Unit(1, 100, 1, 5, {'food': 2, 'gold': 1, 'science': 0}, 10, hextile, civ)
        unit.level_up(20, 2)

        self.assertEqual(unit._health, 120)
        self.assertEqual(unit._max_health, 120)
        self.assertEqual(unit._movement_range, 7)
        self.assertEqual(unit._level, 2)

    def receive_damage(self):
        """Test that the correct amount of damage is taken."""
        hextile = Hex(0, 0, 0)
        grid = Grid(25)
        civ = Civilisation(1, grid)

        unit = Unit(1, 100, 1, 5, {'food': 2, 'gold': 1, 'science': 0}, 10, hextile, civ)
        unit.receive_damage(25)

        self.assertEqual(unit._health, 75)

    def test_restore_health(self):
        """Test that the right amount of health is restored."""
        hextile = Hex(0, 0, 0)
        grid = Grid(25)
        civ = Civilisation(1, grid)

        unit = Unit(1, 100, 1, 5, {'food': 2, 'gold': 1, 'science': 0}, 10, hextile, civ)

        unit.receive_damage(40)
        unit.restore_health(25)

        self.assertEqual(unit._health, 85)

        unit.restore_health(30)

        self.assertEqual(unit._health, 100)

    def test_worker_attributes(self):
        """Test that worker's attributes are initialised correctly."""
        hextile = Hex(0, 0, 0)
        grid = Grid(25)
        civ = Civilisation(1, grid)

        worker = Worker(1, 2, hextile, civ)

        self.assertEqual(worker._health, 110)
        self.assertEqual(worker._movement_range, 5)
        self.assertEqual(worker._cost, {'food': 2, 'gold': 0, 'science': 0})
        self.assertEqual(worker._build_speed, 2)

    def test_worker_level_up(self):
        """Test that worker unit levels up and attributes increase."""
        hextile = Hex(0, 0, 0)
        hextile2 = Hex(1, 0, -1)
        grid = Grid(25)
        civ = Civilisation(1, grid)

        worker1 = Worker(1, 1, hextile, civ)
        worker2 = Worker(1, 3, hextile2, civ)

        worker1.level_up()
        worker2.level_up()

        self.assertEqual(worker1._cost, {'food': 2, 'gold': 0, 'science': 0})
        self.assertEqual(worker1._health, 120)
        self.assertEqual(worker1._movement_range, 5)
        self.assertEqual(worker1._build_speed, 2)

        self.assertEqual(worker2._cost, {'food': 3, 'gold': 0, 'science': 0})
        self.assertEqual(worker2._health, 120)
        self.assertEqual(worker2._movement_range, 6)
        self.assertEqual(worker2._build_speed, 3)

    def test_soldier_attributes(self):
        """Test that soldier's attributes are initialised correctly."""
        hextile = Hex(0, 0, 0)
        grid = Grid(25)
        civ = Civilisation(1, grid)

        soldier = Soldier(1, 120, 1, 5, 6, 4,
                          {'food': 2, 'gold': 1, 'science': 0}, 10, hextile, civ)
        self.assertEqual(soldier._strength, 6)
        self.assertEqual(soldier._attack_range, 4)

    def test_swordsman_attributes(self):
        """Test that swordsman's attributes are initialised correctly."""
        hextile = Hex(0, 0, 0)
        grid = Grid(25)
        civ = Civilisation(1, grid)
        swordsman = Swordsman(1, 1, hextile, civ)

        self.assertEqual(swordsman._health, 130)
        self.assertEqual(swordsman._movement_range, 4)
        self.assertEqual(swordsman._strength, 30)
        self.assertEqual(swordsman._cost, {'food': 1, 'gold': 0, 'science': 0})

    def test_swordsman_level_up(self):
        """Test that swordsman levels up and attributes increase."""
        hextile = Hex(0, 0, 0)
        hextile2 = Hex(1, 0, -1)
        grid = Grid(25)
        civ = Civilisation(1, grid)

        sword1 = Swordsman(1, 1, hextile, civ)
        sword2 = Swordsman(1, 3, hextile2, civ)

        sword1.level_up()
        sword2.level_up()

        self.assertEqual(sword1._cost, {'food': 2, 'gold': 1, 'science': 0})
        self.assertEqual(sword1._health, 160)
        self.assertEqual(sword1._movement_range, 5)
        self.assertEqual(sword1._strength, 50)

        self.assertEqual(sword2._cost, {'food': 3, 'gold': 2, 'science': 0})
        self.assertEqual(sword2._health, 190)
        self.assertEqual(sword2._movement_range, 6)
        self.assertEqual(sword2._strength, 70)

    def test_archer_attributes(self):
        """Test that archer's attributes are initialised correctly."""
        hextile = Hex(0, 0, 0)
        grid = Grid(25)
        civ = Civilisation(1, grid)
        archer = Archer(1, 1, hextile, civ)

        self.assertEqual(archer._health, 110)
        self.assertEqual(archer._movement_range, 5)
        self.assertEqual(archer._strength, 20)
        self.assertEqual(archer._attack_range, 2)
        self.assertEqual(archer._cost, {'food': 2, 'gold': 0, 'science': 0})

    def test_archer_level_up(self):
        """Test that swordsman levels up and attributes increase."""
        hextile = Hex(0, 0, 0)
        hextile2 = Hex(1, 0, -1)
        grid = Grid(25)
        civ = Civilisation(1, grid)

        archer1 = Archer(1, 1, hextile, civ)
        archer2 = Archer(1, 3, hextile2, civ)

        archer1.level_up()
        archer2.level_up()

        self.assertEqual(archer1._cost, {'food': 2, 'gold': 0, 'science': 1})
        self.assertEqual(archer1._health, 130)
        self.assertEqual(archer1._movement_range, 6)
        self.assertEqual(archer1._strength, 30)
        self.assertEqual(archer1._attack_range, 3)

        self.assertEqual(archer2._cost, {'food': 2, 'gold': 0, 'science': 2})
        self.assertEqual(archer2._health, 150)
        self.assertEqual(archer2._movement_range, 7)
        self.assertEqual(archer2._strength, 40)
        self.assertEqual(archer2._attack_range, 4)


if __name__ == "__main__":
    unittest.main()
