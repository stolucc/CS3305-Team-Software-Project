"""Currency Classes."""


class Currency:
    """Class to represent a Currency."""

    def __init__(self, beginning_value, base_increase):
        """
        Create base currency.

        :param beginning_value: value currency begins at
        :param base_increase: base value increase per turn
        """
        self._modifiers = {"unit": {}, "improvement": {}}
        self._value = beginning_value
        self._base_increase = base_increase
        self._turn_increase = 0 #you didn't put in a value for this
        self.update()

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

    def increment(self):
        """Increment value by turn_increase."""
        self._value += self._turn_increase

    def update(self):
        """Update turn_increment."""
        modifier = 0
        for key in self._modifiers["unit"]:
            modifier += self._modifiers["unit"][key]
        for key in self._modifiers["improvement"]:
            modifier += self._modifiers["improvement"][key]
        self._turn_increase = self._base_increase + modifier

    def add_modifier(self, type, id, modification):
        """Add new / change existing modifier."""
        self._modifiers[type][id] = modification

    def remove_modifier(self, type, id):
        """Remove existing modifier."""
        try:
            del self._modifiers[type][id]
        except KeyError:
            raise

    @property
    def value(self):
        """Getter for value."""
        return self._value

    @property
    def turn_increase(self):
        """Getter for turn_increase."""
        return self._turn_increase

    @property
    def modifiers(self):
        """Getter for modifiers."""
        return self._modifiers

    @property
    def base_increase(self):
        """Getter for base_increase."""
        return self._base_increase
