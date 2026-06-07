"""Backtracking Algorithms.

Covers: N-Queens, Graph Coloring, Subset Sum,
Hamiltonian Cycle, 0/1 Knapsack (backtracking), Permutation Generation.
"""

from typing import Generator


# ---------------------------------------------------------------------------
# N-Queens — place n non-attacking queens on an n×n board
# ---------------------------------------------------------------------------

def n_queens(n: int) -> list[list[int]]:
    """Return all solutions. Each solution is a list where sol[i] = col of queen in row i."""
    solutions: list[list[int]] = []
    queens: list[int] = []
    cols: set[int] = set()
    diag1: set[int] = set()  # row - col
    diag2: set[int] = set()  # row + col

    def backtrack(row: int) -> None:
        if row == n:
            solutions.append(queens[:])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            queens.append(col)
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            backtrack(row + 1)
            queens.pop()
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)

    backtrack(0)
    return solutions


def print_board(solution: list[int]) -> None:
    n = len(solution)
    for row in range(n):
        line = ["Q" if solution[row] == col else "." for col in range(n)]
        print("  " + " ".join(line))


# ---------------------------------------------------------------------------
# Graph Coloring — color graph with at most k colors, no adjacent same color
# ---------------------------------------------------------------------------

def graph_coloring(adj: dict[int, list[int]], k: int) -> list[int] | None:
    """Return a k-coloring (node -> color 1..k), or None if impossible."""
    n = len(adj)
    color = [0] * n

    def is_safe(v: int, c: int) -> bool:
        return all(color[u] != c for u in adj[v])

    def backtrack(v: int) -> bool:
        if v == n:
            return True
        for c in range(1, k + 1):
            if is_safe(v, c):
                color[v] = c
                if backtrack(v + 1):
                    return True
                color[v] = 0
        return False

    return color[:] if backtrack(0) else None


# ---------------------------------------------------------------------------
# Subset Sum — find all subsets summing to target
# ---------------------------------------------------------------------------

def subset_sum(nums: list[int], target: int) -> list[list[int]]:
    """Return all subsets of nums that sum to target."""
    results: list[list[int]] = []
    nums_sorted = sorted(nums)

    def backtrack(start: int, current: list[int], remaining: int) -> None:
        if remaining == 0:
            results.append(current[:])
            return
        for i in range(start, len(nums_sorted)):
            if i > start and nums_sorted[i] == nums_sorted[i - 1]:
                continue  # skip duplicates
            if nums_sorted[i] > remaining:
                break
            current.append(nums_sorted[i])
            backtrack(i + 1, current, remaining - nums_sorted[i])
            current.pop()

    backtrack(0, [], target)
    return results


# ---------------------------------------------------------------------------
# Hamiltonian Cycle
# ---------------------------------------------------------------------------

def hamiltonian_cycle(adj_matrix: list[list[int]]) -> list[int] | None:
    """Return Hamiltonian cycle as list of vertices, or None."""
    n = len(adj_matrix)
    path = [0]
    visited = [False] * n
    visited[0] = True

    def backtrack() -> bool:
        if len(path) == n:
            return adj_matrix[path[-1]][path[0]] == 1
        v = path[-1]
        for u in range(n):
            if not visited[u] and adj_matrix[v][u] == 1:
                path.append(u)
                visited[u] = True
                if backtrack():
                    return True
                path.pop()
                visited[u] = False
        return False

    return path + [0] if backtrack() else None


# ---------------------------------------------------------------------------
# 0/1 Knapsack via Backtracking (with upper bound pruning)
# ---------------------------------------------------------------------------

def knapsack_backtrack(weights: list[int], values: list[int], capacity: int) -> int:
    """Solve 0/1 knapsack using backtracking with greedy upper bound."""
    n = len(weights)
    # Sort by value density for better pruning
    items = sorted(zip(weights, values), key=lambda x: x[1] / x[0], reverse=True)
    w_sorted = [x[0] for x in items]
    v_sorted = [x[1] for x in items]

    best = [0]

    def upper_bound(i: int, remaining_cap: int, cur_val: int) -> float:
        ub = cur_val
        for j in range(i, n):
            if w_sorted[j] <= remaining_cap:
                ub += v_sorted[j]
                remaining_cap -= w_sorted[j]
            else:
                ub += v_sorted[j] * remaining_cap / w_sorted[j]
                break
        return ub

    def backtrack(i: int, cap: int, val: int) -> None:
        if i == n or cap == 0:
            best[0] = max(best[0], val)
            return
        if upper_bound(i, cap, val) <= best[0]:
            return
        # Include item i
        if w_sorted[i] <= cap:
            backtrack(i + 1, cap - w_sorted[i], val + v_sorted[i])
        # Exclude item i
        backtrack(i + 1, cap, val)

    backtrack(0, capacity, 0)
    return best[0]


# ---------------------------------------------------------------------------
# Permutation Generation
# ---------------------------------------------------------------------------

def permutations(elements: list) -> list[list]:
    """Generate all permutations of elements."""
    result: list[list] = []

    def backtrack(start: int) -> None:
        if start == len(elements):
            result.append(elements[:])
            return
        for i in range(start, len(elements)):
            elements[start], elements[i] = elements[i], elements[start]
            backtrack(start + 1)
            elements[start], elements[i] = elements[i], elements[start]

    backtrack(0)
    return result


if __name__ == "__main__":
    print("=== N-Queens (n=4) ===")
    sols = n_queens(4)
    print(f"  {len(sols)} solutions found")
    for s in sols:
        print_board(s)
        print()

    print("=== N-Queens count (n=8) ===")
    print(f"  8-queens solutions: {len(n_queens(8))}")

    print("\n=== Graph Coloring ===")
    # Petersen-like graph (simple 5-cycle)
    adj = {0: [1, 4], 1: [0, 2], 2: [1, 3], 3: [2, 4], 4: [3, 0]}
    coloring = graph_coloring(adj, 3)
    print(f"  5-cycle with 3 colors: {coloring}")
    coloring2 = graph_coloring(adj, 2)
    print(f"  5-cycle with 2 colors: {coloring2} (None = impossible)")

    print("\n=== Subset Sum ===")
    nums = [2, 3, 6, 7]
    target = 7
    subsets = subset_sum(nums, target)
    print(f"  nums={nums}, target={target}")
    print(f"  Subsets: {subsets}")

    print("\n=== Hamiltonian Cycle ===")
    # Complete graph K4
    K4 = [[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
    cycle = hamiltonian_cycle(K4)
    print(f"  K4 Hamiltonian cycle: {cycle}")
    # Graph without Hamiltonian cycle
    no_ham = [[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]]
    print(f"  Path graph: {hamiltonian_cycle(no_ham)}")

    print("\n=== 0/1 Knapsack (Backtracking) ===")
    w, v, cap = [2, 3, 4, 5], [3, 4, 5, 6], 8
    print(f"  Weights={w}, Values={v}, Capacity={cap}")
    print(f"  Max value: {knapsack_backtrack(w, v, cap)}")

    print("\n=== Permutations ===")
    perms = permutations([1, 2, 3])
    print(f"  Permutations of [1,2,3]: {perms}")
    print(f"  Count: {len(perms)}")
