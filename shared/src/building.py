"""Enumerated Building classes."""
from enum import Enum
from currency import Currency


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

    @property
    def currency(self):
        """Currency values produced by this building."""
        values = {
            Building.FARM: {
                Currency.GOLD: -2,
                Currency.FOOD: 5,
                Currency.SCIENCE: 0,
            },
            Building.TRADE_POST: {
                Currency.GOLD: 5,
                Currency.FOOD: -2,
                Currency.SCIENCE: 0,
            },
            Building.UNIVERSITY: {
                Currency.GOLD: -2,
                Currency.FOOD: -3,
                Currency.SCIENCE: 5,
            }
        }
        return values[self._type]
