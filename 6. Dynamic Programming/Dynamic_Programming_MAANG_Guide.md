# Dynamic Programming: From Zero to MAANG Interviews
## A Senior Engineer's Guide to Mastering DP

---

# Phase 1: Foundations - What DP Actually Is

## What is Dynamic Programming Really?

**Forget the textbook definition.** Here's what DP actually is:

Dynamic Programming is **intelligent exhaustive search**. It's a way to explore all possible solutions (like brute force), but being smart about it by **remembering** what you've already computed so you don't waste time recalculating the same thing over and over.

**The Real Problem It Solves:**
You have a problem that can be broken into smaller subproblems, but these subproblems overlap (appear multiple times). Without DP, you'd solve the same subproblem hundreds or thousands of times. DP says: "Solve it once, remember the answer, reuse it."

---

## Why Recursion Alone Fails

Let's see the disaster that happens without DP.

### Example: Fibonacci Numbers

```python
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)

# Try this
print(fib_recursive(5))   # Fast
print(fib_recursive(35))  # Noticeable delay
# Try fib_recursive(50) - you'll wait forever
```

**Why does this explode?**

Let's trace `fib(5)`:

```
                    fib(5)
                   /      \
              fib(4)      fib(3)
              /    \      /    \
         fib(3)  fib(2) fib(2) fib(1)
         /   \    /  \   /  \
    fib(2) fib(1) ...  ...
    /   \
fib(1) fib(0)
```

**Notice:**
- `fib(3)` is calculated **2 times**
- `fib(2)` is calculated **3 times**
- `fib(1)` is calculated **5 times**

For `fib(50)`, you'd calculate `fib(2)` **billions** of times!

**Time Complexity:** O(2^n) - exponential disaster

**Why?** Each call branches into 2 more calls, creating an exponential tree.

---

## The Two Pillars of DP

For DP to be applicable, your problem MUST have these two properties:

### 1. Overlapping Subproblems

**What it means:** The same subproblem appears multiple times while solving the main problem.

**Fibonacci Example:** `fib(2)` appears again and again in the recursion tree.

**Why it matters:** If subproblems don't overlap, there's nothing to cache. You'd just use regular recursion or iteration.

**Counter-example (NO DP needed):**
```python
def binary_search(arr, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid+1, right)
    else:
        return binary_search(arr, target, left, mid-1)
```

Binary search has **no overlapping subproblems**. Each recursive call searches a different portion of the array. Nothing repeats. DP is useless here.

### 2. Optimal Substructure

**What it means:** The optimal solution to the problem can be constructed from optimal solutions to its subproblems.

**Example - Shortest Path:**
If the shortest path from A to C goes through B, then:
- A → B must be the shortest path from A to B
- B → C must be the shortest path from B to C

**Why it matters:** If optimal solutions to subproblems don't lead to an optimal solution for the main problem, DP won't give you the right answer.

**Counter-example (DP fails):**
Longest simple path in a graph does NOT have optimal substructure. Why? The longest path from A to D might go through B and C, but the longest path from A to B might also go through C, creating a cycle. Subproblems interfere with each other.

---

## The Three Approaches

### 1. Pure Recursion (The Naive Way)

```python
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)
```

**Pros:** Easy to write, directly matches the mathematical definition
**Cons:** Exponential time complexity due to redundant calculations
**When to use:** Never in production, but always start here to understand the problem

### 2. Memoization (Top-Down DP)

```python
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]
```

**What changes:** Added a dictionary to store results
**How it works:** Before computing, check if we've seen this before. If yes, return cached answer.
**Time Complexity:** O(n) - each unique subproblem solved once
**Space Complexity:** O(n) for memo + O(n) for recursion stack = O(n)

**Pros:**
- Natural extension of recursive thinking
- Only computes subproblems that are actually needed
- Easy to code once you have the recursive solution

**Cons:**
- Recursion stack overhead (can cause stack overflow for very large n)
- Slightly slower than tabulation due to function call overhead

### 3. Tabulation (Bottom-Up DP)

