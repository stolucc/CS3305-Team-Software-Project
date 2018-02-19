"""Currency Classes."""

from enum import Enum


class CurrencyType(Enum):
    """Enum for modifier types."""

    GOLD = 0
    FOOD = 1
    SCIENCE = 2


class Currency():
    """Class to represent a Currency."""

    def __init__(self, currency_type, intial_value):
        """
        Create base currency.

        :param currency_type: Type of currency
        :param initial_value: Initial currency value
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
