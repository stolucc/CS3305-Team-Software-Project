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
        self.tree_setup()

    @property
    def branches(self):
        """
        Return dict of all branches in the Research Tree.

        Each key will point to the first node of that branch.
        :return: dict
        """
        return self._branches

    @property
    def win_node(self):
        """
        Win node of Research Tree.

        This node can only be unlocked after all branches have been unlocked.
        :return: Research Node
        """
        return self._win_node

    @property
    def civilisation(self):
        """
        Civilisation that the Research Tree belongs to.

        :return: Civilisation object
        """
        return self._civilisation

    @property
    def tier(self):
        """
        Return dict of branches in the Research Tree.

        Each key will indicate what tier is currently unlocked.
        :return: dict
        """
        return self._tier

    def tree_setup(self):
        """
        Set up Research Tree.

        Add correct nodes to Tree and the end node to tie branches together.
        """
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

        :param branch: string branch to add node to
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
            if node != self._win_node:
                if self._civilisation.science >= node._unlock_cost:
                    self._civilisation.science -= node._unlock_cost
                    node._unlocked = True
                    self._tier[branch] += 1
                else:
                    print("Not enough Science points.")
            else:
                print("This branch is complete.")
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
        if self._civilisation.science >= self._win_node._unlock_cost:
            self._civilisation.science -= self._win_node._unlock_cost
            self._win_node._unlocked = True
        else:
            print("Not enough research points.")

    def end_node_unlockable(self):
        """
        Check if the end node of the Research Tree is unlockable.

        The node only becomes unlockable after all other branches are unlocked.
        :return: boolean
        """
        if self._tier['worker'] == 3 and self._tier['archer'] == 3\
                and self._tier['swordsman'] == 3:
            return True
        return False

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
        """
        Parent node, or root of tree if first node in branch.

        :return: ResearchNode
        """
        return self._parent

    @property
    def child(self):
        """
        Child node, None if no child.

        :return: ResearchNode, or None
        """
        return self._child

    @property
    def unlock_cost(self):
        """
        Science points needed to unlock node.

        :return: int
        """
        return self._unlock_cost

    @property
    def tier(self):
        """
        Tier that the node is on in the Tree.

        There are three tiers.
        :return: int
        """
        return self._tier

    @property
    def unlocked(self):
        """
        True if node is unlocked, False otherwise.

        :return: boolean
        """
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
