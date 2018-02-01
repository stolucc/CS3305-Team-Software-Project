"""Client game."""
import pygame
import sys
import time
from layout import Layout
from hexgrid import Grid
from enum import Enum


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
                       pygame.HWSURFACE)
        self.infoObject = pygame.display.Info()
        self._window_size = Resolution.get_resolution(Resolution.DEFAULT)
        self._camera_position = (self.infoObject.current_w/2,
                                 self.infoObject.current_h/2)
        self._screen = pygame.display.set_mode(self._window_size,
                                               self._flags,
                                               0)
        self._font = 'freesansbold.ttf'
        self._font_size = 115
        self._grid_size = 51
        self._zoom = 100
        self._zoom_interval = 5
        self._min_zoom = 1
        self._max_zoom = 150
        self.hex_size = lambda x: (self.infoObject.current_w // x)
        self._grid = Grid(self._grid_size)
        self._grid.create_grid()
        self._layout = Layout(self.hex_size(self._zoom),
                              (self._window_size[0]/2,
                               self._window_size[1]/2))

    def start(self):
        """Start game."""
        self.draw_hex_grid()
        while True:
            for event in pygame.event.get():  # something happend
                if event.type in (pygame.QUIT, pygame.KEYDOWN):
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_down(event)
            pygame.display.flip()

    def mouse_button_down(self, event):
        """Mouse down actions."""
        if event.button == 1:  # Left click
            self.panning()
        elif event.button == 2:  # Middle click
            pass
        elif event.button == 3:  # Right click
            pass
        elif event.button == 4:  # Scrole up
            self.zoom_in()
        elif event.button == 5:  # Scrole down
            self.zoom_out()

    def panning(self):
        """Move map while holding down."""
        pygame.mouse.get_rel()
        holding = True
        while holding:
            pygame.event.get()
            change = pygame.mouse.get_rel()
            self._layout.change_origin(change)
            self.draw_hex_grid()
            time.sleep(0.017)
            holding = pygame.mouse.get_pressed()[0]

    def zoom_in(self):
        """Zooming in on map."""
        self._zoom -= self._zoom_interval
        if self._zoom <= self._min_zoom:
            self._zoom = self._min_zoom
        else:
            self._layout.size = self.hex_size(self._zoom)
            self.draw_hex_grid()
            time.sleep(0.017)

    def zoom_out(self):
        """Zooming away from map."""
        self._zoom += self._zoom_interval
        if self._zoom >= self._max_zoom:
            self._zoom = self._max_zoom
        else:
            self._layout.size = self.hex_size(self._zoom)
            self.draw_hex_grid()
            time.sleep(0.017)

    def draw_hex_grid(self):
        """A function which creates a grid."""
        self._screen.fill((0, 0, 0))
        for hex_point in self._grid.get_hextiles():
            hexagon = self._grid.get_hextile(hex_point)
            pygame.draw.polygon(self._screen, pygame.Color("white"),
                                self._layout.polygon_corners(hexagon),
                                1)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.start()
