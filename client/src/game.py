"""Client game."""
import pygame
import math
import sys
from layout import Layout, Point
from hexgrid import Grid


class Game:
    """Class to represent client-side game."""

    def __init__(self):
        """Initalize display surface."""
        pygame.init()
        pygame.font.init()
        self._flags = (pygame.DOUBLEBUF |
                       pygame.HWSURFACE |
                       pygame.RESIZABLE)
        self.infoObject = pygame.display.Info()
        self._window_size = (self.infoObject.current_w//2,
                             self.infoObject.current_h//2)
        self._screen = pygame.display.set_mode(self._window_size,
                                               self._flags,
                                               0)
        self._font = 'freesansbold.ttf'
        self._font_size = 115
        self._grid_size = 51
        self._zoom = 0.3
        self._hex_size = (self._window_size[1] *
                          (self._grid_size * self._zoom) //
                          1000)
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
                elif event.type == pygame.VIDEORESIZE:  # window resized
                    self._window_size = event.dict['size']
                    self._screen = pygame.display.set_mode(self._window_size,
                                                           self._flags,
                                                           0)
                    self._hex_size = (self._window_size[1] *
                                      (self._grid_size * self._zoom) //
                                      1000)
                    self._layout = Layout(Point(self._hex_size,
                                                self._hex_size),
                                          Point(self._window_size[0]/2,
                                                self._window_size[1]/2))
                    self.draw_hex_grid()
            pygame.display.flip()

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
