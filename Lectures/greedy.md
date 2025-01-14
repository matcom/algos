# Greedy Algorithms

## 1. Introduction to Greedy Algorithms

### 1.1 Definition and Characteristics
- **Definition**:
  - A greedy algorithm is an algorithmic paradigm that builds up a solution piece by piece, always choosing the next piece that offers the most immediate benefit (i.e., the locally optimal choice).

- **Characteristics**:
  - **Greedy-choice property**: A globally optimal solution can be arrived at by selecting a local optimum.
  - **Optimal substructure**: An optimal solution to the problem contains optimal solutions to subproblems.

### 1.2 Comparison with Other Paradigms
- **Dynamic Programming**:
  - Dynamic programming is used when the problem can be broken down into overlapping subproblems, and it focuses on solving each subproblem just once and storing the results.
  - Contrast with greedy algorithms, which do not consider future consequences of current choices.

- **Divide-and-Conquer**:
  - Divide-and-conquer algorithms divide the problem into smaller subproblems, solve them independently, and combine their solutions.
  - Discuss how greedy algorithms typically make decisions without revisiting previous choices.

### 1.3 Examples of Greedy Algorithms
- Provide a few real-world examples where greedy algorithms are applicable:
  - **Kruskal’s and Prim's Algorithms** for finding the Minimum Spanning Tree.
  - **Dijkstra’s Algorithm** for finding the shortest path in a graph.
  - **Huffman Coding** for data compression.

### 1.4 When to Use Greedy Algorithms
- Discuss scenarios where greedy algorithms are effective:
  - Problems with optimal substructure and greedy-choice property.
  - Situations where a quick, approximate solution is acceptable.
- Mention common pitfalls where greedy algorithms may fail to produce an optimal solution, such as in problems like the **0/1 Knapsack Problem**, which requires dynamic programming for an optimal solution.

## 2. Classic Problems

### 2.1 Frog Jumping Problem
- **Problem Statement**: Given a series of stones placed at integer locations, and a maximum jump length, determine the minimum number of jumps need to reach the end.
- **Greedy Approach**: Jump the fartest possible stone that is reachable for the current stone.

### 2.2 Activity Selection Problem
- **Problem Statement**: Given a set of activities with start and finish times, select the maximum number of activities that don’t overlap.
- **Greedy Approach**: Explain how sorting activities by finish time leads to an optimal selection strategy.

### 2.3 Fractional Knapsack Problem
- **Problem Statement**: Given weights and values of items that can be divided, maximize the total value in a knapsack with a weight limit $K$.
- **Greedy Approach**:
  - Calculate the value-to-weight ratio for each item.
  - Sort items based on this ratio in descending order.
  - Fill the knapsack starting from the item with the highest ratio, allowing for fractional amounts if necessary.

### 2.4 Minimize Cash Flow Among Friends
- **Problem Statement**: Given a list of debts among friends, minimize the total cash flow required to settle all debts.
- **Greedy Approach**: Discuss calculating net amounts for each person and settling debts by always addressing the largest creditor and debtor first.
