"""Enumerated Building classes."""
from enum import Enum
from currency import CurrencyType


class BuildingType(Enum):
    """Enum for available building types."""

    FARM = 0
    TRADE_POST = 1
    UNIVERSITY = 2


class Building():
    """A single resource-producing building."""

    def __init__(self, building_type, hexagon):
        """
        Instantiate a new building.

        :param building_type: The type of the building to be created.
        :param hexagon: The hexagon tile the building is created on.
        """
        self._location = hexagon
        self._type = building_type

    def __repr__(self):
        """Return string represention of building."""
        string = str(self._type) + " Position: " + str(self._location)
        return string

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
