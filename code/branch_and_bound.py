"""Branch and Bound Algorithms.

Covers: Generic B&B framework, TSP (Branch and Bound),
0/1 Knapsack (B&B with upper-bound pruning),
Assignment Problem (Hungarian-style B&B), Minimize-Cost B&B.
"""

import heapq
import math
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Generic Branch-and-Bound Framework (maximization, best-first)
# ---------------------------------------------------------------------------

@dataclass(order=True)
class BBNode:
    priority: float          # negative upper bound for min-heap (maximization)
    data: Any = field(compare=False)


class BranchAndBound:
    """Abstract best-first B&B solver.

    Subclass and implement: upper_bound(), is_leaf(), branch(), value().
    """

    def solve(self, root_data) -> tuple[float, Any]:
        best_val = -math.inf
        best_data = None
        heap: list[BBNode] = []

        root_ub = self.upper_bound(root_data)
        heapq.heappush(heap, BBNode(-root_ub, root_data))

        while heap:
            node = heapq.heappop(heap)
            ub = -node.priority

            if ub <= best_val:
                continue  # prune

            if self.is_leaf(node.data):
                v = self.value(node.data)
                if v > best_val:
                    best_val = v
                    best_data = node.data
                continue

            for child in self.branch(node.data):
                child_ub = self.upper_bound(child)
                if child_ub > best_val:
                    heapq.heappush(heap, BBNode(-child_ub, child))

        return best_val, best_data

    def upper_bound(self, data) -> float:
        raise NotImplementedError

    def is_leaf(self, data) -> bool:
        raise NotImplementedError

    def branch(self, data) -> list:
        raise NotImplementedError

    def value(self, data) -> float:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# 0/1 Knapsack via Branch and Bound
# ---------------------------------------------------------------------------

def knapsack_bb(weights: list[int], values: list[int], capacity: int) -> tuple[int, list[int]]:
    """Solve 0/1 knapsack using best-first B&B.

    Returns (max_value, selected_item_indices).
    """
    n = len(weights)
    # Sort by value density descending for tighter upper bounds
    order = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    w = [weights[i] for i in order]
    v = [values[i] for i in order]

    def fractional_ub(level: int, cur_val: int, cur_wt: int) -> float:
        ub = cur_val
        rem = capacity - cur_wt
        for i in range(level, n):
            if w[i] <= rem:
                ub += v[i]
                rem -= w[i]
            else:
                ub += v[i] * rem / w[i]
                break
        return ub

    # State: (level, current_value, current_weight, included_items_sorted_indices)
    best_val = [0]
    best_items: list[list[int]] = [[]]

    # heap: (-upper_bound, level, cur_val, cur_wt, items_list)
    heap: list[tuple] = []
    root_ub = fractional_ub(0, 0, 0)
    heapq.heappush(heap, (-root_ub, 0, 0, 0, []))

    while heap:
        neg_ub, level, cur_val, cur_wt, items = heapq.heappop(heap)
        ub = -neg_ub

        if ub <= best_val[0] or level >= n:
            if cur_val > best_val[0]:
                best_val[0] = cur_val
                best_items[0] = items
            continue

        # Branch: include item at level
        if cur_wt + w[level] <= capacity:
            new_val = cur_val + v[level]
            new_wt = cur_wt + w[level]
            new_items = items + [order[level]]
            new_ub = fractional_ub(level + 1, new_val, new_wt)
            if new_ub > best_val[0]:
                heapq.heappush(heap, (-new_ub, level + 1, new_val, new_wt, new_items))

        # Branch: exclude item at level
        excl_ub = fractional_ub(level + 1, cur_val, cur_wt)
        if excl_ub > best_val[0]:
            heapq.heappush(heap, (-excl_ub, level + 1, cur_val, cur_wt, items))

    return best_val[0], sorted(best_items[0])


# ---------------------------------------------------------------------------
# TSP — Branch and Bound with row/column reduction lower bound
# ---------------------------------------------------------------------------

