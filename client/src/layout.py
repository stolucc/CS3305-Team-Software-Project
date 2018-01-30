import math
from hexgrid import Hex, Grid


class Point:
    """A class for a Point."""

    def __init__(self, x, y):
        """
        Create a new Point object.

        :param x: the x coordinate
        :param y: the y coordinate
        """
        self._x = x
        self._y = y

    @property
    def x(self):
        """
        Property for x.

        :return: a x coordinate
        """
        return self._x

    @property
    def y(self):
        """
        Property for y.

        :return: a y coordinate
        """
        return self._y

    def __str__(self):
        """
        The object representation.

        :return: a string showing a Point object.
        """
        return "Point: (x: %s, y: %s)" % (self._x, self._y)


class Orientation:
    """A class for the Hex orientation."""

    def __init__(self, f0, f1, f2, f3, b0, b1, b2, b3, start_angle):
        """
        Create a new Orientation object.
        Can either be pointy top or flat top.

        :param f0: matrix
        :param f1: matrix
        :param f2: matrix
        :param f3: matrix
        :param b0: inverse matrix
        :param b1: inverse matrix
        :param b2: inverse matrix
        :param b3: inverse matrix
        :param start_angle: the angle to start from in multiple of 60°
        """
        self._f0 = f0
        self._f1 = f1
        self._f2 = f2
        self._f3 = f3
        self._b0 = b0
        self._b1 = b1
        self._b2 = b2
        self._b3 = b3
        self._start_angle = start_angle

    @property
    def f0(self):
        """
        Property for f0.

        :return:
        """
        return self._f0

    @property
    def f1(self):
        """
        Property for f1.

        :return:
        """
        return self._f1

    @property
    def f2(self):
        """
        Property for f2.

        :return:
        """
        return self._f2

    @property
    def f3(self):
        """
        Property for f3.

        :return:
        """
        return self._f3

    @property
    def b0(self):
        """
        Property for b0.

        :return:
        """
        return self._b0

    @property
    def b1(self):
        """
        Property for b1.

        :return:
        """
        return self._b1

    @property
    def b2(self):
        """
        Property for b2.

        :return:
        """
        return self._b2

    @property
    def b3(self):
        """
        Property for b3.

        :return:
        """
        return self._b3

    @property
    def start_angle(self):
        """
        Property for start_angle.

        :return: the angle to start from
        """
        return self._start_angle


class Layout:
    """A class for representing a Layout."""

    def __init__(self, size, origin):
        """
        Create a new Layout object.

        :param size: a Point object
        :param origin: a Point object
        """
        self._size = size
        self._origin = origin
        # orientation is pointy topped
        # use the following for flat topped:
        # Orientation(3.0 / 2.0, 0.0, math.sqrt(3.0) / 2.0, math.sqrt(3.0),
        # 2.0 / 3.0, 0.0, -1.0 / 3.0, math.sqrt(3.0) / 3.0, 0.0)
        self._orientation = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0,
                                        0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0,
                                        -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)

    @property
    def orientation(self):
        """
        Property for orientation.

        :return: a Orientation object (pointy topped or flat topped)
        """
        return self._orientation

    @property
    def size(self):
        """
        Property for size.

        :return: a Point object for a size
        """
        return self._size

    @property
    def origin(self):
        """
        Property for origin.

        :return: a Point object for an origin
        """
        return self._origin

    def hex_to_pixel(self, hexagon):
        """
        Convert Hex coordinates to pixel coordinates.
        The pixel coordinate returned is the centre of the Hexagon.

        :param hexagon: a Hex object
        :return: a Point object (x, y) - the centre of the Hex object
        """
        m = self.orientation
        size = self.size
        origin = self.origin
        x = (m.f0 * hexagon.x + m.f1 * hexagon.y) * size.x
        y = (m.f2 * hexagon.x + m.f3 * hexagon.y) * size.y
        return Point(x + origin.x, y + origin.y)

    def pixel_to_hex(self, point):
        """
        Convert from hex to pixel coordinates.

        :param point: a Point
        :return: a Hex object
        """
        m = self.orientation
        size = self.size
        origin = self.origin
        pt = Point((point.x - origin.x) / size.x, (point.y - origin.y) / size.y)
        q = m.b0 * pt.x + m.b1 * pt.y
        r = m.b2 * pt.x + m.b3 * pt.y
        return Hex(q, r, -q-r)

    def hex_corner_offset(self, corner):
        """
l       Position of the corner relative to the center of the hex.

        :param corner: orientation of the corner,
                        either 0.0 for 0° or 0.5 for 60°
        :return: a Point object with the position of the corner
        """
        m = self.orientation
        size = self.size
        angle = 2.0 * math.pi * (m.start_angle - corner) / 6
        return Point(size.x * math.cos(angle), size.y * math.sin(angle))

    def polygon_corners(self, hexagon):
        """
        The corners in screen locations.

        :param hexagon: a Hex object
        :return: an array of corners
        """
        corners = []
        center = self.hex_to_pixel(hexagon)
        for i in range(0, 6):
            offset = self.hex_corner_offset(i)
            corners.append(Point(center.x + offset.x, center.y + offset.y))
        return corners


def main():
    grid = Grid(9)
    hexmap = grid.create_grid()
    hexagon = grid.get_hextile((0, 1, -1))
    print(hexagon)
    pointy = Layout(Point(10, 10), Point(200, 200))
    cursor = pointy.hex_to_pixel(hexagon)
    print(cursor)
    print()
    ph = pointy.pixel_to_hex(cursor)
    result_tile = grid.hex_round((ph.x, ph.y, ph.z))
    r = grid.get_hextile(result_tile)
    print(r)


if __name__ == '__main__':
    main()
