"""Currency Tests."""

import unittest
from currency import Currency, ModifierType


class CurrencyTests(unittest.TestCase):
    """Tests for the Currency class."""

    def test_empty_modifiers(self):
        """Test that modifiers are as expected."""
        cur = Currency(5, 1)
        self.assertEqual(cur._modifiers, {ModifierType.UNIT: {},
                                          ModifierType.IMPROVEMENT: {}})

    def test_beginning_value(self):
        """Test beginning value is the same as the one tested."""
        cur = Currency(5, 1)
        self.assertEqual(cur.value, 5)

    def test_base_increase(self):
        """Test base increase has the correct value."""
        cur = Currency(5, 1)
        self.assertEqual(cur.base_increase, 1)

    def test_turn_increase(self):
        """Test turn increase has the correct value."""
        cur = Currency(5, 1)
        self.assertEqual(cur.turn_increase, 1)

    def test_add(self):
        """Test that the add function adds to value."""
        cur = Currency(5, 1)
        cur.add(2)
        self.assertEqual(cur.value, 7)

    def test_deduct(self):
        """Test that the deduct function deducts from value."""
        cur = Currency(5, 1)
        cur.deduct(2)
        self.assertEqual(cur.value, 3)

    def test_increment(self):
        """Test that the increment adds turn increase to value."""
        cur = Currency(5, 1)
        cur.increment()
        self.assertEqual(cur.value, 5 + cur.turn_increase)

    def test_update_with_no_modifiers(self):
        """Test Update with no modifiers leaves turn increase unchanged."""
        cur = Currency(5, 1)
        cur.update()
        self.assertEqual(cur.turn_increase, 1)

    def test_update_with_unit_modifiers(self):
        """Test Update with unit modifiers."""
        cur = Currency(5, 1)
        cur.add_modifier(ModifierType.UNIT, "type1", 2)
        cur.update()
        self.assertEqual(cur.turn_increase, 3)

    def test_update_with_improvement_modifiers(self):
        """Test update with improvement modifiers."""
        cur = Currency(5, 1)
        cur.add_modifier(ModifierType.IMPROVEMENT, "type2", 1)
        cur.update()
        self.assertEqual(cur.turn_increase, 2)

    def test_update_with_both_modifiers(self):
        """Test update with both types of modifier."""
        cur = Currency(5, 1)
        cur.add_modifier(ModifierType.UNIT, "type1", 2)
        cur.add_modifier(ModifierType.IMPROVEMENT, "type2", 1)
        cur.update()
        self.assertEqual(cur.turn_increase, 4)

    def test_add_modifier(self):
        """Test add modifier to ensure modifier is added to list."""
        cur = Currency(5, 1)
        cur.add_modifier(ModifierType.UNIT, "type1", 2)
        self.assertEqual(cur.modifiers,
                         {ModifierType.UNIT: {"type1": 2},
                          ModifierType.IMPROVEMENT: {}})

    def test_remove_modifier(self):
        """Test remove modifier."""
        cur = Currency(5, 1)
        cur.add_modifier(ModifierType.UNIT, "type1", 2)
        cur.remove_modifier(ModifierType.UNIT, "type1")
        self.assertEqual(cur.modifiers, {ModifierType.UNIT: {},
                                         ModifierType.IMPROVEMENT: {}})

    def test_remove_modifier_on_non_existent_item(self):
        """Test remove modifier on nonexistent modifier."""
        cur = Currency(5, 1)
        with self.assertRaises(KeyError):
            cur.remove_modifier(ModifierType.IMPROVEMENT, "type2")


if __name__ == '__main__':
    unittest.main()
