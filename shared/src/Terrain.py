"""Terrain class"""


class Terrain:
    """
       A class for terrain
    """

    TERRAIN_TYPE_MOVEMENT_COSTS = {"flat": 1, "hill": 2, "river": 2, "mountain": None}
    BIOME_MOVEMENT_COSTS = {"tundra": 2, "grassland": 0, "desert": 1, "jungle": 1}

    def __init__(self, terrain_type, biome):
        """
        Create a new terrain object

        :param terrain_type: the terrain type (eg. flat, hill, river, mountain, etc.)
        :param biome: the terrain biome (eg. tundra, grassland, desert, etc.)
        and biome type
        """

        self._terrain_type = terrain_type
        self._biome = biome
        self._movement_cost = self.calculate_movement_cost(terrain_type, biome)

    @property
    def terrain_type(self):
        """Getter for terrain"""
        return self._terrain_type

    @property
    def biome(self):
        """Getter for biome"""
        return self._biome

    @property
    def movement_cost(self):
        """Getter for cost"""
        return self._movement_cost

    def calculate_movement_cost(self, terrain_type, biome):
        """
        Calculates the combined movement cost of the terrain_type and biome

        :param terrain_type: The terrain type (eg. flat, hill, river, mountain, etc.)
        :param biome: the terrain biome (eg. tundra, grassland, desert, etc.)
        :return: The combined movement cost of the terrain_type and biome, or None if terrain_type is mountain
        """
        terrain_movement_cost = self.TERRAIN_TYPE_MOVEMENT_COSTS[terrain_type]
        biome_movement_cost = self.BIOME_MOVEMENT_COSTS[biome]
        if terrain_movement_cost is None or biome_movement_cost is None:
            return None
        return terrain_movement_cost + biome_movement_cost

    def __repr__(self):
        string = "Terrain:%s, Biome:%s Movement Cost:" % (self.terrain_type, self.biome)
        if self._movement_cost is None:
            string += "Not traversable\n"
        else:
            string += "%d\n" % self.movement_cost
        return string


if __name__ == '__main__':
    terrain1 = Terrain("mountain", "tundra")
    terrain2 = Terrain("hill", "desert",)
    terrain3 = Terrain("flat", "grassland")
    print(terrain1)
    print(terrain2)
    print(terrain3)
