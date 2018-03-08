"""Research tree unit testing"""

import unittest

from civilisation import *
from researchtree import *
from file_logger import Logger
from hexgrid import Grid, Hex

grid = Grid(10)
logger = Logger("log.txt", "logger", "1")

class ResearchTreeTest(unittest.TestCase):
    """Unittest class for research tree"""

    def test_research_tree_constructor_and_tree_setup(self):
        """
        Tests the tree constructor and getters (and also the tree_setup
        function which is called in the constructor)
        """

        civ = Civilisation("myCiv", grid, logger)
        tree = ResearchTree(civ)

        win = ResearchNode(9, "win", False, 50)
        worker1 = ResearchNode(0, "worker", True, 0)
        worker2 = ResearchNode(1, "worker", False, 10)
        worker3 = ResearchNode(2, "worker", False, 20)
        archer1 = ResearchNode(3, "archer", True, 0)
        archer2 = ResearchNode(4, "archer", False, 10)
        archer3 = ResearchNode(5, "archer", False, 20)
        swordsman1 = ResearchNode(6, "swordsman", True, 0)
        swordsman2 = ResearchNode(7, "swordsman", False, 10)
        swordsman3 = ResearchNode(8, "swordsman", False, 20)

        self.assertEqual(tree._civilisation, civ)
        self.assertEqual(sorted(tree._nodes),
                         sorted({9: win, 0: worker1, 1: worker2, 2: worker3,
                                 3: archer1, 4: archer2, 5: archer3,
                                6: swordsman1, 7: swordsman2, 8: swordsman3}))
        self.assertEqual(tree._tier,
                         {'worker': 1, 'archer': 1, 'swordsman': 1})

    def test_add_node(self):
        """Tests the add_node function"""

        civ = Civilisation("myCiv", grid, logger)
        tree = ResearchTree(civ)
        length = len(tree._nodes)

        tree.add_node(10, "test", False, 5)
        self.assertEqual(len(tree._nodes), length + 1)

    def test_unlockable(self):
        """Tests the unlockable function"""

        civ = Civilisation("myCiv", grid, logger)
        tree = ResearchTree(civ)
        unlock1 = tree.unlockable(1)
        self.assertEqual(unlock1, True)
        unlock2 = tree.unlockable(5)
        self.assertEqual(unlock2, False)

    def test_unlock_node(self):
        """Tests the unlock_node function"""

        civ = Civilisation("myCiv", grid, logger)
        tree = ResearchTree(civ)
        tree.unlock_node(1)
        unlock = tree._nodes[1].unlocked

        self.assertEqual(unlock, True)

    def test_research_node_constructor(self):
        """Tests the research node constructor"""

        rnode = ResearchNode(10, "test", False, 5)
        self.assertEqual(rnode.id, 10)
        self.assertEqual(rnode.branch, "test")
        self.assertEqual(rnode.unlock_cost, 5)
        self.assertEqual(rnode.unlocked, False)