def tsp_bb(dist: list[list[float]]) -> tuple[float, list[int]]:
    """Find shortest Hamiltonian cycle via Branch and Bound.

    Args:
        dist: n×n distance matrix (use math.inf for no direct edge)
    Returns:
        (min_tour_cost, tour as list of vertex indices starting and ending at 0)
    """
    n = len(dist)
    INF = math.inf

    def reduce_matrix(mat: list[list[float]]) -> tuple[list[list[float]], float]:
        """Reduce matrix and return (reduced_mat, reduction_cost)."""
        import copy
        m = [row[:] for row in mat]
        cost = 0.0
        for i in range(n):
            row_min = min(m[i])
            if row_min not in (0, INF):
                cost += row_min
                m[i] = [x - row_min for x in m[i]]
        for j in range(n):
            col_min = min(m[i][j] for i in range(n))
            if col_min not in (0, INF):
                cost += col_min
                for i in range(n):
                    m[i][j] -= col_min
        return m, cost

    reduced, lb = reduce_matrix([row[:] for row in dist])

    # heap: (lower_bound, path, reduced_matrix)
    heap: list[tuple] = []
    heapq.heappush(heap, (lb, [0], reduced))

    best_cost = INF
    best_path: list[int] = []

    while heap:
        cost, path, mat = heapq.heappop(heap)
        if cost >= best_cost:
            continue

        if len(path) == n:
            total = cost + dist[path[-1]][path[0]]
            if total < best_cost:
                best_cost = total
                best_path = path + [path[0]]
            continue

        u = path[-1]
        for v in range(n):
            if v in path:
                continue
            if mat[u][v] == INF:
                continue

            new_mat = [row[:] for row in mat]
            # Set row u and col v to INF
            for k in range(n):
                new_mat[u][k] = INF
                new_mat[k][v] = INF
            # Prevent sub-tour: block (v, path[0]) unless this is the last step
            if len(path) < n - 1:
                new_mat[v][path[0]] = INF

            new_mat, reduction = reduce_matrix(new_mat)
            new_cost = cost + mat[u][v] + reduction

            if new_cost < best_cost:
                heapq.heappush(heap, (new_cost, path + [v], new_mat))

    return best_cost, best_path


# ---------------------------------------------------------------------------
# Assignment Problem — minimize total cost (B&B with row-min lower bound)
# ---------------------------------------------------------------------------

def assignment_bb(cost: list[list[float]]) -> tuple[float, list[int]]:
    """Solve assignment problem (minimize total assignment cost).

    Args:
        cost: n×n cost matrix
    Returns:
        (min_total_cost, assignment[i] = job assigned to worker i)
    """
    n = len(cost)
    INF = math.inf

    def lower_bound(worker: int, assigned_jobs: set[int], cur_cost: float) -> float:
        lb = cur_cost
        for i in range(worker, n):
            row_min = min(cost[i][j] for j in range(n) if j not in assigned_jobs)
            lb += row_min
        return lb

    best_cost = [INF]
    best_assignment: list[list[int]] = [[]]

    # heap: (lb, worker_idx, current_cost, assignment_so_far, assigned_jobs_set_as_tuple)
    heap: list[tuple] = []
    init_lb = lower_bound(0, set(), 0.0)
    heapq.heappush(heap, (init_lb, 0, 0.0, [], ()))

    while heap:
        lb, worker, cur_cost, assignment, assigned_tuple = heapq.heappop(heap)
        assigned_jobs = set(assigned_tuple)

        if lb >= best_cost[0]:
            continue

        if worker == n:
            if cur_cost < best_cost[0]:
                best_cost[0] = cur_cost
                best_assignment[0] = assignment[:]
            continue

        for job in range(n):
            if job in assigned_jobs:
                continue
            new_cost = cur_cost + cost[worker][job]
            new_assigned = assigned_jobs | {job}
            new_lb = lower_bound(worker + 1, new_assigned, new_cost)
            if new_lb < best_cost[0]:
                heapq.heappush(heap, (
                    new_lb, worker + 1, new_cost,
                    assignment + [job], tuple(sorted(new_assigned))
                ))

    return best_cost[0], best_assignment[0]


if __name__ == "__main__":
    print("=== 0/1 Knapsack via B&B ===")
    weights = [2, 3, 4, 5]
    values  = [3, 4, 5, 6]
    cap = 8
    val, items = knapsack_bb(weights, values, cap)
    print(f"  Weights={weights}, Values={values}, Capacity={cap}")
    print(f"  Optimal value={val}, Items selected (0-indexed)={items}")

    print("\n=== TSP via B&B ===")
    INF = math.inf
    dist = [
        [INF,  10,   8,   9,   7],
        [ 10, INF,  10,   5,   6],
        [  8,  10, INF,   8,   9],
        [  9,   5,   8, INF,   6],
        [  7,   6,   9,   6, INF],
    ]
    tour_cost, tour = tsp_bb(dist)
    print(f"  Min TSP cost: {tour_cost}")
    print(f"  Tour: {' -> '.join(map(str, tour))}")

    print("\n=== Assignment Problem via B&B ===")
    cost_matrix = [
        [9,  2,  7,  8],
        [6,  4,  3,  7],
        [5,  8,  1,  8],
        [7,  6,  9,  4],
    ]
    total, assignment = assignment_bb(cost_matrix)
    print(f"  Cost matrix:")
    for row in cost_matrix:
        print(f"    {row}")
    print(f"  Min total cost: {total}")
    print(f"  Assignment: worker i -> job {assignment}")
    for i, j in enumerate(assignment):
        print(f"    Worker {i} -> Job {j} (cost={cost_matrix[i][j]})")
