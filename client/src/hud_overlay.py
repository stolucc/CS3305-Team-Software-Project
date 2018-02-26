"""HUD Overlay Class."""

import pygame
import math
from enum import Enum
from layout import Layout
from hexgrid import Grid
from gamestate import GameState
from civilisation import Civilisation


class InfoType(Enum):
    """Enum for types of information."""

    GOLD = 0
    FOOD = 1
    SCIENCE = 2
    PRODUCTION = 3


class HudOverlay:
    """Class to represent a HUD Overlay."""

    def __init__(self, game_state, screen_surface, resolution, zoom_level):
        """
        Construct hud_overlay.

        :param game_state: ref to current game state object.
        :param screen_surface: pygame display surface.
        :param resolution: tuple or screen resolution (w, h).
        """
        self._game_state = game_state
        self._grid = game_state.grid
        self._myciv = game_state.get_civ(self._game_state.my_id)
        self._screen = screen_surface
        self._resolution = resolution
        self._zoom_level = zoom_level
        self.font = pygame.font.Font('freesansbold.ttf', 12)
        path = "resources/images/hud/"
        x, y = 50, 50
        self._hud_images = {
            InfoType.GOLD: self._load_img(path+"gold_logo.png", x, y),
            InfoType.FOOD: self._load_img(path+"food_logo.png", x, y),
            InfoType.SCIENCE: self._load_img(path+"science_logo.png", x, y),
            InfoType.PRODUCTION: self._load_img(path+"production_logo.png", x,
                                                y)
            }
        path = "resources/images/tiles/"
        scale = round(100 / self._grid.size)
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
        self._background = (74, 74, 74)
        self._color1 = (0, 0, 0)
        self._color2 = (255, 255, 255)
        self._color3 = (124, 252, 0)

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
        resources = {InfoType.GOLD: self._myciv.gold,
                     InfoType.FOOD: self._myciv.food,
                     InfoType.SCIENCE: self._myciv.science,
                     InfoType.PRODUCTION: None}
        offset = 10
        for resource in resources:
            value = resources[resource]
            if value is not None:
                logo = self._hud_images[resource]
                self._screen.blit(logo, (offset, 5))
                self.draw_text(value, (offset+5, 30), self._color1)
                offset += 60

    def draw_info_panel(self):
        """Draw info panel containing turn details and ping."""
        points = [(self._resolution[0] - 260, 0),
                  (self._resolution[0], 0),
                  (self._resolution[0], 40),
                  (self._resolution[0] - 220, 40),
                  (self._resolution[0] - 260, 20)]
        pygame.draw.polygon(self._screen, self._background, points, 0)
        offset = self._resolution[0] - 200
        turn_count = self._game_state.turn_count
        self.draw_text("Turn: {}".format(turn_count),
                       (offset, 20),
                       self._color2)
        offset += 80
        current_player = 1  # self._game_state.current_player
        my_turn = True  # self._game_state.my_turn()
        if my_turn:
            color = self._color3
        else:
            color = self._color2
        value = "Player{}\'s Turn".format(current_player)
        self.draw_text(value,
                       (offset + 20, 20),
                       color)

    def draw_minimap(self):
        """Draw minimap."""
        lay = Layout(105, (95, self._resolution[1]-85), False)
        points = lay.polygon_corners(map_ref.get_hextile(self._color1))
        x, y = 0, self._resolution[1] - 176
        pygame.draw.rect(self._screen, self._background, (x, y, 50, 180), 0)
        pygame.draw.polygon(self._screen, self._background, points, 0)
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
        grid = self._grid
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
    civ = Civilisation(map_ref)
    game_state = GameState(1, 1, map_ref)
    game_state.add_civ(civ)
    game_state.my_id = 1
    hud = HudOverlay(game_state, screen, window_size, 50)
    hud.draw()
    while True:
        time.sleep(10)
