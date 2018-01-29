"""Resource Tests."""

import unittest
from resource import Resource


class ResourceTests(unittest.TestCase):
    """Tests for the Resource class."""
    
    def test_available_quantity(self):
        """Test that available quantity matches given value"""
        res = Resource(5)
        self.assertEqual(res.quantity, 5)

    def test_initial_work_state(self):
        """Test that is_worked state is initially False"""
        res = Resource(5)
        self.assertEqual(res.is_worked, False)

    def test_work(self):
        """Test that work method changes is_worked state to True"""
        res = Resource(5)
        res.work()
        self.assertEqual(res.is_worked, True)

    def test_stop_work(self):
        """Test that stop_work method changes is_worked state to False"""
        res = Resource(5)
        res.stop_work()
        self.assertEqual(res.is_worked, False)


if __name__ == '__main__':
    unittest.main()
