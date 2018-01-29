"""Hex map representation."""

from terrain import Terrain, TerrainType, BiomeType


class Hex:
    """A class for an Hexagonal shape."""

    def __init__(self, x, y, z):
        """
        Create a new Hex object.

        :param x: the x coordinate of the hexagon
        :param y: the y coordinate of the hexagon
        :param z: the z coordinate of the hexagon
        """
        self._x = x
        self._y = y
        self._z = z
        self._terrain = Terrain(TerrainType.FLAT, BiomeType.GRASSLAND)

    @property
    def x(self):
        """
        Property for x.

        :return: a x coordinate
        """
        return self._x

    @property
    def y(self):
        """
        Property for y.

        :return: a y coordinate
        """
        return self._y

    @property
    def z(self):
        """
        Property for z.

        :return: a z coordinate
        """
        return self._z

    @property
    def terrain(self):
        """
        Property for terrain.

        :return: a Terrain object
        """
        return self._terrain

    @terrain.setter
    def terrain(self, new_terrain):
        """
        Setter for terrain.

        :param new_terrain: a Terrain object
        """
        self._terrain = new_terrain

    @property
    def vision(self):
        """
        Property for vision allowed across this hex.

        :return: a boolean value of visiona allowed
        """
        return self._terrain.vision

    def __eq__(self, other):
        """
        Equality between two Hex objects.

        :param other: the other Hex to compare
        :return: a boolean. True if the two Hex shapes are the same,
        False otherwise
        """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        """
        Self reference.

        :return: a formatted list showing x, y and z coordinates
        """
        return "x:%s, y:%s, z:%s\n" % (self.x, self.y, self.z)

    def __hash__(self):
        """
        Hash reference.

        :return: the hash value of the tuple (x, y, z)
        """
        return hash((self.x, self.y, self.z))


