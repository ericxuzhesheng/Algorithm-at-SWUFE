"""Divide and Conquer Algorithms.

Covers: Merge Sort, Quick Sort, Binary Search, Strassen Matrix Multiplication,
Closest Pair of Points, Karatsuba Multiplication, Maximum Subarray.
"""

import random
import math
from typing import Optional


# ---------------------------------------------------------------------------
# Merge Sort — O(n log n)
# ---------------------------------------------------------------------------

def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list, right: list) -> list:
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# Quick Sort — O(n log n) expected, O(n^2) worst
# ---------------------------------------------------------------------------

def quick_sort(arr: list, lo: int = 0, hi: int = -1) -> None:
    """In-place quicksort with random pivot."""
    if hi == -1:
        hi = len(arr) - 1
    if lo < hi:
        p = _partition(arr, lo, hi)
        quick_sort(arr, lo, p - 1)
        quick_sort(arr, p + 1, hi)


def _partition(arr: list, lo: int, hi: int) -> int:
    pivot_idx = random.randint(lo, hi)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


# ---------------------------------------------------------------------------
# Binary Search — O(log n)
# ---------------------------------------------------------------------------

def binary_search(arr: list, target) -> int:
    """Return index of target in sorted arr, or -1 if not found."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# ---------------------------------------------------------------------------
# Strassen Matrix Multiplication — O(n^2.807)
# ---------------------------------------------------------------------------

def strassen(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """Strassen matrix multiplication. A and B must be square, size power-of-2."""
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    half = n // 2
    a11, a12, a21, a22 = _split(A, half)
    b11, b12, b21, b22 = _split(B, half)

    m1 = strassen(_add(a11, a22), _add(b11, b22))
    m2 = strassen(_add(a21, a22), b11)
    m3 = strassen(a11, _sub(b12, b22))
    m4 = strassen(a22, _sub(b21, b11))
    m5 = strassen(_add(a11, a12), b22)
    m6 = strassen(_sub(a21, a11), _add(b11, b12))
    m7 = strassen(_sub(a12, a22), _add(b21, b22))

    c11 = _add(_sub(_add(m1, m4), m5), m7)
    c12 = _add(m3, m5)
    c21 = _add(m2, m4)
    c22 = _add(_sub(_add(m1, m3), m2), m6)

    return _combine(c11, c12, c21, c22, n)


def _split(M, h):
    return ([row[:h] for row in M[:h]], [row[h:] for row in M[:h]],
            [row[:h] for row in M[h:]], [row[h:] for row in M[h:]])


def _add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _combine(c11, c12, c21, c22, n):
    h = n // 2
    return ([c11[i] + c12[i] for i in range(h)] +
            [c21[i] + c22[i] for i in range(h)])


# ---------------------------------------------------------------------------
# Closest Pair of Points — O(n log n)
# ---------------------------------------------------------------------------

Point = tuple[float, float]


def closest_pair(points: list[Point]) -> tuple[float, Point, Point]:
    """Return (min_distance, point1, point2)."""
    pts = sorted(points, key=lambda p: p[0])
    return _closest_rec(pts)


def _dist(p: Point, q: Point) -> float:
    return math.hypot(p[0] - q[0], p[1] - q[1])


def _closest_rec(pts: list[Point]) -> tuple[float, Point, Point]:
    n = len(pts)
    if n <= 3:
        return _brute_force(pts)

    mid = n // 2
    mid_x = pts[mid][0]
    dl, pl1, pl2 = _closest_rec(pts[:mid])
    dr, pr1, pr2 = _closest_rec(pts[mid:])

    if dl < dr:
        d, best = dl, (pl1, pl2)
    else:
        d, best = dr, (pr1, pr2)

    strip = [p for p in pts if abs(p[0] - mid_x) < d]
    strip.sort(key=lambda p: p[1])

    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and strip[j][1] - strip[i][1] < d:
            dd = _dist(strip[i], strip[j])
            if dd < d:
                d, best = dd, (strip[i], strip[j])
            j += 1

    return d, best[0], best[1]


def _brute_force(pts: list[Point]) -> tuple[float, Point, Point]:
    best_d = float("inf")
    best_pair = (pts[0], pts[1])
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = _dist(pts[i], pts[j])
            if d < best_d:
                best_d, best_pair = d, (pts[i], pts[j])
    return best_d, best_pair[0], best_pair[1]


# ---------------------------------------------------------------------------
# Karatsuba Integer Multiplication — O(n^1.585)
# ---------------------------------------------------------------------------

def karatsuba(x: int, y: int) -> int:
    if x < 10 or y < 10:
        return x * y
    n = max(len(str(x)), len(str(y)))
    half = n // 2
    m = 10 ** half
    a, b = divmod(x, m)
    c, d = divmod(y, m)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    ad_bc = karatsuba(a + b, c + d) - ac - bd
    return ac * m * m + ad_bc * m + bd


# ---------------------------------------------------------------------------
# Maximum Subarray (Kadane's Algorithm) — O(n)
# ---------------------------------------------------------------------------

def max_subarray(arr: list[int]) -> tuple[int, int, int]:
    """Return (max_sum, start_index, end_index)."""
    best_sum = arr[0]
    best_start = best_end = 0
    cur_sum = arr[0]
    cur_start = 0

    for i in range(1, len(arr)):
        if cur_sum + arr[i] < arr[i]:
            cur_sum = arr[i]
            cur_start = i
        else:
            cur_sum += arr[i]
        if cur_sum > best_sum:
            best_sum = cur_sum
            best_start = cur_start
            best_end = i

    return best_sum, best_start, best_end


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Merge Sort ===")
    data = [38, 27, 43, 3, 9, 82, 10]
    print(f"  Input:  {data}")
    print(f"  Output: {merge_sort(data)}")

    print("\n=== Quick Sort ===")
    data2 = [64, 25, 12, 22, 11]
    quick_sort(data2)
    print(f"  Output: {data2}")

    print("\n=== Binary Search ===")
    sorted_arr = [1, 3, 5, 7, 9, 11, 13]
    print(f"  Search 7 in {sorted_arr}: index {binary_search(sorted_arr, 7)}")
    print(f"  Search 6 in {sorted_arr}: index {binary_search(sorted_arr, 6)}")

    print("\n=== Strassen Matrix Multiplication (2x2) ===")
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    C = strassen(A, B)
    print(f"  A={A}, B={B}")
    print(f"  C=A*B={C}  (expected [[19,22],[43,50]])")

    print("\n=== Closest Pair ===")
    pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    d, p1, p2 = closest_pair(pts)
    print(f"  Points: {pts}")
    print(f"  Closest: {p1} and {p2}, distance={d:.4f}")

    print("\n=== Karatsuba ===")
    x, y = 1234, 5678
    print(f"  {x} * {y} = {karatsuba(x, y)}  (expected {x*y})")

    print("\n=== Maximum Subarray ===")
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    s, lo, hi = max_subarray(arr)
    print(f"  Array: {arr}")
    print(f"  Max sum={s}, subarray={arr[lo:hi+1]} (indices {lo}..{hi})")