```python
def fib_tab(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

**What changes:** No recursion, build solution from smallest to largest subproblems
**How it works:** Start with base cases, iteratively build up to the answer
**Time Complexity:** O(n)
**Space Complexity:** O(n) for dp array, no recursion stack

**Pros:**
- Faster (no function call overhead)
- No stack overflow risk
- Often easier to optimize space

**Cons:**
- Less intuitive to derive
- Computes all subproblems even if not needed

**Space Optimization:**
```python
def fib_optimized(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1
```

**Space Complexity:** O(1) - only store what we need

---

## Visual Comparison: Recursion vs Memoization vs Tabulation

### Computing fib(6)

**Pure Recursion Tree** (redundant calculations in [brackets]):
```
fib(6) calls:
  fib(5) calls:
    fib(4) calls fib(3), fib(2)
    fib(3) calls fib(2), fib(1)  [fib(3) repeated]
  fib(4) calls:                   [fib(4) repeated]
    fib(3) ...                    [fib(3) repeated again]
    fib(2) ...                    [fib(2) repeated many times]
```
**Total function calls:** 25

**Memoization** (with cache hits marked as ✓):
```
fib(6) → calls fib(5), fib(4)
fib(5) → calls fib(4), fib(3)
fib(4) → calls fib(3), fib(2)
fib(3) → calls fib(2), fib(1)
fib(2) → calls fib(1), fib(0)
fib(1) → base case
fib(0) → base case

Then all repeat calls hit cache ✓
```
**Total function calls:** 11 (but 6 compute, 5 cache hits)

**Tabulation** (no function calls):
```
dp[0] = 0
dp[1] = 1
dp[2] = dp[1] + dp[0] = 1
dp[3] = dp[2] + dp[1] = 2
dp[4] = dp[3] + dp[2] = 3
dp[5] = dp[4] + dp[3] = 5
dp[6] = dp[5] + dp[4] = 8
```
**Total operations:** 5 additions

---

# Phase 2: How to Think in DP - The Mental Framework

This is the most important section. Master this, and you can solve any DP problem.

## The 5-Step DP Thinking Framework

### Step 1: Can This Problem Use DP?

**Ask these questions:**

1. **Is there a decision or choice at each step?**
   - Example: Climb 1 stair or 2 stairs?
   - Example: Include item in knapsack or exclude it?

2. **Are we looking for optimal (min/max/count) or enumerate all ways?**
   - "Find the minimum cost"
   - "Count the number of ways"
   - "Find the longest subsequence"

3. **Can the problem be broken into smaller, similar subproblems?**
   - If yes, recursion is possible
   - If recursion solves it, DP might optimize it

4. **Will subproblems repeat?**
   - Dry run the recursion mentally
   - If you're calling the same function with same parameters multiple times, DP applies

**Red flags (DP probably won't help):**
- Problem requires exploring all paths and they're all unique (combinatorial explosion with no overlap)
- Greedy approach works (optimal choice at each step)
- Problem is inherently linear with no branching decisions

### Step 2: Define the State

**The state is what changes from subproblem to subproblem.**

**How to find the state:**
1. Look at the function parameters in your recursive solution
2. What makes one subproblem different from another?
3. Those are your state variables

**Examples:**

**Fibonacci:**
- What changes? Only `n`
- State: `dp[n]` = nth Fibonacci number
- 1D DP

**Grid Paths** (top-left to bottom-right):
- What changes? Current position (row, col)
- State: `dp[i][j]` = number of ways to reach cell (i, j)
- 2D DP

**Knapsack** (items and capacity):
- What changes? Current item index, remaining capacity
- State: `dp[i][w]` = max value using first i items with capacity w
- 2D DP

**Rule of thumb:** Number of state variables = dimensions of DP array

### Step 3: Write the Recurrence Relation

**This is the heart of DP.** It's the formula that relates the current state to previous states.

**Process:**
1. Start with the recursive solution
2. Express current problem in terms of smaller subproblems
3. That expression is your recurrence

**Template:**
```
dp[current_state] = function(dp[smaller_state_1], dp[smaller_state_2], ...)
```

**Examples:**

**Fibonacci:**
```python
# Recursion: fib(n) = fib(n-1) + fib(n-2)
# Recurrence: dp[n] = dp[n-1] + dp[n-2]
```

**Grid Paths:**
```python
# Can reach (i,j) from (i-1,j) or (i,j-1)
# Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

**Knapsack:**
```python
# Either include item i or exclude it
# Include: value[i] + dp[i-1][w-weight[i]]
# Exclude: dp[i-1][w]
# Recurrence: dp[i][w] = max(include, exclude)
```

### Step 4: Identify Base Cases

**Base cases are the smallest subproblems you can solve directly without recursion.**

**How to find them:**
1. What are the termination conditions in your recursive solution?
2. What are the simplest inputs?
3. What happens when state variables are 0 or at boundaries?

**Examples:**

**Fibonacci:**
```python
dp[0] = 0
dp[1] = 1
```

**Grid Paths:**
```python
dp[0][j] = 1  # First row: only one way (move right)
dp[i][0] = 1  # First column: only one way (move down)
```

**Knapsack:**
```python
dp[0][w] = 0  # No items, value = 0
dp[i][0] = 0  # No capacity, value = 0
```

### Step 5: Decide the Order of Computation

**For memoization:** Don't worry, recursion handles this automatically.

**For tabulation:** You must fill the DP table in an order such that when you need `dp[state]`, all the states it depends on are already computed.

**General rule:**
- If `dp[i]` depends on `dp[i-1]`, compute in increasing order of i
- If `dp[i][j]` depends on `dp[i-1][j]` and `dp[i][j-1]`, fill row by row, left to right

**Example - Grid Paths:**
```python
# dp[i][j] depends on dp[i-1][j] (cell above) and dp[i][j-1] (cell left)
# So we must fill top to bottom, left to right

for i in range(m):
    for j in range(n):
        if i == 0 and j == 0:
            dp[i][j] = 1
        elif i == 0:
            dp[i][j] = dp[i][j-1]
        elif j == 0:
            dp[i][j] = dp[i-1][j]
        else:
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

---

## Memoization vs Tabulation: How to Choose?

### Choose Memoization When:
1. **Recursion is more intuitive** for the problem (tree problems, complex state transitions)
2. **Not all subproblems are needed** (sparse state space)
3. **You're in an interview and time is short** (easier to code from recursive solution)

### Choose Tabulation When:
1. **You need maximum performance** (no function call overhead)
2. **All or most subproblems will be solved anyway**
3. **Space optimization is critical** (easier to optimize tabulation to O(1) space)
4. **Risk of stack overflow** (very large n)

### Interview Strategy:
1. Always start with recursive solution (establishes your understanding)
2. Convert to memoization (shows you know DP)
3. If time permits, convert to tabulation (shows you can optimize)
4. If still time left, optimize space (shows mastery)

---

# Phase 3: Patterns - One by One

## Pattern 1: 1D DP (Linear Sequence)

### Characteristics:
- Single variable changes (usually index or count)
- State: `dp[i]` = answer for first i elements or for element at index i
- Recurrence typically looks at previous 1-2 states

---

### Problem 1.1: Climbing Stairs

**Problem:** You're climbing stairs. Each time you can climb 1 or 2 steps. How many distinct ways can you climb to the top (n steps)?

**Example:**
```
n = 3
Ways:
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step
Answer: 3
```

#### Step 1: Why DP?

- **Decision at each step:** Climb 1 stair or 2 stairs
- **Looking for count:** "How many ways"
- **Subproblems:** To reach stair n, you must come from stair n-1 or n-2
- **Overlapping:** Ways to reach stair 3 will be recomputed multiple times in recursion

#### Step 2: Build Intuition

Let's think backwards:
- To reach step n, I must have been at step n-1 (then climb 1) OR step n-2 (then climb 2)
- So, ways(n) = ways(n-1) + ways(n-2)
- This is Fibonacci in disguise!

#### Step 3: Recursive Solution

```python
def climb_stairs_recursive(n):
    # Base cases
    if n == 0:
        return 1  # One way to stay at ground (do nothing)
    if n == 1:
        return 1  # One way: single step

    # Recurrence
    return climb_stairs_recursive(n-1) + climb_stairs_recursive(n-2)

# Test
print(climb_stairs_recursive(5))  # 8
```

**Time Complexity:** O(2^n) - exponential
**Why?** Same redundancy as Fibonacci

**Dry run for n=4:**
```
climb(4)
├── climb(3)
│   ├── climb(2)
│   │   ├── climb(1) → 1
│   │   └── climb(0) → 1
│   │   Result: 2
│   └── climb(1) → 1
│   Result: 3
└── climb(2)  [REDUNDANT - already computed above]
    ├── climb(1) → 1
    └── climb(0) → 1
    Result: 2
Result: 5
```

#### Step 4: Memoization (Top-Down DP)

```python
def climb_stairs_memo(n, memo=None):
    if memo is None:
        memo = {}

    # Check cache
    if n in memo:
        return memo[n]

    # Base cases
    if n == 0 or n == 1:
        return 1

    # Compute and cache
    memo[n] = climb_stairs_memo(n-1, memo) + climb_stairs_memo(n-2, memo)
    return memo[n]

# Test
print(climb_stairs_memo(50))  # Works instantly
```

**Time Complexity:** O(n) - each state computed once
**Space Complexity:** O(n) for memo + O(n) for recursion stack = O(n)

#### Step 5: Tabulation (Bottom-Up DP)

```python
def climb_stairs_tab(n):
    if n == 0 or n == 1:
        return 1

    # Create DP table
    dp = [0] * (n + 1)

    # Base cases
    dp[0] = 1
    dp[1] = 1

    # Fill table
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]

