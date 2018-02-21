"""City representation."""
from currency import CurrencyType
from mapresource import Resource


class City():
    """A city which claims some of it's neighbouring tiles."""

    RANGE = 4

    def __init__(self, identifier, hexagon):
        """Instantiate new City object."""
        self._hex = hexagon
        hexagon.building = self
        self._tiles = []
        self._type = False
        self._id = identifier

    def __repr__(self):
        """Return string representation of City."""
        string = "City: Amount of tiles: %i, " % (len(self.tiles))
        string += "Amount of buildings: %i, Hex: " % (len(self.buildings))
        string += str(self._hex)
        return string

    @property
    def id(self):
        """Return id of civilisation."""
        return self._id

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

    def no_unit_tile(self):
        """Return first tile with no unit on it, None otherwise."""
        for tile in self.tiles:
            if tile.unit is None:
                return tile
        return None

    @property
    def currency(self):
        """Property to evaluate total currency produced by this city."""
        currencies = {}
        for currency in list(CurrencyType):
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

    @property
    def buildings(self):
        """Property to give list of buildings in this city."""
        buildings = []
        for tile in self._tiles:
            building = tile.building
            if building is not None:
                buildings += [building]
        return buildings
