"""Resource Classes."""


class Resource:
    """Class to represent map resources."""

    def __init__(self, available_quantity):
        """
        Create base resource.

        :param available_quantity: Quantity gathered if worked.
        """
        self._available_quantity = available_quantity  # given per turn
        self._is_worked = False

    def work(self):
        """Work resource."""
        self._is_worked = True

    def stop_work(self):
        """Stop working resource."""
        self._is_worked = False

    @property
    def quantity(self):
        """Getter for available_quantity."""
        return self._available_quantity

    @property
    def is_worked(self):
        """Getter for is_worked."""
        return self._is_worked
