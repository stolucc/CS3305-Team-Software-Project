"""Module to represent a variety of specific game actions."""


class MovementAction():
    """An action causing a unit to move."""

    def __init__(self, unit, hexagon):
        """
        Initialise a new movement action.

        :param unit: The unit to be moved
        :param hexagon: The destination hexagon
        """
        self.unit = unit
        self.destination = hexagon


class CombatAction():
    """An action causing one unit to attack another."""

    def __init__(self, attacker, defender):
        """
        Initialise a new combat action.

        :param attacker: The unit which initiates the attack
        :param defender: The unit being attacked
        """
        self.attacker = attacker
        self.defender = defender


class UpgradeAction():
    """An action which upgrades a unit to the nect level."""

    def __init__(self, unit):
        """
        Initialise a new upgrade action.

        :param unit: The unit to be upgraded
        """
        self.unit = unit


class BuildAction():
    """An action which constructs a new building."""

    def __init__(self, unit, building_type):
        """
        Initialise a new build action.

        :param unit: The unit used to construct the building
        :param building_type: The type of building to be constructed
        """
        self.unit = unit
        self.building_type = building_type


class PurchaseAction():
    """An action which purchases a new unit."""

    def __init__(self, city, unit_type, level):
        """
        Initialise a new build action.

        :param city: The city the unit is purchased in
        :param unit_type: The type unit being purchased
        """
        self.building = city
        self.unit_type = unit_type
        self.level = level
