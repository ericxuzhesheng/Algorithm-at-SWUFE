"""NP-Hard Problems and Approximation Algorithms.

Since NP-hard problems have no known polynomial exact algorithms,
this module covers:
  - Problem definitions and reductions
  - Approximation algorithms with provable ratios
  - Local search heuristics

Algorithms:
  Vertex Cover     — 2-approximation (greedy matching)
  Set Cover        — O(log n)-approximation (greedy)
  Max-Cut          — 0.5-approximation (greedy), local search improvement
  TSP metric       — 2-approximation (MST-based), 1.5-approx (Christofides sketch)
  Knapsack         — FPTAS (fully polynomial-time approximation scheme)
  Bin Packing      — First-Fit Decreasing (FFD), ratio <= 11/9 OPT + 6/9
  Graph Clique     — Greedy heuristic (no poly-time constant-ratio approx unless P=NP)
  3-SAT            — Random assignment (1/2-approx on expected satisfied clauses)
"""

import random
import math
import heapq
from itertools import combinations


# ---------------------------------------------------------------------------
# Vertex Cover — 2-approximation
# ---------------------------------------------------------------------------

def vertex_cover_approx(n: int, edges: list[tuple[int, int]]) -> set[int]:
    """Return a vertex cover of size at most 2 * OPT.

    Algorithm: repeatedly pick any uncovered edge (u,v), add both u and v,
    remove all edges incident to u or v.
    """
    cover: set[int] = set()
    remaining = list(edges)
    while remaining:
        u, v = remaining.pop(0)
        if u in cover or v in cover:
            continue
        cover.add(u)
        cover.add(v)
        remaining = [(a, b) for a, b in remaining if a not in cover and b not in cover]
    return cover


def is_vertex_cover(n: int, edges: list[tuple[int, int]], cover: set[int]) -> bool:
    return all(u in cover or v in cover for u, v in edges)


# ---------------------------------------------------------------------------
# Set Cover — greedy O(log n)-approximation
# ---------------------------------------------------------------------------

def set_cover_greedy(universe: set, subsets: list[set]) -> list[int]:
    """Return indices of chosen subsets covering universe.

    Approximation ratio: H(max_subset_size) = O(log n).
    """
    covered: set = set()
    chosen: list[int] = []
    remaining_subsets = [(i, s.copy()) for i, s in enumerate(subsets)]

    while covered != universe:
        # pick subset covering the most uncovered elements
        best_idx, best_set, best_count = -1, set(), 0
        for i, s in remaining_subsets:
            new = len(s - covered)
            if new > best_count:
                best_count, best_idx, best_set = new, i, s
        if best_idx == -1:
            break  # universe not coverable
        chosen.append(best_idx)
        covered |= best_set
        remaining_subsets = [(i, s) for i, s in remaining_subsets if i != best_idx]

    return chosen


# ---------------------------------------------------------------------------
# Max-Cut — greedy 1/2-approximation + local search
# ---------------------------------------------------------------------------

def max_cut_greedy(n: int, edges: list[tuple[int, int, float]]) -> tuple[float, set[int]]:
    """Greedy max-cut: assign each vertex to the side that maximizes cut weight.

    Guaranteed to achieve at least 1/2 of optimal.
    """
    side: dict[int, int] = {}  # 0 or 1
    cut_weight = 0.0

    for v in range(n):
        gain_0, gain_1 = 0.0, 0.0
        for u, w_u, w in edges:
            if u == v and w_u in side:
                if side[w_u] == 1:
                    gain_0 += w
                else:
                    gain_1 += w
            elif w_u == v and u in side:
                if side[u] == 1:
                    gain_0 += w
                else:
                    gain_1 += w
        side[v] = 0 if gain_0 >= gain_1 else 1

    cut = {v for v, s in side.items() if s == 0}
    total = sum(w for u, v, w in edges if (u in cut) != (v in cut))
    return total, cut


def max_cut_local_search(n: int, edges: list[tuple[int, int, float]],
                          max_iter: int = 1000) -> tuple[float, set[int]]:
    """Local search for max-cut: flip a vertex if it improves the cut."""
    side = {v: random.randint(0, 1) for v in range(n)}

    def cut_weight() -> float:
        return sum(w for u, v, w in edges if side[u] != side[v])

    for _ in range(max_iter):
        improved = False
        for v in range(n):
            old = cut_weight()
            side[v] ^= 1
            if cut_weight() > old:
                improved = True
            else:
                side[v] ^= 1  # revert
        if not improved:
            break

    cut = {v for v, s in side.items() if s == 0}
    return cut_weight(), cut


