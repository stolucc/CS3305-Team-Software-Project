"""Building unit testing"""

import unittest
from city import *
from hexgrid import Hex


class CityTest(unittest.TestCase):
    """Unittest class for city"""

    def test_city_constructor(self):
        """Tests the constructor for the city class"""

        hextile = Hex(0, 0, 0)
        city = City(1, hextile, 1)
        self.assertEqual(city._hex, hextile)
        self.assertEqual(hextile.building, city)
        self.assertEqual(city._tiles, [])
        self.assertEqual(city._type, BuildingType.CITY)
        self.assertEqual(city._id, 1)
        self.assertEqual(city._civ_id, 1)
        self.assertEqual(city._buildings, {})

    def test_no_unit_tile(self):
        """Tests the no_unit_tile function"""

        hextile = Hex(0, 0, 0)
        hextile2 = Hex(0, 1, -1)
        city = City(1, hextile, 1)
        tile1 = city.no_unit_tile()
        self.assertEqual(tile1, None)
        city._tiles += [hextile2]
        tile2 = city.no_unit_tile()
        self.assertEqual(tile2, hextile2)