# Test
print(climb_stairs_tab(50))
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

#### Step 6: Space Optimization

```python
def climb_stairs_optimized(n):
    if n == 0 or n == 1:
        return 1

    # Only need last two values
    prev2 = 1  # dp[i-2]
    prev1 = 1  # dp[i-1]

    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr

    return prev1

# Test
print(climb_stairs_optimized(50))
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

---

### Problem 1.2: House Robber

**Problem:** You're a robber planning to rob houses along a street. Each house has a certain amount of money. Adjacent houses have security systems that will alert police if both are robbed. What's the maximum amount you can rob?

**Example:**
```
houses = [2, 7, 9, 3, 1]
Rob houses 0, 2, 4: 2 + 9 + 1 = 12
Answer: 12
```

#### Step 1: Why DP?

- **Decision at each house:** Rob it or skip it
- **Looking for max:** "Maximum amount"
- **Constraint:** Can't rob adjacent houses
- **Subproblems:** For each house, decision depends on previous houses

#### Step 2: Build Intuition

For each house i, two choices:
1. **Rob house i:** Get money[i] + max money from houses up to i-2 (can't use i-1)
2. **Skip house i:** Get max money from houses up to i-1

Take the better choice: `max(rob_it, skip_it)`

#### Step 3: Define State

`dp[i]` = maximum money that can be robbed from houses 0 to i

#### Step 4: Recurrence Relation

```python
dp[i] = max(money[i] + dp[i-2], dp[i-1])
         ^                      ^
         Rob house i          Skip house i
```

#### Step 5: Recursive Solution

```python
def rob_recursive(houses, i=None):
    if i is None:
        i = len(houses) - 1

    # Base cases
    if i < 0:
        return 0
    if i == 0:
        return houses[0]

    # Recurrence: rob this house or skip it
    rob_current = houses[i] + rob_recursive(houses, i-2)
    skip_current = rob_recursive(houses, i-1)

    return max(rob_current, skip_current)

# Test
houses = [2, 7, 9, 3, 1]
print(rob_recursive(houses))  # 12
```

**Dry run for [2, 7, 9, 3, 1]:**
```
rob(4) → max(1 + rob(2), rob(3))
    rob(2) → max(9 + rob(0), rob(1))
        rob(0) → 2
        rob(1) → max(7 + rob(-1), rob(0))
            rob(-1) → 0
            rob(0) → 2  [REDUNDANT]
        → max(7, 2) = 7
    → max(9+2, 7) = 11

    rob(3) → max(3 + rob(1), rob(2))
        rob(1) → 7  [REDUNDANT]
        rob(2) → 11 [REDUNDANT]
    → max(3+7, 11) = 11

→ max(1+11, 11) = 12
```

#### Step 6: Memoization

```python
def rob_memo(houses):
    memo = {}

    def helper(i):
        if i < 0:
            return 0
        if i == 0:
            return houses[0]

        if i in memo:
            return memo[i]

        rob_current = houses[i] + helper(i-2)
        skip_current = helper(i-1)
        memo[i] = max(rob_current, skip_current)

        return memo[i]

    return helper(len(houses) - 1)

# Test
print(rob_memo([2, 7, 9, 3, 1]))  # 12
```

#### Step 7: Tabulation

```python
def rob_tab(houses):
    n = len(houses)
    if n == 0:
        return 0
    if n == 1:
        return houses[0]

    dp = [0] * n
    dp[0] = houses[0]
    dp[1] = max(houses[0], houses[1])

    for i in range(2, n):
        dp[i] = max(houses[i] + dp[i-2], dp[i-1])

    return dp[n-1]

