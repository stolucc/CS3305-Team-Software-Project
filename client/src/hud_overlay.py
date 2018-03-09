"""HUD Overlay Class."""

import pygame
import math
from layout import Layout
from mapresource import ResourceType
from currency import CurrencyType


class HudOverlay:
    """Class to represent a HUD Overlay."""

    def __init__(self, game_state, screen_surface,
                 quick_surface, resolution, layout):
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
        self._quick_surface = quick_surface
        self._resolution = resolution
        self._layout = layout
        self.font = pygame.font.Font('freesansbold.ttf', 12)
        path = "../resources/images/hud/"
        x, y = 50, 50
        self._hud_images = {
            CurrencyType.GOLD: self._load_img(path+"gold_logo.png", x, y),
            CurrencyType.FOOD: self._load_img(path+"food_logo.png", x, y),
            CurrencyType.SCIENCE: self._load_img(path+"science_logo.png",
                                                 x, y),
            ResourceType.GEMS: self._load_img(path+"gems.png", x, y),
            ResourceType.LOGS: self._load_img(path+"logs.png", x, y),
            ResourceType.COAL: self._load_img(path+"coal.png", x, y),
            ResourceType.IRON: self._load_img(path+"iron.png", x, y),
            }
        path = "../resources/images/tiles/"
        scale = round(200 / self._grid.size)
        x, y = math.ceil((scale * 2 * math.sqrt(3) / 2)), scale * 2
        self._map_layout = Layout(scale, (200, self._resolution[1]-170))
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
            (3, 2): self._load_img(path+"ocean.png", x, y),
            0: self._load_img(path+"view-highlight.png", x, y)}
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
        self._screen.fill((0, 0, 0, 0))
        self.draw_resource_panel()
        self.draw_info_panel()
        self.draw_minimap()

    def draw_quick_surface(self, layouts):
        """Draw quick moving HUD elements."""
        self._quick_surface.fill((0, 0, 0, 0))
        self.draw_view(layouts)

    def draw_view(self, layouts):
        """Draw box showing current view."""
        self.highlight_view(self._layout)
        for layout in layouts:
            self.highlight_view(layout)

    def highlight_view(self, layout):
        """Highlight viewed tiles."""
        size = pygame.display.get_surface().get_size()
        image = self.map_imgs[0]
        for hex_point in self._grid.get_hextiles():
            hexagon = self._grid.get_hextile(hex_point)
            hexagon_coords = layout.hex_to_pixel(hexagon)
            if (size[0] + 100 > hexagon_coords[0] > -100 and
               size[1] + 100 > hexagon_coords[1] > -100):
                hexagon_coords = self._map_layout.hex_to_pixel(hexagon)
                self._quick_surface.blit(
                        image,
                        (hexagon_coords[0]
                         - math.ceil(self._map_layout.size
                         * (math.sqrt(3) / 2)),
                         hexagon_coords[1] - self._map_layout.size))

    def draw_resource_panel(self):
        """Draw resource panel."""
        mapresources = self._myciv.resources
        resources = {CurrencyType.GOLD: self._myciv.gold,
                     CurrencyType.FOOD: self._myciv.food,
                     CurrencyType.SCIENCE: self._myciv.science,
                     ResourceType.GEMS: mapresources[ResourceType.GEMS],
                     ResourceType.LOGS: mapresources[ResourceType.LOGS],
                     ResourceType.COAL: mapresources[ResourceType.COAL],
                     ResourceType.IRON: mapresources[ResourceType.IRON]}
        points = [(450, 0),
                  (0, 0),
                  (0, 60),
                  (430, 60),
                  (450, 40)]
        pygame.draw.polygon(self._screen, self._background, points, 0)
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
        my_turn = True  # self._game_state.my_turn()
        if my_turn:
            color = self._color3
        else:
            color = self._color2
        value = "Player{}\'s Turn".format(self._game_state._current_player)
        self.draw_text(value,
                       (offset + 20, 20),
                       color)

    def draw_minimap(self):
        """Draw minimap."""
        lay = Layout(200, (200, self._resolution[1]-170), False)
        points = lay.polygon_corners(self._grid.get_hextile(self._color1))
        x, y = 0, self._resolution[1] - 344
        pygame.draw.rect(self._screen,
                         self._background, (x, y, 100, 350), 0)
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
