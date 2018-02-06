"""City representation."""
from currency import Currency
from mapresource import Resource


class City():
    """A city which claims some of it's neighbouring tiles."""

    RANGE = 4

    def __init__(self, hexagon):
        """Instantiate new City object."""
        self._hex = hexagon
        hexagon.building = self
        self._tiles = None

    @property
    def tiles(self):
        """Property for tiles owned by this city."""
        return self._tiles

    @tiles.setter
    def tiles(self, tiles):
        for tile in tiles:
            if not tile.claimed:
                self._tiles += [tile]
                tile.claim()

    @property
    def currency(self):
        """Property to evaluate total currency produced by this city."""
        currencies = {}
        for currency in list(Currency):
            currencies[currency] = 0
        for tile in self._tiles:
            if tile.building is not None:
                for key in tile.building.currency:
                    currencies[key] += tile.building.currency[key]
        return currencies

    @property
    def resources(self):
        """Property to evaluate total resources produced by this city."""
        resources = {}
        for resource in list(Resource):
            resources[resource] = 0
        for tile in self._tiles:
            if tile.terrain.resource is not None \
               and tile.terrain.resource.is_worked:
                    resources[tile.terrain.resource] += 1
        return resources
