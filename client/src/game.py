"""Client game."""

import pygame
import sys
import time
from layout import Layout
from hexgrid import Grid, Hex
import building
from enum import Enum
from math import floor
import math

IMAGE_PATH = "../resources/images/"


class Resolution(Enum):
    """Enum for resolutions."""

    DEFAULT = 0
    HD = 1
    FULLHD = 2

    @staticmethod
    def get_resolution(index):
        """
        Getter for resolution.

        :param index: Enum which is used to obtain the resolution.
        :return: The resolution to be used.
        """
        resolutions = {Resolution.DEFAULT: (1024, 576),
                       Resolution.HD: (1280, 720),
                       Resolution.FULLHD: (1920, 1080)}
        return resolutions[index]


def load_image(image):
    """
    Load and convert images.

    :param image: The image to be loaded.
    :return: a loaded and converted image.
    """
    return pygame.image.load(IMAGE_PATH + image).convert_alpha()


class Game:
    """Class to represent client-side rendering of the game."""

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
        self._terrain_images = {
            "move-highlight": load_image("tiles/move-highlight.png"),
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
            (3, 2): load_image("tiles/ocean.png")
        }
        self._scaled_terrain_images = self._terrain_images.copy()
        self._sprite_images = {
            "Archer": load_image("units/archers3.png"),
            "health_bar": load_image("health/health_bar_75.png")
        }
        self._scaled_sprite_images = self._sprite_images.copy()
        self._building_images = {
            building.BuildingType.CITY: load_image("buildings/city.png"),
            building.BuildingType.FARM: load_image("buildings/farm.png"),
            building.BuildingType.TRADE_POST: load_image("buildings/trading_post.png"),
            building.BuildingType.UNIVERSITY: load_image("buildings/university.png")
        }
        self._scaled_building_images = self._building_images.copy()
        self._currently_selected_unit = None
        self._currently_selected_tile = None
        self._current_available_moves = {}

    def start(self):
        """Initialize the game."""
        self.scale_images_to_hex_size()
        self.scale_sprites_to_hex_size()
        self.scale_buildings_to_hex_size()
        self.draw_map()
        while True:
            for event in pygame.event.get():  # something happened
                if event.type in [pygame.QUIT, pygame.KEYDOWN]:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_down(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_button_up(event)
            time.sleep(0.001)

    def mouse_button_down(self, event):
        """
        Perform an action depending on the mouse event taking place.

        :param event: a user inputted event.
        """
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

    def mouse_button_up(self, event):
        """
        Perform an action depending on the mouse event taking place.

        :param event: a user inputted event.
        """
        if event.button == 1:  # Left click
            pass
        elif event.button == 2:  # Middle click
            pass
        elif event.button == 3:  # Right click
            self.highlight_new_movement(self._layout)

    def panning(self):
        """
        Pan around the map.

        Method that allows the user to move around the map
        while the left mouse button is being held down.
        """
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
        """
        Zoom in method.

        Method that allows the user to zoom in when the scroll wheel is used.
        """
        self._zoom -= self._zoom_interval
        if self._zoom <= self._min_zoom:
            self._zoom = self._min_zoom
        else:
            self._layout.size = self._hex_size(self._zoom)
            self.scale_images_to_hex_size()
            self.scale_sprites_to_hex_size()
            self.scale_buildings_to_hex_size()
            self.draw_map()

    def zoom_out(self):
        """
        Zoom out method.

        Method that allows the user to zoom out when the scroll wheel is used.
        """
        self._zoom += self._zoom_interval
        if self._zoom >= self._max_zoom:
            self._zoom = self._max_zoom
        else:
            self._layout.size = self._hex_size(self._zoom)
            self.scale_images_to_hex_size()
            self.scale_sprites_to_hex_size()
            self.scale_buildings_to_hex_size()
            self.draw_map()

    def highlight_new_movement(self, layout):
        """
        Highlight tiles which can be moved to by newly selected unit.

        :param layout: the layout object being drawn on.
        """
        click = pygame.mouse.get_pos()
        c_hex = layout.pixel_to_hex(click)
        c_hex_coords = self._grid.hex_round((c_hex.x, c_hex.y, c_hex.z))
        hexagon = self._grid.get_hextile(c_hex_coords)
        if self._currently_selected_tile != hexagon:
            if self._currently_selected_unit is not None:
                if hexagon in self._current_available_moves:
                    self.move_unit(self._currently_selected_unit, hexagon)
                self._currently_selected_tile = None
                self._currently_selected_unit = None
                self._current_available_moves = {}
            else:
                self._currently_selected_tile = hexagon
                self._current_available_moves = {}
                if hexagon.unit is not None:
                    unit = hexagon.unit
                    self._currently_selected_unit = unit
                    if unit.position == hexagon:
                        self._current_available_moves = self._grid.dijkstra(
                            hexagon,
                            unit.movement_range)
                        print(self._current_available_moves)
        self.draw_map()

    def highlight_selected_movement(self, layout):
        """
        Highlight tiles that can be moved to by currently selected unit.

        :param layout: The Layout object being drawn on
        :return:
        """
        for k in self._current_available_moves:
            hexagon_coords = layout.hex_to_pixel(k)
            self._screen.blit(
                self._scaled_terrain_images["move-highlight"],
                (hexagon_coords[0]
                 - math.ceil(layout.size * (math.sqrt(3) / 2)),
                 hexagon_coords[1] - layout.size))

    def move_unit(self, unit, hexagon):
        """
        Move a unit to another hexagon.

        :param unit: Unit to be moved.
        :param hexagon: Hexagon to move to.
        """
        unit.position.unit = None
        unit.position = hexagon
        hexagon.unit = unit

    def scale_images_to_hex_size(self):
        """
        Scale images.

        Takes each image in the terrain_images dictionary,
        scales it to the current hex_size, then stores the
        new image in a copy of the dictionary to preserve
        image quality.
        """
        for k in self._terrain_images:
            self._scaled_terrain_images[k] = pygame.transform.smoothscale(
                self._terrain_images[k],
                (math.ceil(
                    (self._hex_size(self._zoom) * 2)
                    * math.sqrt(3) / 2),
                 self._hex_size(self._zoom) * 2))

    def scale_sprites_to_hex_size(self):
        """
        Scale sprites.

        Takes each sprite in the sprite_images dictionary,
        scales it to the current hex_size, then stores the
        new image in a copy of the dictionary to preserve
        image quality.
        """
        adjusted_size = math.floor(1800 / self._zoom)
        for k in self._sprite_images:
            self._scaled_sprite_images[k] = pygame.transform.smoothscale(
                self._sprite_images[k],
                (adjusted_size, adjusted_size))

    def scale_buildings_to_hex_size(self):
        """
        Scale sprites.

        Takes each sprite in the sprite_images dictionary,
        scales it to the current hex_size, then stores the
        new image in a copy of the dictionary to preserve
        image quality.
        """
        adjusted_size = math.floor(1800 / self._zoom)
        for k in self._building_images:
            self._scaled_building_images[k] = pygame.transform.smoothscale(
                self._building_images[k],
                (adjusted_size, adjusted_size))

    def draw_building(self, hexagon_coords, sprite):
        """
        Draw sprite on hextile terrain.

        :param hexagon_coords: the coordinates of the center of the hexagon.
        :param sprite: the sprite image to draw.
        """
        center_x, center_y = hexagon_coords
        offset = 1800 / (self._zoom * 2)
        self._screen.blit(sprite,
                          (floor(center_x - offset),
                           floor(center_y - offset)))

    def draw_sprite(self, hexagon_coords, sprite):
        """
        Draw sprite on hextile terrain.

        :param hexagon_coords: the coordinates of the center of the hexagon.
        :param sprite: the sprite image to draw.
        """
        center_x, center_y = hexagon_coords
        offset = 1800 / (self._zoom * 2)
        self._screen.blit(sprite,
                          (floor(center_x - offset),
                           floor(center_y - offset)))

    def draw_hex_grid(self, layout):
        """
        Draw the hexgrid.

        Draws all currently visible hextiles to the screen,
        along with any units or structures contained on those tiles.

        :param layout: The layout of the grid to draw. Either the
                       main layout or one of it's mirrors.
        """
        size = pygame.display.get_surface().get_size()
        for hex_point in self._grid.get_hextiles():
            hexagon = self._grid.get_hextile(hex_point)
            hexagon_coords = layout.hex_to_pixel(hexagon)
            if (size[0] + 100 > hexagon_coords[0] > -100 and
               size[1] + 100 > hexagon_coords[1] > -100):
                terrain = hexagon.terrain
                terrain_image = self._scaled_terrain_images[
                    (terrain.terrain_type.value, terrain.biome.value)]
                self._screen.blit(
                    terrain_image,
                    (hexagon_coords[0]
                     - math.ceil(self._layout.size * (math.sqrt(3) / 2)),
                     hexagon_coords[1] - self._layout.size))
                if hexagon.building is not None:
                    building = hexagon.building
                    hexagon_coords = layout.hex_to_pixel(building.position)
                    self.draw_building(hexagon_coords,
                                     self._scaled_building_images[
                                         building.building_type])
                if hexagon.unit is not None:
                    unit = hexagon.unit
                    hexagon_coords = layout.hex_to_pixel(unit.position)
                    self.draw_sprite(hexagon_coords,
                                     self._scaled_sprite_images[
                                         unit.__class__.__name__])
                    self.draw_sprite(hexagon_coords,
                                     self._scaled_sprite_images["health_bar"])

    def get_mirrors(self):
        """Store each hexgrid mirror layout in a list."""
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
        """
        Draw the current instance of the hex grid to the screen.

        Also draws the hexgrid mirrors.
        """
        self._screen.fill((0, 0, 0))
        self.draw_hex_grid(self._layout)
        layouts = self.get_mirrors()
        for layout in layouts:
            self.draw_hex_grid(layout)
        self.highlight_selected_movement(self._layout)
        for layout in layouts:
            self.highlight_selected_movement(layout)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.start()