# Test
print(rob_tab([2, 7, 9, 3, 1]))  # 12
```

**Trace:**
```
houses = [2, 7, 9, 3, 1]
dp[0] = 2
dp[1] = max(2, 7) = 7
dp[2] = max(9+2, 7) = 11
dp[3] = max(3+7, 11) = 11
dp[4] = max(1+11, 11) = 12
```

#### Step 8: Space Optimization

```python
def rob_optimized(houses):
    n = len(houses)
    if n == 0:
        return 0
    if n == 1:
        return houses[0]

    prev2 = houses[0]
    prev1 = max(houses[0], houses[1])

    for i in range(2, n):
        curr = max(houses[i] + prev2, prev1)
        prev2 = prev1
        prev1 = curr

    return prev1

# Test
print(rob_optimized([2, 7, 9, 3, 1]))  # 12
```

**Time:** O(n)  
**Space:** O(1)

---

## Pattern 2: 2D DP (Grid/Matrix Problems)

### Characteristics:
- Two variables change (usually row and column, or two indices)
- State: `dp[i][j]` = answer for subproblem defined by i and j
- Recurrence looks at neighboring cells or previous states in both dimensions

---

### Problem 2.1: Unique Paths in Grid

**Problem:** A robot is on an m×n grid, starting at top-left. It can only move right or down. How many unique paths to bottom-right?

**Example:**
```
3×3 grid:
S . .
. . .
. . E

Paths: 6
```

#### Step 1: Why DP?

- **Decision at each cell:** Move right or move down
- **Looking for count:** "How many unique paths"
- **Subproblems:** To reach (i,j), must come from (i-1,j) or (i,j-1)
- **Overlapping:** Paths to (2,2) will be recomputed multiple times

#### Step 2: Build Intuition

Think about reaching any cell (i, j):
- You can only arrive from above (i-1, j) or from left (i, j-1)
- Total paths to (i,j) = paths to (i-1,j) + paths to (i,j-1)
- Base case: First row and first column have only 1 path (straight line)

**Visualization for 3×3:**
```
1  1  1      (top row: only one way - keep going right)
1  2  3      (cell(1,1): 1 from above + 1 from left = 2)
1  3  6      (cell(2,2): 3 from above + 3 from left = 6)
```

#### Step 3: Define State

`dp[i][j]` = number of unique paths from (0,0) to (i,j)

#### Step 4: Recurrence Relation

```python
dp[i][j] = dp[i-1][j] + dp[i][j-1]
           ^             ^
           from above    from left
```

**Edge cases:**
- `dp[0][j] = 1` (first row: only move right)
- `dp[i][0] = 1` (first column: only move down)

#### Step 5: Recursive Solution

```python
def unique_paths_recursive(m, n, i=0, j=0):
    # Base cases
    if i == m-1 and j == n-1:
        return 1  # Reached destination
    if i >= m or j >= n:
        return 0  # Out of bounds

    # Recurrence: go down or go right
    down = unique_paths_recursive(m, n, i+1, j)
    right = unique_paths_recursive(m, n, i, j+1)

    return down + right

# Test
print(unique_paths_recursive(3, 3))  # 6
```

**Time Complexity:** O(2^(m+n)) - exponential

#### Step 6: Memoization

```python
def unique_paths_memo(m, n):
    memo = {}

    def helper(i, j):
        if i == m-1 and j == n-1:
            return 1
        if i >= m or j >= n:
            return 0

        if (i, j) in memo:
            return memo[(i, j)]

        down = helper(i+1, j)
        right = helper(i, j+1)
        memo[(i, j)] = down + right

        return memo[(i, j)]

    return helper(0, 0)

# Test
print(unique_paths_memo(3, 3))  # 6
```

**Time:** O(m×n)  
**Space:** O(m×n)

#### Step 7: Tabulation

```python
def unique_paths_tab(m, n):
    # Create DP table
    dp = [[0] * n for _ in range(m)]

    # Base cases: first row and column
    for i in range(m):
        dp[i][0] = 1
    for j in range(n):
        dp[0][j] = 1

    # Fill table
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]

    return dp[m-1][n-1]

# Test
print(unique_paths_tab(3, 3))  # 6
```

**Trace for 3×3:**
```
Initial:
[1, 1, 1]
[1, 0, 0]
[1, 0, 0]

After filling:
[1, 1, 1]
[1, 2, 3]
[1, 3, 6]

Result: 6
```

#### Step 8: Space Optimization

```python
def unique_paths_optimized(m, n):
    # Only need previous row
    prev = [1] * n

    for i in range(1, m):
        curr = [1] * n
        for j in range(1, n):
            curr[j] = curr[j-1] + prev[j]
        prev = curr

    return prev[n-1]

# Test
print(unique_paths_optimized(3, 3))  # 6
```

**Time:** O(m×n)  
**Space:** O(n)

---

### Problem 2.2: Minimum Path Sum

**Problem:** Given an m×n grid with non-negative numbers, find path from top-left to bottom-right that minimizes sum. Can only move right or down.

**Example:**
```
grid = [
  [1,3,1],
  [1,5,1],
  [4,2,1]
]
Path: 1→3→1→1→1 = 7
```

#### Step 1: Build Intuition

Similar to unique paths, but now we care about cost:
- To reach (i,j), we come from (i-1,j) or (i,j-1)
- Cost to reach (i,j) = grid[i][j] + min(cost to reach (i-1,j), cost to reach (i,j-1))
- Choose the cheaper path

#### Step 2: Define State

`dp[i][j]` = minimum path sum from (0,0) to (i,j)

#### Step 3: Recurrence Relation

```python
dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
```

#### Step 4: Tabulation

```python
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]

    # Base case: starting cell
    dp[0][0] = grid[0][0]

    # First row: can only come from left
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + grid[0][j]

    # First column: can only come from above
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + grid[i][0]

    # Fill rest of table
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

    return dp[m-1][n-1]

