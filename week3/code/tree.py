import numpy as np
import copy


class TreeError(Exception):
    """Exception for invalid tree operations."""
    pass


class TreeNode:
    def __init__(self, children=None, distances=None, index=None):
        self._is_root = False
        self._distance = 0.0
        self._parent = None

        if index is None:
            # Intermediate node
            if children is None or distances is None:
                raise TypeError(
                    "Either reference index (for terminal node) or "
                    "child nodes including the distance "
                    "(for intermediate node) must be set"
                )

            if len(children) == 0:
                raise TreeError("Intermediate nodes must at least contain one child node")
            if len(children) != len(distances):
                raise ValueError("Number of children must equal number of distances")

            self._index = -1
            self._children = tuple(children)
            for child, dist in zip(children, distances):
                if not isinstance(child, TreeNode):
                    raise TypeError("Children must be TreeNode objects")
                if not isinstance(dist, (float, int)):
                    raise TypeError("Distances must be float or int")
                child._set_parent(self, float(dist))
        elif index < 0:
            raise ValueError("Index cannot be negative")
        else:
            # Leaf node
            if children is not None or distances is not None:
                raise TypeError("Reference index and child nodes are mutually exclusive")
            self._index = index
            self._children = None

    def _set_parent(self, parent, distance):
        if self._parent is not None or self._is_root:
            raise TreeError("Node already has a parent")
        self._parent = parent
        self._distance = distance

    def copy(self):
        if self.is_leaf():
            return TreeNode(index=self._index)
        else:
            distances = [child.distance for child in self._children]
            children_clones = [child.copy() for child in self._children]
            return TreeNode(children_clones, distances)

    @property
    def index(self):
        return None if self._index == -1 else self._index

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @property
    def distance(self):
        return None if self._parent is None else self._distance

    def is_leaf(self):
        return self._index != -1

    def is_root(self):
        return self._is_root

    def as_root(self):
        if self._parent is not None:
            raise TreeError("Node has parent, cannot be root")
        self._is_root = True

    def distance_to(self, node, topological=False):
        lca = self.lowest_common_ancestor(node)
        if lca is None:
            raise TreeError("Nodes do not have common ancestor")

        distance = 0.0
        current = self
        while current is not lca:
            distance += 1 if topological else current._distance
            current = current._parent

        current = node
        while current is not lca:
            distance += 1 if topological else current._distance
            current = current._parent

        return distance

    def lowest_common_ancestor(self, node):
        self_path = _create_path_to_root(self)
        other_path = _create_path_to_root(node)
        lca = None
        for i in range(1, min(len(self_path), len(other_path)) + 1):
            if self_path[-i] is other_path[-i]:
                lca = self_path[-i]
            else:
                break
        return lca

    def get_leaves(self):
        leaves = []
        _get_leaves(self, leaves)
        return leaves

    def get_leaf_count(self):
        return _get_leaf_count(self)

    def to_newick(self, labels=None, include_distance=True, round_distance=None):
        if self.is_leaf():
            label = str(self._index)
            if labels is not None:
                label = labels[self._index]

            if include_distance:
                dist = round(self._distance, round_distance) if round_distance is not None else self._distance
                return f"{label}:{dist}"
            else:
                return label
        else:
            child_strs = [child.to_newick(labels, include_distance, round_distance) for child in self._children]
            joined = ",".join(child_strs)
            if include_distance:
                dist = round(self._distance, round_distance) if round_distance is not None else self._distance
                return f"({joined}):{dist}"
            else:
                return f"({joined})"

    @staticmethod
    def from_newick(newick, labels=None):
        newick = newick.strip().replace(" ", "")
        if not newick:
            raise Exception("Newick string is empty")

        # Leaf node case
        if "(" not in newick:
            if ":" in newick:
                label, dist = newick.split(":")
                dist = float(dist)
            else:
                label, dist = newick, 0.0
            index = int(label) if labels is None else labels.index(label)
            return TreeNode(index=index), dist

        # Intermediate node
        start = newick.find("(")
        stop = newick.rfind(")")
        sub = newick[start + 1:stop]
        after = newick[stop + 1:]
        distance = 0.0
        if ":" in after:
            try:
                _, dist = after.split(":")
                distance = float(dist)
            except ValueError:
                distance = 0.0

        # Split subnodes at commas that aren’t nested
        children, distances = [], []
        level = 0
        parts, last = [], 0
        for i, ch in enumerate(sub):
            if ch == "(":
                level += 1
            elif ch == ")":
                level -= 1
            elif ch == "," and level == 0:
                parts.append(sub[last:i])
                last = i + 1
        parts.append(sub[last:])
        for p in parts:
            child, dist = TreeNode.from_newick(p, labels)
            children.append(child)
            distances.append(dist)
        return TreeNode(children, distances), distance

    def __str__(self):
        return self.to_newick()

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        if self._distance != other._distance:
            return False
        if self._index != other._index:
            return False
        if self._children and other._children:
            return set(self._children) == set(other._children)
        return True

    def __hash__(self):
        children_set = frozenset(self._children) if self._children else None
        return hash((self._index, children_set, self._distance))


