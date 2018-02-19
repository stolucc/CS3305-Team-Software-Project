"""."""


class MovementAction():

    def __init__(self, unit, hexagon):
        self.unit = unit
        self.destination = hexagon


class CombatAction():

    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender


class UpgradeAction():

    def __init__(self, unit):
        self.unit = unit


class BuildAction():

    def __init__(self, unit, building_type):
        self.unit = unit
        self.building_type = building_type


class PurchaseAction():

    def __init__(self, building, unit_type):
        self.building = building
        self.unit_type = unit
