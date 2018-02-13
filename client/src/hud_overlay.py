"""HUD Overlay Class."""

from Enum import enum


class InfoType(enum):
    """Enum for types of information."""

    GOLD = 0
    FOOD = 1
    SCIENCE = 2
    PRODUCTION = 3
    TURN = 4
    TURN_TIME = 5
    TURN_INDICATIOR = 6
    PING = 7


class HudOverlay:
    """Class to represent a HUD Overlay."""

    def __init__(self, info_ref):
        """
        Construct hud_overlay.

        :param info_ref: dictonary containing ref to info to be displayed.
        """
        self.info_references = {InfoType.GOLD: None,
                                InfoType.FOOD: None,
                                InfoType.SCIENCE: None,
                                InfoType.PRODUCTION: None,
                                InfoType.TURN: None,
                                InfoType.TURN_TIME: None,
                                InfoType.TURN_INDICATIOR: None,
                                InfoType.PING: None}
        for key in info_ref:
            self.info_references[key] = info_ref[key]
