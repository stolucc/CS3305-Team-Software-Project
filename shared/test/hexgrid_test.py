"""hexgrid unit testing."""

import unittest
from hexgrid import Grid, Hex
from terrain import Terrain, TerrainType, BiomeType


class HexGridTest(unittest.TestCase):
    """Unittest class for hexgrid."""

    def test_hex_constructor_and_getters(self):
        """Test hex constructor and propertys."""
        hex_tile = Hex(1, 2, 3)
        self.assertEqual(hex_tile.x, 1)
        self.assertEqual(hex_tile.y, 2)
        self.assertEqual(hex_tile.z, 3)

    def test_hex_equal_hex(self):
        """Test hex equality."""
        hex_a = Hex(1, 3, 2)
        hex_b = Hex(1, 3, 2)
        self.assertEqual(hex_a, hex_b)

    def test_hex_not_equal_hex(self):
        """Test hex inequality."""
        hex_a = Hex(1, 3, 2)
        hex_b = Hex(2, 1, 3)
        self.assertNotEqual(hex_a, hex_b)

    def test_grid_amount_of_hex_tiles_from_size(self):
        """Test creating grid."""
        grid = Grid(5)
        grid.create_grid()
        self.assertEqual(len(grid._hextiles), 19)

    def test_adding_hex_to_hex(self):
        """Test adding hexs."""
        grid = Grid(5)
        grid.create_grid()
        hex_a = grid.get_hextile((1, 0, -1))
        hex_b = grid.get_hextile((-1, 2, -1))
        hex_result = Hex(0, 2, -2)
        self.assertEqual(grid.add_coords(hex_a, hex_b), hex_result)

    def test_subtracting_hex_from_hex(self):
        """Test subtracting hexs."""
        grid = Grid(5)
        grid.create_grid()
        hex_a = grid.get_hextile((1, 0, -1))
        hex_b = grid.get_hextile((-1, 2, -1))
        hex_result = Hex(2, -2, 0)
        self.assertEqual(grid.sub_coords(hex_a, hex_b), hex_result)

    def test_scaling_of_hex(self):
        """Test hex scaling."""
        grid = Grid(5)
        grid.create_grid()
        hex_a = grid.get_hextile((0, 1, -1))
        hex_result = Hex(0, 2, -2)
        self.assertEqual(grid.scale(hex_a, 2), hex_result)

    def test_getting_neighbours_of_hex(self):
        """Test get neighbours (adjacent tiles)."""
        grid = Grid(5)
        grid.create_grid()
        hex_a = grid.get_hextile((1, -1, 0))
        result = [Hex(2, -2, 0), Hex(2, -1, -1), Hex(1, 0, -1),
                  Hex(0, 0, 0), Hex(0, -1, 1), Hex(1, -2, 1)]
        self.assertEqual(grid.get_all_neighbours(hex_a), result)

    def test_getting_neighbour_of_hex_in_direction(self):
        """Test get neighbour in direction."""
        grid = Grid(5)
        grid.create_grid()
        hex_a = grid.get_hextile((1, -1, 0))
        hex_result = Hex(2, -1, -1)
        self.assertEqual(grid.get_neighbour_in_direction(hex_a, 1), hex_result)

    def test_get_diagonals_of_hex(self):
        """Test get diagonals."""
        grid = Grid(7)
        grid.create_grid()
        hex_a = grid.get_hextile((0, -1, 1))
        result = [Hex(2, -2, 0), Hex(1, 0, -1), Hex(-1, 1, 0),
                  Hex(-2, 0, 2), Hex(-1, -2, 3), Hex(1, -3, 2)]
        self.assertEqual(grid.get_diagonals(hex_a), result)

    def test_rotate_left_of_hex(self):
        """Test rotate left."""
        grid = Grid(5)
        grid.create_grid()
        hex_a = grid.get_hextile((1, 0, -1))
        hex_result = Hex(1, -1, 0)
        self.assertEqual(grid.rotate_left(hex_a), hex_result)

    def test_rotate_right_of_hex(self):
        """Test rotate right."""
        grid = Grid(5)
        grid.create_grid()
        hex_a = grid.get_hextile((1, 0, -1))
        hex_result = Hex(0, 1, -1)
        self.assertEqual(grid.rotate_right(hex_a), hex_result)

    def test_distance_between_hexes(self):
        """Test distance between hexs."""
        grid = Grid(5)
        grid.create_grid()
        hex_a = grid.get_hextile((-2, 0, 2))
        hex_b = grid.get_hextile((2, -2, 0))
        result = 4
        self.assertEqual(grid.hex_distance(hex_a, hex_b), result)

    def test_hex_rounding(self):
        """Test coordinate rounding."""
        grid = Grid(5)
        grid.create_grid()
        float_coordinates = (1.75, -0.75, -1.25)
        result_coordinates = (2, -1, -1)
        self.assertEqual(grid.hex_round(float_coordinates), result_coordinates)

    def test_coordinate_interpollating(self):
        """Test coordinate interpollating."""
        grid = Grid(5)
        grid.create_grid()
        result = 20
        interp = grid.interpolate(0, 100, 0.2)
        self.assertEqual(interp, result)

    def test_hex_interpollating(self):
        """Test hex interpollating."""
        grid = Grid(5)
        grid.create_grid()
        hex_a = Hex(-1, 0, 1)
        hex_b = Hex(1, 0, -1)
        hex_result = (0, 0, 0)
        self.assertEqual(grid.hex_interpolate(hex_a, hex_b, 0.5), hex_result)

    def test_hex_linedrawing(self):
        """Test line drawing."""
        grid = Grid(5)
        grid.create_grid()
        hex_a = Hex(-2, 0, 2)
        hex_b = Hex(2, 0, -2)
        result = [Hex(-2, 0, 2),
                  Hex(-1, 0, 1),
                  Hex(0, 0, 0),
                  Hex(1, 0, -1),
                  Hex(2, 0, -2)]
        self.assertEqual(grid.hex_linedraw(hex_a, hex_b), result)

    def test_single_ring(self):
        """Test single ring."""
        grid = Grid(7)
        grid.create_grid()
        hexagon = Hex(-1, 1, 0)
        result = [Hex(-3, 1, 2),
                  Hex(-2, 0, 2),
                  Hex(-1, -1, 2),
                  Hex(0, -1, 1),
                  Hex(1, -1, 0),
                  Hex(1, 0, -1),
                  Hex(1, 1, -2),
                  Hex(0, 2, -2),
                  Hex(-1, 3, -2),
                  Hex(-2, 3, -1),
                  Hex(-3, 3, 0),
                  Hex(-3, 2, 1)]
        self.assertEqual(grid.single_ring(hexagon, 2), result)

    def test_spiral_ring(self):
        """Test spiral rings."""
        grid = Grid(7)
        grid.create_grid()
        hexagon = Hex(-1, 1, 0)
        result = [Hex(-2, 1, 1),
                  Hex(-1, 0, 1),
                  Hex(0, 0, 0),
                  Hex(0, 1, -1),
                  Hex(-1, 2, -1),
                  Hex(-2, 2, 0),
                  Hex(-3, 1, 2),
                  Hex(-2, 0, 2),
                  Hex(-1, -1, 2),
                  Hex(0, -1, 1),
                  Hex(1, -1, 0),
                  Hex(1, 0, -1),
                  Hex(1, 1, -2),
                  Hex(0, 2, -2),
                  Hex(-1, 3, -2),
                  Hex(-2, 3, -1),
                  Hex(-3, 3, 0),
                  Hex(-3, 2, 1),
                  Hex(-1, 1, 0)]
        self.assertEqual(grid.spiral_ring(hexagon, 2), result)

    def test_intersecting_ranges(self):
        """Test intersecting hex ranges."""
        grid = Grid(7)
        grid.create_grid()
        range1 = [Hex(-1, 1, 0), Hex(0, 0, 0)]
        range2 = [Hex(1, -1, 0), Hex(0, 0, 0)]
        result = [Hex(0, 0, 0)]
        self.assertEqual(grid.intersecting_hex_ranges(range1, range2), result)

    def test_wrap_around(self):
        """Test wrap-around coordinates."""
        grid = Grid(5)
        grid.create_grid()
        coordinates = (-3, 3, 0)
        result = (0, -2, 2)
        self.assertEqual(grid.wrap_around(coordinates), result)

    def test_vision(self):
        """Test vision."""
        grid = Grid(5)
        grid.create_grid()
        hexagon = Hex(-2, 2, 0)
        grid.get_hextile((-1, 1, 0)).terrain = Terrain(TerrainType.MOUNTAIN,
                                                       BiomeType.GRASSLAND)
        result = [Hex(-1, 1, 0),
                  Hex(0, 2, -2),
                  Hex(-2, 0, 2),
                  Hex(-2, 1, 1),
                  Hex(-2, 2, 0),
                  Hex(-1, 0, 1),
                  Hex(-1, 2, -1),
                  Hex(0, 1, -1)]
        self.assertEqual(set(grid.vision(hexagon, 2)), set(result))

    def test_dijkstra(self):
        """Test dijkstras."""
        grid = Grid(5)
        grid.create_grid()
        hexagon = Hex(-1, 1, 0)
        grid.get_hextile((0, 0, 0)).terrain = Terrain(TerrainType.MOUNTAIN,
                                                      BiomeType.GRASSLAND)
        grid.get_hextile((0, 1, -1)).terrain = Terrain(TerrainType.MOUNTAIN,
                                                       BiomeType.GRASSLAND)
        grid.get_hextile((-1, 0, 1)).terrain = Terrain(TerrainType.MOUNTAIN,
                                                       BiomeType.GRASSLAND)
        result = [Hex(-1, 1, 0),
                  Hex(-1, 2, -1),
                  Hex(-2, 2, 0),
                  Hex(-2, 1, 1),
                  Hex(0, 2, -2),
                  Hex(2, 0, -2),
                  Hex(2, -1, -1),
                  Hex(-2, 0, 2),
                  Hex(2, -2, 0),
                  Hex(1, -2, 1),
                  Hex(0, -2, 2)]
        dijkstra = [x for x in grid.dijkstra(hexagon, 2)]
        result = set(result).difference(dijkstra)
        self.assertEqual(set(), result)

    def test_shortest_path(self):
        """Test shortest path."""
        grid = Grid(5)
        grid.create_grid()
        start = Hex(-1, 1, 0)
        end = Hex(1, -1, 0)
        grid.get_hextile((0, 0, 0)).terrain = Terrain(TerrainType.MOUNTAIN,
                                                      BiomeType.GRASSLAND)
        grid.get_hextile((0, 1, -1)).terrain = Terrain(TerrainType.MOUNTAIN,
                                                       BiomeType.GRASSLAND)
        grid.get_hextile((-1, 0, 1)).terrain = Terrain(TerrainType.MOUNTAIN,
                                                       BiomeType.GRASSLAND)
        result = [Hex(-1, 2, -1),
                  Hex(2, -2, 0),
                  Hex(1, -1, 0)]
        self.assertEqual(grid.shortest_path(start, end, 3), result)


if __name__ == '__main__':
    unittest.main()
