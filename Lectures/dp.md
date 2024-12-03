# Dynamic programming

## Principles of Dynamic Programming

- **Optimal Substructure**
  - Explanation: Optimal solutions to subproblems can be combined to form the optimal solution to the overall problem.
  - Example: Shortest path problems in graphs.

- **Overlapping Subproblems**
  - Explanation: The same subproblems are solved multiple times during the recursive computation.
  - Example: Fibonacci sequence calculation.

### Workflow

1. **Write the Recursive Problem**
   - Describe the problem in recursive terms.

2. **Identify Subproblems**
   - Break down the main problem into smaller subproblems.
   - Draw the subproblem graph.
   - Identify and characterize overlapping subproblems.

3. **Rewrite the Algorithm**
   - **Top-Down Approach (Memoization)**
     - Store results of subproblems as they are computed in an efficient data structure (e.g., a dictionary).

   - **Bottom-Up Approach (Tabulation)**
     - Solve subproblems in order of increasing size and store results in a table.

### Memoization vs Tabulation

**Memoization**

- Top-down approach.
- Solve the problem recursively and store the results of subproblems.
- Use a dictionary or array to cache results.
- Easier to Implement, more intuitive.
- Less space-intensive.
- Slightly less efficient due to method calls.
- Can be more efficient if not all subproblems are necessary.

**Tabulation**

- Bottom-up approach.
- Solve subproblems in order of increasing size and store results in a table.
- Use an array or matrix to store results.
- Each subproblems solved exactly once.
- No fancy data structures required.
- Can be more space-intensive.

### Dynamic Programming vs Divide and Conquer

**Divide and Conquer**

- Break down the problem into non-overlapping subproblems.
- Solve each subproblem separately and combine the results.
- Usually the combination is involved.

**Dynamic Programming**

- Break down the problem into overlapping subproblems.
- Solve each subproblem once and store the results.
- Use the stored results to solve larger subproblems.
- Usually the combination is straightforward.

#### Comparison

- Both techniques involve breaking down a problem into smaller subproblems.
- Both techniques required optimal substructure, that is, independent subproblems.

## Exercises

### Rod Cutting Problem

The Rod Cutting Problem is a classic example of dynamic programming. The problem can be stated as follows:

#### Problem Statement

Given a rod of length $n$ and a list of prices for each length $i$ (where $i$ ranges from 1 to $n$), determine the maximum revenue obtainable by cutting up the rod and selling the pieces.

#### Example

- **Rod Length**: 8
- **Prices**:
  - Length 1: $1
  - Length 2: $5
  - Length 3: $8
  - Length 4: $9
  - Length 5: $10
  - Length 6: $17
  - Length 7: $17
  - Length 8: $20

#### Objective

Maximize the revenue obtained from cutting the rod.

#### Naive Recursive Method

The naive recursive approach to the Rod Cutting Problem involves solving the problem by considering all possible ways to cut the rod into two or more pieces. The idea is to recursively calculate the maximum revenue obtainable for each possible cut and return the maximum of these revenues.

1. **Recursive Formulation**:
   We can define a recursive function `cutRod(n)` that computes the maximum revenue obtainable for a rod of length $n$:

   $$
   \text{cutRod}(n) = \max(p[i] + \text{cutRod}(n-i)) \quad \text{for } i = 1, ..., n
   $$

   where $p[i]$ is the price of a rod of length $i$.

2. **Identify Subproblems**:
   The subproblems are the maximum revenues for rods of lengths from $1$ to $n-1$.

```python
def cut_rod(prices, n):
    # Base case: if the length is 0, no revenue can be obtained
    if n == 0:
        return 0

    M = float('-inf')

    # Try every possible first cut
    for i in range(1, n + 1):
        M = max(M, prices[i - 1] + cut_rod(prices, n - i))

    return M
```

#### Cost Analysis

The time complexity of this naive recursive solution can be analyzed using a recurrence relation.

$$
T(n) = 1 + \sum_{i=0}^{n-1} T(n-i)
$$

The base case occurs when $n = 0$:

$$
T(0) = 1
$$

To analyze the time complexity:
- At each level of recursion, we make $n$ calls (one for each possible first cut).
- This results in an n-ary tree of recursive calls where each node has up to $n$ children.

