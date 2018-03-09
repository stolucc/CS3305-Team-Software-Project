"""Module for loading of game resources."""
import pygame
from building import BuildingType
from mapresource import ResourceType


IMAGE_PATH = "../resources/images/"


class LoadImages:
    """Class to load and store images in dictionaries."""

    @staticmethod
    def load_image(image):
        """
        Load and convert images.

        :param image: The image to be loaded.
        :return: a loaded and converted image.
        """
        return pygame.image.load(IMAGE_PATH + image).convert_alpha()

    def __init__(self):
        """Initialise a LoadImages object."""
        self._terrain_images = {
            "move-highlight":
                LoadImages.load_image("tiles/move-highlight.png"),
            "civ1_border": LoadImages.load_image("tiles/civ1_border.png"),
            "civ2_border": LoadImages.load_image("tiles/civ2_border.png"),
            "civ3_border": LoadImages.load_image("tiles/civ3_border.png"),
            "civ4_border": LoadImages.load_image("tiles/civ4_border.png"),
            (0, 0): LoadImages.load_image("tiles/tundra_flat.png"),
            (0, 1): LoadImages.load_image("tiles/grassland_flat.png"),
            (0, 2): LoadImages.load_image("tiles/desert_flat.png"),
            (1, 0): LoadImages.load_image("tiles/tundra_hill.png"),
            (1, 1): LoadImages.load_image("tiles/grassland_hill.png"),
            (1, 2): LoadImages.load_image("tiles/desert_hill.png"),
            (2, 0): LoadImages.load_image("tiles/tundra_mountain.png"),
            (2, 1): LoadImages.load_image("tiles/grassland_mountain.png"),
            (2, 2): LoadImages.load_image("tiles/desert_mountain.png"),
            (3, 0): LoadImages.load_image("tiles/ocean.png"),
            (3, 1): LoadImages.load_image("tiles/ocean.png"),
            (3, 2): LoadImages.load_image("tiles/ocean.png"),
            "fogofwar": LoadImages.load_image("tiles/fog-of-war.png")
        }
        self._sprite_images = {
            "Archer1": LoadImages.load_image("units/archers1.png"),
            "Archer2": LoadImages.load_image("units/archers2.png"),
            "Archer3": LoadImages.load_image("units/archers3.png"),
            "Swordsman1": LoadImages.load_image("units/swords1.png"),
            "Swordsman2": LoadImages.load_image("units/swords2.png"),
            "Swordsman3": LoadImages.load_image("units/swords3.png"),
            "Worker1": LoadImages.load_image("units/workers1.png"),
            "Worker2": LoadImages.load_image("units/workers2.png"),
            "Worker3": LoadImages.load_image("units/workers3.png")
        }
        self._health_bar_images = {
            0: LoadImages.load_image("health/health_bar_0.png"),
            5: LoadImages.load_image("health/health_bar_5.png"),
            10: LoadImages.load_image("health/health_bar_10.png"),
            15: LoadImages.load_image("health/health_bar_15.png"),
            20: LoadImages.load_image("health/health_bar_20.png"),
            25: LoadImages.load_image("health/health_bar_25.png"),
            30: LoadImages.load_image("health/health_bar_30.png"),
            35: LoadImages.load_image("health/health_bar_35.png"),
            40: LoadImages.load_image("health/health_bar_40.png"),
            45: LoadImages.load_image("health/health_bar_45.png"),
            50: LoadImages.load_image("health/health_bar_50.png"),
            55: LoadImages.load_image("health/health_bar_55.png"),
            60: LoadImages.load_image("health/health_bar_60.png"),
            65: LoadImages.load_image("health/health_bar_65.png"),
            70: LoadImages.load_image("health/health_bar_70.png"),
            75: LoadImages.load_image("health/health_bar_75.png"),
            80: LoadImages.load_image("health/health_bar_80.png"),
            85: LoadImages.load_image("health/health_bar_85.png"),
            90: LoadImages.load_image("health/health_bar_90.png"),
            95: LoadImages.load_image("health/health_bar_95.png"),
            100: LoadImages.load_image("health/health_bar_100.png")
        }
        self._building_images = {
            BuildingType.CITY: LoadImages.load_image("buildings/city.png"),
            BuildingType.FARM: LoadImages.load_image("buildings/farm.png"),
            BuildingType.TRADE_POST:
                LoadImages.load_image("buildings/" + "trading_post.png"),
            BuildingType.UNIVERSITY:
                LoadImages.load_image("buildings/university.png")
        }
        self._resource_images = {
            ResourceType.COAL: LoadImages.load_image("map_resources/coal.png"),
            ResourceType.IRON: LoadImages.load_image("map_resources/iron.png"),
            ResourceType.GEMS: LoadImages.load_image("map_resources/gems.png"),
            ResourceType.LOGS: LoadImages.load_image("map_resources/logs.png")
        }

    def load_terrain_images(self):
        """
        Getter for terrain images.

        :return: Dictonary of terrain images.
        """
        return self._terrain_images

    def load_sprite_images(self):
        """
        Getter for sprite images.

        :return: Dictonary of sprite images.
        """
        return self._sprite_images

    def load_health_bar_images(self):
        """
        Getter for health bar images.

        :return: Dictonary of health bar images.
        """
        return self._health_bar_images

    def load_building_images(self):
        """
        Getter for building images.

        :return: Dictonary of building images.
        """
        return self._building_images

    def load_resource_images(self):
        """
        Getter for resource images.

        :return: Dictonary of resource images.
        """
        return self._resource_images
