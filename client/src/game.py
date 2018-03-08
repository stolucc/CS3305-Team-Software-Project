"""Client game."""

import pygame
import math
import os
import json
import sys
import time
import threading
from layout import Layout
import server_API
from hexgrid import Grid, Hex
from load_resources import LoadImages
from unit import Worker
from hud_overlay import HudOverlay
from client_gamestate import GameState
from civilisation import Civilisation
from building import BuildingType
from math import floor
from file_logger import Logger
from object_select import SelectMenu


class Game:
    """Class to represent client-side rendering of the game."""

    def __init__(self, game_state, logger, server_api):
        """Initialise display surface."""
        self._server_api = server_api
        pygame.init()
        pygame.font.init()
        civ_borders = ["civ1_border", "civ2_border", "civ3_border",
                       "civ4_border"]
        self._threads = []
        self._game_state = game_state
        self._civ_colours = dict((civ, colour)
                                 for (civ, colour)in
                                 zip(sorted(self._game_state.civs),
                                     civ_borders))
        self._flags = (pygame.DOUBLEBUF |
                       pygame.HWSURFACE)
        self.infoObject = pygame.display.Info()
        self._window_size = (self.infoObject.current_w,
                             self.infoObject.current_h)
        self._camera_position = (self._window_size[0] / 2,
                                 self._window_size[1] / 2)
        self._screen = pygame.display.set_mode(self._window_size,
                                               self._flags,
                                               0)
        hud_flags = (pygame.HWSURFACE | pygame.SRCALPHA)
        self._hud_surface = pygame.Surface(self._window_size, hud_flags)
        self._hud_quick_surface = pygame.Surface(self._window_size, hud_flags)
        self._font = 'freesansbold.ttf'
        self._font_size = 115
        self._zoom = 30
        self._zoom_interval = 5
        self._min_zoom = 1
        self._max_zoom = 40
        self._hex_size = lambda x: (self.infoObject.current_w // x)
        self._select_menu = SelectMenu(self._screen)
        self._menu_displayed = False
        self._grid = self._game_state.grid
        self._layout = Layout(self._hex_size(self._zoom),
                              (self._window_size[0] / 2,
                               self._window_size[1] / 2))
        self._hud = HudOverlay(self._game_state,
                               self._hud_surface,
                               self._hud_quick_surface,
                               self._window_size,
                               self._layout)
        self._load_images = LoadImages()
        self._scaled_terrain_images = \
            self._load_images.load_terrain_images().copy()
        self._scaled_sprite_images = \
            self._load_images.load_sprite_images().copy()
        self._scaled_building_images = \
            self._load_images.load_building_images().copy()
        self._scaled_health_bar_images = \
            self._load_images.load_health_bar_images().copy()
        self._scaled_resource_images = \
            self._load_images.load_resource_images().copy()
        self._currently_selected_unit = None
        self._currently_selected_tile = None
        self._current_available_moves = {}

    def start(self):
        """Initialize the game."""
        self.scale_images_to_hex_size()
        self.scale_sprites_to_hex_size()
        self.scale_buildings_to_hex_size()
        self.scale_resources_to_hex_size()
        self.draw_map()
        count = 0
        t = threading.Thread(group=None,
                             target=self.render_hud,
                             name="HUD_render",
                             args=(),
                             daemon=True)
        self._threads.append(t)
        t.start()
        while True:
            self.check_for_events()
            time.sleep(0.004)
            count += 1
            if count == 100:
                count = 0
                self.draw_map()

    def check_for_events(self):
        """Check for mouse and keyboard events."""
        for event in pygame.event.get():  # something happened
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[306] == 1 and pressed[99] == 1:  # 306 CTRL,99 C
                    self.quit()
                elif pressed[32] == 1:
                    self._server_api.end_turn()
                elif pressed[98] == 1:
                    self.build_structure(self._layout, BuildingType.CITY)
                elif pressed[102] == 1:
                    self.build_structure(self._layout, BuildingType.FARM)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_down(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_up(event)

    def quit(self):
        """Close game."""
        for thread in self._threads:
            thread.shutdown = True
            thread.join()
        sys.exit()

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
            self.scale_resources_to_hex_size()
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
            self.scale_resources_to_hex_size()
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
        unit = self._currently_selected_unit
        if self._currently_selected_tile != hexagon:
            if unit is not None:
                if hexagon in self._current_available_moves:
                    self._server_api.move_unit(unit, hexagon)
                    self._game_state.get_civ(
                        self._game_state.my_id).calculate_vision()
                elif type(unit) != Worker \
                        and hexagon.unit is not None:
                    self._server_api.attack(unit, hexagon.unit)
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

    def unit_menu(self, layout):
        """
        Build a structure using selected worker.

        :param layout: Layout object being drawn on.
        """

        click = pygame.mouse.get_pos()
        c_hex = layout.pixel_to_hex(click)
        c_hex_coords = self._grid.hex_round((c_hex.x, c_hex.y, c_hex.z))
        hexagon = self._grid.get_hextile(c_hex_coords)
        unit = self._currently_selected_unit

        def move_unit():
            self.highlight_new_movement(layout)

        def build_city():
            self._server_api.build_city(unit)
            self._game_state.get_civ(self._game_state.my_id).calculate_vision()
            self.draw_map()

        def build_farm():
            self._server_api.build(unit, BuildingType.FARM)
            self._game_state.get_civ(self._game_state.my_id).calculate_vision()
            self.draw_map()

        def build_trade_post():
            self._server_api.build(unit, BuildingType.TRADE_POST)
            self._game_state.get_civ(self._game_state.my_id).calculate_vision()
            self.draw_map()

        def build_uni():
            self._server_api.build(unit, BuildingType.UNIVERSITY)
            self._game_state.get_civ(self._game_state.my_id).calculate_vision()
            self.draw_map()

        if unit == hexagon.unit and self._menu_displayed is False:
            if unit.__class__.__name__ == "Worker":
                self._menu_displayed = self._select_menu.display_menu(click, [
                    ("Move", move_unit),
                    ("Build City", build_city),
                    ("Build Farm", build_farm),
                    ("Build Trade Post", build_trade_post),
                    ("Build Uni", build_uni)])
            else:
                self._menu_displayed = self._select_menu.display_menu(click, [
                    ("Move", move_unit)])

        else:
            self._menu_displayed = self._select_menu.menu_click(click)
            if not self._menu_displayed:
                self._screen.fill((0, 0, 0))
                pygame.display.flip()

    def scale_images_to_hex_size(self):
        """
        Scale images.

        Takes each image in the terrain_images dictionary,
        scales it to the current hex_size, then stores the
        new image in a copy of the dictionary to preserve
        image quality.
        """
        for k in self._load_images.load_terrain_images():
            self._scaled_terrain_images[k] = pygame.transform.smoothscale(
                self._load_images.load_terrain_images()[k],
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
        for k in self._load_images.load_sprite_images():
            self._scaled_sprite_images[k] = pygame.transform.smoothscale(
                self._load_images.load_sprite_images()[k],
                (adjusted_size, adjusted_size))
        for k in self._load_images.load_health_bar_images():
            self._scaled_health_bar_images[k] = pygame.transform.smoothscale(
                self._load_images.load_health_bar_images()[k],
                (adjusted_size, adjusted_size))
        for l in self._load_images.load_resource_images():
            self._scaled_resource_images[l] = pygame.transform.smoothscale(
                self._load_images.load_resource_images()[l],
                (adjusted_size, adjusted_size))

    def scale_resources_to_hex_size(self):
        """
        Take each sprite in the sprite_images dictionary.

        scales it to the current hex_size, then stores the
        new image in a copy of the dictionary to preserve
        image quality.
        """
        adjusted_size = math.floor(1800 / self._zoom)
        for k in self._load_images.load_resource_images():
            self._scaled_resource_images[k] = pygame.transform.smoothscale(
                self._load_images.load_resource_images()[k],
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
        for k in self._load_images.load_building_images():
            self._scaled_building_images[k] = pygame.transform.smoothscale(
                self._load_images.load_building_images()[k],
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
        my_civ = self._game_state.get_civ(self._game_state.my_id)
        my_id = self._game_state.my_id
        my_vision = my_civ.vision
        size = pygame.display.get_surface().get_size()
        for hex_point in self._grid.get_hextiles():
            hexagon = self._grid.get_hextile(hex_point)
            hexagon_coords = layout.hex_to_pixel(hexagon)
            if size[0] + 100 > hexagon_coords[0] > -100 and \
               size[1] + 100 > hexagon_coords[1] > -100:
                terrain = hexagon.terrain
                terrain_image = self._scaled_terrain_images[
                    (terrain.terrain_type.value, terrain.biome.value)]
                self._screen.blit(
                    terrain_image,
                    (hexagon_coords[0]
                     - math.ceil(self._layout.size * (math.sqrt(3) / 2)),
                     hexagon_coords[1] - self._layout.size))
                if hexagon.building is not None:
                    build = hexagon.building
                    hexagon_coords = layout.hex_to_pixel(hexagon)
                    self.draw_building(hexagon_coords,
                                       self._scaled_building_images[
                                         build.building_type])
                if hexagon.terrain.resource is not None:
                    resource = hexagon.terrain.resource
                    hexagon_coords = layout.hex_to_pixel(hexagon)
                    self.draw_sprite(hexagon_coords,
                                     self._scaled_resource_images[
                                          resource.resource_type])
                if hexagon.civ_id is not None:
                    self._screen.blit(
                        self._scaled_terrain_images[self._civ_colours[hexagon.civ_id]],
                        (hexagon_coords[0]
                         - math.ceil(self._layout.size * (math.sqrt(3) / 2)),
                         hexagon_coords[1] - self._layout.size))
                if hexagon.unit is not None and hexagon in my_vision:
                    unit = hexagon.unit
                    unit_level = unit.level
                    unit_health = unit.get_health_percentage()
                    hexagon_coords = layout.hex_to_pixel(unit.position)
                    if unit.civ_id == my_id:
                        self._screen.blit(
                            self._scaled_terrain_images
                            [self._civ_colours[my_id]],
                            (hexagon_coords[0] - math.ceil(
                                self._layout.size * (math.sqrt(3) / 2)),
                                hexagon_coords[1] - self._layout.size))
                    self._screen.blit(
                        self._scaled_terrain_images[
                            self._civ_colours[unit.civ_id]],
                        (hexagon_coords[0]
                         - math.ceil(self._layout.size * (math.sqrt(3) / 2)),
                         hexagon_coords[1] - self._layout.size))
                    self.draw_sprite(hexagon_coords,
                                     self._scaled_sprite_images[
                                         unit.__class__.__name__
                                         + str(unit_level)])
                    self.draw_sprite(hexagon_coords,
                                     self._scaled_health_bar_images[
                                        unit_health])
                if hexagon not in my_vision:
                    self._screen.blit(
                        self._scaled_terrain_images["fogofwar"],
                        (hexagon_coords[0]
                         - math.ceil(self._layout.size * (math.sqrt(3) / 2)),
                         hexagon_coords[1] - self._layout.size))

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
        self._screen.blit(self._hud_surface, (0, 0))
        self._hud.draw_quick_surface(layouts)
        self._screen.blit(self._hud_quick_surface, (0, 0))
        pygame.display.flip()

    def render_hud(self):
        """Render heads up display."""
        while True:
            self._hud.draw()
            time.sleep(1)


if __name__ == "__main__":
    with open(os.path.join("..", "config", "config.json")) as config_file:
        config = json.load(config_file)
    map_ref = Grid(26)
    map_ref.create_grid()
    map_ref.static_map()
    logger = Logger("client.log", "client", config["logging"]["log_level"])
    logger = logger.get_logger()
    civ = Civilisation(1, map_ref, logger)
    game_state = GameState(1, 1, map_ref, logger)
    game_state.add_civ(civ)
    game_state.my_id = 1
    server_api = server_API.ServerAPI()
    game = Game(game_state, logger, server_api)
    game.start()