Thus, the total number of calls grows exponentially. The time complexity can be approximated as:

$$
T(n) = T(n-1) + T(n-2) + ... + T(0)
$$

This leads to an exponential growth in terms of time complexity:

$$
T(n) = O(2^n)
$$

The space complexity is determined by the depth of the recursion stack. In this case, it is $O(n)$, as each recursive call adds a new layer to the stack until reaching the base case.

#### Analysis of the problem structure

The Rod Cutting Problem exhibits both **optimal substructure** and **overlapping subproblems**, which are key characteristics of dynamic programming problems.

##### Optimal Substructure

The property of optimal substructure means that the optimal solution to a problem can be constructed from optimal solutions of its subproblems. In the case of the Rod Cutting Problem, the maximum revenue obtainable from a rod of length $n$ can be derived from the maximum revenues obtainable from rods of shorter lengths.

To see why, consider a rod of length $n$ split into $i$ and $n-i$ parts. Assume the part $n-i$ is not sold for its optimal value. You can create a new solution to the problem by selling the part $n-i$ optimally, which will yield a higher revenue than the original solution.

This contradicts the assumption that the original solution was optimal, so the assumption must be false. Therefore, the part $n-i$ must be sold optimally to achieve the maximum revenue for the rod of length $n$.

##### Overlapping Subproblems

The property of overlapping subproblems indicates that the same subproblems are solved multiple times during the computation. In the naive recursive approach to solving the Rod Cutting Problem, many calls are made to compute revenues for the same lengths repeatedly.

For instance, if you compute $R(4)$, you may find that it requires calculating $R(2)$ multiple times as you explore different cutting options. This redundancy leads to inefficiency and is illustrated in the recursion tree, where certain nodes (subproblems) are revisited multiple times.

#### Dynamic Programming Approach

Here’s how you can implement this using both memoization and tabulation approaches.

##### Memoization Approach

```python
def _cut_rod_memo(prices, n, memo):
    if n == 0:
        return 0
    if n in memo:
        return memo[n]

    M = float('-inf')

    for i in range(n):
        M = max(M, prices[i] + cut_rod_memo(prices, n - i - 1, memo))

    return memo[n] := M

def cut_rod_mempo(prices):
    n = len(prices)
    memo = {}
    memo[0] = 0
    return _cut_rod_memo(prices, n, memo)
```

##### Tabulation Approach

```python
def cut_rod_dp(prices):
    n = len(prices)
    dp = [0] * (n + 1)

    for j in range(1, n + 1):
        M = float('-inf')

        for i in range(j):
            M = max(M, prices[i] + dp[j - i - 1])

        dp[j] = M

    return dp[n]
```

#### Cost Analysis for DP

The time complexity of the dynamic programming approach is $O(n^2)$, as we have two nested loops. The space complexity is $O(n)$, as we only need to store the maximum revenue for each rod length in the `dp` array.

Both the memoization and tabulation approaches have better time complexity than the naive recursive solution. However, the tabulation approach is more space-efficient than the memoization approach, as it only uses a single array to store the results, while the memoization approach uses a dictionary and the call stack.

### Matrix Chain Multiply

#### Problem Statement

The **Matrix Chain Multiplication** problem involves finding the most efficient way to multiply a given sequence of matrices. The objective is to determine the minimum number of scalar multiplications needed to compute the product of these matrices. The matrices are represented by an array where each entry corresponds to the dimensions of the matrices. For instance, if you have matrices $A_1, A_2, \ldots, A_n$ with dimensions specified in an array $p$ such that matrix $A_i$ has dimensions $p[i-1] \times p[i]$, the goal is to find the optimal way to parenthesize the product $A_1 A_2 \ldots A_n$.

#### Naive Recursive Method

```python
def matrix_chain_order(p, i, j):
    # Base case: when there is only one matrix
    if i == j:
        return 0

    min_cost = float('inf')

    # Try every possible split point
    for k in range(i, j):
        # Calculate cost of multiplying (A_i...A_k) and (A_(k+1)...A_j)
        cost = (matrix_chain_order(p, i, k) +
                matrix_chain_order(p, k + 1, j) +
                p[i - 1] * p[k] * p[j])
        min_cost = min(min_cost, cost)

    return min_cost
```

#### Dynamic Programming Method

