import argparse

# -------------------- Scoring constants --------------------
MATCH = 3
MISMATCH = -3
GAP = -2

# Affine gap penalties (used only in affine global)
GAP_OPEN = -5
GAP_EXTEND = -1


# -------------------- FASTA reader --------------------
def read_first_fasta(path: str) -> str:
    seq = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(">"):
                continue
            seq.append(line)
    return "".join(seq)


# -------------------- Scoring helper --------------------
def score(a: str, b: str) -> int:
    return MATCH if a == b else MISMATCH


# -------------------- Global alignment --------------------
def global_align(A: str, B: str) -> int:
    n, m = len(A), len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i * GAP
    for j in range(1, m + 1):
        dp[0][j] = j * GAP
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = max(
                dp[i - 1][j - 1] + score(A[i - 1], B[j - 1]),
                dp[i - 1][j] + GAP,
                dp[i][j - 1] + GAP,
            )
    return dp[n][m]


# -------------------- Local alignment --------------------
def local_align(A: str, B: str) -> int:
    n, m = len(A), len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    best = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = max(
                0,
                dp[i - 1][j - 1] + score(A[i - 1], B[j - 1]),
                dp[i - 1][j] + GAP,
                dp[i][j - 1] + GAP,
            )
            best = max(best, dp[i][j])
    return best


# -------------------- Semi-global (fitting) alignment --------------------
def semi_global_align(A: str, B: str) -> int:
    n, m = len(A), len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = max(
                dp[i - 1][j - 1] + score(A[i - 1], B[j - 1]),
                dp[i - 1][j] + GAP,
                dp[i][j - 1] + GAP,
            )
    # best at last row or last column
    return max(max(dp[n]), max(row[m] for row in dp))


# -------------------- Affine gap global alignment --------------------
def affine_global_align(A: str, B: str) -> int:
    n, m = len(A), len(B)
    NEG_INF = -10**9
    M = [[0] * (m + 1) for _ in range(n + 1)]
    X = [[NEG_INF] * (m + 1) for _ in range(n + 1)]
    Y = [[NEG_INF] * (m + 1) for _ in range(n + 1)]

    # Correct initialization
    M[0][0] = 0
    X[0][0] = Y[0][0] = NEG_INF
    for i in range(1, n + 1):
        X[i][0] = GAP_OPEN + (i - 1) * GAP_EXTEND
        M[i][0] = NEG_INF
        Y[i][0] = NEG_INF
    for j in range(1, m + 1):
        Y[0][j] = GAP_OPEN + (j - 1) * GAP_EXTEND
        M[0][j] = NEG_INF
        X[0][j] = NEG_INF

    # Fill DP
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            X[i][j] = max(X[i - 1][j] + GAP_EXTEND, M[i - 1][j] + GAP_OPEN + GAP_EXTEND)
            Y[i][j] = max(Y[i][j - 1] + GAP_EXTEND, M[i][j - 1] + GAP_OPEN + GAP_EXTEND)
            M[i][j] = max(
                M[i - 1][j - 1] + score(A[i - 1], B[j - 1]),
                X[i][j],
                Y[i][j],
            )

    return M[n][m]


# -------------------- Main CLI --------------------
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
