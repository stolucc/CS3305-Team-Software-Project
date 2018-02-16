"""HUD Overlay Class."""

import pygame
from enum import Enum


class InfoType(Enum):
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

    def __init__(self, info_ref, screen_surface, resolution):
        """
        Construct hud_overlay.

        :param info_ref: dictonary containing ref to info to be displayed.
        :param screen_surface: pygame display surface.
        :param resolution: tuple or screen resolution (w, h).
        """
        self._scale = 3
        self._info_references = {InfoType.GOLD: None,
                                 InfoType.FOOD: None,
                                 InfoType.SCIENCE: None,
                                 InfoType.PRODUCTION: None,
                                 InfoType.TURN: None,
                                 InfoType.TURN_TIME: None,
                                 InfoType.TURN_INDICATIOR: None,
                                 InfoType.PING: None}
        for key in info_ref:
            self._info_references[key] = info_ref[key]

        self._screen = screen_surface
        self._resolution = resolution
        self.font = pygame.font.Font('freesansbold.ttf', self._scale * 4)
        path = "../resources/hud/"
        self._hud_images = {
            InfoType.GOLD: self._load_img(path+"gold_logo.png", 16, 16),
            InfoType.FOOD: self._load_img(path+"food_logo.png", 16, 16),
            InfoType.SCIENCE: self._load_img(path+"science_logo.png", 16, 16),
            InfoType.PRODUCTION: self._load_img(path+"production_logo.png", 16,
                                                16)
            }

    def _load_img(self, img, size_w, size_h):
        image = pygame.image.load(img).convert_alpha()
        return self._img_scale(image, size_w, size_h)

    def _img_scale(self, img, size_w, size_h):
        return pygame.transform.scale(img, (self._scale * size_w,
                                            self._scale * size_h))

    def draw(self):
        """Draw all HUD elements."""
        self.draw_resource_panel()
        pygame.display.flip()

    def draw_resource_panel(self):
        """Draw resource panel."""
        resources = [InfoType.GOLD,
                     InfoType.FOOD,
                     InfoType.SCIENCE,
                     InfoType.PRODUCTION]
        offset = self._scale * 3
        for resource in resources:
            value = self._info_references[resource]
            if value is not None:
                logo = self._hud_images[resource]
                self._screen.blit(logo, (offset, self._scale * 2))
                self.draw_text(value, (offset, self._scale * 10))
                offset += self._scale * 20

    def draw_text(self, text, position):
        """
        Draw text to screen.

        :param text: text to be drawn.
        :param position: tuple (x,y).
        """
        text = str(text)
        text = self.font.render(text, True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (position[0] + self._scale * 8, position[1])
        self._screen.blit(text, rect)
