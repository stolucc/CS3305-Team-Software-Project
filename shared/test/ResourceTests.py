"""Resource Tests."""

import unittest
import sys
sys.path.insert(0, "/Users/alessianardotto/projects/CS3305-Team-Software-Project/shared/src")
from Resource import Resource


class ResourceTests(unittest.TestCase):
    """Tests for the Resource class."""
    
    def testAvailableQuantity(self):
        """Test that available quantity matches given value"""
        res = Resource(5)
        self.assertEqual(res.quantity, 5)
        
        
    def testInitialWorkState(self):
        """Test that is_worked state is initially False"""
        res = Resource(5)
        self.assertEqual(res.is_worked, False)
        

    def testWork(self):
        """Test that work method changes is_worked state to True"""
        res = Resource(5)
        res.work()
        self.assertEqual(res.is_worked, True)
        

    def testStopWork(self):
        """Test that stop_work method changes is_worked state to False"""
        res = Resource(5)
        res.stop_work()
        self.assertEqual(res.is_worked, False)
        
if __name__ == '__main__':

    unittest.main()
