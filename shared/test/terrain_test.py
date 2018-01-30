import unittest
from math import inf
from terrain import Terrain, TerrainType, BiomeType


class TerrainTest(unittest.TestCase):

    def test_mountain_terrain_type_movement_cost(self):
        terrain = Terrain(TerrainType.MOUNTAIN, BiomeType.TUNDRA)
        self.assertEqual(terrain.movement_cost, inf)

    def test_ocean_terrain_type_movement_cost(self):
        terrain = Terrain(TerrainType.OCEAN, BiomeType.DESERT)
        self.assertEqual(terrain.movement_cost, inf)

    def test_flat_grassland_movement_cost(self):
        terrain = Terrain(TerrainType.FLAT, BiomeType.GRASSLAND)
        self.assertEqual(terrain.movement_cost, 1)


if __name__ == '__main__':
    unittest.main()
