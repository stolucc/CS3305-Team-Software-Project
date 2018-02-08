"""Client game."""
from copy import copy

import pygame
import sys
import time
from layout import Layout
from hexgrid import Grid, Hex
from enum import Enum
import os
from math import floor
import math


class Resolution(Enum):
    """Enum for resolutions."""

    DEFAULT = 0
    HD = 1
    FULLHD = 2

    @staticmethod
    def get_resolution(index):
        """Getter for resolution."""
        resolutions = {Resolution.DEFAULT: (1024, 576),
                       Resolution.HD: (1280, 720),
                       Resolution.FULLHD: (1920, 1080)}
        return resolutions[index]


class Game:
    """Class to represent client-side game."""

    def __init__(self):
        """Initialise display surface."""
        pygame.init()
        pygame.font.init()
        self._flags = (pygame.DOUBLEBUF |
                       pygame.HWSURFACE |
                       pygame.FULLSCREEN)
        self.infoObject = pygame.display.Info()
        self._window_size = Resolution.get_resolution(Resolution.FULLHD)
        self._camera_position = (self._window_size[0] / 2,
                                 self._window_size[1] / 2)
        self._screen = pygame.display.set_mode(self._window_size,
                                               self._flags,
                                               0)
        self._font = 'freesansbold.ttf'
        self._font_size = 115
        self._grid_size = 25
        self._zoom = 50
        self._zoom_interval = 5
        self._min_zoom = 1
        self._max_zoom = 1000
        self._hex_size = lambda x: (self.infoObject.current_w // x)
        self._grid = Grid(self._grid_size)
        self._grid.create_grid()
        self._layout = Layout(self._hex_size(self._zoom),
                              (self._window_size[0] / 2,
                               self._window_size[1] / 2))
        self._terrain_images = {(0, 0): pygame.image.load("tundra_flat.png").convert_alpha(),
                                (0, 1): pygame.image.load("grassland_flat.png").convert_alpha(),
                                (0, 2): pygame.image.load("desert_flat.png").convert_alpha(),
                                (1, 0): pygame.image.load("tundra_hill.png").convert_alpha(),
                                (1, 1): pygame.image.load("grassland_hill.png").convert_alpha(),
                                (1, 2): pygame.image.load("desert_hill.png").convert_alpha(),
                                (2, 0): pygame.image.load("tundra_mountain.png").convert_alpha(),
                                (2, 1): pygame.image.load("grassland_mountain.png").convert_alpha(),
                                (2, 2): pygame.image.load("desert_mountain.png").convert_alpha(),
                                (3, 0): pygame.image.load("ocean.png").convert_alpha(),
                                (3, 1): pygame.image.load("ocean.png").convert_alpha(),
                                (3, 2): pygame.image.load("ocean.png").convert_alpha()}

        self._scaled_terrain_images = self._terrain_images.copy()

    def start(self):
        """Start game."""
        self.scale_images_to_hex_size()
        self.draw_map()
        while True:
            for event in pygame.event.get():  # something happened
                if event.type in [pygame.QUIT, pygame.KEYDOWN]:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_down(event)
            time.sleep(0.001)

    def mouse_button_down(self, event):
        """Mouse down actions."""
        if event.button == 1:  # Left click
            self.panning()
        elif event.button == 2:  # Middle click
            pass
        elif event.button == 3:  # Right click
            pass
        elif event.button == 4:  # Scroll up
            self.zoom_in()
        elif event.button == 5:  # Scroll down
            self.zoom_out()

    def panning(self):
        """Move map while holding down."""
        pygame.mouse.get_rel()
        holding = True
        while holding:
            pygame.event.get()
            change = pygame.mouse.get_rel()
            c_hex = self._layout.pixel_to_hex(self._camera_position)
            c_hex_coords = self._grid.hex_round((c_hex.x, c_hex.y, c_hex.z))
            wrap = self._grid.get_hextile(c_hex_coords)
            if (wrap.x, wrap.y, wrap.z) != c_hex_coords:
                pix_change = self._layout.hex_to_pixel(wrap)
                change = (self._camera_position[0] - pix_change[0],
                          self._camera_position[1] - pix_change[1])
            self._layout.change_origin(change)
            self.draw_map()
            holding = pygame.mouse.get_pressed()[0]

    def zoom_in(self):
        """Zooming in on map."""
        self._zoom -= self._zoom_interval
        if self._zoom <= self._min_zoom:
            self._zoom = self._min_zoom
        else:
            self._layout.size = self._hex_size(self._zoom)
            self.scale_images_to_hex_size()
            self.draw_map()

    def zoom_out(self):
        """Zooming away from map."""
        self._zoom += self._zoom_interval
        if self._zoom >= self._max_zoom:
            self._zoom = self._max_zoom
        else:
            self._layout.size = self._hex_size(self._zoom)
            self.scale_images_to_hex_size()
            self.draw_map()

    def scale_images_to_hex_size(self, ):
        for k in self._terrain_images:
            self._scaled_terrain_images[k] = pygame.transform.smoothscale(
                self._terrain_images[k],
                (math.ceil((self._hex_size(self._zoom) * 2) * math.sqrt(3) / 2),
                 self._hex_size(self._zoom) * 2))

    def draw_sprite(self, hexagon, layout, size, sprite):
        """Draw a sprite on a hex tile."""
        center_x, center_y = layout.hex_to_pixel(hexagon)
        adjusted_size = floor(size / self._zoom)
        sprite = pygame.transform.scale(sprite,
                                        (adjusted_size,
                                         adjusted_size))
        sprite.convert()
        offset = size / (self._zoom * 2)
        self._screen.blit(sprite,
                          (floor(center_x - offset),
                           floor(center_y - offset)))

    def draw_hex_grid(self, layout):
        """Create a hex grid."""
        size = pygame.display.get_surface().get_size()
        for hex_point in self._grid.get_hextiles():

            hexagon = self._grid.get_hextile(hex_point)
            hexagon_coords = layout.hex_to_pixel(hexagon)
            if (size[0] + 100 > hexagon_coords[0] > -100 and
               size[1] + 100 > hexagon_coords[1] > -100):
                terrain = hexagon.terrain
                terrain_image = self._scaled_terrain_images[(terrain.terrain_type.value, terrain.biome.value)]
                self._screen.blit(terrain_image,
                                  (hexagon_coords[0] - math.ceil(self._layout.size * (math.sqrt(3) / 2)),
                                   hexagon_coords[1] - self._layout.size))
                sprite = pygame.image.load(os.path.join("..", "resources",
                                                        "units", "archers3.png"))
                self.draw_sprite(hexagon, layout, 1800, sprite)
                sprite = pygame.image.load(os.path.join("..", "resources",
                                                        "health",
                                                        "health_bar_75.png"))
                self.draw_sprite(hexagon, layout, 1800, sprite)

def get_mirrors(self):
        """Get mirrored grids."""
        mirror_centers = self._grid.mirrors
        layouts = []
        for mirror in mirror_centers:
            layout = Layout(self._layout.size,
                            self._layout.hex_to_pixel(Hex(mirror[0],
                                                          mirror[1],
                                                          mirror[2])))
            layouts.append(layout)
        return layouts

    def draw_map(self):
        """Draw a map."""
        self._screen.fill((0, 0, 0))
        self.draw_hex_grid(self._layout)
        layouts = self.get_mirrors()
        for layout in layouts:
            self.draw_hex_grid(layout)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.start()
