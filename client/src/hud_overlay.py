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

    def __init__(self, info_ref, screen, resolution):
        """
        Construct hud_overlay.

        :param info_ref: dictonary containing ref to info to be displayed.
        :param screen: pygame display surface.
        :param resolution: tuple or screen resolution (w, h).
        """
        self._info_references = {InfoType.GOLD: 12,
                                 InfoType.FOOD: 9,
                                 InfoType.SCIENCE: 160,
                                 InfoType.PRODUCTION: 1280,
                                 InfoType.TURN: None,
                                 InfoType.TURN_TIME: None,
                                 InfoType.TURN_INDICATIOR: None,
                                 InfoType.PING: None}
        for key in info_ref:
            self._info_references[key] = info_ref[key]

        self._screen = screen
        self._resolution = resolution
        self.font = pygame.font.Font('freesansbold.ttf', 12)
        self._load_img = lambda x: pygame.image.load(x).convert_alpha()
        self._hud_images = {
            InfoType.GOLD: self._load_img("gold_logo.png"),
            InfoType.FOOD: self._load_img("food_logo.png"),
            InfoType.SCIENCE: self._load_img("science_logo.png"),
            InfoType.PRODUCTION: self._load_img("production_logo.png")
            }

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
        offset = 10
        for resource in resources:
            value = self._info_references[resource]
            if value is not None:
                logo = self._hud_images[resource]
                screen.blit(logo, (offset, 6))
                self.draw_text(value, (offset, 30))
                offset += 60

    def draw_text(self, text, position):
        """
        Draw text to screen.

        :param text: text to be drawn.
        :param position: tuple (x,y).
        """
        text = str(text)
        text = self.font.render(text, True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (position[0] + 24, position[1])
        screen.blit(text, rect)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    flags = (pygame.DOUBLEBUF |
             pygame.HWSURFACE)
    window_size = (1024, 576)
    camera_position = (window_size[0]/2,
                       window_size[1]/2)
    screen = pygame.display.set_mode(window_size,
                                     flags,
                                     0)
    font = 'freesansbold.ttf'
    font_size = 115
    hud = HudOverlay({}, screen, window_size)
    hud.draw()
    while True:
        pass
