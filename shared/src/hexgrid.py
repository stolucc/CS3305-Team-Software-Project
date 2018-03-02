"""Hex map representation."""

from queue import PriorityQueue
from terrain import Terrain, TerrainType, BiomeType
from building import BuildingType, Building
import unit
from random import choice
from mapresource import ResourceType, Resource


class Hex:
    """A class for a Hexagonal shape."""

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
        self._unit = None
        self._building = None
        self._civ_id = None
        self._city_id = None

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
    def unit(self):
        """
        Property for unit.

        :return: a unit
        """
        return self._unit

    @unit.setter
    def unit(self, new_unit):
        """
        Setter for terrain.

        :param unit: a Unit object, or None
        """
        self._unit = new_unit

    @property
    def coords(self):
        """
        Property for coordinates.

        :return: a tuple in the form (x,y,z)
        """
        return (self._x, self._y, self._z)

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

    @property
    def movement_cost(self):
        """
        Property for movement cost moving through this hex.

        :return: movement cost value
        """
        return self._terrain.movement_cost

    @property
    def unit(self):
        """
        Return unit currently on this hex.

        :return: unit object
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """
        Set unit currently on this hex.

        :param unit: unit object
        """
        self._unit = unit

    @property
    def building(self):
        """
        Return building currently on this hex.

        :return: building object
        """
        return self._building

    @building.setter
    def building(self, building):
        """
        Set building currently on this hex.

        :param building: building object
        """
        self._building = building

    @property
    def civ_id(self):
        """Return civilisation that owns tile."""
        return self._civ_id

    @civ_id.setter
    def civ_id(self, civilisation_id):
        """Set civilisation ID of tile."""
        self._civ_id = civilisation_id

    @property
    def city_id(self):
        """Return city that owns tile."""
        return self._city_id

    @city_id.setter
    def city_id(self, city_id):
        """Set city ID of tile."""
        self._city_id = city_id

    def __eq__(self, other):
        """
        Equality between two Hex objects.

        :param other: the other Hex to compare
        :return: a boolean. True if the two Hex shapes are the same,
        False otherwise
        """
        if type(other) != type(self):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __lt__(self, other):
        """Less than comparison between hexes."""
        return self.x < other.x or self.y < other.y or self.z < other.z

    def __repr__(self):
        """
        Self reference.

        :return: a formatted list showing x, y and z coordinates
        """
        return "(x:%s, y:%s, z:%s)" % (self.x, self.y, self.z)

    def __hash__(self):
        """
        Hash reference.

        :return: the hash value of the tuple (x, y, z)
        """
        return hash((self.x, self.y, self.z))


class Grid:
    """Class for the Grid."""

    def __init__(self, size):
        """
        Create a new Grid object.

        :param size: the size of the grid
        """
        self._size = size
        self._hextiles = {}
        self._radius = size // 2
        x, y, z = 2*self._radius+1, -self._radius, -self._radius-1
        self._mirrors = [(x, y, z),
                         (-y, -z, -x),
                         (z, x, y),
                         (-x, -y, -z),
                         (y, z, x),
                         (-z, -x, -y)]

    @property
    def mirrors(self):
        """Getter for mirrors."""
        return self._mirrors

    @property
    def size(self):
        """Getter for size."""
        return self._size

    def get_hextile(self, coordinates):
        """
        Get hex at coordinates.

        :param coordinates: tuple (x, y, z)
        :return: Hex object
        """
        coordinates_sum = coordinates[0] + coordinates[1] + coordinates[2]
        should_wrap = ((abs(coordinates[0]) > self._radius) or
                       (abs(coordinates[1]) > self._radius) or
                       (abs(coordinates[2]) > self._radius))
        if coordinates_sum is not 0:
            raise KeyError
        elif should_wrap:
            return self.get_hextile(self.wrap_around(coordinates))
        else:
            return self._hextiles[coordinates]

    def get_hextiles(self):
        """
        Get the dictionary containing all hexs.

        :return: Dictionary of hex objects.
        """
        return self._hextiles

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

    def get_all_neighbours(self, hexagon):
        """
        Get all the neighbouring tiles coordinates.

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

    def get_neighbour_in_direction(self, hexagon, dire):
        """
        Get neighbouring tile in a given direction.

        :param hexagon: a Hex object
        :param dire: a direction to pick
        :return: a Hex object
        """
        possible_directions = self.get_all_neighbours(hexagon)
        return possible_directions[dire]

    def get_diagonals(self, hexagon):
        """
        Get diagonal tile coordinates.

        :param hexagon: a Hex object
        :return: a list containing Hex objects that are neighbours of hexagon
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

    def hex_distance_coordinates(self, first_coord, second_coord):
        """
        Return the distance between two coordinates.

        :param first_coord: coordinates (x, y, z)
        :param second_coord: coordinates (x, y, z)
        :return: the distance between first_hex and second_hex,
            in the form of an int
        """
        distance = 0
        distance += abs(first_coord[0] - second_coord[0])
        distance += abs(first_coord[1] - second_coord[1])
        distance += abs(first_coord[2] - second_coord[2])
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
        Compute a ring of hex objects of a given radius.

        :param ring_radius: the radius of the ring
        :param centre_hexagon: the centre tile of the ring
        :return: a list of Hex objects forming a ring
        """
        results = []
        hexagon = self.get_hextile((centre_hexagon.x - ring_radius,
                                    centre_hexagon.y,
                                    centre_hexagon.z + ring_radius))
        for side in range(6):
            for j in range(ring_radius):
                results.append(hexagon)
                hexagon = self.get_neighbour_in_direction(hexagon, side)
        return results

    def spiral_ring(self, centre_hexagon, spiral_radius):
        """
        Compute an outward spiral ring originating from centre hex.

        :param centre_hexagon: the centre tile of the ring
        :param spiral_radius: the radius of the spiral
        :return: a list of Hex objects forming a ring
        """
        results = []
        for ring_radius in range(1, spiral_radius+1):
            results += self.single_ring(centre_hexagon, ring_radius)
        results += [centre_hexagon]
        return results

    def intersecting_hex_ranges(self, first_range, second_range):
        """
        Get list of all hex objects common to both ranges.

        :param first_range: list of Hexs
        :param second_range: list of Hexs
        :return: list of hex objects
        """
        return list(set(first_range).intersection(set(second_range)))

    def wrap_around(self, coordinates):
        """
        Wrap coordinates.

        :param coordinates: tuple (x, y, z)
        :return: tuple (x, y, z)
        """
        min_mirror = self._mirrors[0]
        last_distance = self.hex_distance_coordinates(coordinates, min_mirror)
        for mirror in self._mirrors[1:]:
            distance = self.hex_distance_coordinates(coordinates, mirror)
            if distance <= last_distance:
                min_mirror = mirror
                last_distance = self.hex_distance_coordinates(coordinates,
                                                              min_mirror)
        return (round(coordinates[0] - min_mirror[0]),
                round(coordinates[1] - min_mirror[1]),
                round(coordinates[2] - min_mirror[2]))

    def vision(self, hex, radius):
        """
        Determine which tiles are visible in a certain radius.

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
                    if not ray[raytile].vision:
                        view = False
        return list(result)

    def dijkstra(self, start_hex, movement):
        """
        Implement Dijkstra's algorithm for hex tiles.

        :param start_hex: the starting hex to determine paths from
        :param movement: the movement cost limit available
        :return: a dictionary with keys as reachable tiles and
            values as previous tile in path
        """
        opn = PriorityQueue()
        opn.put((0, start_hex))
        visited, previous_tiles, result = {}, {start_hex: (0, None)}, {}
        while opn.qsize() > 0:
            current_hex = opn.get()
            prev = previous_tiles[current_hex[1]]
            if prev[0] > movement:
                break
            current_cost = current_hex[0]
            current_hex = current_hex[1]
            visited[current_hex] = None
            neighbours = self.get_all_neighbours(current_hex)
            result[current_hex] = prev[1]
            for neighbour in neighbours:
                if neighbour in previous_tiles:
                    if (current_cost + neighbour.movement_cost) < \
                                        previous_tiles[neighbour][0]:
                        previous_tiles[neighbour] = (current_cost +
                                                     neighbour.movement_cost,
                                                     current_hex)
                else:
                    previous_tiles[neighbour] = (current_cost +
                                                 neighbour.movement_cost,
                                                 current_hex)
                if neighbour not in visited:
                    opn.put((current_cost +
                             neighbour.movement_cost, neighbour))
        for tile in list(result):
            if tile.unit is not None:
                del result[tile]
        return result

    def shortest_path(self, start_hex, end_hex, movement):
        """
        Determine the shortest path from one tile to another.

        :param start_hex: the hex the path begins from
        :param end_hex: the hex the path ends at
        :param movement: the total movement cost available
        :return: a list of the tiles on the path from start_hex to second_hex
            returns an empty list if no path is available
        """
        reachable = self.dijkstra(start_hex, movement)
        path = []
        if end_hex in reachable:
            nxt = end_hex
            while nxt != start_hex:
                path += [nxt]
                nxt = reachable[nxt]
        return path[::-1]

    def move_along_path(self, start_hex, end_hex, movement):
        """
        Move the unit along the path to their destination.

        :param start_hex: the hex the path begins from
        :param end_hex: the hex the path ends at
        :param movement: the total movement cost available
        """
        path = self.shortest_path(start_hex, end_hex, movement)
        unit = start_hex.unit
        for tile in range(len(path)):
            unit.position = path[tile]
            path[tile].unit = unit
            if tile > 0:
                path[tile - 1].unit = None

    def randomize_terrain(self, hex):
        """
        Pick a random terrain type for the hex tile.

        :param hex: the hex tile to be randomized
        """
        terraintype = choice(list(TerrainType))
        biometype = hex.terrain._biome
        hex._terrain = Terrain(terraintype, biometype)

    def static_map(self):
        for hex_point in self.get_hextiles():
            hexagon = self.get_hextile(hex_point)
            if abs(hexagon._x) == (self._size // 2) or \
               abs(hexagon._y) == (self._size // 2) or \
               abs(hexagon._z) == (self._size // 2):
                if abs(hexagon._x) == (self._size // 6) or \
                   abs(hexagon._y) == (self._size // 6) or \
                   abs(hexagon._z) == (self._size // 6):
                    terraintype = TerrainType.FLAT
                else:
                    terraintype = TerrainType.OCEAN
            elif hexagon._x % 3 == 1 and hexagon._y % 2 == 1:
                terraintype = TerrainType.OCEAN
            elif hexagon._y % 3 != 1 and hexagon._z % 2 == 1:
                terraintype = TerrainType.HILL
            elif hexagon._z % 3 == 2 and hexagon._x % 2 == 0:
                terraintype = TerrainType.MOUNTAIN
            else:
                terraintype = TerrainType.FLAT

            if abs(hexagon._y) < (self._size // 6):
                biometype = BiomeType.DESERT
            elif abs(hexagon._y) > (self._size // 3):
                biometype = BiomeType.TUNDRA
            else:
                biometype = BiomeType.GRASSLAND

            resource = None
            if terraintype != TerrainType.OCEAN:
                if hexagon._y % 2 == 1 and hexagon._z % 3 == 1:
                    if hexagon._y % 4 == 1:
                        if hexagon._z % 6 == 1:
                            resource = Resource(ResourceType.COAL, 1)
                        elif hexagon._z % 6 == 4:
                            resource = Resource(ResourceType.GEMS, 1)
                    elif hexagon._y % 4 == 3:
                        if hexagon._z % 6 == 1:
                            resource = Resource(ResourceType.LOGS, 1)
                        if hexagon._z % 6 == 4:
                            resource = Resource(ResourceType.IRON, 1)

            hexagon._terrain = Terrain(terraintype, biometype, resource)