class Grid:
    """A class for the Grid."""

    def __init__(self, size):
        """
        Create a new Grid object.

        :param size: the size of the grid
        """
        self._size = size
        self._hextiles = {}

    def get_hextile(self, coordinates):
        """
        Get hex at coordinates.

        :param coordinates: tuple (x, y, z)
        :return: Hex object
        """
        try:
            return self._hextiles[coordinates]
        except KeyError:
            raise  # implement wrapround function here when created

    def create_grid(self):
        """
        Create a grid layout.

        :return: a dictionary in the form {(x,y,z):Hex},
        where (x,y,z) is a tuple of coordinates and Hex is a Hex object
        """
        map_radius = self._size // 2
        x = -map_radius
        while x <= map_radius:
            y1 = max(-map_radius, -x - map_radius)
            y2 = min(map_radius, -x + map_radius)
            y = y1
            while y <= y2:
                self._hextiles[(x, y, -x-y)] = Hex(x, y, -x-y)
                y += 1
            x += 1
        return self._hextiles

    def add_coords(self, first_hex, second_hex):
        """
        Add coordinates.

        :param first_hex: an Hex
        :param second_hex: and Hex
        :return: a Hex object with new coordinates
        """
        return self.get_hextile((first_hex.x + second_hex.x,
                                 first_hex.y + second_hex.y,
                                 first_hex.z + second_hex.z))

    def sub_coords(self, first_hex, second_hex):
        """
        Subtract coordinates.

        :param first_hex: an Hex
        :param second_hex: an Hex
        :return: a Hex object with new coordinates
        """
        return self.get_hextile((first_hex.x - second_hex.x,
                                 first_hex.y - second_hex.y,
                                 first_hex.z - second_hex.z))

    def scale(self, hexagon, scale_by):
        """
        Scale/Multiply an Hex.

        :param hexagon: an Hex
        :param scale_by: an int to scale by
        :return: a scaled Hex object
        """
        return self.get_hextile((hexagon.x * scale_by,
                                 hexagon.y * scale_by,
                                 hexagon.z * scale_by))

    def get_all_neighbors(self, hexagon):
        """
        Get all the neighboring tiles coordinates.

        :param hexagon: a Hex object
        :return: a list in the form [(x, y, z)],
        where (x,y,z) is a tuple of coordinates
        """
        x, y, z = hexagon.x, hexagon.y, hexagon.z
        return [self.get_hextile((x+1, y-1, z)),
                self.get_hextile((x+1, y, z-1)),
                self.get_hextile((x, y+1, z-1)),
                self.get_hextile((x-1, y+1, z)),
                self.get_hextile((x-1, y, z+1)),
                self.get_hextile((x, y-1, z+1))]

    def get_neighbor_in_direction(self, hexagon, dire):
        """
        The direction to take when computing the neighbors.

        :param hexagon: a Hex object
        :param dire: a direction to pick
        :return: a Hex object
        """
        possible_directions = self.get_all_neighbors(hexagon)
        return possible_directions[dire]

    def get_diagonals(self, hexagon):
        """
        Get diagonal tile coordinates.

        :param hexagon: a Hex object
        :return: a list containing Hex objects that are neighbors of hexagon
        """
        x, y, z = hexagon.x, hexagon.y, hexagon.z
        return [self.get_hextile((x+2, y-1, z-1)),
                self.get_hextile((x+1, y+1, z-2)),
                self.get_hextile((x-1, y+2, z-1)),
                self.get_hextile((x-2, y+1, z+1)),
                self.get_hextile((x-1, y-1, z+2)),
                self.get_hextile((x+1, y-2, z+1))]

    def rotate_left(self, hexagon):
        """
        Rotate a Hex vector to the left to point to a different Hex.

        :param hexagon: a Hex object
        :return: a Hex object
        """
        return self.get_hextile((-hexagon.z, -hexagon.x, -hexagon.y))

    def rotate_right(self, hexagon):
        """
        Rotate a Hex vector to the right to point to a different Hex.

        :param hexagon: a Hex object
        :return: a Hex object
        """
        return self.get_hextile((-hexagon.y, -hexagon.z, -hexagon.x))

    def hex_distance(self, first_hex, second_hex):
        """
        Return the distance between two Hexes.

        :param first_hex: A Hex object
        :param second_hex: A Hex object
        :return: the distance between first_hex and second_hex,
        in the form of an int
        """
        distance = 0
        distance += abs(first_hex.x - second_hex.x)
        distance += abs(first_hex.y - second_hex.y)
        distance += abs(first_hex.z - second_hex.z)
        distance /= 2
        return distance

    def hex_round(self, coordinates):
        """
        Turn fractional hex coordinates(floating point) into nearest integer.

        :param coordinates: x, y, z coordinate float
        :return: (x, y, z) hex coordinates in int form
        """
        rx = int(round(coordinates[0]))
        ry = int(round(coordinates[1]))
        rz = int(round(coordinates[2]))
        x_dif = abs(rx - coordinates[0])
        y_dif = abs(ry - coordinates[1])
        z_dif = abs(rz - coordinates[2])

        if x_dif > y_dif and x_dif > z_dif:
            rx = -ry-rz
        elif y_dif > z_dif:
            ry = -rx-rz
        else:
            rz = -rx-ry
        return (rx, ry, rz)

    def interpolate(self, a_coord, b_coord, i):
        """
        Interpolate between two coordinates.

        :param a_coord: first coordinate of x, y, or z
        :param b_coord: second coordinate of x, y, or z
        :param i: the percentage between the two coordinates
        :return: float hex coordinates
        """
        return a_coord * (1 - i) + b_coord * i

    def hex_interpolate(self, hex_a, hex_b, i):
        """
        Interpolate between two hex tiles.

        :param hex_a: a Hex object
        :param hex_b: a Hex object
        :param i: the percentage between the two coordinates
        :return: x,y,z coordinates in float form
        """
        x = self.interpolate(hex_a.x, hex_b.x, i)
        y = self.interpolate(hex_a.y, hex_b.y, i)
        z = self.interpolate(hex_a.z, hex_b.z, i)
        return (x, y, z)

    def hex_linedraw(self, hex_a, hex_b):
        """
        To draw a line between two hexes.

        :param hex_a: a Hex object
        :param hex_b: a Hex object
        :return: list of hex tiles on the line
        """
        distance = int(self.hex_distance(hex_a, hex_b))
        results = []
        jump = 1 / max(distance, 1)  # to handle lines with length 0
        for i in range(distance+1):
            results.append(self.get_hextile((self.hex_round(
                self.hex_interpolate(hex_a, hex_b, jump * i)))))
        return results

    def single_ring(self, centre_hexagon, ring_radius):
        """
        A ring.

        :param ring_radius: the radius of the ring
        :param centre_hexagon: the centre tile of the ring
        :return: a list of Hex objects forming a ring
        """
        results = []
        hexagon = self.add_coords(centre_hexagon,
                                  self.scale(self.get_neighbor_in_direction(
                                            centre_hexagon, 4),
                                             ring_radius))
        for side in range(6):
            for j in range(ring_radius):
                results.append(hexagon)
                hexagon = self.get_neighbor_in_direction(hexagon, side)
        return results

    def spiral_ring(self, centre_hexagon, spiral_radius):
        """
        An outward spiral ring originating from centre hex.

        :param centre_hexagon: the centre tile of the ring
        :param spiral_radius: the radius of the spiral
        :return: a list of Hex objects forming a ring
        """
        results = [centre_hexagon]
        for ring_radius in range(1, spiral_radius+1):
            results += self.single_ring(centre_hexagon, ring_radius)
        return results

    def hex_range(self, hexagon, hex_range):
        """
        Get all tiles within hex_range of hex.

        :param hexagon: a Hex object
        :param hex_range: desired range
        :return: a list in the form [(x, y, z)],
        where (x,y,z) is a tuple of coordinates
        """
        dx, dy = hexagon.x, hexagon.y
        hexs_in_range = []
        for x in range((-hex_range+dx), (hex_range+dx+1)):
            for y in range(max((-hex_range+dy), (-x-hex_range+dy)),
                           min((hex_range+dy), (-x+hex_range)+dy+1)):
                z = -x-y
                hexs_in_range += [self.get_hextile((x, y, z))]
        return hexs_in_range

    def intersecting_hex_ranges(self, first_range, second_range):
        """
        Get list of all hex objects common to both ranges.

        :param first_range: tuple in form (HexObject, range)
        :param second_range: tuple in form (HexObject, range)
        :return: list of hex objects
        """
        first_range = self.hex_range(first_range[0], first_range[1])
        second_range = self.hex_range(second_range[0], second_range[1])
        return list(set(first_range).intersection(set(second_range)))

    def vision(self, hex, radius):
        """
        A function to determine which tiles are visible in a certain radius.

        :param hex: a hex marking centre of the vision radius
        :param radius: the radius to calculate
        :return: the list of values visible from the current tile
        """
        result = {hex}
        ring = self.single_ring(hex, radius)
        for tile in ring:
            view = True
            ray = self.hex_linedraw(hex, tile)
            for raytile in range(len(ray)):
                if(view):
                    result = result | {ray[raytile]}
                    if(not ray[raytile].vision):
                        view = False
        return list(result)


