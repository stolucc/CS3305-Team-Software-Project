from action import MovementAction, CombatAction, \
                   UpgradeAction, BuildAction, PurchaseAction
from terrain import TerrainType, BiomeType

class ActionValidatior():

    def __init__(self, gamestate):
        self._gamestate = gamestate

    def validate(self, action):
        if type(action) == MovementAction:
            #return validate_movement(action)
            #TODO: Valid Hex
            #      Unit exists
            #      Path exists
            #      Destination tile suitable
            pass
        elif type(action) == CombatAction:
            #TODO: Units exists
            #      Within range
            pass
        elif type(action) == UpgradeAction:
            #TODO: Unit exists
            #      Upgrade possible
            #      Research available
            #      Curreny available
            #      Resources available
            pass
        elif type(action) == BuildAction:
            #TODO: Unit exists
            #      Valid Building type
            #      Is worker
            #      No building on tile
            #      Valid terrain and biome type
            #      Currency available
            #      Resource tile if resource improvement
            pass
        elif type(action) == PurchaseAction:
            #TODO: Building exists
            #      Building is city
            #      Valid unit type
            #      Curreny available
            #      Resources available
            #      Tile not occupied
            pass

    def valid_hex(self, tile):
        """Determine if hex is a valid tile."""
        coords = tile.coords
        try:
            return self._gamestate.map.get_hextile(coords)
        except Exception:
            # TODO: Log error
            return None

    def valid_unit(self, unit_id):
        """Determine if a unit is valid."""
        try:
            return self._gamestate.get_unit(unit_id)
        except Exception:
            # TODO: Log error
            return None

    def tile_suitable_for_unit(self, tile):
        """Determine if a tile can support a unit."""
        if tile.unit is not None:
            return False
        if tile.terrain.terrain_type == TerrainType.MOUNTAIN:
            return False
        if tile.terrain.terrain_type == TerrainType.OCEAN:
            return False
        return True

    def path_exists(self, unit, tile):
        """Determine if a path from units position to tile exists."""
        position = unit.get_hextile()
        path = self._gamestate.map.shortest_path(position, tile, unit.movement)
        return path != []

    def in_range(self, attacker, defender):
        """Determine if a unit is within range to attack another."""
        arange = attacker.range
        atile = attacker.get_hextile()
        dtile = defender.get_hextile()
        distance = self._gamestate.map.hex_distance(atile, dtile)
        return arange >= distance

    def validate_movement(self, action):
        destination = self.valid_hex(action.destination)
        unit = self.valid_unit(action.unit)
        path_exists = self.path_exists(unit, destination)
