"""Selection Algorithms — Finding the k-th Smallest Element.

Covers: Randomized QuickSelect (O(n) expected),
Median of Medians (O(n) worst-case deterministic).
"""

import random
from typing import TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Randomized QuickSelect — O(n) expected
# ---------------------------------------------------------------------------

def quickselect(arr: list, k: int) -> object:
    """Return the k-th smallest element (1-indexed) using randomized pivot.

    Expected O(n), worst-case O(n^2).
    """
    if len(arr) == 0 or k < 1 or k > len(arr):
        raise ValueError("k out of range")
    return _quickselect(list(arr), 0, len(arr) - 1, k - 1)


def _quickselect(arr: list, lo: int, hi: int, k: int) -> object:
    if lo == hi:
        return arr[lo]
    pivot_idx = random.randint(lo, hi)
    pivot_idx = _partition(arr, lo, hi, pivot_idx)
    if k == pivot_idx:
        return arr[pivot_idx]
    elif k < pivot_idx:
        return _quickselect(arr, lo, pivot_idx - 1, k)
    else:
        return _quickselect(arr, pivot_idx + 1, hi, k)


def _partition(arr: list, lo: int, hi: int, pivot_idx: int) -> int:
    pivot = arr[pivot_idx]
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    store = lo
    for i in range(lo, hi):
        if arr[i] < pivot:
            arr[store], arr[i] = arr[i], arr[store]
            store += 1
    arr[store], arr[hi] = arr[hi], arr[store]
    return store


# ---------------------------------------------------------------------------
# Median of Medians — O(n) worst-case
# ---------------------------------------------------------------------------

def median_of_medians(arr: list, k: int) -> object:
    """Return the k-th smallest element (1-indexed) in deterministic O(n).

    Uses groups of 5 and recursive median-of-medians pivot selection.
    """
    if len(arr) == 0 or k < 1 or k > len(arr):
        raise ValueError("k out of range")
    return _mom_select(list(arr), k - 1)


def _mom_select(arr: list, k: int) -> object:
    if len(arr) <= 5:
        return sorted(arr)[k]

    # Split into groups of 5, find each group's median
    chunks = [arr[i:i + 5] for i in range(0, len(arr), 5)]
    medians = [sorted(chunk)[len(chunk) // 2] for chunk in chunks]

    # Recursively find median of medians
    pivot = _mom_select(medians, len(medians) // 2)

    low = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    high = [x for x in arr if x > pivot]

    if k < len(low):
        return _mom_select(low, k)
    elif k < len(low) + len(equal):
        return pivot
    else:
        return _mom_select(high, k - len(low) - len(equal))


# ---------------------------------------------------------------------------
# Order Statistics: minimum, maximum, simultaneous min-max
# ---------------------------------------------------------------------------

def find_minimum(arr: list) -> object:
    """Find minimum with n-1 comparisons."""
    m = arr[0]
    for x in arr[1:]:
        if x < m:
            m = x
    return m


def find_maximum(arr: list) -> object:
    m = arr[0]
    for x in arr[1:]:
        if x > m:
            m = x
    return m


def simultaneous_min_max(arr: list) -> tuple:
    """Find both min and max using floor(3n/2)-2 comparisons."""
    if len(arr) == 1:
        return arr[0], arr[0]

    if arr[0] < arr[1]:
        mn, mx = arr[0], arr[1]
    else:
        mn, mx = arr[1], arr[0]

    # Process remaining elements in pairs
    i = 2
    while i + 1 < len(arr):
        if arr[i] < arr[i + 1]:
            smaller, larger = arr[i], arr[i + 1]
        else:
            smaller, larger = arr[i + 1], arr[i]
        if smaller < mn:
            mn = smaller
        if larger > mx:
            mx = larger
        i += 2

    if i < len(arr):  # odd element remaining
        if arr[i] < mn:
            mn = arr[i]
        if arr[i] > mx:
            mx = arr[i]

    return mn, mx


if __name__ == "__main__":
    data = [7, 10, 4, 3, 20, 15, 1, 8, 12, 6]
    print("Array:", data)
    print()

    print("=== Randomized QuickSelect ===")
    for k in [1, 3, 5, 7, 10]:
        result = quickselect(data, k)
        expected = sorted(data)[k - 1]
        print(f"  k={k:2d}: {result}  (expected {expected})")

    print("\n=== Median of Medians ===")
    for k in [1, 3, 5, 7, 10]:
        result = median_of_medians(data, k)
        expected = sorted(data)[k - 1]
        print(f"  k={k:2d}: {result}  (expected {expected})")

    print("\n=== Simultaneous Min-Max ===")
    mn, mx = simultaneous_min_max(data)
    print(f"  Min={mn}, Max={mx}  (expected {min(data)}, {max(data)})")