if __name__ == '__main__':
    grid = Grid(9)
    hexmap = grid.create_grid()
    # print("neighboring  (0,0,0):\n", grid.get_all_neighbors(hexmap[(0, 0, 0)]))
    # print("diagonals    (0,0,0):\n", grid.get_diagonals(hexmap[(0, 0, 0)]))
    # print("hex range    (0,0,0):\n", grid.hex_range(hexmap[(0, 0, 0)], 2))
    # print("single ring  (0,0,0):\n", grid.single_ring(hexmap[(0, 0, 0)], 2))
    # print("spiral ring  (0,0,0):\n", grid.spiral_ring(hexmap[(0, 0, 0)], 2))
    # print("line draw    (0,0,0)->(3,-2,-1):\n",
    #       grid.hex_linedraw(hexmap[(0, 0, 0)], hexmap[(3, -2, -1)]))
    # print("intersection ((0,0,0),2)n((1,1,-2),2):\n",
    #       grid.intersecting_hex_ranges((hexmap[(0, 0, 0)], 2),
    #                                    (hexmap[(1, 1, -2)], 2)))
    tile = grid.get_hextile((0, 0, 0))
    grid.get_hextile((-1, 0, 1)).terrain = \
        Terrain(TerrainType.MOUNTAIN, BiomeType.TUNDRA)
    grid.get_hextile((-1, 1, 0)).terrain = \
        Terrain(TerrainType.MOUNTAIN, BiomeType.TUNDRA)
    grid.get_hextile((0, -1, 1)).terrain = \
        Terrain(TerrainType.MOUNTAIN, BiomeType.TUNDRA)
    print(grid.vision(tile, 2))
