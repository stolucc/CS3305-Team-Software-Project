"""Research Tree representation."""


class ResearchTree(object):
    """Class for Reserach Tree."""

    def __init__(self, civilisation):
        """
        Initialise attributes of Tree.

        :param civilisation: reference to civilisation class
        """
        self._branches = {'worker': None, 'archer': None, 'swordsman': None}
        self._win_node = None
        self._civilisation = civilisation
        self._tier = {'worker': 0, 'swordsman': 0, 'archer': 0}

    @property
    def branches(self):
        """Return dict of all branches in tree and reference to the first node
        of each branch."""
        return self._branches

    @property
    def win_node(self):
        """Return win node."""
        return self._win_node

    @property
    def civilisation(self):
        """Return civilisation object."""
        return self._civilisation

    @property
    def tier(self):
        """Return dict of branches and what tier each branch is unlocked to."""
        return self._tier

    def tree_setup(self):
        """Set up tree."""
        self.add_node('worker')
        self.add_node('worker')
        self.add_node('worker')
        self.add_node('archer')
        self.add_node('archer')
        self.add_node('archer')
        self.add_node('swordsman')
        self.add_node('swordsman')
        self.add_node('swordsman')
        self.add_end_node()

    def add_node(self, branch):
        """
        Add node to tree on specific branch.

        :param branch: string branch to add node
        """
        if branch in self._branches:
            node = self._branches[branch]
            if node is None:
                self._tier[branch] = 1
                self._branches[branch] = ResearchNode(self, None, 0, 1, True)
            else:
                node.add_child(10, 2)
        else:
            print("Branch does not exist.")

    def add_end_node(self):
        """Add end node to tree, after all other nodes have been added."""
        end_node = ResearchNode(None, None, 40, 4)
        for branch in self._branches:
            node = self._branches[branch]
            while node._child is not None:
                node = node._child
            node._child = end_node
        self._win_node = end_node

    def unlock_tier(self, branch):
        """
        Unlock next tier for certain branch.

        :param branch: string of branch to unlock next tier
        """
        if branch in self._branches:
            node = self.next_unlock_node(branch)
            if node != self._win_node\
                    and self._civilisation.science >= node._unlock_cost:
                self._civilisation.science -= node._unlock_cost
                node._unlocked = True
                self._tier[branch] += 1
            else:
                self.unlock_end_node()
        else:
            print("Branch does not exist.")

    def next_unlock_node(self, branch):
        """
        Get node of certain branch that is next to be unlocked.

        :param branch: string name of branch
        :return: ResearchNode to be unlocked
        """
        node = self._branches[branch]
        while node._unlocked is True:
            node = node._child
        return node

    def unlock_end_node(self):
        """Unlock end node."""
        if self._tier['worker'] == 3 and self._tier['archer'] == 3\
                and self._tier['swordsman'] == 3:
            if self._civilisation.science >= self._win_node._unlock_cost:
                self._civilisation.science -= self._win_node._unlock_cost
                self._win_node._unlocked = True
            else:
                print("Not enough research points.")
        else:
            print("Cannot unlock end node. Not all branches fully unlocked.")

    def __repr__(self):
        """String representation of Research Tree."""
        string = "Root -> 3 Branches -> End Node:\nTier: Worker: %i, Archer: %i,\
 Swordsman: %i\n" % (self._tier['worker'], self._tier['archer'],
                     self._tier['swordsman'])
        for branch in self._branches:
            string += branch
            string += str(self._branches[branch])
            string += "\n"
        return string


class ResearchNode(object):
    """Class for nodes of Research Tree."""

    def __init__(self, parent, child, unlock_cost, tier, unlocked=False):
        """
        Initialise Research Nodes attributes.

        :param parent: parent ResearchNode, or ResearchTree
        :param child: child ResearchNode
        :param unlock_cost: int amount of science needed to unlock
        :param tier: int tier node is on
        :param unlocked: boolean
        """
        self._parent = parent
        self._child = child
        self._unlock_cost = unlock_cost
        self._tier = tier
        self._unlocked = unlocked

    @property
    def parent(self):
        """Return parent node, or tree if first node in branch."""
        return self._parent

    @property
    def child(self):
        """Return child node, None if no child."""
        return self._child

    @property
    def unlock_cost(self):
        """Return amount of science points needed to unlock node."""
        return self._unlock_cost

    @property
    def tier(self):
        """Return tier that the node is on in the Tree."""
        return self._tier

    @property
    def unlocked(self):
        """Return True if node is unlocked, False otherwise."""
        return self._unlocked

    def add_child(self, unlock_cost, tier):
        """
        Add child node to node.

        :param unlock_cost: int amount of science needed to unlock
        :param tier: int tier of tree that node will be on
        """
        if self._child is None:
            node = ResearchNode(self, None, unlock_cost, tier)
            self._child = node
        else:
            self._child.add_child(unlock_cost*2, tier + 1)

    def __repr__(self):
        """String representation of Research Node."""
        string = " %i : %s " % (self._tier, str(self._unlocked))
        if self._child is not None:
            string += "->" + str(self._child)
        return string
