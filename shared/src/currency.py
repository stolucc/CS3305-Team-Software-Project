"""Currency Classes."""

from enum import Enum


class ModifierType(Enum):
    """Enum for modifier types."""

    UNIT = 0
    IMPROVEMENT = 1


class Currency(Enum):
    """Class to represent a Currency."""

    GOLD = 0
    FOOD = 1
    SCIENCE = 2

    def __init__(self, currency_type, intial_value):
        """
        Create base currency.

        :param intial_value: value currency begins at
        :param base_increase: base value increase per turn
        """
        self._type = currency_type
        self._value = intial_value

    def add(self, increase):
        """
        Add value.

        :param increase: increase in value
        """
        self._value += increase

    def deduct(self, decrease):
        """
        Deduct value.

        :param decrease: decrease in value
        """
        self._value -= decrease

    @property
    def value(self):
        """
        Getter for value.

        :return: the value of the currency
        """
        return self._value
