# test_phylo.py
# Compatible with your pure-Python Tree, UPGMA, and Neighbor Joining implementations.

from os.path import join, dirname, abspath
import numpy as np
import pytest

# Import your Python versions
from tree import Tree, TreeNode
from upgma import upgma
from nj import neighbor_joining


@pytest.fixture
def distances():
    """
    Load the test distance matrix.
    Expected to be in ./data/distances.txt relative to this file.
    """
    data_path = join(dirname(dirname(abspath(__file__))), "data", "distances.txt")
    return np.loadtxt(data_path, dtype=int)


@pytest.fixture
def tree(distances):
    """
    Generate the tree from the distance matrix using UPGMA.
    """
    return upgma(distances)


@pytest.fixture
def upgma_newick():
    """
    Load reference Newick string from DendroUPGMA output.
    Expected in ./data/newick_upgma.txt
    """
    path = join(dirname(dirname(abspath(__file__))), "data", "newick_upgma.txt")
    with open(path, "r") as f:
        return f.read().strip()


def test_upgma(tree, upgma_newick):
    """
    Compare the results of `upgma()` with the DendroUPGMA reference.
    """
    ref_tree = Tree.from_newick(upgma_newick)

    for i in range(len(tree)):
        for j in range(len(tree)):
            # Compare distances numerically (allow small FP tolerance)
            assert tree.get_distance(i, j) == pytest.approx(
                ref_tree.get_distance(i, j), abs=1e-3
            )
            # Compare topological structure
            assert tree.get_distance(i, j, topological=True) == ref_tree.get_distance(
                i, j, topological=True
            )


def test_neighbor_joining():
    """
    Validate neighbor joining with known tree topology.
    """
    dist = np.array([
        [0, 5, 4, 7, 6, 8],
        [5, 0, 7, 10, 9, 11],
        [4, 7, 0, 7, 6, 8],
        [7, 10, 7, 0, 5, 9],
        [6, 9, 6, 5, 0, 8],
        [8, 11, 8, 9, 8, 0],
    ])

    ref_tree = Tree(
        TreeNode(
            [
                TreeNode(
                    [
                        TreeNode(
                            [
                                TreeNode(index=0),
                                TreeNode(index=1),
                            ],
                            [1, 4],
                        ),
                        TreeNode(index=2),
                    ],
                    [1, 2],
                ),
                TreeNode(
                    [
                        TreeNode(index=3),
                        TreeNode(index=4),
                    ],
                    [3, 2],
                ),
                TreeNode(index=5),
            ],
            [1, 1, 5],
        )
    )

    test_tree = neighbor_joining(dist)
    assert test_tree == ref_tree


def test_distances(tree):
    """
    Confirm UPGMA tree’s leaf nodes have equal distance to the root,
    and topological distances match expected values.
    """
    dist_to_root = tree.root.distance_to(tree.leaves[0])
    for leaf in tree.leaves:
        assert leaf.distance_to(tree.root) == dist_to_root

    # Example topological distances from Biotite’s dataset
    assert tree.get_distance(0, 19, True) == 9
    assert tree.get_distance(4, 2, True) == 10


def main():
    """
    Standalone performance runner — prints total Python runtime in ms.
    """
    import time

    base_dir = dirname(dirname(abspath(__file__)))
    distances_path = join(base_dir, "data", "distances.txt")
    newick_path = join(base_dir, "data", "newick_upgma.txt")

    distances_data = np.loadtxt(distances_path, dtype=int)
    with open(newick_path, "r") as f:
        upgma_newick_data = f.read().strip()

    tree_data = upgma(distances_data)

    start = time.time()
    test_distances(tree_data)
    test_neighbor_joining()
    test_upgma(tree_data, upgma_newick_data)
    elapsed = (time.time() - start) * 1000

    print(f"python      {elapsed:.0f}ms")


if __name__ == "__main__":
    main()