# Test
grid = [
  [1,3,1],
  [1,5,1],
  [4,2,1]
]
print(min_path_sum(grid))  # 7
```

**Trace:**
```
Grid:          DP table:
1  3  1        1  4  5
1  5  1   →    2  7  6
4  2  1        6  8  7

Path: (0,0)→(0,1)→(0,2)→(1,2)→(2,2) = 1+3+1+1+1 = 7
```

---

## Pattern 3: Subsequence DP

### Characteristics:
- Problems involving sequences (arrays, strings)
- Typically 2D DP with state `dp[i][j]` representing relationship between two sequences or first i elements
- Common: Longest Common Subsequence, Longest Increasing Subsequence, Edit Distance

**Key concept:** Subsequence vs substring
- **Subsequence:** Elements in relative order but not necessarily consecutive (e.g., "ace" from "abcde")
- **Substring:** Consecutive elements (e.g., "abc" from "abcde")

---

### Problem 3.1: Longest Common Subsequence (LCS)

**Problem:** Given two strings, find the length of their longest common subsequence.

**Example:**
```
text1 = "abcde"
text2 = "ace"
LCS = "ace" (length 3)
```

#### Step 1: Build Intuition

Compare strings character by character from start:
- If characters match: they're part of LCS, move both pointers forward
- If they don't match: try skipping one character from either string, take the better result

**Example walkthrough:**
```
text1 = "abcde"
text2 = "ace"

Compare 'a' and 'a': Match! LCS length = 1 + LCS("bcde", "ce")
Compare 'b' and 'c': No match. Try:
  - Skip 'b': LCS("cde", "ce")
  - Skip 'c': LCS("bcde", "e")
  Take max
...
```

#### Step 2: Define State

`dp[i][j]` = length of LCS of text1[0...i-1] and text2[0...j-1]

**Why i-1 and j-1?** `dp[i][j]` represents "first i characters" of text1 and "first j characters" of text2. This makes base cases cleaner (dp[0][j] and dp[i][0] are empty strings).

#### Step 3: Recurrence Relation

```python
if text1[i-1] == text2[j-1]:
    dp[i][j] = 1 + dp[i-1][j-1]  # Match: include this char, move both
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # No match: skip one
```

#### Step 4: Recursive Solution

```python
def lcs_recursive(text1, text2, i=None, j=None):
    if i is None:
        i = len(text1) - 1
    if j is None:
        j = len(text2) - 1

    # Base cases
    if i < 0 or j < 0:
        return 0

    # If characters match
    if text1[i] == text2[j]:
        return 1 + lcs_recursive(text1, text2, i-1, j-1)

    # If characters don't match, try both options
    skip_text1 = lcs_recursive(text1, text2, i-1, j)
    skip_text2 = lcs_recursive(text1, text2, i, j-1)

    return max(skip_text1, skip_text2)

# Test
print(lcs_recursive("abcde", "ace"))  # 3
```

#### Step 5: Memoization

```python
def lcs_memo(text1, text2):
    memo = {}

    def helper(i, j):
        if i < 0 or j < 0:
            return 0

        if (i, j) in memo:
            return memo[(i, j)]

        if text1[i] == text2[j]:
            memo[(i, j)] = 1 + helper(i-1, j-1)
        else:
            memo[(i, j)] = max(helper(i-1, j), helper(i, j-1))

        return memo[(i, j)]

    return helper(len(text1)-1, len(text2)-1)

# Test
print(lcs_memo("abcde", "ace"))  # 3
```

#### Step 6: Tabulation

```python
def lcs_tab(text1, text2):
    m, n = len(text1), len(text2)

    # Create DP table with extra row/column for base case
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]

# Test
print(lcs_tab("abcde", "ace"))  # 3
```

**Trace for "abcde" and "ace":**
```
      ""  a  c  e
""     0  0  0  0
a      0  1  1  1
b      0  1  1  1
c      0  1  2  2
d      0  1  2  2
e      0  1  2  3

Reading: dp[5][3] = 3
```

**How to read the table:**
- `dp[1][1]`: 'a' vs 'a' → match, 1 + dp[0][0] = 1
- `dp[2][1]`: 'ab' vs 'a' → 'b' ≠ 'a', max(dp[1][1], dp[2][0]) = 1
- `dp[3][2]`: 'abc' vs 'ac' → 'c' = 'c', 1 + dp[2][1] = 2
- `dp[5][3]`: 'abcde' vs 'ace' → 'e' = 'e', 1 + dp[4][2] = 3

#### Step 7: Space Optimization

```python
def lcs_optimized(text1, text2):
    m, n = len(text1), len(text2)

    # Only need previous row
    prev = [0] * (n + 1)

    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                curr[j] = 1 + prev[j-1]
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev = curr

    return prev[n]

# Test
print(lcs_optimized("abcde", "ace"))  # 3
```

**Time:** O(m×n)  
**Space:** O(n)

---

### Problem 3.2: Longest Increasing Subsequence (LIS)

**Problem:** Given an array, find the length of the longest strictly increasing subsequence.

**Example:**
```
nums = [10, 9, 2, 5, 3, 7, 101, 18]
LIS = [2, 3, 7, 101] or [2, 3, 7, 18]
Length: 4
```

#### Step 1: Build Intuition

For each element, ask: "What's the longest increasing subsequence ending at this element?"

To find that, look at all previous elements smaller than current:
- For each smaller element, we can extend its LIS by including current element
- Take the longest such LIS and add 1

#### Step 2: Define State

`dp[i]` = length of LIS ending at index i

#### Step 3: Recurrence Relation

```python
dp[i] = 1 + max(dp[j] for all j < i where nums[j] < nums[i])

# If no such j exists, dp[i] = 1 (just the element itself)
```

#### Step 4: Tabulation

```python
def length_of_lis(nums):
    n = len(nums)
    if n == 0:
        return 0

    # Each element is an LIS of length 1 by itself
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], 1 + dp[j])

    # Answer is the max value in dp (LIS can end anywhere)
    return max(dp)

