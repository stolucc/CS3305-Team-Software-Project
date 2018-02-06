"""Resource Classes."""
from enum import Enum


class Resource(Enum):
    """Class to represent map resources."""

    COAL = 0
    GEMS = 1
    IRON = 2
    LOGS = 3

    def __init__(self, resource_type, available_quantity):
        """
        Create base resource.

        :param available_quantity: Quantity gathered if worked.
        """
        self._resource_type = resource_type
        self._available_quantity = available_quantity
        self._is_worked = False

    def work(self):
        """Work resource."""
        self._is_worked = True

    def stop_work(self):
        """Stop working resource."""
        self._is_worked = False

    @property
    def quantity(self):
        """
        Getter for available_quantity.

        :return: the available quantity
        """
        return self._available_quantity

    @property
    def is_worked(self):
        """
        Getter for is_worked.

        :return: boolean variable for work resource
        """
        return self._is_worked

    @property
    def resource_type(self):
        """
        Getter for resource type.

        :return: the resource type
        """
        return self._resource_type
