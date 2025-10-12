# upgma.py (pure Python version)

import numpy as np
from tree import Tree, TreeNode

# Use float64 for safety/consistency
MAX_FLOAT = np.finfo(np.float64).max
def upgma(distances):
    """
    Perform hierarchical clustering using UPGMA (Unweighted Pair Group Method with Arithmetic mean).
    """
    # ---- Validation ----
    if distances.ndim != 2 or distances.shape[0] != distances.shape[1]:
        raise ValueError("Distance matrix must be square")
    if not np.allclose(distances, distances.T):
        raise ValueError("Distance matrix must be symmetric")
    if np.isnan(distances).any():
        raise ValueError("Distance matrix contains NaN values")
    if (distances >= MAX_FLOAT).any() or np.isinf(distances).any():
        raise ValueError("Distance matrix contains infinity")
    if (distances < 0).any():
        raise ValueError("Distances must be positive")

    n = distances.shape[0]

    # ---- Homogeneous lists ----
    nodes: List[TreeNode] = [TreeNode(index=i) for i in range(n)]
    is_clustered: List[bool] = [False for _ in range(n)]
    cluster_size: List[int] = [1 for _ in range(n)]
    node_height: List[float] = [0.0 for _ in range(n)]

    D = distances.astype(np.float64, copy=True)

    while True:
        dist_min = MAX_FLOAT
        i_min, j_min = -1, -1
        for i in range(n):
            if is_clustered[i]:
                continue
            for j in range(i):
                if is_clustered[j]:
                    continue
                d = D[i, j]
                if d < dist_min:
                    dist_min = d
                    i_min, j_min = i, j

        if i_min == -1 or j_min == -1:
            break

        height = dist_min / 2.0
        nodes[i_min] = TreeNode(
            (nodes[i_min], nodes[j_min]),
            (height - node_height[i_min], height - node_height[j_min])
        )
        node_height[i_min] = height
        is_clustered[j_min] = True

        # Update distances
        for k in range(n):
            if (not is_clustered[k]) and k != i_min:
                mean = (
                    D[i_min, k] * cluster_size[i_min]
                    + D[j_min, k] * cluster_size[j_min]
                ) / (cluster_size[i_min] + cluster_size[j_min])
                D[i_min, k] = mean
                D[k, i_min] = mean

        cluster_size[i_min] = cluster_size[i_min] + cluster_size[j_min]

    remaining: List[int] = [i for i, used in enumerate(is_clustered) if not used]
    if len(remaining) != 1:
        raise ValueError("UPGMA ended with an unexpected number of active nodes")

    root_idx = remaining[0]
    root_node = nodes[root_idx]
    return Tree(root_node)