# Test
nums = [10, 9, 2, 5, 3, 7, 101, 18]
print(length_of_lis(nums))  # 4
```

**Trace:**
```
nums = [10, 9, 2, 5, 3, 7, 101, 18]
dp   = [1,  1, 1, 1, 1, 1, 1,   1]

i=1: nums[1]=9, no j where nums[j]<9 in [10], dp[1]=1
i=2: nums[2]=2, no j where nums[j]<2 in [10,9], dp[2]=1
i=3: nums[3]=5, j=2 works (2<5), dp[3]=1+dp[2]=2
i=4: nums[4]=3, j=2 works (2<3), dp[4]=1+dp[2]=2
i=5: nums[5]=7, j=2,3,4 work, max: 1+dp[3]=3
i=6: nums[6]=101, all previous work, max: 1+dp[5]=4
i=7: nums[7]=18, j=2,3,4,5 work, max: 1+dp[5]=4

dp = [1, 1, 1, 2, 2, 3, 4, 4]
Answer: max(dp) = 4
```

**Time:** O(n²)  
**Space:** O(n)

---

## Pattern 4: Knapsack DP

### Characteristics:
- Problems involving selection/inclusion decisions
- Typically constraint (capacity/weight) and optimization (maximize/minimize value)
- State often includes current item and remaining capacity

---

### Problem 4.1: 0/1 Knapsack

**Problem:** Given weights and values of n items, and a knapsack with capacity W. Each item can be included at most once. Maximize total value without exceeding capacity.

**Example:**
```
values  = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50

Solution: Include items 1 and 2
Value = 100 + 120 = 220
Weight = 20 + 30 = 50
```

#### Step 1: Build Intuition

For each item, two choices:
1. **Include it:** Get its value, reduce capacity by its weight, solve for remaining items
2. **Exclude it:** Move to next item with same capacity

Take the better choice.

#### Step 2: Define State

`dp[i][w]` = maximum value achievable using first i items with capacity w

#### Step 3: Recurrence Relation

```python
if weight[i-1] <= w:
    # Can include item i
    include = value[i-1] + dp[i-1][w - weight[i-1]]
    exclude = dp[i-1][w]
    dp[i][w] = max(include, exclude)
else:
    # Item too heavy, must exclude
    dp[i][w] = dp[i-1][w]
```

#### Step 4: Recursive Solution

```python
def knapsack_recursive(weights, values, capacity, n=None):
    if n is None:
        n = len(weights)

    # Base cases
    if n == 0 or capacity == 0:
        return 0

    # If current item is too heavy, skip it
    if weights[n-1] > capacity:
        return knapsack_recursive(weights, values, capacity, n-1)

    # Try both including and excluding
    include = values[n-1] + knapsack_recursive(weights, values, 
                                                capacity - weights[n-1], n-1)
    exclude = knapsack_recursive(weights, values, capacity, n-1)

    return max(include, exclude)

# Test
values = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50
print(knapsack_recursive(weights, values, capacity))  # 220
```

#### Step 5: Memoization

```python
def knapsack_memo(weights, values, capacity):
    n = len(weights)
    memo = {}

    def helper(i, w):
        if i == 0 or w == 0:
            return 0

        if (i, w) in memo:
            return memo[(i, w)]

        if weights[i-1] > w:
            memo[(i, w)] = helper(i-1, w)
        else:
            include = values[i-1] + helper(i-1, w - weights[i-1])
            exclude = helper(i-1, w)
            memo[(i, w)] = max(include, exclude)

        return memo[(i, w)]

    return helper(n, capacity)

# Test
print(knapsack_memo([10, 20, 30], [60, 100, 120], 50))  # 220
```

#### Step 6: Tabulation

```python
def knapsack_tab(weights, values, capacity):
    n = len(weights)

    # Create DP table
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Fill table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                include = values[i-1] + dp[i-1][w - weights[i-1]]
                exclude = dp[i-1][w]
                dp[i][w] = max(include, exclude)
            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][capacity]

# Test
print(knapsack_tab([10, 20, 30], [60, 100, 120], 50))  # 220
```

**Trace (partial for capacity=50):**
```
weights = [10, 20, 30]
values  = [60, 100, 120]

         w=0  10  20  30  40  50
i=0 []    0   0   0   0   0   0
i=1 [10]  0  60  60  60  60  60
i=2 [20]  0  60 100 160 160 160
i=3 [30]  0  60 100 160 180 220

Reading dp[3][50]:
- Can include item 3 (weight 30 ≤ 50)
- Include: 120 + dp[2][20] = 120 + 100 = 220
- Exclude: dp[2][50] = 160
- Max = 220
```

#### Step 7: Space Optimization

```python
def knapsack_optimized(weights, values, capacity):
    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        # Iterate backwards to avoid using updated values
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])

    return dp[capacity]

# Test
print(knapsack_optimized([10, 20, 30], [60, 100, 120], 50))  # 220
```

**Time:** O(n × capacity)  
**Space:** O(capacity)

---

## Pattern 5: Partition DP

### Characteristics:
- Divide array/string into parts
- Optimize over all possible partition points
- Often nested loops: outer for end point, inner for partition point

---

### Problem 5.1: Palindrome Partitioning II

**Problem:** Given a string, partition it such that every substring is a palindrome. Return minimum cuts needed.

**Example:**
```
s = "aab"
Partition: "aa" | "b" (both palindromes)
Cuts: 1
```

#### Step 1: Build Intuition

For each position i, try all possible last partitions:
- If s[j:i+1] is palindrome, we can partition there
- Cost = cuts needed for s[0:j] + 1 cut

#### Step 2: Define State

`dp[i]` = minimum cuts needed for s[0:i+1]

Also need helper: `is_palindrome[i][j]` = whether s[i:j+1] is palindrome

#### Step 3: Solution

```python
def min_cut(s):
    n = len(s)

    # Precompute palindrome table
    is_palin = [[False] * n for _ in range(n)]

    # Every single character is palindrome
    for i in range(n):
        is_palin[i][i] = True

    # Check for length 2+
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                if length == 2:
                    is_palin[i][j] = True
                else:
                    is_palin[i][j] = is_palin[i+1][j-1]

    # DP for minimum cuts
    dp = [float('inf')] * n

    for i in range(n):
        if is_palin[0][i]:
            dp[i] = 0  # Entire string is palindrome, no cuts
        else:
            for j in range(i):
                if is_palin[j+1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)

    return dp[n-1]

