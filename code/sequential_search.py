"""Sequential Search Algorithms and Self-Organizing Structures.

Covers: Basic sequential search, sentinel search, self-organizing search
(move-to-front and transposition rules), skip list.
"""

import random
import math
from typing import Optional, Any


# ---------------------------------------------------------------------------
# Basic Sequential Search — O(n)
# ---------------------------------------------------------------------------

def sequential_search(arr: list, target) -> int:
    """Return first index of target, or -1."""
    for i, x in enumerate(arr):
        if x == target:
            return i
    return -1


# ---------------------------------------------------------------------------
# Sentinel Search — O(n), ~50% fewer branch instructions
# ---------------------------------------------------------------------------

def sentinel_search(arr: list, target) -> int:
    """Append sentinel to avoid bounds check inside loop."""
    arr_copy = list(arr) + [target]
    i = 0
    while arr_copy[i] != target:
        i += 1
    return i if i < len(arr) else -1


# ---------------------------------------------------------------------------
# Self-Organizing Search: Move-to-Front
# ---------------------------------------------------------------------------

class MoveToFrontList:
    """Sequential search with move-to-front heuristic.

    After a successful search, the found element is moved to position 0.
    Competitive ratio vs static optimal: 2.
    """

    def __init__(self, items: list) -> None:
        self._data = list(items)

    def search(self, target) -> int:
        """Return position where target was found (before moving), or -1."""
        for i, x in enumerate(self._data):
            if x == target:
                self._data.pop(i)
                self._data.insert(0, x)
                return i
        return -1

    @property
    def data(self) -> list:
        return list(self._data)


# ---------------------------------------------------------------------------
# Self-Organizing Search: Transposition Rule
# ---------------------------------------------------------------------------

class TranspositionList:
    """Sequential search with transposition heuristic.

    After a successful search at position i, swap A[i] with A[i-1].
    Converges to frequency-sorted order more slowly but with less disruption.
    """

    def __init__(self, items: list) -> None:
        self._data = list(items)

    def search(self, target) -> int:
        for i, x in enumerate(self._data):
            if x == target:
                if i > 0:
                    self._data[i], self._data[i - 1] = self._data[i - 1], self._data[i]
                return i
        return -1

    @property
    def data(self) -> list:
        return list(self._data)


# ---------------------------------------------------------------------------
# Skip List — O(log n) expected for search/insert/delete
# ---------------------------------------------------------------------------

class _SkipNode:
    def __init__(self, key, level: int) -> None:
        self.key = key
        self.forward: list[Optional["_SkipNode"]] = [None] * (level + 1)


class SkipList:
    """Probabilistic data structure supporting O(log n) expected operations."""

    MAX_LEVEL = 16
    P = 0.5

    def __init__(self) -> None:
        self._header = _SkipNode(float("-inf"), self.MAX_LEVEL)
        self._level = 0

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def search(self, key) -> bool:
        cur = self._header
        for i in range(self._level, -1, -1):
            while cur.forward[i] and cur.forward[i].key < key:
                cur = cur.forward[i]
        cur = cur.forward[0]
        return cur is not None and cur.key == key

    def insert(self, key) -> None:
        update = [None] * (self.MAX_LEVEL + 1)
        cur = self._header
        for i in range(self._level, -1, -1):
            while cur.forward[i] and cur.forward[i].key < key:
                cur = cur.forward[i]
            update[i] = cur

        new_level = self._random_level()
        if new_level > self._level:
            for i in range(self._level + 1, new_level + 1):
                update[i] = self._header
            self._level = new_level

        node = _SkipNode(key, new_level)
        for i in range(new_level + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def delete(self, key) -> bool:
        update = [None] * (self.MAX_LEVEL + 1)
        cur = self._header
        for i in range(self._level, -1, -1):
            while cur.forward[i] and cur.forward[i].key < key:
                cur = cur.forward[i]
            update[i] = cur

        target = cur.forward[0]
        if target is None or target.key != key:
            return False

        for i in range(self._level + 1):
            if update[i].forward[i] != target:
                break
            update[i].forward[i] = target.forward[i]

        while self._level > 0 and self._header.forward[self._level] is None:
            self._level -= 1
        return True

    def to_list(self) -> list:
        result = []
        cur = self._header.forward[0]
        while cur:
            result.append(cur.key)
            cur = cur.forward[0]
        return result


if __name__ == "__main__":
    data = [5, 3, 8, 1, 9, 2, 7, 4, 6, 10]

    print("=== Basic Sequential Search ===")
    print(f"  Array: {data}")
    print(f"  Search 7: index {sequential_search(data, 7)}")
    print(f"  Search 99: index {sequential_search(data, 99)}")

    print("\n=== Sentinel Search ===")
    print(f"  Search 9: index {sentinel_search(data, 9)}")
    print(f"  Search 0: index {sentinel_search(data, 0)}")

    print("\n=== Move-to-Front Self-Organizing List ===")
    mtf = MoveToFrontList(list(range(1, 6)))
    print(f"  Initial: {mtf.data}")
    for target in [5, 5, 3, 5, 1]:
        pos = mtf.search(target)
        print(f"  Search {target} at pos {pos} -> list: {mtf.data}")

    print("\n=== Transposition Self-Organizing List ===")
    trl = TranspositionList(list(range(1, 6)))
    print(f"  Initial: {trl.data}")
    for target in [5, 5, 5, 4]:
        pos = trl.search(target)
        print(f"  Search {target} at pos {pos} -> list: {trl.data}")

    print("\n=== Skip List ===")
    sl = SkipList()
    for v in [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]:
        sl.insert(v)
    print(f"  Inserted: {sl.to_list()}")
    print(f"  Search 19: {sl.search(19)}")
    print(f"  Search 15: {sl.search(15)}")
    sl.delete(19)
    print(f"  After delete 19: {sl.to_list()}")
