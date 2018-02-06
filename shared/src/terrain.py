"""Terrain class."""

from enum import Enum
from math import inf


class TerrainType(Enum):
    """Enum for terrain types."""

    FLAT = 0
    HILL = 1
    MOUNTAIN = 2
    OCEAN = 3

    @staticmethod
    def get_movement_cost(terrain_type):
        """
        Get movement cost for terrain type.

        :param terrain_type: the type of the Terrain
        :return: movement cost for terrain type
        """
        values = {
            TerrainType.FLAT.value: 1,
            TerrainType.HILL.value: 2,
            TerrainType.MOUNTAIN.value: inf,
            TerrainType.OCEAN.value: inf
        }
        return values[terrain_type.value]

    @staticmethod
    def vision_allowed(terrain_type):
        """
        Determine if vision is allowed over a certain tile type.

        :param terrain_type: the terrain type to be checked
        :return: a boolean value indicating whether vision is allowed
        """
        allowed = [TerrainType.FLAT,
                   TerrainType.OCEAN]
        return terrain_type in allowed


class BiomeType(Enum):
    """Enum for terrain biomes."""

    TUNDRA = 0
    GRASSLAND = 1
    DESERT = 2

    @staticmethod
    def get_movement_cost(biome_type):
        """
        Get movement cost for biome type.

        :param biome_type: the type of the Terrain
        :return: movement cost for biome type
        """
        values = {
            BiomeType.TUNDRA.value: 2,
            BiomeType.GRASSLAND.value: 0,
            BiomeType.DESERT.value: 1
        }
        return values[biome_type.value]


class Terrain:
    """A class for a terrain object."""

    def __init__(self, terrain_type, biome, resource=None):
        """
        Create a new terrain object.

        :param terrain_type: the terrain type
            (eg. flat, hill, river, mountain, etc.)
        :param biome: the terrain biome
            (eg. tundra, grassland, desert, etc.)
        :param resource: the strategic resource available at this tile
        """
        self._terrain_type = terrain_type
        self._biome = biome
        self._movement_cost = self.calculate_movement_cost()
        self._resource = resource

    @property
    def terrain_type(self):
        """
        Getter for terrain.

        :return: the terrain type
        """
        return self._terrain_type

    @property
    def biome(self):
        """
        Getter for biome.

        :return: the biome of the terrain
        """
        return self._biome

    @property
    def movement_cost(self):
        """
        Getter for movement cost.

        :return: the total movement cost of the terrain
        """
        return self._movement_cost

    @property
    def vision(self):
        """
        Determine if it is possible to see past this tile.

        :return: boolean value indicating vision allowed
        """
        return TerrainType.vision_allowed(self._terrain_type)

    @property
    def has_resource(self):
        """
        Determine if terrain has available resource.

        :return: true if resource exists, false otherwise
        """
        return self._resource is not None

    @property
    def resource(self):
        """
        Get tile resource if it exists.

        :return: Resource object or None
        """
        return self._resource

    @resource.setter
    def resource(self, resource):
        """
        Set tile resource.

        :param resource: Resource object to be set
        """
        self._resource = resource

    def calculate_movement_cost(self):
        """
        Calculate the combined movement cost of the terrain_type and biome.

        :return: The combined movement cost of the terrain_type and biome
        """
        return TerrainType.get_movement_cost(self._terrain_type) + \
            BiomeType.get_movement_cost(self._biome)

    def __repr__(self):
        """
        Provide a string representation of a Terrain object.

        :return: A string containing terrain type,
            biome and movement cost of the object
        """
        string = "Terrain:%s, Biome:%s Movement Cost:" % \
            (self.terrain_type, self.biome)
        if self._movement_cost == inf:
            string += "Not traversable (Infinity)\n"
        else:
            string += "%d\n" % self.movement_cost
        return string
