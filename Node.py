import random

class Node:
    """Node from a tree"""

    def __init__(self, node_id, ancestor=None, childs=None):
        if childs is None:
            childs = set()
        assert isinstance(childs, set)

        self._node_id = node_id
        self._ancestor = ancestor
        self._childs = childs
        self._anc_count = 0
        self._depth = 1

    def _update_depth(self, new_depth):
        if self._depth < new_depth:
            self._depth = new_depth
            if self._ancestor:
                self._ancestor._update_depth(new_depth + 1)

    def add_node(self, node):
        """Adds node as child"""
        assert isinstance(node, Node)
        assert node._ancestor is None
        assert node._anc_count == 0

        node._ancestor = self
        node._anc_count = self._anc_count + 1
        self._childs.add(node)
        self._update_depth(node._depth + 1)

    def iter_in_order(self):
        yield self
        for child in self._childs:
            for x in child.iter_in_order():
                yield x

    def getLongestPathLen(self):
        return self._anc_count + self._depth

    def getChildren(self):
        return self._childs

    def indentPrint(self, level):
        indenter = "|-"
        result = (indenter * level) + str(self._node_id)
        if self._childs:
            result += '\n'
            result += '\n'.join(list(map(lambda x: x.indentPrint(level + 1), self._childs)))
        return result

    def __str__(self):
        return self.indentPrint(0)

def createTree(max_childs, min_childs, max_depth, node_count=None):

    max_node_count = int(((max_childs ** max_depth) - 1) / (max_childs - 1))
    if node_count is None:
        node_count = max_node_count
    assert node_count <= max_node_count
    assert min_childs <= max_childs

    next_id = 1
    root = Node(0)
    active_set = set()
    active_set.add(root)
    for next_id in range(1, node_count):
        if not active_set:
            print('fail ' + str(next_id))
            return root

        anc_node = random.sample(active_set, 1)[0]

        # Always add at least one new node, and fill a node with the minimum
        # required amount of children
        while True:
            cur_node = Node(next_id)
            anc_node.add_node(cur_node)
            if cur_node.getLongestPathLen() < max_depth:
                active_set.add(cur_node)

            if len(anc_node.getChildren()) >= min_childs:
                break

        if len(anc_node.getChildren()) >= max_childs:
            active_set.remove(anc_node)

    return root
