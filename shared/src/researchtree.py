"""Research Tree representation."""


class ResearchTree(object):
    """Class for Research Tree."""

    def __init__(self, civilisation):
        """
        Initialise attributes of Tree.

        :param civilisation: reference to civilisation class
        """
        self._civilisation = civilisation
        self._branches = {}
        self._unlocked = []
        self._unlockable = []
        self.tree_setup()

    @property
    def civilisation(self):
        """
        Civilisation that the Research Tree belongs to.

        :return: Civilisation object
        """
        return self._civilisation

    def tree_setup(self):
        """
        Set up Research Tree.

        Add correct nodes to Tree and the end node to tie branches together.
        """
        self.add_branch('worker')
        self.add_branch('archer')
        self.add_branch('swordsman')
        self.add_end_node()
        self._unlocked = self.unlocked_nodes()
        self._unlockable = self.unlockable_nodes()

    def add_branch(self, branch, nodes):
        """Add branch to tree with 3 nodes."""
        self._branches[branch] = []
        for node in range(3):
            if node == 0:
                new_node = ResearchNode(node, branch, False, True, 0)
            elif node == 1:
                new_node = ResearchNode(node, branch, True, False, 10)
            else:
                new_node = ResearchNode(node, branch, False, False, 20)
            self._branches[branch] += [new_node]

    def add_end_node(self):
        """Add end/win node."""
        node = ResearchNode(0, 'win', False, False, 0)
        self._branches['win'] = [node]

    def unlockable(self, node_id, branch):
        """Check if node is able to be unlocked, based on id."""
        return self._branches[node_id]._unlockable

    def unlock_node(self, node_id, branch):
        """Unlock node."""
        node = self._branches[branch][node_id]
        node._unlockable = False
        node._unlocked = True
        if node_id < 2 and branch != 'win':
            next_node = self._branches[branch][node_id + 1]
            next_node._unlockable = True
        self.win_node_unlockable()
        self._unlocked = self.unlocked_nodes()
        self._unlockable = self.unlockable_nodes()

    def win_node_unlockable(self):
        """Make win node unlockable if all other nodes unlocked."""
        branches = self._branches
        if branches['worker'][2]._unlocked and branches['archer'][2]._unlocked\
                and branches['swordsman'][2]._unlocked:
            branches['win'][0]._unlockable = True

    def unlockable_nodes(self):
        """Return list of unlockable nodes."""
        unlockable = []
        for branch_id in self._branches:
            branch = self._branches[branch_id]
            for node in branch:
                if node._unlockable:
                    unlockable += [node]
        return unlockable

    def unlocked_nodes(self):
        """Return list of unlocked nodes."""
        unlocked = []
        for branch_id in self._branches:
            branch = self._branches[branch_id]
            for node in branch:
                if node._unlocked:
                    unlocked += [node]
        return unlocked

    def __repr__(self):
        """Return string representation of Research Tree."""
        string = ""
        for branch_id in self._branches:
            branch = self._branches[branch_id]
            for node in branch:
                string += str(node)
                string += "\n"
        return string


class ResearchNode(object):
    """Class for nodes of Research Tree."""

    def __init__(self, id, branch, unlockable, unlocked, unlock_cost):
        """
        Initialise Research Nodes attributes.

        :param unlock_cost: int amount of science needed to unlock
        :param unlocked: boolean
        """
        self._branch = branch
        self._unlock_cost = unlock_cost
        self._unlocked = unlocked
        self._unlockable = unlockable
        self._id = id

    @property
    def branch(self):
        """
        Branch node belongs to.

        :return: string
        """
        return self._branch

    @property
    def unlock_cost(self):
        """
        Science points needed to unlock node.

        :return: int
        """
        return self._unlock_cost

    @property
    def unlocked(self):
        """
        Return true if node is unlocked, False otherwise.

        :return: boolean
        """
        return self._unlocked

    @property
    def id(self):
        """
        Return id of node.

        :return: int
        """
        return self._id

    def __repr__(self):
        """Return string representation of Research Node."""
        string = "Branch: %s, ID: %i, Unlocked: %s, Unlockable: %s, Cost: %i"\
            % (self._branch, self._id, str(self._unlocked),
               str(self._unlockable), self._unlock_cost)
        return string