# Test
print(min_cut("aab"))  # 1
print(min_cut("aaabba"))  # 1 (aaa|bba or aa|abba)
```

---

## Pattern 6: DP on Strings

### Problem 6.1: Edit Distance (Levenshtein Distance)

**Problem:** Given two strings, find minimum operations (insert, delete, replace) to convert one to another.

**Example:**
```
word1 = "horse"
word2 = "ros"

horse → rorse (replace 'h' with 'r')
rorse → rose (delete 'r')
rose → ros (delete 'e')

Answer: 3
```

#### Step 1: Build Intuition

Compare characters from start:
- If same: no operation needed, move both pointers
- If different: try all three operations, take minimum
  - **Insert:** Add char to word1, move pointer in word2
  - **Delete:** Remove char from word1, move pointer in word1
  - **Replace:** Change char in word1, move both pointers

#### Step 2: Define State

`dp[i][j]` = minimum operations to convert word1[0:i] to word2[0:j]

#### Step 3: Recurrence

```python
if word1[i-1] == word2[j-1]:
    dp[i][j] = dp[i-1][j-1]  # No operation needed
else:
    insert = dp[i][j-1] + 1
    delete = dp[i-1][j] + 1
    replace = dp[i-1][j-1] + 1
    dp[i][j] = min(insert, delete, replace)
