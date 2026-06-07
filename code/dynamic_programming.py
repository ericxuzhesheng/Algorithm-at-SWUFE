"""Dynamic Programming Algorithms.

Covers: Fibonacci, 0/1 Knapsack, LCS, Matrix Chain Multiplication,
Edit Distance, Optimal BST, Coin Change, Longest Increasing Subsequence.
"""

import math
from functools import lru_cache


# ---------------------------------------------------------------------------
# Fibonacci — O(n) bottom-up, O(n) memoized top-down
# ---------------------------------------------------------------------------

def fib_bottom_up(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


# ---------------------------------------------------------------------------
# 0/1 Knapsack — O(nW) time, O(W) space
# ---------------------------------------------------------------------------

def knapsack_01(weights: list[int], values: list[int], capacity: int) -> tuple[int, list[int]]:
    """Return (max_value, selected_item_indices)."""
    n = len(weights)
    # dp[j] = max value with capacity j
    dp = [0] * (capacity + 1)
    # track choices for backtracking
    keep = [[False] * (capacity + 1) for _ in range(n)]

    for i in range(n):
        for j in range(capacity, weights[i] - 1, -1):
            if dp[j - weights[i]] + values[i] > dp[j]:
                dp[j] = dp[j - weights[i]] + values[i]
                keep[i][j] = True

    # Backtrack to find selected items
    selected = []
    j = capacity
    for i in range(n - 1, -1, -1):
        if keep[i][j]:
            selected.append(i)
            j -= weights[i]
    return dp[capacity], selected[::-1]


# ---------------------------------------------------------------------------
# Longest Common Subsequence — O(mn) time and space
# ---------------------------------------------------------------------------

def lcs(X: str, Y: str) -> tuple[int, str]:
    """Return (length, one LCS string)."""
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack
    seq = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            seq.append(X[i - 1])
            i -= 1; j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], "".join(reversed(seq))


# ---------------------------------------------------------------------------
# Matrix Chain Multiplication — O(n^3)
# ---------------------------------------------------------------------------

def matrix_chain(dims: list[int]) -> tuple[int, str]:
    """Given dims=[p0,p1,...,pn], matrices A_i has size dims[i-1] x dims[i].

    Returns (min_multiplications, optimal_parenthesization).
    """
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = math.inf
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

    def _parenthesize(i: int, j: int) -> str:
        if i == j:
            return f"A{i+1}"
        k = split[i][j]
        return f"({_parenthesize(i, k)} x {_parenthesize(k+1, j)})"

    return dp[0][n - 1], _parenthesize(0, n - 1)


# ---------------------------------------------------------------------------
# Edit Distance (Levenshtein) — O(mn)
# ---------------------------------------------------------------------------

def edit_distance(s: str, t: str) -> int:
    m, n = len(s), len(t)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if s[i - 1] == t[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[n]


# ---------------------------------------------------------------------------
# Optimal Binary Search Tree — O(n^3)
# ---------------------------------------------------------------------------

def optimal_bst(keys: list, p: list[float], q: list[float]) -> float:
    """Compute minimum expected search cost for an optimal BST.

    keys[0..n-1]: sorted keys
    p[i]: probability of searching for key i
    q[i]: probability of searching for a value between keys (dummy keys)
    """
    n = len(keys)
    # e[i][j]: expected cost of optimal BST for keys i..j
    # w[i][j]: sum of probabilities p[i..j] + q[i-1..j]
    e = [[0.0] * (n + 1) for _ in range(n + 2)]
    w = [[0.0] * (n + 1) for _ in range(n + 2)]

    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]

    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            e[i][j] = math.inf
            w[i][j] = w[i][j - 1] + p[j - 1] + q[j]
            for r in range(i, j + 1):
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if t < e[i][j]:
                    e[i][j] = t

    return e[1][n]


# ---------------------------------------------------------------------------
# Coin Change — O(n * amount)
# ---------------------------------------------------------------------------

def coin_change(coins: list[int], amount: int) -> int:
    """Minimum number of coins to make amount. Returns -1 if impossible."""
    dp = [math.inf] * (amount + 1)
    dp[0] = 0
    for c in coins:
        for j in range(c, amount + 1):
            if dp[j - c] + 1 < dp[j]:
                dp[j] = dp[j - c] + 1
    return dp[amount] if dp[amount] != math.inf else -1


# ---------------------------------------------------------------------------
# Longest Increasing Subsequence — O(n log n) with patience sorting
# ---------------------------------------------------------------------------

def lis(arr: list[int]) -> tuple[int, list[int]]:
    """Return (length, one LIS)."""
    import bisect
    tails = []   # tails[i] = smallest tail of all increasing subseqs of length i+1
    prev = [-1] * len(arr)
    pos_in_tails = []

    for i, x in enumerate(arr):
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
        pos_in_tails.append(idx)
        prev[i] = -1

    # Backtrack
    length = len(tails)
    seq = []
    cur_len = length - 1
    for i in range(len(arr) - 1, -1, -1):
        if pos_in_tails[i] == cur_len:
            seq.append(arr[i])
            cur_len -= 1
            if cur_len < 0:
                break

    return length, seq[::-1]


if __name__ == "__main__":
    print("=== Fibonacci ===")
    print(f"  fib(10) = {fib_bottom_up(10)}, fib(20) = {fib_bottom_up(20)}")

    print("\n=== 0/1 Knapsack ===")
    w, v, cap = [2, 3, 4, 5], [3, 4, 5, 6], 8
    val, items = knapsack_01(w, v, cap)
    print(f"  Weights={w}, Values={v}, Capacity={cap}")
    print(f"  Max value={val}, Items selected (0-indexed)={items}")

    print("\n=== LCS ===")
    X, Y = "ABCBDAB", "BDCABA"
    length, seq = lcs(X, Y)
    print(f"  X={X!r}, Y={Y!r}")
    print(f"  LCS length={length}, sequence={seq!r}")

    print("\n=== Matrix Chain Multiplication ===")
    dims = [30, 35, 15, 5, 10, 20, 25]
    cost, parens = matrix_chain(dims)
    print(f"  Dimensions: {dims}")
    print(f"  Min cost: {cost}")
    print(f"  Parenthesization: {parens}")

    print("\n=== Edit Distance ===")
    pairs = [("kitten", "sitting"), ("sunday", "saturday"), ("", "abc")]
    for s, t in pairs:
        print(f"  edit_distance({s!r}, {t!r}) = {edit_distance(s, t)}")

    print("\n=== Coin Change ===")
    print(f"  coins=[1,5,10,25], amount=41 -> {coin_change([1,5,10,25], 41)} coins")
    print(f"  coins=[2], amount=3 -> {coin_change([2], 3)} (impossible)")

    print("\n=== LIS ===")
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    length, seq = lis(arr)
    print(f"  Array: {arr}")
    print(f"  LIS length={length}, sequence={seq}")
