"""Unit representation."""


class Unit:
    """Base class for the units."""

    def __init__(self, health, level, movement_range, cost, hextile):
        """
        Initialise units attributes.

        :param health: Amount of health unit begins with
        :param level: Level of the unit
        :param movement_range: Amount of tiles the unit can travel
        :param cost: Cost of the unit in resources per turn
        :param hex: Current hex tile the unit is on
        """
        self._health = health
        self._max_health = health
        self._level = level
        self._movement_range = movement_range
        self._cost = cost
        self._position = hextile

    @property
    def health(self):
        """
        Health of the unit.

        :return: current health of the unit
        """
        return self._health

    @health.setter
    def health(self, health):
        """
        Set health of the unit.

        :param health:
        """
        self._health = health

    @property
    def max_health(self):
        """
        Max health of the unit.

        :return: current max health of the unit
        """
        return self._max_health

    @max_health.setter
    def max_health(self, max_health):
        """
        Set max health.

        :param max_health: new max health of the unit
        """
        self._max_health = max_health

    @property
    def level(self):
        """
        Level of the unit.

        :return: current level of the unit
        """
        return self._level

    @level.setter
    def level(self, level):
        """
        Set level.

        :param level: set new level of the unit
        """
        self._level = level

    @property
    def movement_range(self):
        """
        Movement range of the unit.

        :return: current movement range of the unit
        """
        return self._movement_range

    @movement_range.setter
    def movement_range(self, movement_range):
        """
        Set movement range.

        :param movement_range: set new movement range of the unit
        """
        self._movement_range = movement_range

    @property
    def cost(self):
        """
        Cost of unit per turn.

        :return: dict of resource costs
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """
        Set new cost of unit.

        :param cost: dict of resource costs
        """
        self._cost = cost

    @property
    def position(self):
        """
        Position of unit.

        :return: hex tile that unit is positioned on
        """
        return self._position

    @position.setter
    def position(self, hex):
        """
        Set position of unit.

        :param hex: new hex tile that unit is situated on
        """
        self._position = hex

    def cost_increase(self, food, gold, science):
        """
        Increase cost of resources used per turn.

        :param food: int
        :param gold: int
        :param science: int
        :return:
        """
        self._cost['food'] += food
        self._cost['gold'] += gold
        self._cost['science'] += science

    def level_up(self, health_increase, movement_increase):
        """
        Increase level and attributes.

        :param health_increase: amount health should increase by
        :param movement_increase: amount movement_range should increase by
        """
        self._health += health_increase
        self._max_health += health_increase
        self._movement_range += movement_increase
        self._level += 1

    def receive_damage(self, damage):
        """
        Take damage from attack.

        :param damage: amount of damage to be taken from health
        """
        self._health -= damage
        if self._health <= 0:
            self.health = 0

    def restore_health(self, restore):
        """
        Restore health of unit.

        :param restore: amount of health to be restored
        """
        health = self.health + restore
        if health > self.max_health:
            self._health = self.max_health
        else:
            self._health = health

    def __repr__(self):
        """
        Return string representation.

        :return: string
        """
        string = "Health: %i, Max Health: %i, " \
                 "Movement Range: %i, Level: %i, Cost:(Food:%i Gold:%i, " \
                 "Science:%i), Position: %i,%i,%i, " % \
                 (self._health, self._max_health, self._movement_range,
                  self._level, self._cost['food'], self._cost['gold'],
                  self._cost['science'], self._position.x, self._position.y,
                  self._position.z)
        return string


class Worker(Unit):
    """Worker class, for creating and upgrading buildings."""

    def __init__(self, level, hex):
        """
        Initialise workers attributes.

        :param level: int Level of the unit
        :param hex: Current hex tile the unit is on
        """
        increment = level - 1
        health = 100 + 10 * increment
        movement = 4 + increment
        cost = {'food': level, 'gold': 0, 'science': 0}
        super().__init__(health, level, movement, cost, hex)
        self._build_speed = level

    @property
    def build_speed(self):
        """
        Build speed of worker.

        :return: int current build speed of worker
        """
        return self._build_speed

    @build_speed.setter
    def build_speed(self, build_speed):
        """
        Set new build speed of worker.

        :param build_speed: int new build speed of worker
        """
        self._build_speed = build_speed

    def level_up(self):
        """
        Worker unit levels up.

        Health increases by 20, movement and build_speed by 1, each level
        """
        if self.level >= 3:
            print("Max level reached.")
        else:
            self.cost_increase(food=1, gold=0, science=0)
            super().level_up(health_increase=20, movement_increase=1)
            self.build_speed += 1

    def __repr__(self):
        """
        Return string representation of Worker class.

        :return: string
        """
        string = "Worker: "
        string += super().__repr__()
        string += "Build Speed: %i" % (self._build_speed)
        return string


class Soldier(Unit):
    """Soldier unit, for attacking other units and buildings."""

    def __init__(self, health, level, movement_range, strength, attack_range,
                 cost, hex):
        """
        Initialise soldiers attributes.

        :param health: Amount of health unit begins with
        :param level: Level of the unit
        :param movement_range: Amount of tiles the unit can travel
        :param strength: Strength of the soldier
        :param attack_range: Amount of tiles unit can attack across
        :param cost: Cost of unit on resources per turn
        :param hex: Current hex tile the unit is on
        """
        self._strength = strength
        self._attack_range = attack_range
        super().__init__(health, level, movement_range, cost, hex)

    @property
    def strength(self):
        """
        Soldier strength when attacking.

        :return: int current soldiers strength
        """
        return self._strength

    @strength.setter
    def strength(self, strength):
        """
        Set new strength of soldier.

        :param strength: int new strength of soldier
        """
        self._strength = strength

    @property
    def attack_range(self):
        """
        Attack range of the soldier.

        :return: int amount of tiles unit can attack across
        """
        return self._attack_range

    @attack_range.setter
    def attack_range(self, attack_range):
        """
        Set attack range.

        :param attack_range: int new attack range of unit
        """
        self._attack_range = attack_range

    def attack_power(self):
        """
        Attack power.

        :return:
        """
        power = self.strength * (self.health/self.max_health)
        return power


class Swordsman(Soldier):
    """Close range soldier."""

    def __init__(self, level, hex):
        """
        Set Swordsman attributes according to level.

        :param level: int
        :param hex: Hex
        """
        increment = level - 1
        health = 130 + 30 * increment
        movement_range = 4 + increment
        strength = 30 + 20 * increment
        cost = {'food': level, 'gold': level-1, 'science': 0}
        super().__init__(health, level, movement_range, strength,
                         attack_range=1, cost=cost, hex=hex)

    def level_up(self):
        """Level up Swordsman."""
        if self._level >= 3:
            print("Max level reached.")
        else:
            super().level_up(health_increase=30, movement_increase=1)
            self.cost_increase(food=1, gold=1, science=0)
            self.strength += 20

    def __repr__(self):
        """
        Return string representation of Swordsman.

        :return: string
        """
        string = "Swordsman: " + super().__repr__()
        string += "Strength: %i, Attack Range: %i" % (self.strength,
                                                      self.attack_range)
        return string


class Archer(Soldier):
    """Long range Soldier class."""

    def __init__(self, level, hex):
        """
        Set Archers attributes according to level.

        :param level: int
        :param hex: Hex
        """
        increment = level - 1
        health = 110 + 20 * increment
        movement_range = 5 + increment
        strength = 20 + 10 * increment
        attack_range = 2 + increment
        cost = {'food': 2, 'gold': 0, 'science': level-1}
        super().__init__(health, level, movement_range, strength, attack_range,
                         cost, hex)

    def level_up(self):
        """Level up Archer."""
        if self._level >= 3:
            print("Max level reached.")
        else:
            super().level_up(health_increase=20, movement_increase=1)
            self.cost_increase(food=0, gold=0, science=1)
            self.strength += 10
            self.attack_range += 1

    def __repr__(self):
        """
        Return string representation of Archer class.

        :return: string
        """
        string = "Archer: " + super().__repr__()
        string += "Strength: %i, Attack Range: %i" % (self.strength,
                                                      self.attack_range)
        return string


# if __name__ == "__main__":
    # hex = Hex(1, -1, 0)
    # worker = Worker(3, hex)
    # sword = Swordsman(3, hex)
    # archer = Archer(3, hex)
    # print(worker)
    # print(sword)
    # print(archer)