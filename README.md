# 西南财经大学算法学 | Algorithm Design and Analysis at SWUFE

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/LaTeX-source-008080?style=flat-square&logo=latex&logoColor=white" alt="LaTeX" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License" />
</p>

<p align="center">
  <a href="#chinese">中文</a> · <a href="#english">English</a>
</p>

---

<a id="chinese"></a>

## 中文

本仓库整合了**西南财经大学《算法设计与分析》课程**的全套学习资料，包括英文命名的讲义 PDF、LaTeX 格式的课后作业源文件，以及课程中所有核心算法的 Python 实现。

## 仓库结构

```
.
├── slides/
│   ├── Lecture01-Algorithm_Introduction.pdf
│   ├── Lecture02-NP_Hard_Problems_Supplement.pdf
│   ├── Lecture03-Mathematical_Foundations.pdf
│   ├── Lecture04_05-Divide_and_Conquer_1_2.pdf
│   ├── Lecture06-Divide_and_Conquer_3.pdf
│   ├── Lecture07_08-Dynamic_Programming_1_2.pdf
│   ├── Lecture09-Dynamic_Programming_3.pdf
│   ├── Lecture10_11_12-Greedy_Algorithm_1_2_3.pdf
│   ├── Lecture13_14_15-Backtracking_and_Branch_Bound_1_2_3.pdf
│   └── Lecture16-Deep_Learning_Basics_Part1.pdf
├── hw/
│   ├── Recurrence_Equation.{pdf,tex}
│   ├── General_Selection_Problem.{pdf,tex}
│   ├── Improved_Sequential_Search_Algorithm.{pdf,tex}
│   ├── Dynamic_Programming.{pdf,tex}
│   ├── Branch_and_bound.{pdf,tex}
│   └── Minimize_Cost_by_Branch_and_Bound.{pdf,tex}
└── code/
    ├── math_foundations.py
    ├── divide_and_conquer.py
    ├── selection.py
    ├── sequential_search.py
    ├── dynamic_programming.py
    ├── greedy.py
    ├── backtracking.py
    └── branch_and_bound.py
```

## 课程模块

| # | 主题 | 讲义 | Python 实现 |
|---|------|------|------------|
| 1 | 算法介绍 | [Lecture01](slides/Lecture01-Algorithm_Introduction.pdf) | — |
| 2 | NP-hard 问题补充 | [Lecture02](slides/Lecture02-NP_Hard_Problems_Supplement.pdf) | — |
| 3 | 数学基础 | [Lecture03](slides/Lecture03-Mathematical_Foundations.pdf) | [math_foundations.py](code/math_foundations.py) |
| 4–5 | 分治策略（一、二）| [Lecture04\_05](slides/Lecture04_05-Divide_and_Conquer_1_2.pdf) | [divide\_and\_conquer.py](code/divide_and_conquer.py) |
| 6 | 分治策略（三）| [Lecture06](slides/Lecture06-Divide_and_Conquer_3.pdf) | [selection.py](code/selection.py) · [sequential\_search.py](code/sequential_search.py) |
| 7–8 | 动态规划（一、二）| [Lecture07\_08](slides/Lecture07_08-Dynamic_Programming_1_2.pdf) | [dynamic\_programming.py](code/dynamic_programming.py) |
| 9 | 动态规划（三）| [Lecture09](slides/Lecture09-Dynamic_Programming_3.pdf) | [dynamic\_programming.py](code/dynamic_programming.py) |
| 10–12 | 贪心算法（一、二、三）| [Lecture10\_11\_12](slides/Lecture10_11_12-Greedy_Algorithm_1_2_3.pdf) | [greedy.py](code/greedy.py) |
| 13–15 | 回溯与分支限界（一、二、三）| [Lecture13\_14\_15](slides/Lecture13_14_15-Backtracking_and_Branch_Bound_1_2_3.pdf) | [backtracking.py](code/backtracking.py) · [branch\_and\_bound.py](code/branch_and_bound.py) |
| 16 | 深度学习基础（一）| [Lecture16](slides/Lecture16-Deep_Learning_Basics_Part1.pdf) | — |

## 作业说明

| 文件 | 主题 | 方法 |
|------|------|------|
| [Recurrence\_Equation](hw/Recurrence_Equation.tex) | 递推方程与主定理 | 主定理三种情况、递推树 |
| [General\_Selection\_Problem](hw/General_Selection_Problem.tex) | 一般选择问题 | QuickSelect、中位数的中位数 |
| [Improved\_Sequential\_Search](hw/Improved_Sequential_Search_Algorithm.tex) | 改进顺序搜索 | 哨兵、自组织搜索 |
| [Dynamic\_Programming](hw/Dynamic_Programming.tex) | 动态规划 | 背包、LCS、矩阵链 |
| [Branch\_and\_bound](hw/Branch_and_bound.tex) | 分支限界法 | 优先队列 B&B、上界剪枝 |
| [Minimize\_Cost\_by\_B&B](hw/Minimize_Cost_by_Branch_and_Bound.tex) | 分支限界最小化代价 | 任务分配问题 |

## 快速开始

```bash
git clone https://github.com/ericxuzhesheng/Algorithm-at-SWUFE.git
cd Algorithm-at-SWUFE

# 运行任意算法文件
python code/dynamic_programming.py
python code/branch_and_bound.py

# 编译 LaTeX 作业
pdflatex hw/Dynamic_Programming.tex
```

---

<a id="english"></a>

## Overview

