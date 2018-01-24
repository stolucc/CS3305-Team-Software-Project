MOVEMENT_COSTS = {"flat": 1, "river": 2, "snow": 3, "hill": 5, "snowy hill": 8, "mountain": None}
#mountain is impassable

class Terrain:

    def __init__(self, terrain, modifier):
        self._terrain = terrain
        self._modifier = modifier
        self._cost = MOVEMENT_COSTS[modifier]