def _get_leaves(node, leaf_list):
    if node._index == -1:
        for c in node._children:
            _get_leaves(c, leaf_list)
    else:
        leaf_list.append(node)


def _get_leaf_count(node):
    if node._index == -1:
        return sum(_get_leaf_count(c) for c in node._children)
    else:
        return 1


def _create_path_to_root(node):
    path = []
    current = node
    while current is not None:
        path.append(current)
        current = current._parent
    return path


class Tree:
    def __init__(self, root):
        root.as_root()
        self._root = root

        leaves_unsorted = root.get_leaves()
        indices = [leaf.index for leaf in leaves_unsorted]
        leaf_count = len(leaves_unsorted)
        self._leaves = [None] * leaf_count
        for i, idx in enumerate(indices):
            if idx >= leaf_count or idx < 0:
                raise TreeError("Tree indices are out of range")
            self._leaves[idx] = leaves_unsorted[i]

    @property
    def root(self):
        return self._root

    @property
    def leaves(self):
        return copy.copy(self._leaves)

    def get_distance(self, index1, index2, topological=False):
        return self._leaves[index1].distance_to(self._leaves[index2], topological)

    def to_newick(self, labels=None, include_distance=True, round_distance=None):
        return self._root.to_newick(labels, include_distance, round_distance) + ";"

    @staticmethod
    def from_newick(newick, labels=None):
        newick = newick.strip()
        if newick.endswith(";"):
            newick = newick[:-1]
        root, _ = TreeNode.from_newick(newick, labels)
        return Tree(root)

    def __len__(self):
        return len(self._leaves)

    def __str__(self):
        return self.to_newick()

    def __eq__(self, other):
        return isinstance(other, Tree) and self._root == other._root

    def __hash__(self):
        return hash(self._root)


def as_binary(tree_or_node):
    if isinstance(tree_or_node, Tree):
        node, _ = _as_binary(tree_or_node.root)
        return Tree(node)
    elif isinstance(tree_or_node, TreeNode):
        node, _ = _as_binary(tree_or_node)
        return node
    else:
        raise TypeError("Expected Tree or TreeNode")


def _as_binary(node):
    if node.children is None:
        return TreeNode(index=node.index), node.distance
    elif len(node.children) == 1:
        child, dist = _as_binary(node.children[0])
        if node.is_root():
            return child, None
        return child, (node.distance or 0.0) + (dist or 0.0)
    elif len(node.children) > 2:
        rem_children, distances = zip(*[_as_binary(c) for c in node.children])
        rem_children = list(rem_children)
        distances = list(distances)
        current = None
        while rem_children:
            if current is None:
                current = TreeNode(rem_children[:2], distances[:2])
                rem_children = rem_children[2:]
                distances = distances[2:]
            else:
                current = TreeNode((current, rem_children[0]), (0, distances[0]))
                rem_children.pop(0)
                distances.pop(0)
        return current, node.distance
    else:
        binary_children, dists = zip(*[_as_binary(c) for c in node.children])
        return TreeNode(binary_children, dists), node.distance
