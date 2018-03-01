import pygame
from pygame.locals import *
from building import BuildingType


IMAGE_PATH = "../resources/images/"


def load_image(image):
    """
    Load and convert images.

    :param image: The image to be loaded.
    :return: a loaded and converted image.
    """
    return pygame.image.load(IMAGE_PATH + image).convert_alpha()


class LoadImages:
    def __init__(self):
        self._terrain_images = {
            "move-highlight": load_image("tiles/move-highlight.png"),
            "civ1_border": load_image("tiles/civ1_border.png"),
            "civ2_border": load_image("tiles/civ2_border.png"),
            "civ3_border": load_image("tiles/civ3_border.png"),
            "civ4_border": load_image("tiles/civ4_border.png"),
            (0, 0): load_image("tiles/tundra_flat.png"),
            (0, 1): load_image("tiles/grassland_flat.png"),
            (0, 2): load_image("tiles/desert_flat.png"),
            (1, 0): load_image("tiles/tundra_hill.png"),
            (1, 1): load_image("tiles/grassland_hill.png"),
            (1, 2): load_image("tiles/desert_hill.png"),
            (2, 0): load_image("tiles/tundra_mountain.png"),
            (2, 1): load_image("tiles/grassland_mountain.png"),
            (2, 2): load_image("tiles/desert_mountain.png"),
            (3, 0): load_image("tiles/ocean.png"),
            (3, 1): load_image("tiles/ocean.png"),
            (3, 2): load_image("tiles/ocean.png"),
        }
        self._sprite_images = {
            "Archer1": load_image("units/archers1.png"),
            "Archer2": load_image("units/archers2.png"),
            "Archer3": load_image("units/archers3.png"),
            "Swordsman1": load_image("units/swords1.png"),
            "Swordsman2": load_image("units/swords2.png"),
            "Swordsman3": load_image("units/swords3.png"),
            "Worker1": load_image("units/workers1.png"),
            "Worker2": load_image("units/workers2.png"),
            "Worker3": load_image("units/workers3.png")
        }
        self._health_bar_images = {
            0: load_image("health/health_bar_0.png"),
            5: load_image("health/health_bar_5.png"),
            10: load_image("health/health_bar_10.png"),
            15: load_image("health/health_bar_15.png"),
            20: load_image("health/health_bar_20.png"),
            25: load_image("health/health_bar_25.png"),
            30: load_image("health/health_bar_30.png"),
            35: load_image("health/health_bar_35.png"),
            40: load_image("health/health_bar_40.png"),
            45: load_image("health/health_bar_45.png"),
            50: load_image("health/health_bar_50.png"),
            55: load_image("health/health_bar_55.png"),
            60: load_image("health/health_bar_60.png"),
            65: load_image("health/health_bar_65.png"),
            70: load_image("health/health_bar_70.png"),
            75: load_image("health/health_bar_75.png"),
            80: load_image("health/health_bar_80.png"),
            85: load_image("health/health_bar_85.png"),
            90: load_image("health/health_bar_90.png"),
            95: load_image("health/health_bar_95.png"),
            100: load_image("health/health_bar_100.png")
        }
        self._building_images = {
            BuildingType.CITY: load_image("buildings/city.png"),
            BuildingType.FARM: load_image("buildings/farm.png"),
            BuildingType.TRADE_POST: load_image("buildings/trading_post.png"),
            BuildingType.UNIVERSITY: load_image("buildings/university.png")
        }

    def load_terrain_images(self):
        return self._terrain_images

    def load_sprite_images(self):
        return self._sprite_images

    def load_health_bar_images(self):
        return self._health_bar_images

    def load_building_images(self):
        return self._building_images

