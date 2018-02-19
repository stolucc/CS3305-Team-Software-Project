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
        self._scale = 50
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
        self.font = pygame.font.Font('freesansbold.ttf', int(self._scale // 3))
        path = "../resources/images/hud/"
        self._hud_images = {
            InfoType.GOLD: self._load_img(path+"gold_logo.png", 1, 1),
            InfoType.FOOD: self._load_img(path+"food_logo.png", 1, 1),
            InfoType.SCIENCE: self._load_img(path+"science_logo.png", 1, 1),
            InfoType.PRODUCTION: self._load_img(path+"production_logo.png", 1,
                                                1)
            }

    def _load_img(self, img, size_w, size_h):
        image = pygame.image.load(img).convert_alpha()
        return self._img_scale(image, size_w, size_h)

    def _img_scale(self, img, size_w, size_h):
        return pygame.transform.scale(img, (self._scale // size_w,
                                            self._scale // size_h))

    def draw(self):
        """Draw all HUD elements."""
        self.draw_resource_panel()
        self.draw_info_panel()
        pygame.display.flip()

    def draw_resource_panel(self):
        """Draw resource panel."""
        resources = [InfoType.GOLD,
                     InfoType.FOOD,
                     InfoType.SCIENCE,
                     InfoType.PRODUCTION]
        offset = self._scale // 3
        for resource in resources:
            value = self._info_references[resource]
            if value is not None:
                logo = self._hud_images[resource]
                self._screen.blit(logo, (offset, self._scale // 4))
                self.draw_text(value, (offset, self._scale * 0.75), (0, 0, 0))
                offset += self._scale // 0.75

    def draw_info_panel(self):
        """Draw info panel containing turn details and ping."""
        info = [(InfoType.TURN, "Turn: "),
                (InfoType.TURN_TIME, "Time left: "),
                (InfoType.PING, "Ping: ")]
        offset = self._resolution[0]/2 + self._scale
        for detail in info:
            value = self._info_references[detail[0]]
            if value is not None:
                # logo = self._hud_images[resource]
                # self._screen.blit(logo, (offset, self._scale * 2))
                self.draw_text(detail[1] + str(value),
                               (offset, self._scale * 0.4),
                               (255, 255, 255))
                offset += self._scale // 0.5
        value = self._info_references[InfoType.TURN_INDICATIOR]
        if value[1]:
            color = (124, 252, 0)
        else:
            color = (0, 0, 0)
        value = value[0] + "\'s Turn"
        self.draw_text(value,
                       (offset + self._scale // 2, self._scale * 0.4),
                       color)

    def draw_text(self, text, position, color):
        """
        Draw text to screen.

        :param text: text to be drawn.
        :param position: tuple (x,y).
        """
        text = str(text)
        text = self.font.render(text, True, color)
        rect = text.get_rect()
        rect.center = (position[0] + self._scale // 2, position[1])
        self._screen.blit(text, rect)


if __name__ == "__main__":
    import time
    pygame.init()
    pygame.font.init()
    flags = (pygame.DOUBLEBUF |
             pygame.HWSURFACE)
    window_size = (1024, 576)
    screen = pygame.display.set_mode(window_size, flags, 0)
    hud = HudOverlay({InfoType.GOLD: 9,
                      InfoType.FOOD: 12,
                      InfoType.SCIENCE: 980,
                      InfoType.PRODUCTION: 1200,
                      InfoType.TURN: 56,
                      InfoType.TURN_TIME: 30,
                      InfoType.TURN_INDICATIOR: ("Alessia", True),
                      InfoType.PING: 32},
                     screen, window_size)
    hud.draw()
    while True:
        time.sleep(10)
