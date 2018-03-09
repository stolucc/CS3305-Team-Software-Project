"""City representation."""
from currency import CurrencyType
from mapresource import ResourceType
from building import BuildingType


class City():
    """A city which claims some of it's neighbouring tiles."""

    RANGE = 3

    def __init__(self, identifier, hexagon, civ_id):
        """Instantiate new City object."""
        self._hex = hexagon
        hexagon.building = self
        self._tiles = []
        self._type = BuildingType.CITY
        self._id = identifier
        self._civ_id = civ_id
        self._buildings = {}

    def __repr__(self):
        """Return string representation of City."""
        string = "City: Amount of tiles: %i, " % (len(self.tiles))
        string += "Amount of buildings: %i, Hex: " % (len(self.buildings))
        string += str(self._hex)
        return string

    @property
    def id(self):
        """Return id of city."""
        return self._id

    @property
    def tiles(self):
        """Property for tiles owned by this city."""
        return self._tiles

    @tiles.setter
    def tiles(self, tiles):
        for tile in tiles:
            if not tile.city_id:
                self._tiles += [tile]
                tile.city_id = self._id
                tile.civ_id = self._civ_id

    @property
    def civ_id(self):
        """Return civilisation of id."""
        return self._civ_id

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
        for resource in list(ResourceType):
            resources[resource] = 0
        for tile in self._tiles:
            resource = tile.terrain.resource
            if resource is not None \
               and resource.is_worked:
                    resources[resource] += resource.quantity
        return resources

    @property
    def buildings(self):
        """Property to give dict of buildings in this city."""
        return self._buildings

    @buildings.setter
    def buildings(self, building):
        """Add building to dict of buildings."""
        self._buildings += building

    @property
    def position(self):
        """Property to get position."""
        return self._hex

    @property
    def building_type(self):
        """Property to get building type."""
        return self._type