In the Matrix Chain Multiplication problem, the dynamic programming approach uses chain lengths to define subproblems because the cost of multiplying matrices depends on how many matrices are involved in the multiplication at any given time.

The dynamic programming solution iterates through increasing chain lengths (from 2 to $n$), where $n$ is the number of matrices. This approach allows us to build solutions from smaller subproblems systematically.

By starting with shorter chains and progressively increasing their length, you ensure that when you calculate the cost of multiplying a new chain, you have already computed the minimum costs for all smaller chains that contribute to it. This is crucial because the cost of multiplying a chain of matrices depends on how those matrices are grouped.

For instance, when calculating the minimum multiplication cost for a chain of matrices $A_1, A_2, A_3 $:
- You first compute costs for chains of length 2 (like $A_1A_2$, $A_2A_3$).
- Then, using those results, you compute the cost for the full chain $A_1A_2A_3$.

This stepwise approach ensures that every time you calculate a new cost, it's based on optimal solutions from subproblems that have already been solved.

```python
def matrix_chain_dp(p):
    n = len(p) - 1  # Number of matrices
    # Create a table to store minimum costs
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    # Fill dp table
    for length in range(2, n + 1):  # Length of chain
        for i in range(1, n - length + 2):  # Starting index
            j = i + length - 1  # Ending index
            dp[i][j] = float('inf')
            # Try every possible split point
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j]
                dp[i][j] = min(dp[i][j], cost)

    return dp[1][n]
```

### Longest Common Subsequence (LCS) Problem

The **Longest Common Subsequence (LCS)** problem is a classic algorithmic problem in computer science and bioinformatics. It involves finding the longest subsequence common to two sequences (strings). A subsequence is defined as a sequence that appears in the same relative order but not necessarily consecutively.

#### Problem Statement

Given two sequences (strings) $X$ and $Y$, find the length of their longest common subsequence. For example:

- **Input**:
  - X: "AGGTAB"
  - Y: "GXTXAYB"
- **Output**: Length of LCS = 4 (The LCS is "GTAB").

#### Problem analysis

Note that this problem has optimal substructure. If the last two (or the first two) symbols of `X` and `Y` match, then they must belong to the LCS. Otherwise we could grow the LCS appending these last characters. In the other case, if `X[n-1] != Y[n-1]` then we must find the `LCS(X, Y[:n-1])` and the `LCS(X[:n-1], Y)`.


#### Recursive Solution

The naive recursive approach to solving the LCS problem involves comparing characters from both sequences and recursively determining the length of the LCS based on these comparisons.

```python
def lcs(X, Y, m, n):
    # Base case: If either string is empty
    if m == 0 or n == 0:
        return 0

    # If last characters match
    if X[m - 1] == Y[n - 1]:
        return 1 + lcs(X, Y, m - 1, n - 1)

    # If last characters do not match
    return max(lcs(X, Y, m, n - 1), lcs(X, Y, m - 1, n))
```

#### Dynamic Programming Approach

The dynamic programming approach optimizes the naive recursive solution by storing intermediate results in a table to avoid redundant calculations. This approach builds up solutions for smaller subproblems to solve larger instances efficiently.

```python
def lcs_dp(X, Y):
    m = len(X)
    n = len(Y)

    # Create a DP table to store lengths of longest common subsequence
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Build the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:  # Characters match
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:                      # Characters do not match
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
```

Note that we can reduce the space complexity by keeping only the last two rows in the `dp`.

### Weighted Interval Scheduling Problem

The **Weighted Interval Scheduling** problem involves selecting a subset of non-overlapping intervals (jobs) such that the total weight (or value) of the selected intervals is maximized. Each interval has a start time, finish time, and associated weight. The challenge is to find the optimal combination of intervals that do not overlap.

#### Recursive Formulation

To solve this problem using dynamic programming, we can define a recursive function based on whether we include the last interval in our optimal solution or not. Here's how this works:

1. **Sort Intervals**: First, sort the intervals by their finish times.

