import pygame
import math
from pygame.locals import *
import sys

from client.src.layout import Layout, Point
from hexgrid import Grid


grid = Grid(9)
grid.create_grid()
layout = Layout(Point(100,100), Point(400,400))
def hex_corner(corner, size, center):
    """
    Calculates the pixel coordinates of a hexagon corner given
    it's size and center coordinate.

    :param corner: (float) The corner of the hexagon. Can be a value between 0.0 and 5.0.
    :param size: (float) The radius of the circle inscribing the hexagon.
    :param center: (list) The pixel coordinates of the center of the hexagon.
    :return: (list) The x and y coordinates of the hexagon corner.
    """

    angle_deg = (60 * corner) + 30
    angle_rad = (math.pi / 180.0) * angle_deg
    return [center[0] + size * math.cos(angle_rad),
            center[1] + size * math.sin(angle_rad)]


def calculate_hexagon_corner_coordinates(size, center):
    """
    Helper function to calculate the coordinates of all 6 corners of a hexagon
    and store them in a list.

    :param size: (float) The size of the circle inscribing the hexagon.
    :param center: (list) The pixel coordinates of the center of the hexagon.
    :return: (list) A list containing the set of hexagon corner coordinates.
    """

    corners = []
    for corner in range(6):
        corners += [hex_corner(corner, size, center)]
    return corners


def draw_hex_grid(hexagon_coord_dict, size):
    """
    A function which takes a list of multiple hexagon coordinates
    and creates a grid using the given values.

    :param hexagon_coord_list: (list) A list of lists of hexagon corner coordinates.
    :param size: (float) The radius of the circle which inscribes the hexagon.
    """

    for hex_point in hexagon_coord_dict:
        print(hex_point)
        print(grid.get_hextile(hex_point))
        point_coords = layout.hex_to_pixel(grid.get_hextile(hex_point))
        pygame.draw.polygon(screen, pygame.Color("white"),
                            calculate_hexagon_corner_coordinates(size,[point_coords.x, point_coords.y]),
                            1)


if __name__ == "__main__":

    # down = False
    # start_height = 200.0
    # start_width = 200.0
    # for i in range(25):
    #     if down is True:
    #         start_height += 75.0
    #     else:
    #         start_height -= 75.0
    #     hex_list += [[start_width, start_height]]
    #     start_width += (math.sqrt(3) / 4.0) * 100.0
    #     down = not down
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    draw_hex_grid(grid.get_hextiles(), 100)

    while 1:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()
        pygame.display.update()
        pygame.time.delay(100)
