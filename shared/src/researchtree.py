"""Research Tree representation."""


class ResearchTree(object):
    """Class for Research Tree."""

    def __init__(self, civilisation):
        """
        Initialise attributes of Tree.

        :param civilisation: reference to civilisation class
        """
        self._civilisation = civilisation
        self._nodes = {}
        self._tier = {'worker': 1, 'archer': 1, 'swordsman': 1}
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
        self.add_node(0, 'worker', True, 0)
        self.add_node(1, 'worker', False, 10)
        self.add_node(2, 'worker', False, 20)
        self.add_node(3, 'archer', True, 0)
        self.add_node(4, 'archer', False, 10)
        self.add_node(5, 'archer', False, 20)
        self.add_node(6, 'swordsman', True, 0)
        self.add_node(7, 'swordsman', False, 10)
        self.add_node(8, 'swordsman', False, 20)
        self.add_node(9, 'win', False, 50)

    def add_node(self, id, branch, unlocked, cost):
        """
        Add node on specific branch.

        :param branch: string branch to add node to
        """
        node = ResearchNode(id, branch, unlocked, cost)
        self._nodes[id] = node

    def unlockable(self, node_id):
        """Check if node is able to be unlocked, based on id."""
        nodes = self._nodes
        if node_id == 2 or node_id == 5 or node_id == 8:
            if nodes[node_id - 1]._unlocked:
                return True
            return False
        elif node_id == 9:
            if nodes[2] and nodes[5] and nodes[8]:
                return True
            return False
        return True

    def unlock_node(self, node_id):
        """Unlock node."""
        if node_id in self._nodes:
            node = self._nodes[node_id]
            node._unlocked = True
            self._tier[node._branch] += 1

    def get_unlocked(self):
        """Get unlocked nodes."""
        unlocked_nodes = []
        for node in self._nodes:
            if node.unlocked:
                unlocked_nodes += [node]
        return unlocked_nodes

    def get_unlockable(self):
        """Get unlockable nodes."""
        unlockable_nodes = []
        for node in self._nodes:
            if self.unlockable(node.id):
                unlockable_nodes += [node]
        return unlockable_nodes

    def __repr__(self):
        """Return string representation of Research Tree."""
        string = ""
        for node_id in self._nodes:
            string += str(self._nodes[node_id])
            string += "\n"
        return string


class ResearchNode(object):
    """Class for nodes of Research Tree."""

    def __init__(self, id, branch, unlocked, unlock_cost):
        """
        Initialise Research Nodes attributes.

        :param unlock_cost: int amount of science needed to unlock
        :param unlocked: boolean
        """
        self._branch = branch
        self._unlock_cost = unlock_cost
        self._unlocked = unlocked
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
        string = "Branch: %s, ID: %i, Unlocked: %s, Cost: %i"\
            % (self._branch, self._id, str(self._unlocked), self._unlock_cost)
        return string
