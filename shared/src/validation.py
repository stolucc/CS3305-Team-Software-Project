"""Module for validation of possible moves."""
from action import MovementAction, CombatAction, \
                   UpgradeAction, BuildAction, PurchaseAction
from terrain import TerrainType
from unit import Worker, Swordsman, Archer
from building import BuildingType


class ActionValidatior():
    """Class used to validate actions created."""

    def __init__(self, gamestate):
        """
        Instantiate new validator.

        :param gamestate: A reference to the current gamestate to be used
        """
        self._gamestate = gamestate

    def validate(self, action):
        """
        Validate a created action.

        :param action: Action to be validated
        """
        if type(action) == MovementAction:
            return self.validate_movement(action)
        elif type(action) == CombatAction:
            return self.validate_combat(action)
        elif type(action) == UpgradeAction:
            return self.validate_upgrade(action)
        elif type(action) == BuildAction:
            self.validate_build(action)
        elif type(action) == PurchaseAction:
            self.validate_purchase(action)

    def valid_hex(self, tile):
        """
        Determine if hex is a valid tile.

        :param tile: The hextile object to be checked
        """
        coords = tile.coords
        try:
            return self._gamestate.map.get_hextile(coords)
        except Exception:
            # TODO: Log error
            return None

    def valid_unit(self, unit_id):
        """
        Determine if a unit is valid.

        :param unit_id: The identifier of the unit to be checked.
        """
        try:
            return self._gamestate.get_unit(unit_id)
        except Exception:
            # TODO: Log error
            return None

    def valid_building(self, building):
        """
        Determine if a building is valid.

        :param building: The building object to be checked.
        """
        try:
            return self._gamestate.get_building(building)
        except Exception:
            # TODO: Log error
            return None

    def unit_is_worker(self, unit):
        """
        Determine if a unit is a worker.

        :param unit: The unit to be checked.
        """
        return type(unit) == Worker

    def tile_suitable_for_unit(self, tile):
        """
        Determine if a tile can support a unit.

        :param tile: The tile to be checked
        """
        if tile.unit is not None:
            return False
        if tile.terrain.terrain_type == TerrainType.MOUNTAIN:
            return False
        if tile.terrain.terrain_type == TerrainType.OCEAN:
            return False
        return True

    def tile_suitable_for_building(self, tile):
        """
        Determine if a tile can support a building.

        :param tile: The tile to be checked
        """
        if tile.building is not None:
            return False
        if tile.terrain.terrain_type == TerrainType.MOUNTAIN:
            return False
        if tile.terrain.terrain_type == TerrainType.OCEAN:
            return False
        return True

    def path_exists(self, unit, tile):
        """
        Determine if a path from units position to tile exists.

        :param unit: The unit to be checked
        :param tile: The destination tile
        """
        position = unit.position
        path = self._gamestate.map.shortest_path(position, tile, unit.movement)
        return path != []

    def in_range(self, attacker, defender):
        """
        Determine if a unit is within range to attack another.

        :param attacker: The unit object attacking
        :param defender: The unit object defending
        """
        arange = attacker.range
        atile = attacker.position
        dtile = defender.position
        distance = self._gamestate.map.hex_distance(atile, dtile)
        return arange >= distance

    def upgrade_possible(self, unit):
        """
        Determine if unit is not already at max level.

        :param unit: The unit to be checked
        """
        return unit.level < 3

    def research_available(self, unit):
        """
        Determine if civ has required research available.

        :param unit: The unit to be checked
        """
        # TODO: Complete when research implemented.
        return True

    def currency_available(self, civ, gold=0, food=0, science=0):
        """
        Determine if civ has the currency available.

        :param civ: The civilisation which is being checked
        :param gold: The gold amount required, defaults to 0
        :param food: The food amount required, defaults to 0
        :param science: The science amount required, defaults to 0
        """
        return civ.gold >= gold and civ.food >= food and civ.science > science

    def resources_available(self, civ, resource_type, resource_amount):
        """
        Determine if civ has the required resource available.

        :param civ: The civ to be checked
        :param resource_type: The type of resource to be checked
        :param resource_amount: The amount of the resource required
        """
        return civ.resources[resource_type] > resource_amount

    def get_tile_resource(self, tile):
        """
        Get resource available on tile.

        :param tile: The tile to be checked
        """
        return tile.terrain.resource.resource_type

    def tile_has_city(self, tile):
        """
        Determine if a city exists on the current tile.

        :param tile: The tile to be checked
        """
        return tile.building.building_type == BuildingType.CITY

    def valid_building_type(self, building_type):
        """
        Ensure building type exists.

        :param building_type: The building type to be checked
        """
        return building_type in BuildingType

    def valid_unit_type(self, unit_type):
        """
        Ensure unit type exists.

        :param unit_type: The building type to be checked
        """
        return unit_type in [Worker, Swordsman, Archer]

    def validate_movement(self, action):
        """
        Ensure that movement action is valid.

        :param action: The action to be validated
        """
        try:
            destination = self.valid_hex(action.destination)
            unit = self.valid_unit(action.unit)
            path_exists = self.path_exists(unit, destination)
            tile_valid = self.valid_hex(destination)
            return path_exists and tile_valid
        except TypeError:
            # Unit or tile is invalid
            return False

    def validate_combat(self, action):
        """
        Ensure that combat action is valid.

        :param action: The action to be validated
        """
        try:
            attacker = self.valid_unit(action.attacker)
            defender = self.valid_unit(action.defender)
            return self.in_range(attacker, defender)
        except TypeError:
            # At least one unit is invalid
            return False

    def validate_upgrade(self, action):
        """
        Ensure that upgrade action is valid.

        :param action: The action to be validated
        """
        try:
            unit = self.valid_unit(action.unit)
            civ = self._gamestate.get_civ_from_unit(unit)
            upgrade_possible = self.upgrade_possible(unit)
            research_available = self.research_available(unit)

            currency_available = \
                self.currency_available(civ, *unit.upgrade_cost)
            resources_available = \
                self.resources_available(civ, *unit.upgrade_resource_cost)

            return upgrade_possible and research_available and\
                currency_available and resources_available
        except TypeError:
            # Unit is invalid
            return False

    def validate_build(self, action):
        """
        Ensure build is valid.

        :param action: The action to be validated
        """
        try:
            unit = self.valid_unit
            is_worker = self.unit_is_worker(unit)
            valid_building_type = \
                self.valid_building_type(action.building_type)
            tile_suitable_for_building = \
                self.tile_suitable_for_building(unit.position)
            currency_available = self.currency_available(
                BuildingType.cost(action.building_type))
            resource_exists = True
            if action.building_type == BuildingType.RESOURCE_IMPROVEMENT:
                resource_exists = \
                    self.get_tile_resource(unit.position) is not None

            return is_worker and valid_building_type and \
                tile_suitable_for_building and currency_available and \
                resource_exists
        except TypeError:
            # Unit is invalid
            return False

    def validate_purchase(self, action):
        """
        Ensure purchase is valid.

        :param action: The action to be validated
        """
        try:
            building = self.valid_building(action.building)
            is_city = self.tile_has_city(building.position)
            civ = self._gamestate.get_civ_from_building(building)
            valid_unit_type = self.valid_unit_type(action.unit_type)
            gold_cost = action.unit_type.gold_cost(action.level)
            currency_available = self.currency_available(civ, gold=gold_cost)
            resource_cost = action.unit_type.resource_cost(action.level)
            resources_available = \
                self.resources_available(civ, resource_cost, 1)
            tile_suitable_for_unit = \
                self.tile_suitable_for_unit(building.position)
            return is_city and valid_unit_type and valid_unit_type and \
                currency_available and resources_available and \
                tile_suitable_for_unit
        except TypeError:
            # Unit is invalid
            return False