2. **Define the Recursive Function**:
   - Let $\text{opt}(j)$ represent the maximum weight of non-overlapping intervals from the first $j$ intervals.
   - Let $p(j)$ be the last interval that is compatible with $j$ (finishes before $j$ starts).
   - We have two cases to consider for the $j$-th interval:
     - **Case 1**: The $j$-th interval is included in the optimal solution. In this case, we must also include the optimal solution from the compatible intervals that finish before this interval starts. This can be represented as:
       $$
       \text{opt}(j) = v_j + \text{opt}(p(j))
       $$
       where $v_j$ is the weight of the $j$-th interval and $p(j)$ is the index of the last non-overlapping interval before $j$.
     - **Case 2**: The $j$-th interval is not included in the optimal solution. In this case, we simply take the optimal solution from the first $j-1$ intervals:
       $$
       \text{opt}(j) = \text{opt}(j-1)
       $$

3. **Combining Cases**: The overall recursive formula can be expressed as:
   $$
   \text{opt}(j) = \max(\text{opt}(j-1), v_j + \text{opt}(p(j)))
   $$

4. **Base Case**: If there are no intervals (i.e., $j = 0$), then:
   $$
   \text{opt}(0) = 0
   $$

#### Dynamic Programming Approach

The dynamic programming approach builds upon this recursive formulation to avoid redundant calculations by storing intermediate results in a table.

```python
def weighted_interval_scheduling(intervals):
    # Sort intervals based on finish times
    intervals.sort(key=lambda x: x[1])  # Sorting by finish time

    n = len(intervals)
    M = [0] * (n + 1)
    p = [0] * (n + 1)

    # Compute p(j)
    for j in range(1, n + 1):
        p[j] = _non_conflicts(intervals, j - 1)

    # Fill M array using DP approach
    for j in range(1, n + 1):
        M[j] = max(M[j - 1], intervals[j - 1][2] + M[p[j]])

    return M[n]

def _non_conflicts(intervals, index):
    # Find the latest non-conflicting job
    for j in range(index - 1, -1, -1):
        if intervals[j][1] <= intervals[index][0]:
            return j + 1
    return 0
```

### Longest Increasing Subsequence (LIS) Problem

The **Longest Increasing Subsequence (LIS)** problem involves finding the longest subsequence in a given sequence of numbers such that all elements of the subsequence are sorted in increasing order. The subsequence does not need to be contiguous, meaning that elements can be omitted as long as their order is preserved.

#### Recursive Method

The (not so) naive recursive method involves computing all LISs ending with each element and returning the maximum of them.

```python
def _lis(arr, idx):

    # Base case
    if idx == 0:
        return 1

    # Consider all elements on the left of i,
    # recursively compute LISs ending with
    # them and consider the largest
    mx = 1
    for prev in range(idx):
        if arr[prev] < arr[idx]:
            mx = max(mx, _lis(arr, prev) + 1)
    return mx

def lis(arr):
    n = len(arr)
    res = 1

    for idx in range(1, n):
        res = max(res, _lis(arr, idx))

    return res
```

The time complexity of this naive approach is $O(2^n)$ because it explores all possible subsequences, leading to an exponential number of recursive calls.

#### Dynamic Programming Method

The dynamic programming approach optimizes the naive method by storing results in a table (array) to avoid redundant calculations.

1. **DP Array**: We create an array `dp` where `dp[i]` stores the length of the longest increasing subsequence that ends with the element at index `i`.

2. **Building DP Array**:
   - For each element at index `i`, we check all previous elements (from `0` to `i-1`).
   - If a previous element is smaller than the current element (`arr[j] < arr[i]`), we update `dp[i]` as:
     $$
     dp[i] = \max(dp[i], dp[j] + 1)
     $$
   - This ensures that we are building upon previously computed results.

3. **Result Extraction**: The length of the longest increasing subsequence will be the maximum value in the `dp` array.

```python
def lis_dp(arr):
    n = len(arr)
    dp = [1] * n  # Initialize DP array with 1s

    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:  # Check for increasing condition
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)
```

The time complexity of this dynamic programming approach is $O(n^2)$ due to the nested loops iterating through pairs of elements.

#### Efficient Method using Binary Search

The efficient method utilizes binary search along with a dynamic programming-like approach to achieve a time complexity of $O(n \log n)$.

1. **Tail Array**: We maintain an array called `tail`, where each index represents the smallest possible tail value for all increasing subsequences of different lengths found so far.

