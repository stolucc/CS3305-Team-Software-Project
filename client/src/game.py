"""Client game."""
import pygame
import math
import sys
import time
from layout import Layout, Point
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
        """Initalize display surface."""
        pygame.init()
        pygame.font.init()
        self._flags = (pygame.DOUBLEBUF |
                       pygame.HWSURFACE)
        self.infoObject = pygame.display.Info()
        self._window_size = Resolution.get_resolution(Resolution.DEFAULT)
        self._camera_position = (self._window_size[0]/2,
                                 self._window_size[1]/2)
        self._screen = pygame.display.set_mode(self._window_size,
                                               self._flags,
                                               0)
        self._font = 'freesansbold.ttf'
        self._font_size = 115
        self._grid_size = 51
        self._zoom = 150
        self._hex_size = (self._window_size[0] //
                          self._zoom)
        self._grid = Grid(self._grid_size)
        self._grid.create_grid()
        self._layout = Layout(Point(self._hex_size, self._hex_size),
                              Point(self._window_size[0]/2,
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
            pygame.mouse.get_rel()
            holding = True
            while holding:
                pygame.event.get()
                change = pygame.mouse.get_rel()
                self._layout.change_origin(change)
                self.draw_hex_grid()
                time.sleep(0.017)
                holding = pygame.mouse.get_pressed()[0]

        elif event.button == 2:  # Middle click
            pass
        elif event.button == 3:  # Right click
            pass
        elif event.button == 4:  # Scrole up
            pass
        elif event.button == 5:  # Scrole down
            pass

    def text_objects(self, text, font, color):
        """."""
        textSurface = font.render(str(text), True, color)
        return textSurface, textSurface.get_rect()

    def message_display(self, text):
        """."""
        large_text = pygame.font.Font(self._font, self._font_size)
        text_surf, text_rect = self.text_objects(text,
                                                 large_text,
                                                 pygame.Color(0, 255, 0, 255))
        text_rect.center = ((self._window_size[0]/2),
                            (self._window_size[1]/2))
        self._screen.blit(text_surf, text_rect)
        pygame.display.flip()

    def hex_corner(self, corner, center):
        """
        Calculate the pixel coordinates of a hexagon corner.

        :param corner: The corner of the hexagon.
        :param size: The radius of the circle inscribing the hexagon.
        :param center: The pixel coordinates of the center of the hexagon.
        :return: The x and y coordinates of the hexagon corner.
        """
        angle_deg = (60 * corner) + 30
        angle_rad = (math.pi / 180.0) * angle_deg
        return [center[0] + self._hex_size * math.cos(angle_rad),
                center[1] + self._hex_size * math.sin(angle_rad)]

    def calculate_hexagon_corner_coordinates(self, center):
        """
        Helper function to calculate the coordinates of all 6 corners.

        :param size: float the size of the circle inscribing the hexagon.
        :param center: list of pixel coordinates of the center of the hexagon.
        :return: list containing the set of hexagon corner coordinates.
        """
        corners = []
        for corner in range(6):
            corners += [self.hex_corner(corner, center)]
        return corners

    def draw_hex_grid(self):
        """A function which creates a grid."""
        self._screen.fill((0, 0, 0))
        for hex_point in self._grid.get_hextiles():
            hexagon = self._grid.get_hextile(hex_point)
            point_coords = self._layout.hex_to_pixel(hexagon)
            pygame.draw.polygon(self._screen, pygame.Color("white"),
                                self.calculate_hexagon_corner_coordinates(
                                [point_coords.x, point_coords.y]),
                                1)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.start()