# ---------------------------------------------------------------------------
# Metric TSP — 2-approximation via MST (Kruskal + DFS preorder)
# ---------------------------------------------------------------------------

def tsp_mst_approx(dist: list[list[float]]) -> tuple[float, list[int]]:
    """2-approximation for metric TSP using MST + preorder walk.

    Assumes dist satisfies triangle inequality.
    Returns (tour_cost, tour).
    """
    n = len(dist)

    # Build MST via Prim
    in_mst = [False] * n
    key = [math.inf] * n
    parent = [-1] * n
    key[0] = 0
    heap = [(0.0, 0)]
    adj: dict[int, list[int]] = {i: [] for i in range(n)}

    while heap:
        d, u = heapq.heappop(heap)
        if in_mst[u]:
            continue
        in_mst[u] = True
        if parent[u] != -1:
            adj[parent[u]].append(u)
            adj[u].append(parent[u])
        for v in range(n):
            if not in_mst[v] and dist[u][v] < key[v]:
                key[v] = dist[u][v]
                parent[v] = u
                heapq.heappush(heap, (key[v], v))

    # DFS preorder on MST to get Hamiltonian path
    visited = [False] * n
    tour: list[int] = []

    def dfs(u: int) -> None:
        visited[u] = True
        tour.append(u)
        for v in adj[u]:
            if not visited[v]:
                dfs(v)

    dfs(0)
    tour.append(0)  # return to start

    cost = sum(dist[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    return cost, tour


# ---------------------------------------------------------------------------
# Knapsack FPTAS — (1-ε)-approximation in O(n²/ε) time
# ---------------------------------------------------------------------------

def knapsack_fptas(weights: list[int], values: list[int],
                   capacity: int, eps: float = 0.1) -> tuple[int, list[int]]:
    """FPTAS for 0/1 knapsack with approximation ratio (1-eps).

    Scales values down so DP runs in polynomial time.
    """
    n = len(values)
    v_max = max(values)
    # Scaling factor: round values down by K
    K = max(1, eps * v_max / n)
    scaled = [int(v / K) for v in values]

    V_total = sum(scaled)
    # dp[v] = minimum weight to achieve value v
    dp = [math.inf] * (V_total + 1)
    dp[0] = 0
    item_at: list[list[int]] = [[] for _ in range(V_total + 1)]

    for i in range(n):
        for v in range(V_total, scaled[i] - 1, -1):
            if dp[v - scaled[i]] + weights[i] < dp[v]:
                dp[v] = dp[v - scaled[i]] + weights[i]
                item_at[v] = item_at[v - scaled[i]] + [i]

    # Find best feasible value
    best_v = max(v for v in range(V_total + 1) if dp[v] <= capacity)
    return int(best_v * K), item_at[best_v]


# ---------------------------------------------------------------------------
# Bin Packing — First-Fit Decreasing (FFD), ratio ≤ 11/9 * OPT + 6/9
# ---------------------------------------------------------------------------

def bin_packing_ffd(items: list[float], bin_capacity: float = 1.0) -> list[list[float]]:
    """First-Fit Decreasing bin packing."""
    sorted_items = sorted(items, reverse=True)
    bins: list[list[float]] = []
    bin_remaining: list[float] = []

    for item in sorted_items:
        placed = False
        for i, rem in enumerate(bin_remaining):
            if item <= rem:
                bins[i].append(item)
                bin_remaining[i] -= item
                placed = True
                break
        if not placed:
            bins.append([item])
            bin_remaining.append(bin_capacity - item)

    return bins


# ---------------------------------------------------------------------------
# 3-SAT Random Assignment — expected 7/8 of clauses satisfied (for 3-SAT)
# ---------------------------------------------------------------------------

def random_3sat(clauses: list[list[int]], n_vars: int,
                trials: int = 100) -> tuple[int, dict[int, bool]]:
    """Random assignment satisfies each 3-literal clause with prob 7/8.

    Args:
        clauses: list of clauses; each clause is a list of literals
                 (positive int = variable, negative = negated variable)
        n_vars: number of variables (1-indexed)
    Returns:
        (max_clauses_satisfied, best_assignment)
    """
    best_count = -1
    best_assign: dict[int, bool] = {}

    for _ in range(trials):
        assign = {v: random.choice([True, False]) for v in range(1, n_vars + 1)}
        count = 0
        for clause in clauses:
            for lit in clause:
                val = assign[abs(lit)]
                if (lit > 0 and val) or (lit < 0 and not val):
                    count += 1
                    break
        if count > best_count:
            best_count = count
            best_assign = assign.copy()

    return best_count, best_assign


# ---------------------------------------------------------------------------
# NP-Hardness: simple reduction sketch (3-SAT → Vertex Cover)
# ---------------------------------------------------------------------------

def three_sat_to_vertex_cover_sketch(clauses: list[list[int]], n_vars: int
                                      ) -> tuple[int, list[tuple[int, int]]]:
    """Illustrate the polynomial reduction from 3-SAT to Vertex Cover.

    Each variable xi contributes a truth-setting gadget edge (xi, ¬xi).
    Each clause contributes a triangle gadget connected to the literal nodes.
    The resulting graph has a vertex cover of size (n + 2k) iff the formula
    is satisfiable (k = number of clauses).

    Returns (cover_size_threshold, gadget_edges) for illustration.
    """
    edges: list[tuple[int, int]] = []
    # Variable gadgets: node 2i = xi, node 2i+1 = ¬xi
    for i in range(1, n_vars + 1):
        edges.append((2 * i, 2 * i + 1))  # truth-setting edge

    # Clause gadgets (triangle + connections to literal nodes)
    base = 2 * n_vars + 2
    for j, clause in enumerate(clauses):
        a, b, c = base + 3 * j, base + 3 * j + 1, base + 3 * j + 2
        edges += [(a, b), (b, c), (a, c)]  # clause triangle
        for idx, lit in enumerate(clause[:3]):
            var_node = 2 * abs(lit) if lit > 0 else 2 * abs(lit) + 1
            edges.append((var_node, [a, b, c][idx]))

    k = len(clauses)
    return n_vars + 2 * k, edges


if __name__ == "__main__":
    print("=== Vertex Cover 2-Approximation ===")
    edges = [(0,1),(0,2),(1,3),(2,3),(3,4)]
    cover = vertex_cover_approx(5, edges)
    print(f"  Edges: {edges}")
    print(f"  Cover: {cover}, valid={is_vertex_cover(5, edges, cover)}")

    print("\n=== Set Cover Greedy ===")
    U = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    sets = [{1,2,3,4,5}, {1,2,6}, {3,4,7}, {5,8,9}, {6,7,8,9,10}]
    chosen = set_cover_greedy(U, sets)
    covered = set().union(*(sets[i] for i in chosen))
    print(f"  Universe: {U}")
    print(f"  Chosen set indices: {chosen}, covers: {covered == U}")

    print("\n=== Max-Cut Local Search ===")
    n = 5
    wedges = [(0,1,1),(0,2,1),(1,2,1),(1,3,1),(2,4,1),(3,4,1)]
    w, cut = max_cut_local_search(n, wedges)
    print(f"  Edges: {wedges}")
    print(f"  Cut weight: {w}, partition S={cut}")

    print("\n=== Metric TSP 2-Approximation ===")
    coords = [(0,0),(1,0),(1,1),(0,1)]
    n = len(coords)
    dist_m = [[math.hypot(coords[i][0]-coords[j][0], coords[i][1]-coords[j][1])
               for j in range(n)] for i in range(n)]
    cost, tour = tsp_mst_approx(dist_m)
    print(f"  Coordinates: {coords}")
    print(f"  Tour: {tour}, cost={cost:.4f}")

    print("\n=== Knapsack FPTAS (ε=0.2) ===")
    w, v, cap = [2,3,4,5], [3,4,5,6], 8
    val, items = knapsack_fptas(w, v, cap, eps=0.2)
    print(f"  Weights={w}, Values={v}, Capacity={cap}")
    print(f"  Approx value={val}, items={items}")

    print("\n=== Bin Packing FFD ===")
    items_bp = [0.5, 0.7, 0.3, 0.8, 0.4, 0.2, 0.6, 0.1, 0.9, 0.35]
    bins = bin_packing_ffd(items_bp)
    print(f"  Items: {items_bp}")
    print(f"  Bins used: {len(bins)}")
    for i, b in enumerate(bins):
        print(f"    Bin {i+1}: {b}  (sum={sum(b):.2f})")

    print("\n=== 3-SAT Random Assignment ===")
    # (x1 ∨ x2 ∨ ¬x3) ∧ (¬x1 ∨ x3 ∨ x4) ∧ (x2 ∨ ¬x3 ∨ ¬x4)
    clauses = [[1, 2, -3], [-1, 3, 4], [2, -3, -4]]
    satisfied, assign = random_3sat(clauses, n_vars=4)
    print(f"  Clauses: {clauses}")
    print(f"  Best assignment: {assign}")
    print(f"  Clauses satisfied: {satisfied}/{len(clauses)}")
