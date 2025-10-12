import numpy as np
from tree import Tree, TreeNode


MAX_FLOAT = np.finfo(np.float32).max


def neighbor_joining(distances: np.ndarray) -> Tree:
    """
    Perform hierarchical clustering using the Neighbor Joining algorithm.
    Based on Saitou and Nei (1987); Studier and Keppler (1988).

    Parameters
    ----------
    distances : ndarray, shape=(n, n)
        Pairwise distance matrix.

    Returns
    -------
    Tree
        A rooted Tree object where leaf nodes correspond to indices of
        the original matrix.
    """
    # ---- Validation ----
    if distances.shape[0] != distances.shape[1] or not np.allclose(distances.T, distances):
        raise ValueError("Distance matrix must be symmetric")
    if np.isnan(distances).any():
        raise ValueError("Distance matrix contains NaN values")
    if (distances >= MAX_FLOAT).any():
        raise ValueError("Distance matrix contains infinity")
    if distances.shape[0] < 4:
        raise ValueError("At least 4 nodes are required")
    if (distances < 0).any():
        raise ValueError("Distances must be positive")

    # ---- Initialization ----
    n = distances.shape[0]
    nodes = np.array([TreeNode(index=i) for i in range(n)], dtype=object)
    is_clustered = np.full(n, False, dtype=bool)
    divergence = np.zeros(n, dtype=np.float32)
    corr_distances = np.zeros((n, n), dtype=np.float32)
    distances_v = distances.astype(np.float32, copy=True)

    n_rem_nodes = n - np.count_nonzero(is_clustered)

    # ---- Main loop ----
    while True:
        # 1. Compute divergence for each active node
        for i in range(n):
            if is_clustered[i]:
                continue
            dist_sum = 0.0
            for k in range(n):
                if not is_clustered[k]:
                    dist_sum += distances_v[i, k]
            divergence[i] = dist_sum

        # 2. Compute corrected distances
        for i in range(n):
            if is_clustered[i]:
                continue
            for j in range(i):
                if is_clustered[j]:
                    continue
                corr_distances[i, j] = (n_rem_nodes - 2) * distances_v[i, j] - divergence[i] - divergence[j]

        # 3. Find minimum corrected distance pair
        dist_min = MAX_FLOAT
        i_min, j_min = -1, -1
        for i in range(n):
            if is_clustered[i]:
                continue
            for j in range(i):
                if is_clustered[j]:
                    continue
                dist = corr_distances[i, j]
                if dist < dist_min:
                    dist_min = dist
                    i_min, j_min = i, j

        # No valid pair found → done
        if i_min == -1 or j_min == -1:
            break

        # 4. Compute node distances
        node_dist_i = 0.5 * (
            distances_v[i_min, j_min]
            + (divergence[i_min] - divergence[j_min]) / (n_rem_nodes - 2)
        )
        node_dist_j = 0.5 * (
            distances_v[i_min, j_min]
            + (divergence[j_min] - divergence[i_min]) / (n_rem_nodes - 2)
        )

        # 5. Cluster merge step
        if n_rem_nodes > 3:
            nodes[i_min] = TreeNode(
                (nodes[i_min], nodes[j_min]),
                (float(node_dist_i), float(node_dist_j))
            )
            nodes[j_min] = None
            is_clustered[j_min] = True
        else:
            # Last join → build root node
            is_clustered[i_min] = True
            is_clustered[j_min] = True
            # Find the last unclustered node
            remaining = np.where(~is_clustered)[0]
            if len(remaining) != 1:
                raise ValueError("Unexpected number of remaining nodes at final step")
            k = remaining[0]
            node_dist_k = 0.5 * (
                distances_v[i_min, k] + distances_v[j_min, k] - distances_v[i_min, j_min]
            )
            root = TreeNode(
                (nodes[i_min], nodes[j_min], nodes[k]),
                (float(node_dist_i), float(node_dist_j), float(node_dist_k))
            )
            return Tree(root)

        # 6. Update distance matrix for new cluster
        for k in range(n):
            if not is_clustered[k] and k != i_min:
                dist = 0.5 * (
                    distances_v[i_min, k] + distances_v[j_min, k] - distances_v[i_min, j_min]
                )
                distances_v[i_min, k] = dist
                distances_v[k, i_min] = dist

        # 7. Update remaining node count
        n_rem_nodes = n - np.count_nonzero(is_clustered)
