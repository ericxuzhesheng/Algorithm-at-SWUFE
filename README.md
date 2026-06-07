# Algorithm-at-SWUFE

西南财经大学《算法设计与分析》课程学习资料库，包含课程讲义、课后作业（LaTeX 源文件）及所有核心算法的 Python 实现。

Course materials for *Algorithm Design and Analysis* at SWUFE (Southwestern University of Finance and Economics), including lecture slides, homework write-ups in LaTeX, and Python implementations of every major algorithm covered in the course.

---

## 目录结构 / Repository Structure

```
Algorithm-at-SWUFE/
├── slides/          # 课程讲义 PDF（英文命名）/ Lecture slides (English-named)
├── hw/              # 作业 PDF + LaTeX 源文件 / Homework PDFs + LaTeX sources
└── code/            # Python 算法实现 / Python algorithm implementations
```

---

## 讲义 / Slides

| 文件 | 内容 |
|------|------|
| `Lecture01-Algorithm_Introduction.pdf` | 算法介绍 |
| `Lecture02-NP_Hard_Problems_Supplement.pdf` | NP-hard 问题补充 |
| `Lecture03-Mathematical_Foundations.pdf` | 数学基础 |
| `Lecture04_05-Divide_and_Conquer_1_2.pdf` | 分治策略（一、二）|
| `Lecture06-Divide_and_Conquer_3.pdf` | 分治策略（三）|
| `Lecture07_08-Dynamic_Programming_1_2.pdf` | 动态规划（一、二）|
| `Lecture09-Dynamic_Programming_3.pdf` | 动态规划（三）|
| `Lecture10_11_12-Greedy_Algorithm_1_2_3.pdf` | 贪心算法（一、二、三）|
| `Lecture13_14_15-Backtracking_and_Branch_Bound_1_2_3.pdf` | 回溯与分支限界（一、二、三）|
| `Lecture16-Deep_Learning_Basics_Part1.pdf` | 深度学习基础（一）|

---

## 作业 / Homework

每份作业包含 PDF 和配套 LaTeX 源文件，内容使用英文撰写。

Each homework includes a PDF and the corresponding LaTeX source, written in English.

| 文件 | 主题 |
|------|------|
| `Recurrence_Equation` | 递推方程与主定理 / Recurrence Equations & Master Theorem |
| `General_Selection_Problem` | 一般选择问题 / General Selection Problem |
| `Improved_Sequential_Search_Algorithm` | 改进的顺序搜索 / Improved Sequential Search |
| `Dynamic_Programming` | 动态规划 / Dynamic Programming |
| `Branch_and_bound` | 分支限界法 / Branch and Bound |
| `Minimize_Cost_by_Branch_and_Bound` | 分支限界最小化代价 / Minimize Cost via B&B |

---

## Python 算法实现 / Python Implementations

所有算法均有可运行的示例（`python code/<file>.py`）。

All algorithms include a runnable demo (`python code/<file>.py`).

| 文件 | 涵盖算法 |
|------|----------|
| `math_foundations.py` | Master Theorem 求解器、增长率比较 |
| `divide_and_conquer.py` | 归并排序、快速排序、二分搜索、Strassen 矩阵乘法、最近点对、Karatsuba、最大子数组 |
| `selection.py` | 随机化 QuickSelect、中位数的中位数（线性时间）、同时求最值 |
| `sequential_search.py` | 顺序搜索、哨兵搜索、自组织搜索（MTF/转置）、跳表 |
| `dynamic_programming.py` | 0/1 背包、LCS、矩阵链乘法、编辑距离、最优 BST、硬币找零、LIS |
| `greedy.py` | 活动选择、Huffman 编码、分数背包、Prim、Kruskal、Dijkstra、任务调度 |
| `backtracking.py` | N 皇后、图着色、子集和、哈密顿回路、0/1 背包回溯、排列生成 |
| `branch_and_bound.py` | 0/1 背包 B&B、TSP B&B、任务分配 B&B |

---

## 使用方法 / Usage

```bash
# 运行任意算法文件 / Run any algorithm file
python code/dynamic_programming.py
python code/greedy.py
python code/branch_and_bound.py
```

LaTeX 作业编译 / Compile LaTeX homework:

```bash
pdflatex hw/Dynamic_Programming.tex
```

---

## 参考教材 / Textbook

屈婉玲、刘田、张立昂、王捍贫，《算法设计与分析》（第3版），清华大学出版社。