Course materials for **Algorithm Design and Analysis** at [Southwestern University of Finance and Economics (SWUFE)](https://www.swufe.edu.cn/). The repository includes English-renamed lecture slides, LaTeX homework source files, and Python implementations of every major algorithm covered across the 16-lecture course.

## Repository Structure

```
.
├── slides/          # Lecture PDFs (English-named, Lecture01–16)
├── hw/              # Homework PDFs + LaTeX source files
└── code/            # Python algorithm implementations
```

## Course Modules

| # | Topic | Slides | Python |
|---|-------|--------|--------|
| 1 | Algorithm Introduction | [Lecture01](slides/Lecture01-Algorithm_Introduction.pdf) | — |
| 2 | NP-Hard Problems (Supplement) | [Lecture02](slides/Lecture02-NP_Hard_Problems_Supplement.pdf) | — |
| 3 | Mathematical Foundations | [Lecture03](slides/Lecture03-Mathematical_Foundations.pdf) | [math_foundations.py](code/math_foundations.py) |
| 4–5 | Divide and Conquer I & II | [Lecture04\_05](slides/Lecture04_05-Divide_and_Conquer_1_2.pdf) | [divide\_and\_conquer.py](code/divide_and_conquer.py) |
| 6 | Divide and Conquer III | [Lecture06](slides/Lecture06-Divide_and_Conquer_3.pdf) | [selection.py](code/selection.py) · [sequential\_search.py](code/sequential_search.py) |
| 7–8 | Dynamic Programming I & II | [Lecture07\_08](slides/Lecture07_08-Dynamic_Programming_1_2.pdf) | [dynamic\_programming.py](code/dynamic_programming.py) |
| 9 | Dynamic Programming III | [Lecture09](slides/Lecture09-Dynamic_Programming_3.pdf) | [dynamic\_programming.py](code/dynamic_programming.py) |
| 10–12 | Greedy Algorithm I, II & III | [Lecture10\_11\_12](slides/Lecture10_11_12-Greedy_Algorithm_1_2_3.pdf) | [greedy.py](code/greedy.py) |
| 13–15 | Backtracking & Branch and Bound I, II & III | [Lecture13\_14\_15](slides/Lecture13_14_15-Backtracking_and_Branch_Bound_1_2_3.pdf) | [backtracking.py](code/backtracking.py) · [branch\_and\_bound.py](code/branch_and_bound.py) |
| 16 | Deep Learning Basics Part 1 | [Lecture16](slides/Lecture16-Deep_Learning_Basics_Part1.pdf) | — |

## Python Implementations

Each file is self-contained with a runnable demo (`python code/<file>.py`).

| File | Algorithms |
|------|-----------|
| [math_foundations.py](code/math_foundations.py) | Master Theorem solver (3 cases), growth rate comparison |
| [divide_and_conquer.py](code/divide_and_conquer.py) | Merge Sort, Quick Sort, Binary Search, Strassen, Closest Pair, Karatsuba, Max Subarray |
| [selection.py](code/selection.py) | Randomized QuickSelect, Median of Medians (O(n) worst-case), simultaneous min-max |
| [sequential_search.py](code/sequential_search.py) | Sequential search, sentinel search, move-to-front, transposition, skip list |
| [dynamic_programming.py](code/dynamic_programming.py) | 0/1 Knapsack, LCS, Matrix Chain, Edit Distance, Optimal BST, Coin Change, LIS |
| [greedy.py](code/greedy.py) | Activity Selection, Huffman Coding, Fractional Knapsack, Prim, Kruskal, Dijkstra, Task Scheduling |
| [backtracking.py](code/backtracking.py) | N-Queens, Graph Coloring, Subset Sum, Hamiltonian Cycle, 0/1 Knapsack, Permutations |
| [branch_and_bound.py](code/branch_and_bound.py) | 0/1 Knapsack B&B, TSP B&B (matrix reduction bound), Assignment Problem B&B |

## Homework Summary

| File | Topic | Method |
|------|-------|--------|
| [Recurrence\_Equation.tex](hw/Recurrence_Equation.tex) | Recurrence equations & Master Theorem | 3-case analysis, recursion tree |
| [General\_Selection\_Problem.tex](hw/General_Selection_Problem.tex) | General selection problem | QuickSelect, Median of Medians |
| [Improved\_Sequential\_Search.tex](hw/Improved_Sequential_Search_Algorithm.tex) | Improved sequential search | Sentinel, self-organizing lists |
| [Dynamic\_Programming.tex](hw/Dynamic_Programming.tex) | Dynamic programming | 0/1 Knapsack, LCS, Matrix Chain |
| [Branch\_and\_bound.tex](hw/Branch_and_bound.tex) | Branch and bound | Best-first B&B, upper-bound pruning |
| [Minimize\_Cost\_by\_B&B.tex](hw/Minimize_Cost_by_Branch_and_Bound.tex) | Cost minimization via B&B | Assignment problem, row-min lower bound |

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/ericxuzhesheng/Algorithm-at-SWUFE.git
cd Algorithm-at-SWUFE

# 2. Run any algorithm file
python code/dynamic_programming.py

# 3. Compile a LaTeX homework
pdflatex hw/Dynamic_Programming.tex
```

## Prerequisites

- Python 3.10+  
- A LaTeX distribution (e.g. [TeX Live](https://www.tug.org/texlive/) or [MiKTeX](https://miktex.org/)) to compile `.tex` files

---

## 授权证 | License

本项目采用 [MIT 授权证](LICENSE) 开源。  
Released under the [MIT License](LICENSE).
