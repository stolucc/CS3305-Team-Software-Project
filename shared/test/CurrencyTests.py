import unittest
import Currency

"""Currency Tests."""


class CurrencyTests:

    """Tests for the Currency class."""



    def testModifiersAreBothEmptyDictionariesCalledUnitAndImprovement(self):

        cur = Currency(5, 1)

        assertEquals(cur._modifiers, {"unit": {}, "improvement": {}})


    def testBeginningValue(self):

        cur = Currency(5, 1)

        assertEquals(cur.value(), 5)


    def testBaseIncrease(self):

        cur = Currency(5, 1)

        assertEquals(cur.base_increase(), 1)


    def testTurnIncrease(self):

        cur = Currency(5, 1)

        assertEquals(cur.turn_increase(), 0)


    def testAdd(self, increase):

        cur = Currency(5, 1)

        cur.add(2)

        assertEquals(cur.value(), 7)


    def testDeduct(self, decrease):

        cur = Currency(5, 1)

        cur.deduct(2)

        assertEquals(cur.value(), 3)


    def testIncrement(self):

        cur = Currency(5, 1)

        cur.increment()

        assertEquals(cur.value(), 5 + cur.turn_increase())



    def testUpdateWithNoModifiers(self):

        cur = Currency(5, 1)

        cur.update()

        assertEquals(self.turn_increase(), 1)

        

    def testUpdateWithUnitModifiers(self):

        cur = Currency(5, 1)

        cur.add_modifier("unit", "type1", 2)

        cur.update()

        assertEquals(self.turn_increase(), 3)


        
    def testUpdateWithImprovementModifiers(self):

        cur = Currency(5, 1)

        cur.add_modifier("improvement", "type2", 1)

        cur.update()

        assertEquals(self.turn_increase(), 2)



    def testUpdateWithBothModifiers(self):

        cur = Currency(5, 1)

        cur.add_modifier("unit", "type1", 2)
        
        cur.add_modifier("improvement", "type2", 1)

        cur.update()

        assertEquals(self.turn_increase(), 4)


    def testAddModifier(self):

        cur = Currency(5, 1)

        cur.add_modifier("unit", "type1", 2)

        assertEquals(self.modifiers(), {"unit": {"type1": 2}, "improvement": {}})



    def testRemoveModifier(self):

        cur = Currency(5, 1)

        cur.add_modifier("unit", "type1", 2)

        cur.remove_modifier("unit", "type1")

        assertEquals(self.modifiers(), {"unit": {}, "improvement": {}})



    def testRemoveModifierOnNonExistentItem(self):

        cur = Currency(5, 1)

        cur.remove_modifier("improvement", "type1")

        assertThrows(KeyError)
        
