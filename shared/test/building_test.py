"""Building unit testing"""

import unittest
from building import *
from hexgrid import Hex


class BuildingTest(unittest.TestCase):
    """Unittest class for building"""

    def test_building_constructor(self):
        """Tests the building constructor"""

        hextile = Hex(0, 0, 0)
        building = Building(1, BuildingType.UNIVERSITY, hextile, 1, 2)

        self.assertEqual(building._id, 1)
        self.assertEqual(building._type, BuildingType.UNIVERSITY)
        self.assertEqual(building._city_id, 2)
        self.assertEqual(building._civ_id, 1)
        self.assertEqual(building._location, hextile)

    def test_get_type_of_farm(self):
        """Tests the get_type function on a farm"""

        farmtype = Building.get_type(BuildingType.FARM)
        self.assertEqual(farmtype, 0)

    def test_get_type_of_trade_post(self):
        """Tests the get_type function on a trade post"""

        tradeposttype = Building.get_type(BuildingType.TRADE_POST)
        self.assertEqual(tradeposttype, 1)

    def test_get_type_of_university(self):
        """Tests the get_type function on a university"""

        universitytype = Building.get_type(BuildingType.UNIVERSITY)
        self.assertEqual(universitytype, 2)

    def test_get_type_of_city(self):
        """Tests the get_type function on a city"""

        citytype = Building.get_type(BuildingType.CITY)
        self.assertEqual(citytype, 3)

    def test_buy_cost_for_farm(self):
        """Tests the buy_cost function on a farm"""

        farmcost = Building.buy_cost(BuildingType.FARM)
        self.assertEqual(farmcost, 10)

    def test_buy_cost_for_trade_post(self):
        """Tests the buy_cost function on a trade post"""

        tradepostcost = Building.buy_cost(BuildingType.TRADE_POST)
        self.assertEqual(tradepostcost, 10)

    def test_buy_cost_for_university(self):
        """Tests the buy_cost function on a university"""

        universitycost = Building.buy_cost(BuildingType.UNIVERSITY)
        self.assertEqual(universitycost, 10)
