from unit import *
#from building import Building
from currency import Currency
#from mapresource import Resource


class Civilisation(object):
    """Civilisation class."""

    def __init__(self):
        """Initialise Civilisation attributes."""
        self._units = []
        self._cities = []
        self._cost = {'gold': 0, 'food': 0, 'science': 0}

    @property
    def currency(self):
        """Return currency of all cities combined."""
        currencies = {}
        for currency in list(Currency):
            currencies[currency] = 0
        for city in self._cities:
            city_currency = city.currency
            for currency in city_currency:
                currencies[currency] += city_currency[currency]
        return currencies

    @property
    def resources(self):
        """Resources."""
        resources = {}
        for resource in list(Resource):
            resources[resource] = 0
        for city in self._cities:
            city_resources = city.resources
            for resource in city_resources:
                resources[resource] += city_resources[resource]
        return resources

    @property
    def units(self):
        """Units."""
        return self._units

    @units.setter
    def units(self, unit):
        """Set units."""
        self._units += [unit]

    @property
    def cities(self):
        """Cities."""
        return self._cities

    @cities.setter
    def cities(self, city):
        """Set city."""
        self._cities += [city]

    @property
    def cost(self):
        """Cost of currency per turn."""
        return self._cost

    def update_cost(self, cost_change):
        """
        Update cost of currency per turn.

        :param cost_change: dict
        """
        for currency in self._cost:
            self._cost[currency] += cost_change[currency]

    def cost_of_units(self):
        """Cost of units on currency per turn."""
        for unit in self.units:
            for currency in self.cost:
                cost[currency] += unit.cost[currency]
        return cost

if __name__ == "__main__":
    civ = Civilisation()
    hexa = Hex(1, -1, 0)
    worker = Worker(3, hexa)
    civ.units += [worker]

    for unit in civ.units:
        print(unit)

    print(civ.cost)
    cost = {'gold': 1, 'food': -1, 'science': 3}
    civ.update_cost(cost)
    print(civ.cost)