2. **Binary Search**:
   - For each element in the input array:
     - Use binary search to determine its position in `tail`.
     - If it can extend an existing subsequence (i.e., it's larger than any value in `tail`), append it.
     - Otherwise, replace an existing value in `tail` to maintain potential for longer increasing subsequences.

3. **Result Extraction**: The length of `tail` at the end gives us the length of the longest increasing subsequence.

```python
import bisect

def lis_binary_search(arr):
    tail = []  # This will store our increasing subsequences' tails

    for num in arr:
        pos = bisect.bisect_left(tail, num)  # Find position using binary search
        if pos == len(tail):
            tail.append(num)  # Extend tail if num is larger than any element
        else:
            tail[pos] = num   # Replace existing value to keep tail minimal

    return len(tail)
```

The time complexity of this method is $O(n \log n)$ because we perform a binary search for each element in the input array.

### Knapsack Problem

The **Knapsack Problem** is a classic optimization problem where the goal is to maximize the total value of items placed in a knapsack without exceeding its weight capacity. Given a set of items, each with a weight and a value, the challenge is to determine the most valuable combination of items that can fit into the knapsack.

#### Pseudopolynomial Dynamic Programming Solution

The Knapsack Problem can be solved using dynamic programming in a pseudopolynomial time complexity. The key idea is to use a table to store the maximum value that can be achieved for every possible weight up to the maximum capacity of the knapsack.

If the weight of the current item $i$ is less than or equal to $w$:
$$
dp[i][w] = \max(dp[i-1][w], \text{value}[i-1] + dp[i-1][w - \text{weight}[i-1]])
$$

If the weight of the current item $i$ exceeds $w$:
$$
dp[i][w] = dp[i-1][w]
$$

**Base Case**: When there are no items or the capacity is zero, the maximum value is zero:
$$
dp[w] = 0 \quad \text{for all } w \\
dp[i] = 0 \quad \text{for all } i
$$

#### Implementation

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    # Create a DP table with (n+1) x (capacity+1)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]
```

#### Time Complexity Analysis

The time complexity of this dynamic programming solution is $O(nW)$.

However, this complexity is considered **pseudopolynomial** because it depends on both $n$ and $W$. Specifically, while $n$ is a count of items (which is polynomial in terms of input size), $W$ represents a numeric value (the maximum weight), which can be very large and thus affects performance disproportionately.

#### Why This Does Not Prove P = NP

The fact that the Knapsack problem can be solved in pseudopolynomial time does not imply that P equals NP for several reasons:

The running time of $O(nW)$ is polynomial only in terms of $n$ and not necessarily in terms of the input size. The input size for $W$ is proportional to $\log W$, meaning that as $W$ increases (e.g., to very large values), it can lead to exponential running times relative to input size.

The Knapsack problem is classified as **weakly NP-complete** because it has pseudopolynomial time solutions but remains NP-complete when considering arbitrary weights or when weights are represented as binary numbers (in which case they may require exponential time).

## On the nature of problem structure

Consider the **Shortest-Path** and **Longest-Path** problems in graph theory. They are very similar in surface, but they exhibit distinct characteristics in terms of their subproblem structures and optimality.

The shortest-path problem exhibits optimal substructure, meaning that if you have an optimal solution to a problem (the shortest path from vertex A to vertex B), then any subpath within that solution must also be optimal. For example, if the shortest path from A to C involves going through B, then the path from A to B and the path from B to C must each be the shortest paths between those respective vertices.

The shortest-path problem has independent subproblems. When calculating the shortest path from vertex A to vertex C, it will always be composed of shortest-paths from A to B and B to C (for any B) that do not share any vertex.

This independence allows for efficient algorithms like Dijkstra's (greedy) or Bellman-Ford (dynamic programming).

Unlike the shortest-path problem, the longest-path problem does not exhibit optimal substructure in a straightforward manner. If you have an optimal solution for a longest path from vertex A to vertex C through vertex B, it does not guarantee that any subpath (like A to B) will also be a longest path.

This is because the longest-path problem has dependent subproblems. The two longest path from A to B and B to C might include the same vertices, and thus they cannot assemble a legal solution to the longest path from A to C.

Thus, independent subproblems are a key trait of problems that can be solved with dynamic programming.

Can we say then that some problems, like longest-path, cannot be solved with dynamic programming? Maybe this is a way to get to P=NP?

Sadly, no, because we don't know all the ways we could divide a problem into subproblems.