```

#### Step 4: Tabulation

```python
def edit_distance(word1, word2):
    m, n = len(word1), len(word2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all chars from word1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all chars to match word2

    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                insert = dp[i][j-1] + 1
                delete = dp[i-1][j] + 1
                replace = dp[i-1][j-1] + 1
                dp[i][j] = min(insert, delete, replace)

    return dp[m][n]

# Test
print(edit_distance("horse", "ros"))  # 3
```

**Trace:**
```
      ""  r  o  s
""     0  1  2  3
h      1  1  2  3
o      2  2  1  2
r      3  2  2  2
s      4  3  3  2
e      5  4  4  3

Answer: dp[5][3] = 3
```

---

## Pattern 7: DP on Trees (Introduction)

### Problem 7.1: House Robber III

**Problem:** Binary tree where each node has money. Can't rob two directly connected nodes. Maximize money.

**Example:**
```
     3
    / \
   2   3
    \   \
     3   1

Rob root and leaves: 3 + 3 + 1 = 7
```

#### Solution

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rob_tree(root):
    def helper(node):
        if not node:
            return (0, 0)  # (rob, not_rob)

        left = helper(node.left)
        right = helper(node.right)

        # If rob current node, can't rob children
        rob = node.val + left[1] + right[1]

        # If don't rob current, take max of children
        not_rob = max(left) + max(right)

        return (rob, not_rob)

    return max(helper(root))
```

---

# Phase 4: Interview Conversion

## How to Identify DP in Interviews

### Signals That Scream DP:

1. **Keywords:**
   - "Minimum/maximum"
   - "Longest/shortest"
   - "Count number of ways"
   - "Is it possible to..."

2. **Problem characteristics:**
   - Optimization problem (min/max)
   - Counting problem (how many ways)
   - Decision at each step
   - Constraints that relate to past decisions

3. **Recursive structure:**
   - If you can express solution as f(n) = function(f(n-1), f(n-2), ...)
   - Problem can be broken into smaller similar subproblems

4. **Input constraints:**
   - Small array/string sizes (n ≤ 1000 suggests O(n²))
   - Two arrays/strings suggests 2D DP

### Not DP:

- **Greedy works:** If locally optimal choice always leads to global optimum
- **No overlap:** If subproblems don't repeat (use regular recursion)
- **Graph traversal:** BFS/DFS usually better
- **Very large constraints:** n > 10^5 might need greedy or other approach

---

## Interview Strategy: The 7-Step Process

### Step 1: Understand and Clarify (2 minutes)
- Restate the problem in your own words
- Ask about edge cases
- Clarify input constraints

### Step 2: Examples (2 minutes)
- Work through 2-3 examples manually
- Include edge cases
- This builds intuition

### Step 3: Identify Pattern (1 minute)
- "This looks like [pattern name] because..."
- "I can break this into subproblems where..."

### Step 4: Recursive Solution (5 minutes)
- Define state
- Write recurrence relation on whiteboard
- Code recursive solution
- "This is exponential, but it establishes correctness"

### Step 5: Memoization (5 minutes)
- Add memo dictionary
- Explain how this eliminates redundant computation
- Analyze time/space complexity

### Step 6: If Time Permits - Tabulation (5 minutes)
- Convert to bottom-up
- Show you understand both approaches

### Step 7: If Time Permits - Optimize Space (3 minutes)
- Reduce space complexity
- Shows mastery

---

## How to Explain DP to an Interviewer

### Bad Explanation:
"I'll use dynamic programming. Let me create the DP array..."

### Good Explanation:
"I notice this problem has overlapping subproblems - for example, when computing X, we'll compute Y multiple times. It also has optimal substructure because [explain]. So I'll start with a recursive solution to establish the logic, then optimize with memoization."

### Template:
1. **Identify:** "This is a DP problem because..."
2. **State:** "I'll define my state as..."
3. **Recurrence:** "The relationship between states is..."
4. **Base case:** "The simplest cases are..."
5. **Complexity:** "This will be O(...) time and O(...) space"

---

## Common Traps and How to Avoid Them

### Trap 1: Jumping to DP Too Fast
**Problem:** You see "minimum/maximum" and immediately start writing DP code.
**Solution:** First check if greedy works. Prove to yourself why DP is needed.

### Trap 2: Wrong State Definition
**Problem:** State doesn't capture all information needed to make decisions.
**Solution:** Ask: "What do I need to know to solve this subproblem independently?"

**Example:**
```
Problem: "Find max sum subarray of length k"
Wrong state: dp[i] = max sum ending at i
Right state: dp[i][len] = max sum ending at i with length len
```

### Trap 3: Off-by-One Errors in Index
**Problem:** Confusing dp[i] representing "first i elements" vs "element at index i"
**Solution:** Be explicit in state definition. Write it down.

### Trap 4: Wrong Iteration Order in Tabulation
**Problem:** Accessing dp[i-1] before it's computed
**Solution:** Draw dependencies, fill in correct order

### Trap 5: Not Handling Edge Cases
**Problem:** Forgot n=0, n=1, or empty array cases
**Solution:** Always write base cases first

---

## Debugging DP Solutions

### Debug Checklist:

1. **Print DP table:**
```python
# After computation
for row in dp:
    print(row)
```

2. **Verify base cases:**
- Check dp[0], dp[0][0], first row, first column
- Do they match your expectation?

3. **Trace small example by hand:**
- Pick n=3 or n=4
- Fill DP table manually
- Compare with code output

4. **Check recurrence:**
- Is the mathematical relation correct?
- Are you using right indices?

5. **Verify iteration order:**
- Are you filling table in correct order?
- For memoization, are you checking memo before computing?

---

## Practice Roadmap

### Week 1: Foundations
- Fibonacci (all 3 approaches)
- Climbing Stairs
- Min Cost Climbing Stairs
- House Robber

**Goal:** Master 1D DP and understand recursion→memoization→tabulation flow

### Week 2: 2D DP
- Unique Paths
- Minimum Path Sum
- Longest Common Subsequence
- Edit Distance

**Goal:** Get comfortable with 2D state

### Week 3: Knapsack & Subsequences
- 0/1 Knapsack
- Subset Sum
- Longest Increasing Subsequence
- Coin Change

**Goal:** Recognize knapsack pattern

### Week 4: Advanced Patterns
- Palindrome Partitioning
- Word Break
- Decode Ways
- Egg Drop

**Goal:** Handle partition and string DP

### Week 5: MAANG Interview Questions
- Best Time to Buy/Sell Stock (all variants)
- Burst Balloons
- Distinct Subsequences
- Regular Expression Matching
- Interleaving String

**Goal:** Apply patterns to hard problems

---

## Interview Mindset

### What Interviewers Look For:

1. **Structured thinking:** Do you follow a process or just code randomly?
2. **Communication:** Can you explain your thought process?
3. **Optimization awareness:** Do you know multiple approaches?
4. **Edge case handling:** Do you think about corner cases?
5. **Code quality:** Clean, readable, bug-free?

### If You're Stuck:

1. **Go back to examples:** Work through manually
2. **Start with brute force:** Even if it's exponential
3. **Draw the recursion tree:** Visualize the problem
4. **Think about state:** What varies between subproblems?
5. **Ask for hint:** Better than sitting silent for 10 minutes

### Time Management:

- 15 minutes stuck? Ask for help
- 20 minutes passed? Should have recursive solution
- 30 minutes passed? Should have memoization
- 40 minutes? Discuss optimizations or move to test cases

---

## Quick Reference: DP Patterns

| Pattern | State | Example Problems |
|---------|-------|------------------|
| **1D Linear** | dp[i] = answer for position i | Fibonacci, Climbing Stairs, House Robber |
| **2D Grid** | dp[i][j] = answer for cell (i,j) | Unique Paths, Min Path Sum |
| **Subsequence** | dp[i][j] = answer for seq1[0:i] and seq2[0:j] | LCS, Edit Distance |
| **Knapsack** | dp[i][w] = answer for first i items, capacity w | 0/1 Knapsack, Partition Equal Subset |
| **Partition** | dp[i] = min cost for s[0:i] | Palindrome Partitioning, Word Break |
| **String DP** | dp[i][j] = answer for substring i to j | Longest Palindromic Substring |
| **Tree DP** | (rob, not_rob) per node | House Robber III |

---

## Final Checklist Before Interview

**Can you:**

- [ ] Identify when a problem needs DP?
- [ ] Write recursive solution first?
- [ ] Convert recursion to memoization?
- [ ] Convert memoization to tabulation?
- [ ] Analyze time and space complexity?
- [ ] Optimize space when possible?
- [ ] Handle edge cases (n=0, n=1, empty input)?
- [ ] Explain your approach clearly?
- [ ] Debug your DP table?
- [ ] Solve at least one problem from each pattern?

**If you answered yes to all, you're interview-ready.**

---

## Closing Thoughts

Dynamic Programming is not about memorizing patterns or formulas. It's a way of thinking:

1. **Break problems into subproblems**
2. **Recognize when subproblems overlap**
3. **Remember solutions to avoid recomputation**

Start with recursion (intuitive), add memoization (optimization), then tabulation if needed (further optimization).

Every DP problem you solve strengthens your pattern recognition. The first 10 will be hard. The next 20 will be easier. After 50, you'll recognize patterns instantly.

**Practice deliberately. Solve problems. Fail. Learn. Repeat.**

Good luck with your interviews!

---

*Remember: The goal is not to memorize solutions, but to build the thinking framework that lets you solve any DP problem you encounter.*
