"""HUD Overlay Class."""

import pygame
import math
from enum import Enum
from layout import Layout
from hexgrid import Grid


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
    MAP = 8


class HudOverlay:
    """Class to represent a HUD Overlay."""

    def __init__(self, info_ref, screen_surface, resolution):
        """
        Construct hud_overlay.

        :param info_ref: dictonary containing ref to info to be displayed.
        :param screen_surface: pygame display surface.
        :param resolution: tuple or screen resolution (w, h).
        """
        self._info_references = {InfoType.GOLD: None,
                                 InfoType.FOOD: None,
                                 InfoType.SCIENCE: None,
                                 InfoType.PRODUCTION: None,
                                 InfoType.TURN: None,
                                 InfoType.TURN_TIME: None,
                                 InfoType.TURN_INDICATIOR: None,
                                 InfoType.PING: None,
                                 InfoType.MAP: None}
        for key in info_ref:
            self._info_references[key] = info_ref[key]

        self._screen = screen_surface
        self._resolution = resolution
        self.font = pygame.font.Font('freesansbold.ttf', 12)
        path = "../resources/images/hud/"
        x, y = 50, 50
        self._hud_images = {
            InfoType.GOLD: self._load_img(path+"gold_logo.png", x, y),
            InfoType.FOOD: self._load_img(path+"food_logo.png", x, y),
            InfoType.SCIENCE: self._load_img(path+"science_logo.png", x, y),
            InfoType.PRODUCTION: self._load_img(path+"production_logo.png", x,
                                                y)
            }
        path = "../resources/images/tiles/"
        scale = round(100 / self._info_references[InfoType.MAP].size)
        x, y = math.ceil((scale * 2 * math.sqrt(3) / 2)), scale * 2
        self._map_layout = Layout(scale, (95, self._resolution[1]-85))
        self.map_imgs = {
            (0, 0): self._load_img(path+"tundra_flat.png", x, y),
            (0, 1): self._load_img(path+"grassland_flat.png", x, y),
            (0, 2): self._load_img(path+"desert_flat.png", x, y),
            (1, 0): self._load_img(path+"tundra_hill.png", x, y),
            (1, 1): self._load_img(path+"grassland_hill.png", x, y),
            (1, 2): self._load_img(path+"desert_hill.png", x, y),
            (2, 0): self._load_img(path+"tundra_mountain.png", x, y),
            (2, 1): self._load_img(path+"grassland_mountain.png", x, y),
            (2, 2): self._load_img(path+"desert_mountain.png", x, y),
            (3, 0): self._load_img(path+"ocean.png", x, y),
            (3, 1): self._load_img(path+"ocean.png", x, y),
            (3, 2): self._load_img(path+"ocean.png", x, y)}

    def _load_img(self, img, size_w, size_h):
        image = pygame.image.load(img).convert_alpha()
        return self._img_scale(image, size_w, size_h)

    def _img_scale(self, img, size_w, size_h):
        return pygame.transform.smoothscale(img, (size_w, size_h))

    def draw(self):
        """Draw all HUD elements."""
        self.draw_resource_panel()
        self.draw_info_panel()
        self.draw_minimap()
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
                self._screen.blit(logo, (offset, 5))
                self.draw_text(value, (offset+5, 30), (0, 0, 0))
                offset += 60

    def draw_info_panel(self):
        """Draw info panel containing turn details and ping."""
        points = [(self._resolution[0] - 380, 0),
                  (self._resolution[0], 0),
                  (self._resolution[0], 40),
                  (self._resolution[0] - 360, 40),
                  (self._resolution[0] - 380, 20)]
        pygame.draw.polygon(self._screen, (74, 74, 74), points, 0)
        info = [(InfoType.TURN, "Turn: "),
                (InfoType.TURN_TIME, "Time left: "),
                (InfoType.PING, "Ping: ")]
        offset = self._resolution[0] - 360
        for detail in info:
            value = self._info_references[detail[0]]
            if value is not None:
                self.draw_text(detail[1] + str(value),
                               (offset, 20),
                               (255, 255, 255))
                offset += 80
        value = self._info_references[InfoType.TURN_INDICATIOR]
        if value[1]:
            color = (124, 252, 0)
        else:
            color = (255, 255, 255)
        value = value[0] + "\'s Turn"
        self.draw_text(value,
                       (offset + 20, 20),
                       color)

    def draw_minimap(self):
        """Draw minimap."""
        lay = Layout(105, (95, self._resolution[1]-85), False)
        points = lay.polygon_corners(map_ref.get_hextile((0, 0, 0)))
        x, y = 0, self._resolution[1] - 176
        pygame.draw.rect(self._screen, (74, 74, 74), (x, y, 50, 180), 0)
        pygame.draw.polygon(self._screen, (74, 74, 74), points, 0)
        self.draw_hex_grid()

    def draw_text(self, text, position, color):
        """
        Draw text to screen.

        :param text: text to be drawn.
        :param position: tuple (x,y).
        """
        text = str(text)
        text = self.font.render(text, True, color)
        rect = text.get_rect()
        rect.center = (position[0] + 20, position[1])
        self._screen.blit(text, rect)

    def draw_hex_grid(self):
        """Draw the hexgrid."""
        grid = self._info_references[InfoType.MAP]
        for hex_point in grid.get_hextiles():
            hexagon = grid.get_hextile(hex_point)
            hexagon_coords = self._map_layout.hex_to_pixel(hexagon)
            terrain = hexagon.terrain
            terrain_image = self.map_imgs[
                    (terrain.terrain_type.value, terrain.biome.value)]
            self._screen.blit(
                    terrain_image,
                    (hexagon_coords[0]
                     - math.ceil(self._map_layout.size * (math.sqrt(3) / 2)),
                     hexagon_coords[1] - self._map_layout.size))


if __name__ == "__main__":
    import time
    pygame.init()
    pygame.font.init()
    map_ref = Grid(26)
    map_ref.create_grid()
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
                      InfoType.PING: 32,
                      InfoType.MAP: map_ref
                      },
                     screen, window_size)
    hud.draw()
    while True:
        time.sleep(10)
