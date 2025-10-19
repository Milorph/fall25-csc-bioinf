#!/usr/bin/env python3
import argparse
import numpy as np

# =====================================================
# Scoring constants
# =====================================================
MATCH = 3
MISMATCH = -3
GAP = -2
GAP_OPEN = -5
GAP_EXTEND = -1


# =====================================================
# FASTA Reader
# =====================================================
def read_first_fasta(path: str) -> str:
    seq = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(">"):
                continue
            seq.append(line)
    return "".join(seq)


# =====================================================
# 1. Global Alignment (Needleman–Wunsch)
# =====================================================
def global_align(a: str, b: str) -> int:
    n, m = len(a), len(b)
    F = np.zeros((n + 1, m + 1), dtype=int)

    # Initialize
    F[0, 1:] = np.arange(1, m + 1) * GAP
    F[1:, 0] = np.arange(1, n + 1) * GAP

    # DP fill
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = F[i - 1, j - 1] + (MATCH if a[i - 1] == b[j - 1] else MISMATCH)
            up = F[i - 1, j] + GAP
            left = F[i, j - 1] + GAP
            F[i, j] = max(diag, up, left)

    return int(F[n, m])


# =====================================================
# 2. Local Alignment (Smith–Waterman)
# =====================================================
def local_align(a: str, b: str) -> int:
    n, m = len(a), len(b)
    F = np.zeros((n + 1, m + 1), dtype=int)
    best = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = F[i - 1, j - 1] + (MATCH if a[i - 1] == b[j - 1] else MISMATCH)
            up = F[i - 1, j] + GAP
            left = F[i, j - 1] + GAP
            F[i, j] = max(0, diag, up, left)
            if F[i, j] > best:
                best = F[i, j]

    return int(best)


# =====================================================
# 3. Semi-global (Fitting) Alignment
# =====================================================
def semi_global_align(a: str, b: str) -> int:
    n, m = len(a), len(b)
    F = np.zeros((n + 1, m + 1), dtype=int)

    # Initialize: query penalized, target free at start
    F[1:, 0] = np.arange(1, n + 1) * GAP
    F[0, :] = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = F[i - 1, j - 1] + (MATCH if a[i - 1] == b[j - 1] else MISMATCH)
            up = F[i - 1, j] + GAP
            left = F[i, j - 1] + GAP
            F[i, j] = max(diag, up, left)

    # Best alignment must end at end of query (row n)
    return int(np.max(F[n, :]))


# =====================================================
# 4. Affine Gap Global Alignment
# =====================================================
def affine_global_align(a: str, b: str) -> int:
    n, m = len(a), len(b)
    NEG_INF = -10**9

    M = np.full((n + 1, m + 1), NEG_INF, dtype=int)
    X = np.full((n + 1, m + 1), NEG_INF, dtype=int)
    Y = np.full((n + 1, m + 1), NEG_INF, dtype=int)

    M[0, 0] = 0
    for i in range(1, n + 1):
        X[i, 0] = GAP_OPEN + (i - 1) * GAP_EXTEND
    for j in range(1, m + 1):
        Y[0, j] = GAP_OPEN + (j - 1) * GAP_EXTEND

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match_score = MATCH if a[i - 1] == b[j - 1] else MISMATCH
            M[i, j] = max(
                M[i - 1, j - 1] + match_score,
                X[i - 1, j - 1] + match_score,
                Y[i - 1, j - 1] + match_score,
            )
            X[i, j] = max(M[i - 1, j] + GAP_OPEN + GAP_EXTEND, X[i - 1, j] + GAP_EXTEND)
            Y[i, j] = max(M[i, j - 1] + GAP_OPEN + GAP_EXTEND, Y[i, j - 1] + GAP_EXTEND)

    return int(max(M[n, m], X[n, m], Y[n, m]))


# =====================================================
# Main CLI
# =====================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", required=True)
    parser.add_argument("--a", required=True)
    parser.add_argument("--b", required=True)
    args = parser.parse_args()

    A = read_first_fasta(args.a)
    B = read_first_fasta(args.b)

    if args.method == "global":
        res = global_align(A, B)
    elif args.method == "local":
        res = local_align(A, B)
    elif args.method == "semi-global":
        res = semi_global_align(A, B)
    elif args.method == "affine-global":
        res = affine_global_align(A, B)
    else:
        raise ValueError("Invalid method name")

    print(res)


if __name__ == "__main__":
    main()
