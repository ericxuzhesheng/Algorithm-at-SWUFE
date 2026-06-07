"""Mathematical Foundations for Algorithm Analysis.

Covers: Master Theorem solver, recursion tree simulation,
asymptotic notation helpers, common growth rate comparisons.
"""

import math
from enum import Enum


class MasterCase(Enum):
    CASE1 = 1
    CASE2 = 2
    CASE3 = 3
    NOT_APPLICABLE = 0


def master_theorem(a: int, b: int, k: float, p: float = 0) -> tuple[MasterCase, str]:
    """Solve T(n) = a*T(n/b) + Theta(n^k * log^p(n)) via Master Theorem.

    Args:
        a: number of sub-problems
        b: size reduction factor
        k: polynomial exponent of f(n)
        p: log exponent of f(n) (default 0)

    Returns:
        (case, solution_string)
    """
    if a < 1 or b <= 1:
        return MasterCase.NOT_APPLICABLE, "Invalid parameters: a>=1, b>1 required"

    c_star = math.log(a, b)  # critical exponent log_b(a)

    if k < c_star:
        sol = f"Theta(n^{c_star:.4g})"
        return MasterCase.CASE1, sol
    elif math.isclose(k, c_star, rel_tol=1e-9):
        if p > -1:
            sol = f"Theta(n^{k:.4g} * log^{p+1:.4g}(n))"
        elif math.isclose(p, -1, rel_tol=1e-9):
            sol = f"Theta(n^{k:.4g} * log(log(n)))"
        else:
            sol = f"Theta(n^{k:.4g})"
        return MasterCase.CASE2, sol
    else:  # k > c_star
        sol = f"Theta(n^{k:.4g} * log^{p:.4g}(n))" if p != 0 else f"Theta(n^{k:.4g})"
        return MasterCase.CASE3, sol


def recursion_tree_cost(a: int, b: int, f_cost_at_n: float, n: int) -> float:
    """Simulate total work done by a recursion tree T(n)=aT(n/b)+f(n).

    Args:
        a: branching factor
        b: problem size reduction
        f_cost_at_n: work per node at size n (O(n^k) evaluated at n)
        n: problem size

    Returns:
        approximate total work (floating point)
    """
    total = 0.0
    level_size = n
    num_nodes = 1
    while level_size >= 1:
        total += num_nodes * (level_size / n * f_cost_at_n)
        level_size /= b
        num_nodes *= a
    return total


def big_o_compare(n: int) -> dict[str, float]:
    """Evaluate common complexity functions at n for comparison."""
    return {
        "1 (constant)":     1,
        "log(n)":           math.log2(n),
        "sqrt(n)":          math.sqrt(n),
        "n":                n,
        "n*log(n)":         n * math.log2(n),
        "n^2":              n ** 2,
        "n^3":              n ** 3,
        "2^n":              2 ** n if n <= 60 else float("inf"),
        "n!":               math.factorial(n) if n <= 20 else float("inf"),
    }


def geometric_series_sum(ratio: float, terms: int) -> float:
    """Sum a geometric series: 1 + r + r^2 + ... + r^(terms-1)."""
    if math.isclose(ratio, 1.0):
        return float(terms)
    return (1 - ratio ** terms) / (1 - ratio)


if __name__ == "__main__":
    print("=" * 60)
    print("Master Theorem Examples")
    print("=" * 60)

    examples = [
        (2, 2, 1, 0, "Merge Sort: T(n)=2T(n/2)+n"),
        (1, 2, 0, 0, "Binary Search: T(n)=T(n/2)+1"),
        (4, 2, 2, 0, "T(n)=4T(n/2)+n^2"),
        (3, 3, 1, 1, "T(n)=3T(n/3)+n*log(n)"),
        (8, 2, 2, 0, "Strassen-like: T(n)=8T(n/2)+n^2"),
        (7, 2, 2, 0, "Strassen: T(n)=7T(n/2)+n^2"),
    ]

    for a, b, k, p, desc in examples:
        case, solution = master_theorem(a, b, k, p)
        print(f"\n{desc}")
        print(f"  log_{b}({a}) = {math.log(a, b):.4g}, f(n)=n^{k}*log^{p}(n)")
        print(f"  -> {case.name}: T(n) = {solution}")

    print("\n" + "=" * 60)
    print("Growth Rate Comparison at n=20")
    print("=" * 60)
    rates = big_o_compare(20)
    for name, val in rates.items():
        val_str = f"{val:.2e}" if val != float("inf") else "inf"
        print(f"  {name:<20}: {val_str}")
