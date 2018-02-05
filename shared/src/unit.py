from enum import Enum
from hexgrid import Hex

class Unit():
    """
    Base class for the units
    """

    def __init__(self, health, level, movement_range, hex):
        """
        Initialise units attributes
        :param health: Amount of health unit begins with
        :param level: Level of the unit
        :param movement_range: Amount of tiles the unit can travel
        :param hex: Current hex tile the unit is on
        """
        self._health = health
        self._max_health = health
        self._level = level
        self._movement_range = movement_range
        self._position = hex

    @property
    def health(self):
        """
        Health of the unit
        :return: current health of the unit
        """
        return self._health

    @health.setter
    def health(self, health):
        """
        Set health of the unit
        :param health:
        """
        self._health = health

    @property
    def max_health(self):
        """
        Max health of the unit
        :return: current max health of the unit
        """
        return self._max_health

    @max_health.setter
    def max_health(self, max_health):
        """
        Set max health
        :param max_health: new max health of the unit
        """
        self._max_health = max_health

    @property
    def level(self):
        """
        Level of the unit
        :return: current level of the unit
        """
        return self._level

    @level.setter
    def level(self, level):
        """
        Set level
        :param level: set new level of the unit
        """
        self._level = level

    @property
    def movement_range(self):
        """
        Movement range of the unit
        :return: current movement range of the unit
        """
        return self._movement_range

    @movement_range.setter
    def movement_range(self, movement_range):
        """
        Set movement range
        :param movement_range: set new movement range of the unit
        """
        self._movement_range = movement_range

    @property
    def position(self):
        """
        Position of unit
        :return: hex tile that unit is positioned on
        """
        return self._position

    @position.setter
    def position(self, hex):
        """
        Set position of unit
        :param hex: new hex tile that unit is situated on
        """
        self._position = hex

    def level_up(self, health_increase, movement_increase):
        """
        Units level increases along with certain attributes
        :param health_increase: amount health should increase by
        :param movement_increase: amount movement_range should increase by
        """
        self.health += health_increase
        self.max_health += health_increase
        self.movement_range += movement_increase
        self.level += 1

    def receive_damage(self, damage):
        """
        Take damage from attack
        :param damage: amount of damage to be taken from health
        """
        self.health -= damage
        if self.health <= 0:
            self.death()

    def death(self):
        pass

    def restore_health(self, restore):
        """
        Restore health of unit
        :param restore: amount of health to be restored
        """
        health = self.health + restore
        if health > self.max_health:
            self.health = self.max_health
        else:
            self.health = health

    def __repr__(self):
        string = "Health: %i, Max Health: %i, " \
                 "Movement Range: %i, Level: %i, Position: %i,%i,%i, " % \
                 (self.health, self.max_health,self.movement_range, self.level,
                  self.position.x, self.position.y, self.position.z)
        return string


class Worker(Unit):
    """
    Worker class, for creating and upgrading buildings
    """

    def __init__(self, health, level, movement, build_speed, hex):
        """
        Initialise workers attributes
        :param health: Amount of health unit begins with
        :param level: Level of the unit
        :param movement_range: Amount of tiles the unit can travel
        :param hex: Current hex tile the unit is on
        """
        super().__init__(health, level, movement, hex)
        self._build_speed = build_speed

    @property
    def build_speed(self):
        """
        Build speed of worker
        :return: int current build speed of worker
        """
        return self._build_speed

    @build_speed.setter
    def build_speed(self, build_speed):
        """
        Set new build speed of worker
        :param build_speed: int new build speed of worker
        """
        self._build_speed = build_speed

    def level_up(self):
        """
        Worker unit levels up
        Health increases by 20, movement and build_speed by 1, each level
        """
        super().level_up(health_increase=20, movement_increase=1)
        self.build_speed += 1

    def build(self, building):
        """
        Build building on current hex tile
        :param building: the building to be built
        """
        pass

    def upgrade_building(self):
        """
        Upgrade building on units hex tile
        :return:
        """
        pass

    def __repr__(self):
        string = "Worker: "
        string += super().__repr__()
        string += "Build Speed: %i" %(self.build_speed)
        return string


