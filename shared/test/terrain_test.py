import unittest
from Terrain import Terrain


class TerrainTest(unittest.TestCase):

    def test_mountain_terrain_type_returns_infinity_for_movement_cost(self):
        self.terrain = Terrain("mountain", "tundra")
        self.assertEqual(self.terrain.movement_cost, float("inf"))

    def test_ocean_terrain_type_returns_infinity_for_movement_cost(self):
        self.terrain = Terrain("ocean", "desert")
        self.assertEqual(self.terrain.movement_cost, float("inf"))

    def test_movement_cost_of_flat_grassland_equals_1(self):
        self.terrain = Terrain("flat", "grassland")
        self.assertEqual(self.terrain.movement_cost, 1)


if __name__ == '__main__':
    unittest.main()
