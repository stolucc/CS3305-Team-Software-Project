"""Terrain"""


class Terrain:
    """
    A class for terrain
    """
    def __init__(self, terrain, biome, movement_cost):
        """
        Create a new terrain object

        :param terrain: the terrain type (eg. flat, hill, river, mountain, etc.)
        :param biome: the terrain biome (eg. tundra, grassland, desert, etc.)
        :param movement_cost: movement cost for units crossing this tile, calculated based on the terrain type
        and biome type
        """

        self._terrain = terrain
        self._biome = biome
        self._movement_cost = movement_cost

    @property
    def terrain(self):
        """Getter for terrain"""
        return self._terrain

    @property
    def biome(self):
        """Getter for biome"""
        return self._biome

    @property
    def movement_cost(self):
        """Getter for cost"""
        return self._movement_cost

    def __repr__(self):
        return "Terrain:%s, Biome:%s, Movement Cost:%d\n" % (self.terrain, self.biome, self.movement_cost)


if __name__ == '__main__':
    terrain1 = Terrain("flat", "grassland", 1)
    terrain2 = Terrain("hill", "desert", 3)
    print(terrain1)
    print(terrain2)
