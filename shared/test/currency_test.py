"""Currency Tests."""

import unittest
from currency import Currency, CurrencyType


class CurrencyTests(unittest.TestCase):
    """Tests for the Currency class."""

    def test_value(self):
        """Test beginning value is the same as the one tested."""
        cur = Currency(CurrencyType.GOLD, 5)
        self.assertEqual(cur.value, 5)

    def test_add(self):
        """Test that the add function adds to value."""
        cur = Currency(CurrencyType.GOLD, 5)
        cur.add(2)
        self.assertEqual(cur.value, 7)

    def test_deduct(self):
        """Test that the deduct function deducts from value."""
        cur = Currency(CurrencyType.GOLD, 5)
        cur.deduct(2)
        self.assertEqual(cur.value, 3)

    def test_type(self):
        """Test that the increment adds turn increase to value."""
        cur = Currency(CurrencyType.SCIENCE, 5)
        self.assertEqual(cur.type, CurrencyType.SCIENCE)


if __name__ == '__main__':
    unittest.main()