class Soldier(Unit):
    """
    Soldier unit, for attacking other units and buildings
    """

    def __init__(self, health, level, movement_range, strength, attack_range, hex):
        """
        Initialise soldiers attributes
        :param health: Amount of health unit begins with
        :param level: Level of the unit
        :param movement_range: Amount of tiles the unit can travel
        :param strength: Strength of the soldier
        :param attack_range: Amount of tiles unit can attack across
        :param hex: Current hex tile the unit is on
        """
        self._strength = strength
        self._attack_range = attack_range
        super().__init__(health, level, movement_range, hex)

    @property
    def strength(self):
        """
        Soldiers strength when attacking
        :return: int current soldiers strength
        """
        return self._strength

    @strength.setter
    def strength(self, strength):
        """
        Set new strength of soldier
        :param strength: int new strength of soldier
        """
        self._strength = strength

    @property
    def attack_range(self):
        """
        Attack range of the soldier
        :return: int amount of tiles unit can attack across
        """
        return self._attack_range

    @attack_range.setter
    def attack_range(self, attack_range):
        """
        Set attack range
        :param attack_range: int new attack range of unit
        """
        self._attack_range = attack_range

    def level_up(self):
        """
        Increase soldiers health, movement, strength, attack range
        Increases depend on if soldier is close range or not
        """
        if self.attack_range == 1:
            super().level_up(health_increase=30, movement_increase=1)
            self.strength += 20
        else:
            super().level_up(health_increase=20, movement_increase=1)
            self.strength += 10
            self.attack_range += 1

    def attack(self, hex):
        """

        :param hex:
        :return:
        """
        strength = self.strength * (self.health/self.max_health)
        pass

    def __repr__(self):
        if self.attack_range == 1:
            string = "Swordsman: "
        else:
            string = "Archer: "
        string += super().__repr__()
        string += "Strength: %i, Attack Range: %i"\
                 %(self.strength, self.attack_range)
        return string


class Unit_type(Enum):
    """Enum for unit types."""

    WORKER = 0
    SWORDSMAN = 1
    ARCHER = 2

    def level_one(Unit_type, hex):
        values = {
            Unit_type.WORKER: Worker(health=100, level=1, movement=4, build_speed=1, hex=hex),
            Unit_type.SWORDSMAN: Soldier(health=130, level=1, movement_range=4, strength=30, attack_range=1, hex=hex),
            Unit_type.ARCHER: Soldier(health=110, level=1, movement_range=5, strength=20, attack_range=2, hex=hex)
        }
        return values[Unit_type]

    def level_two(Unit_type, hex):
        values = {
            Unit_type.WORKER: Worker(health=120, level=2, movement=5, build_speed=2, hex=hex),
            Unit_type.SWORDSMAN: Soldier(health=160, level=2, movement_range=5, strength=50, attack_range=1, hex=hex),
            Unit_type.ARCHER: Soldier(health=130, level=2, movement_range=6, strength=30, attack_range=3, hex=hex)
        }
        return values[Unit_type]

    def level_three(Unit_type, hex):
        values = {
            Unit_type.WORKER: Worker(health=140, level=3, movement=6, build_speed=3, hex= hex),
            Unit_type.SWORDSMAN: Soldier(health=190, level=3, movement_range=6, strength=70, attack_range=1, hex=hex),
            Unit_type.ARCHER: Soldier(health=150, level=3, movement_range=7, strength=40, attack_range=4, hex=hex)
        }
        return values[Unit_type]


if __name__ == "__main__":
    hex = Hex(1,-1,0)
    worker = Unit_type.WORKER.level_one(hex)
    print(worker)
    worker.level_up()
    print(worker)
    workertwo = Unit_type.WORKER.level_three(hex)
    print(workertwo)
    sword = Unit_type.SWORDSMAN.level_one(hex)
    archer = Unit_type.ARCHER.level_three(hex)
    print(sword)
    print(archer)

