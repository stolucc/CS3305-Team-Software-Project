"""Tests for layout."""
import unittest
import math
from layout import Orientation, Layout
from hexgrid import Hex


class LayoutTest(unittest.TestCase):
    """Unittest class for Layout."""

    def test_orientation_contructor_and_getters(self):
        """Test orientation and getter."""
        # orientation is flat topped
        flat_orientation = Orientation(1.5, 0.0, math.sqrt(3.0) / 2.0,
                                       math.sqrt(3.0), 2.0 / 3.0, 0.0,
                                       -1.0 / 3.0,
                                       math.sqrt(3.0) / 3.0, 0.0)
        self.assertEqual(flat_orientation.f0, 1.5)
        self.assertEqual(flat_orientation.f1, 0.0)
        self.assertEqual(flat_orientation.f2, 0.8660254037844386)
        self.assertEqual(flat_orientation.f3, 1.7320508075688772)
        self.assertEqual(flat_orientation.b0, 0.6666666666666666)
        self.assertEqual(flat_orientation.b1, 0.0)
        self.assertEqual(flat_orientation.b2, -0.3333333333333333)
        self.assertEqual(flat_orientation.b3, 0.5773502691896257)
        self.assertEqual(flat_orientation.start_angle, 0.0)

        # orientation is pointy topped
        pointy_orientation = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0,
                                         0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0,
                                         -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
        self.assertEqual(pointy_orientation.f0, 1.7320508075688772)
        self.assertEqual(pointy_orientation.f1, 0.8660254037844386)
        self.assertEqual(pointy_orientation.f2, 0.0)
        self.assertEqual(pointy_orientation.f3, 1.5)
        self.assertEqual(pointy_orientation.b0, 0.5773502691896257)
        self.assertEqual(pointy_orientation.b1, -0.3333333333333333)
        self.assertEqual(pointy_orientation.b2, 0.0)
        self.assertEqual(pointy_orientation.b3, 0.6666666666666666)
        self.assertEqual(pointy_orientation.start_angle, 0.5)

    def test_layout_constructor_and_getters(self):
        """Test layout and constructors."""
        pointy_orientation = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0,
                                         0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0,
                                         -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
        layout = Layout(20, (100, 100))
        self.assertEqual(layout.size, 20)
        self.assertEqual(layout.origin, (100, 100))
        self.assertEqual(layout.orientation, pointy_orientation,
                         'not pointy oriented')

    def test_hex_to_pixel(self):
        """Test hex to pixel."""
        hexagon = Hex(0, 1, -1)
        pointy = Layout(10, (200, 200))
        self.assertEqual(pointy.hex_to_pixel(hexagon),
                         (208.6602540378444, 215.0))

    def test_pixel_to_hex(self):
        """Test pixel to hex."""
        point = (208.6602540378444, 215.0)
        pointy = Layout(10, (200, 200))
        self.assertEqual(pointy.pixel_to_hex(point),
                         Hex(5.551115123125783e-16, 1, -1.0000000000000004))
        # when using the pixel to hex function
        # the Hex must be rounded with grid.hex_round((Hex.x, Hex.y, Hex.z))

    def test_hex_corner_offset(self):
        """Test hex corner offset."""
        corner = 0.5
        pointy = Layout(10, (200, 200))
        self.assertEqual(pointy.hex_corner_offset(corner), (10, 0))

    def test_polygon_corners(self):
        """Test polygon corners."""
        hexagon = Hex(1, 0, -1)
        pointy = Layout(10, (200, 200))
        self.assertEqual(pointy.polygon_corners(hexagon),
                         [(225.98076211353316, 205.0),
                          (225.98076211353316, 195.0),
                          (217.32050807568876, 190.0),
                          (208.66025403784437, 195.0),
                          (208.66025403784437, 205.0),
                          (217.32050807568876, 210.0)])


if __name__ == '__main__':
    unittest.main()
