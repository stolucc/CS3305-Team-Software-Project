"""Enumerated Building classes."""
from enum import Enum
from currency import CurrencyType


class BuildingType(Enum):
    """Enum for available building types."""

    FARM = 0
    TRADE_POST = 1
    UNIVERSITY = 2
    CITY = 3
    # RESOURCE_IMPROVEMENT = 4


class Building():
    """A single resource-producing building."""

    def __init__(self, identifier, building_type, hexagon, civilisation_id,
                 city_id):
        """
        Instantiate a new building.

        :param building_type: The type of the building to be created.
        :param hexagon: The hexagon tile the building is created on.
        """
        self._id = identifier
        self._location = hexagon
        self._type = building_type
        self._city_id = city_id
        self._civ_id = civilisation_id

    def __repr__(self):
        """Return string represention of building."""
        string = str(self._type) + " Position: " + str(self._location)
        return string

    @property
    def id(self):
        """Return unique id."""
        return self._identifier

    @property
    def civ_id(self):
        """Return civilisation that owns tile."""
        return self._civ_id

    @property
    def city_id(self):
        """Return city that owns building."""
        return self._city_id

    @property
    def currency(self):
        """Currency values produced by this building."""
        values = {
            BuildingType.FARM: {
                CurrencyType.GOLD: -2,
                CurrencyType.FOOD: 5,
                CurrencyType.SCIENCE: 0,
            },
            BuildingType.TRADE_POST: {
                CurrencyType.GOLD: 5,
                CurrencyType.FOOD: -2,
                CurrencyType.SCIENCE: 0,
            },
            BuildingType.UNIVERSITY: {
                CurrencyType.GOLD: -2,
                CurrencyType.FOOD: -3,
                CurrencyType.SCIENCE: 5,
            }
        }
        return values[self._type]

    @staticmethod
    def buy_cost(type):
        """Cost in gold to purchase building."""
        values = {
            BuildingType.FARM: 10,
            BuildingType.TRADE_POST: 10,
            BuildingType.UNIVERSITY: 10
        }
        return values[type]

    @staticmethod
    def get_type(type):
        """Return int corresponding to Building type."""
        if type == BuildingType.FARM:
            return 0
        elif type == BuildingType.TRADE_POST:
            return 1
        elif type == BuildingType.UNIVERSITY:
            return 2
        elif type == BuildingType.CITY:
            return 3
        elif type == BuildingType.RESOURCE_IMPROVEMENT:
            return 4

    @property
    def position(self):
        """Location of the building."""
        return self._location

    @property
    def building_type(self):
        """Location of the building."""
        return self._type
