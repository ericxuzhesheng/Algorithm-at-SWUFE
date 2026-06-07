"""Greedy Algorithms.

Covers: Activity Selection, Huffman Coding, Fractional Knapsack,
Prim's MST, Kruskal's MST (Union-Find), Dijkstra's Shortest Path,
Task Scheduling (minimize maximum lateness).
"""

import heapq
from collections import defaultdict


# ---------------------------------------------------------------------------
# Activity Selection — O(n log n) if unsorted, O(n) if sorted by finish time
# ---------------------------------------------------------------------------

def activity_selection(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Select maximum number of non-overlapping activities.

    Args:
        activities: list of (start, finish) pairs
    Returns:
        list of selected (start, finish) pairs
    """
    sorted_acts = sorted(activities, key=lambda a: a[1])
    selected = [sorted_acts[0]]
    last_finish = sorted_acts[0][1]
    for s, f in sorted_acts[1:]:
        if s >= last_finish:
            selected.append((s, f))
            last_finish = f
    return selected


# ---------------------------------------------------------------------------
# Huffman Coding — O(n log n)
# ---------------------------------------------------------------------------

class HuffmanNode:
    def __init__(self, char: str, freq: int,
                 left: "HuffmanNode | None" = None,
                 right: "HuffmanNode | None" = None) -> None:
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: "HuffmanNode") -> bool:
        return self.freq < other.freq


def huffman_coding(freq_map: dict[str, int]) -> dict[str, str]:
    """Return character -> binary code mapping."""
    heap = [HuffmanNode(c, f) for c, f in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode("", left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    root = heap[0]
    codes: dict[str, str] = {}

    def _traverse(node: HuffmanNode, code: str) -> None:
        if node.left is None and node.right is None:
            codes[node.char] = code or "0"
            return
        if node.left:
            _traverse(node.left, code + "0")
        if node.right:
            _traverse(node.right, code + "1")

    _traverse(root, "")
    return codes


# ---------------------------------------------------------------------------
# Fractional Knapsack — O(n log n)
# ---------------------------------------------------------------------------

def fractional_knapsack(items: list[tuple[float, float]], capacity: float) -> float:
    """Return maximum value for fractional knapsack.

    Args:
        items: list of (weight, value)
        capacity: knapsack capacity
    Returns:
        maximum achievable value
    """
    sorted_items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)
    total_value = 0.0
    remaining = capacity
    for w, v in sorted_items:
        if remaining <= 0:
            break
        take = min(w, remaining)
        total_value += take * (v / w)
        remaining -= take
    return total_value


# ---------------------------------------------------------------------------
# Prim's Minimum Spanning Tree — O((V+E) log V) with binary heap
# ---------------------------------------------------------------------------

def prim_mst(graph: dict[int, list[tuple[int, float]]]) -> tuple[float, list[tuple]]:
    """Compute MST using Prim's algorithm.

    Args:
        graph: adjacency list {node: [(neighbor, weight), ...]}
    Returns:
        (total_weight, list of (u, v, weight) edges in MST)
    """
    if not graph:
        return 0.0, []

    start = next(iter(graph))
    visited = {start}
    edges_in_mst = []
    total = 0.0
    # heap: (weight, u, v)
    heap = [(w, start, v) for v, w in graph[start]]
    heapq.heapify(heap)

    while heap and len(visited) < len(graph):
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        edges_in_mst.append((u, v, w))
        total += w
        for neighbor, weight in graph.get(v, []):
            if neighbor not in visited:
                heapq.heappush(heap, (weight, v, neighbor))

    return total, edges_in_mst


# ---------------------------------------------------------------------------
# Kruskal's Minimum Spanning Tree — O(E log E) with Union-Find
# ---------------------------------------------------------------------------

class _UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal_mst(n: int, edges: list[tuple[int, int, float]]) -> tuple[float, list[tuple]]:
    """Compute MST using Kruskal's algorithm.

    Args:
        n: number of vertices (0-indexed)
        edges: list of (u, v, weight)
    Returns:
        (total_weight, list of edges in MST)
    """
    uf = _UnionFind(n)
    sorted_edges = sorted(edges, key=lambda e: e[2])
    mst_edges = []
    total = 0.0
    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total += w
            if len(mst_edges) == n - 1:
                break
    return total, mst_edges


# ---------------------------------------------------------------------------
# Dijkstra's Shortest Path — O((V+E) log V)
# ---------------------------------------------------------------------------

def dijkstra(graph: dict[int, list[tuple[int, float]]], source: int
             ) -> dict[int, float]:
    """Return shortest distances from source to all reachable vertices."""
    dist: dict[int, float] = defaultdict(lambda: float("inf"))
    dist[source] = 0.0
    heap = [(0.0, source)]
    visited: set[int] = set()

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        for v, w in graph.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))

    return dict(dist)


# ---------------------------------------------------------------------------
# Task Scheduling: Minimize Maximum Lateness — O(n log n)
# ---------------------------------------------------------------------------

def minimize_max_lateness(tasks: list[tuple[int, int]]) -> tuple[int, list[int]]:
    """Schedule tasks to minimize maximum lateness.

    Args:
        tasks: list of (processing_time, deadline)
    Returns:
        (max_lateness, order of task indices)
    """
    indexed = sorted(enumerate(tasks), key=lambda x: x[1][1])  # sort by deadline
    time = 0
    max_lateness = 0
    order = []
    for orig_idx, (p, d) in indexed:
        time += p
        lateness = max(0, time - d)
        max_lateness = max(max_lateness, lateness)
        order.append(orig_idx)
    return max_lateness, order


if __name__ == "__main__":
    print("=== Activity Selection ===")
    acts = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    selected = activity_selection(acts)
    print(f"  Selected {len(selected)} activities: {selected}")

    print("\n=== Huffman Coding ===")
    freq = {"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}
    codes = huffman_coding(freq)
    total_bits = sum(freq[c] * len(code) for c, code in codes.items())
    print(f"  Frequencies: {freq}")
    for c, code in sorted(codes.items()):
        print(f"  '{c}' (freq={freq[c]}): {code}")
    print(f"  Total bits: {total_bits} (fixed-3-bit would be {sum(freq.values())*3})")

    print("\n=== Fractional Knapsack ===")
    items = [(10, 60), (20, 100), (30, 120)]  # (weight, value)
    cap = 50
    val = fractional_knapsack(items, cap)
    print(f"  Items (w,v): {items}, capacity={cap}")
    print(f"  Max value: {val:.2f}")

    print("\n=== Prim's MST ===")
    g = {
        0: [(1, 2), (3, 6)],
        1: [(0, 2), (2, 3), (3, 8), (4, 5)],
        2: [(1, 3), (4, 7)],
        3: [(0, 6), (1, 8), (4, 9)],
        4: [(1, 5), (2, 7), (3, 9)],
    }
    total, mst = prim_mst(g)
    print(f"  MST weight={total}, edges={mst}")

    print("\n=== Kruskal's MST ===")
    edges = [(0,1,2),(0,3,6),(1,2,3),(1,3,8),(1,4,5),(2,4,7),(3,4,9)]
    total, mst = kruskal_mst(5, edges)
    print(f"  MST weight={total}, edges={mst}")

    print("\n=== Dijkstra's Shortest Path ===")
    dg = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: [],
    }
    dists = dijkstra(dg, 0)
    print(f"  Shortest from 0: {dict(sorted(dists.items()))}")

    print("\n=== Minimize Maximum Lateness ===")
    tasks = [(3, 6), (2, 9), (1, 8), (4, 9), (3, 14), (2, 15)]
    lateness, order = minimize_max_lateness(tasks)
    print(f"  Tasks (p,d): {tasks}")
    print(f"  Schedule order (indices): {order}, max lateness={lateness}")
