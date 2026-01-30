# Dynamic Programming: From Foundations to MAANG Interviews

**A Senior Engineer's Guide to Mastering DP**

---

## Table of Contents

1. [Phase 1: Foundations](#phase-1-foundations)
2. [Phase 2: How to Think in DP](#phase-2-how-to-think-in-dp)
3. [Phase 3: Pattern Mastery](#phase-3-pattern-mastery)
4. [Phase 4: Interview Conversion](#phase-4-interview-conversion)
5. [Quick Reference & Checklists](#quick-reference--checklists)

---

# PHASE 1: FOUNDATIONS

## What Dynamic Programming Really Is (Not the Textbook Definition)

### The Honest Definition

Dynamic Programming is **a way to avoid repeating the same calculations by storing results you've already computed**.

That's it. No fancy math. No mystical formulas.

### The Real-World Intuition

Imagine you're planning a road trip:

```
City A → City B → City C → City D → City E
```

**Without DP (naive recursion):**
- You calculate the best route from A to E
- This depends on the best route from B to E
- This depends on the best route from C to E
- And so on...
- But while calculating routes, you might recalculate "best route from C to E" hundreds of times

**With DP:**
- You calculate "best route from C to E" once
- You store it
- Whenever you need it again, you just look it up (instead of recalculating)

### Why This Matters

**Time Explosion Example:**

```python
# Fibonacci without DP - exponential explosion
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# fib(5) calls:
#       fib(5)
#      /      \
#   fib(4)   fib(3)
#   /    \    /   \
# fib(3) fib(2) fib(2) fib(1)
# /  \
# fib(2) fib(1)

# Notice: fib(2) and fib(3) are calculated multiple times!
# For fib(40), we make ~300 MILLION function calls
# For fib(50), we make ~40 BILLION function calls
# This grows exponentially → O(2^n)
```

**With DP:**
- fib(40) takes microseconds
- fib(1000) is still fast
- We trade computation time for memory

---

## The Two Key Concepts: Overlapping Subproblems & Optimal Substructure

### 1. Overlapping Subproblems

**Definition:** The same smaller problem is solved multiple times.

**Example: Climbing Stairs**

```
Problem: You're at floor 0, want to reach floor 5.
Each step, you can climb 1 or 2 floors.
How many ways to reach floor 5?

Recursive breakdown:
ways(5) = ways(4) + ways(3)
ways(4) = ways(3) + ways(2)
ways(3) = ways(2) + ways(1)

Notice: ways(3), ways(2), ways(1) are calculated MULTIPLE times!
- ways(3) is needed for both ways(5) and ways(4)
- ways(2) is needed for ways(4), ways(3)
- This is "overlapping subproblems"
```

**How to Detect:**
- Do you see the same function call appearing multiple times in the recursion tree?
- If yes → overlapping subproblems exist → DP can help

### 2. Optimal Substructure

**Definition:** The optimal solution to a problem contains optimal solutions to its subproblems.

**Example: Longest Increasing Subsequence**

```
Array: [10, 9, 2, 5, 3, 7, 101, 18]

If the LIS ending at position 3 (value=5) is [2, 3, 5]
Then we know: the LIS up to position 2 must be [2, 3]

Why? Because if LIS up to position 2 had any extra elements,
then LIS ending at position 3 would be longer.

This is optimal substructure:
"Optimal solution contains optimal solutions to subproblems"
```

**How to Detect:**
- Can you express the optimal solution in terms of optimal solutions to smaller problems?
- If yes → optimal substructure exists → DP is applicable

### When BOTH Exist

```
✓ Overlapping subproblems → Repeating calculations waste time
✓ Optimal substructure → We can build solutions from smaller solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ This is when DP shines
```

---

## Why Recursion Alone Fails: The Time Explosion

### Fibonacci: The Classic Failure Case

```python
# Without DP
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)

# Time complexity: O(2^n) ← EXPONENTIAL!
# Space complexity: O(n) ← call stack depth

# Test:
# fib_recursive(40) → takes ~20 seconds
# fib_recursive(50) → takes ~lifetime
```

**Why does it explode?**

```
fib(5) calls:
- fib(4) and fib(3)
- fib(4) calls fib(3) and fib(2)
- So fib(3) is called twice
- Each level multiplies the calls by ~2
- By fib(40), we have 2^40 ≈ 1 trillion calls

Work tree doubles at each level → exponential growth
```

**The core issue:**
- Recursion naturally explores all possibilities
- Without memory of past results, it recalculates everything
- For overlapping subproblems, this is catastrophic

---

## Three Approaches: Recursion → Memoization → Tabulation

### Approach 1: Pure Recursion (No Optimization)

```python
def fib(n):
    """
    Simple recursion - explores all possibilities.
    NO caching, NO optimization.
    Time: O(2^n)
    Space: O(n) call stack
    """
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# Dry run for fib(5):
# fib(5)
#   fib(4)
#     fib(3)
#       fib(2)
#         fib(1) + fib(0)
#       fib(1)
#     fib(2)
#       fib(1) + fib(0)
#   fib(3)
#     fib(2)
#       fib(1) + fib(0)
#     fib(1)
# Notice: fib(2), fib(3), fib(1) are calculated MANY times
```

**When to use:** Only for learning / small n values

---

### Approach 2: Memoization (Top-Down DP)

```python
def fib_memo(n, memo=None):
    """
    Memoization: remember results as you compute.
    Top-down: start from the goal, work down to base cases.
    Time: O(n)
    Space: O(n)
    """
    if memo is None:
        memo = {}
    
    # Check if already computed
    if n in memo:
        return memo[n]
    
    # Base case
    if n <= 1:
        return n
    
    # Compute and store
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# Dry run for fib(5):
# fib(5) → compute, store in memo
#   fib(4) → compute, store in memo
#     fib(3) → compute, store in memo
#       fib(2) → compute, store in memo
#         fib(1) → return 1
#         fib(0) → return 0
#       memo[2] = 1
#     fib(2) → FOUND IN MEMO! Return 1 (no recursion)
#   memo[3] = 2
# fib(3) → FOUND IN MEMO! Return 2
# Result stored in memo: {1: 1, 0: 0, 2: 1, 3: 2, 4: 3, 5: 5}

# Each value computed exactly once → O(n) time
```

**Key insight:**
- Same recursion structure as pure recursion
- But we check memo first: "Have I seen this input before?"
- If yes: instant answer (O(1) lookup)
- If no: compute once, store for future
- Each unique subproblem solved exactly once

**When to use:**
- When you're thinking recursively
- When it's hard to identify the iteration order
- In interviews (shows you understand the concept)

---

### Approach 3: Tabulation (Bottom-Up DP)

```python
def fib_tab(n):
    """
    Tabulation: fill a table from bottom up.
    Bottom-up: start from base cases, build up to the goal.
    Time: O(n)
    Space: O(n)
    """
    if n <= 1:
        return n
    
    # Create table
    dp = [0] * (n + 1)
    dp[1] = 1
    
    # Fill from bottom up
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

# Dry run for fib(5):
# dp = [0, 1, 0, 0, 0, 0]
# i = 2: dp[2] = dp[1] + dp[0] = 1 + 0 = 1
#        dp = [0, 1, 1, 0, 0, 0]
# i = 3: dp[3] = dp[2] + dp[1] = 1 + 1 = 2
#        dp = [0, 1, 1, 2, 0, 0]
# i = 4: dp[4] = dp[3] + dp[2] = 2 + 1 = 3
#        dp = [0, 1, 1, 2, 3, 0]
# i = 5: dp[5] = dp[4] + dp[3] = 3 + 2 = 5
#        dp = [0, 1, 1, 2, 3, 5]
# Return dp[5] = 5
```

**Key insight:**
- No recursion, pure iteration
- Build solutions from smallest subproblems upward
- Each value computed exactly once → O(n) time
- No call stack overhead → often faster in practice

**When to use:**
- When you can identify the iteration order clearly
- When you want guaranteed O(n) space (can optimize)
- In production code (usually faster, no recursion overhead)

---

### Space Optimization: Tabulation Only

```python
def fib_optimized(n):
    """
    Space-optimized tabulation.
    Observation: fib(i) only needs fib(i-1) and fib(i-2)
    We don't need to store the entire array.
    Time: O(n)
    Space: O(1) ← CONSTANT SPACE!
    """
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    for i in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr

# Dry run for fib(5):
# i = 2: prev=1, curr=0+1=1
# i = 3: prev=1, curr=1+1=2
# i = 4: prev=2, curr=1+2=3
# i = 5: prev=3, curr=2+3=5
# Return 5

# Space: O(1) - only 2 variables
```

**This is the final form for simple problems!**

---

### Comparison Table

| Aspect | Recursion | Memoization | Tabulation | Optimized Tab |
|--------|-----------|-------------|------------|---|
| **Time** | O(2^n) | O(n) | O(n) | O(n) |
| **Space** | O(n) stack | O(n) memo | O(n) array | O(1) |
| **Intuitive** | ✓ | ✓✓ | ✗ | ✗ |
| **Easy to code** | ✓ | ✓ | ✓ | - |
| **Fast in practice** | ✗ | ✓ | ✓✓ | ✓✓✓ |
| **Call stack** | O(n) | O(n) | None | None |
| **When to use** | Learning | Interviews | Production | Final answer |

---

# PHASE 2: HOW TO THINK IN DP

## The DP Thinking Framework (Mental Checklist)

This is the **most important section**. Use this framework for EVERY DP problem.

### Step 1: Define the State

**What does the state represent?**

The state is **what you're computing**. It answers: "What subproblem are we solving?"

```
Examples:
- fib(n) → state is: "What is the n-th Fibonacci number?"
- dp[i] → state is: "What is the max profit ending at index i?"
- dp[i][j] → state is: "What is the shortest path from (0,0) to (i,j)?"
- dp[i][w] → state is: "What is max value with weight limit w, using items 0..i?"
```

**How to identify state:**

1. Look at the recursive function parameters
2. Ask: "What information uniquely defines this subproblem?"
3. Those parameters are your state

```python
# Example: Climbing Stairs
# Recursive: how many ways to reach floor n?
# Function: ways(n) - parameter is n
# State: dp[i] = "number of ways to reach floor i"

# Example: Coin Change
# Recursive: min coins needed for amount n?
# Function: minCoins(amount, coins)
# State: dp[i] = "min coins needed for amount i"
# (we store coins implicitly - it doesn't change)

# Example: 2D Grid
# Recursive: paths from (0,0) to (i,j)?
# Function: paths(i, j)
# State: dp[i][j] = "number of paths to position (i,j)"
```

**Red flag:** If you can't clearly explain what dp[i] means, you haven't defined the state correctly.

---

### Step 2: Write the Recurrence Relation

**How do we compute the state from smaller states?**

The recurrence relation is the **formula that connects subproblems**.

```
Format: dp[state] = f(dp[smaller_state_1], dp[smaller_state_2], ...)

Examples:
- Fibonacci: dp[i] = dp[i-1] + dp[i-2]
- Climbing Stairs: dp[i] = dp[i-1] + dp[i-2]
- Max Sum Subarray: dp[i] = max(arr[i], dp[i-1] + arr[i])
- LCS: dp[i][j] = dp[i-1][j-1] if s1[i]==s2[j] else max(dp[i-1][j], dp[i][j-1])
```

**How to derive the recurrence:**

1. Assume you already have solutions to smaller subproblems
2. Think: "How can I combine them to get my current answer?"
3. Enumerate all possibilities (if-else, min/max, etc.)

**Example: Climbing Stairs (visual derivation)**

```
Problem: Reach floor n. Each step: +1 or +2 floors.

Recursive thinking:
- To reach floor n, where did I come from?
- Option 1: I was at floor (n-1) and took a 1-floor step
- Option 2: I was at floor (n-2) and took a 2-floor step
- These are the ONLY two options

So: ways(n) = ways(n-1) + ways(n-2)
Because: ways(n-1) gives me all ways to reach n-1, then +1 step = n
         ways(n-2) gives me all ways to reach n-2, then +2 steps = n

Recurrence: dp[i] = dp[i-1] + dp[i-2]
```

**Example: Max Sum Subarray (Kadane's Algorithm)**

```
Problem: Find max sum of any contiguous subarray.
Array: [−2, 1, −3, 4, −1, 2, 1, −5, 4]

Recursive thinking:
- To maximize sum ending at position i, what can I do?
- Option 1: Start fresh at i → sum = arr[i]
- Option 2: Extend previous subarray → sum = (max_ending_at_i-1) + arr[i]

Why? Because if (max_ending_at_i-1) is negative, starting fresh is better.
     If (max_ending_at_i-1) is positive, extending is better.

Recurrence: dp[i] = max(arr[i], dp[i-1] + arr[i])

Dry run:
arr = [−2, 1, −3, 4, −1, 2, 1, −5, 4]
dp[0] = -2
dp[1] = max(1, -2+1) = max(1, -1) = 1
dp[2] = max(-3, 1-3) = max(-3, -2) = -2
dp[3] = max(4, -2+4) = max(4, 2) = 4
dp[4] = max(-1, 4-1) = max(-1, 3) = 3
dp[5] = max(2, 3+2) = max(2, 5) = 5
dp[6] = max(1, 5+1) = max(1, 6) = 6
dp[7] = max(-5, 6-5) = max(-5, 1) = 1
dp[8] = max(4, 1+4) = max(4, 5) = 5

Answer: max(dp) = 6 (subarray [4, -1, 2, 1])
```

---

### Step 3: Identify Base Cases

**What are the simplest subproblems that need no recursion?**

Base cases are where **you stop the recursion and return a known answer**.

```
Examples:
- Fibonacci: fib(0) = 0, fib(1) = 1
- Climbing Stairs: dp[0] = 1 (one way: stay there), dp[1] = 1
- Coin Change: dp[0] = 0 (zero coins for zero amount)
- LCS: If either string is empty, LCS = 0
- Grid Paths: dp[0][j] = 1 for all j, dp[i][0] = 1 for all i
```

**How to identify base cases:**

1. What's the smallest input?
2. What's the answer for that input?
3. Can you compute it directly without recursion?

**Example: Climbing Stairs**

```
Smallest inputs:
- n=0: Already at floor 0. Ways to reach floor 0? = 1 (do nothing)
- n=1: Need to reach floor 1. Ways? = 1 (only +1 step)

Why 1? Because there's exactly one way to reach each.

If we think recursively:
- ways(2) = ways(1) + ways(0) = 1 + 1 = 2 ✓
- This matches: we can do [+1,+1] or [+2]
```

**Red flag:** If your base case is wrong, entire DP solution is wrong.

---

### Step 4: Decide DP Array Dimensions

**What shape should our DP array be?**

The dimensions follow from the state definition.

```
1D Problem:
- State: dp[i] → 1D array
- Example: Fibonacci, Climbing Stairs, Coin Change, LIS, LCS

2D Problem:
- State: dp[i][j] → 2D array
- Example: Grid paths, LCS, Edit Distance, Knapsack with conditions

3D+ Problem:
- State: dp[i][j][k] → 3D array (rare, but possible)
- Example: DP on trees with multiple dimensions
```

**How to decide:**

1. How many independent parameters in your state?
2. That's your number of dimensions
3. What's the range of each parameter?
4. That's the size of each dimension

**Example: Coin Change**

```
Problem: Minimum coins for given amount
Parameters: amount (0 to target)
State: dp[amount] = min coins needed
Array: 1D of size (target + 1)

dp[0] = 0
dp[1] = ?
dp[2] = ?
...
dp[target] = answer
```

**Example: 0/1 Knapsack**

```
Problem: Max value with weight limit, choosing from items
Parameters: 
  - item_index (0 to n-1)
  - weight_limit (0 to W)
State: dp[i][w] = max value using items 0..i with weight limit w
Array: 2D of size (n+1) × (W+1)

dp[0][0] = 0
dp[0][w] = 0 for all w (no items)
dp[i][0] = 0 for all i (no weight capacity)
...
dp[n][W] = answer
```

---

### Step 5: Choose Memoization vs Tabulation

**When should you use which approach?**

#### Memoization (Top-Down)

**Use when:**
- The recursion structure is complex
- It's hard to identify the iteration order
- You need to explore a sparse subproblem space
- You're in an interview (shows deeper thinking)

**Advantages:**
- Follows natural recursive thinking
- Only computes needed subproblems (sparse exploration)
- Easy to understand and verify

**Disadvantages:**
- Call stack overhead (recursion depth)
- Harder to optimize space
- Might hit stack overflow on deep recursion

```python
# Use memoization for:
# - Tree DP (naturally recursive)
# - Recursive exploration (not all subproblems visited)
# - Complex recurrences

def solve(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    # ... recurrence logic ...
    memo[n] = result
    return result
```

#### Tabulation (Bottom-Up)

**Use when:**
- The iteration order is clear
- You need to visit all subproblems
- You want to optimize space/time further
- You're in production code

**Advantages:**
- No recursion overhead (pure loops)
- Easy to optimize (sliding window, etc.)
- Predictable performance
- Clear iteration order

**Disadvantages:**
- Must compute all subproblems (even unneeded ones)
- Requires identifying the correct iteration order
- Sometimes harder to derive initially

```python
# Use tabulation for:
# - Linear DP (clear iteration order)
# - Optimization-critical code
# - When you want space optimization

for i in range(1, n+1):
    dp[i] = recurrence(dp[i-1], dp[i-2], ...)
```

**Decision tree:**

```
Does the recurrence naturally flow upward (small → large)?
  YES → Tabulation
  NO → Memoization

Is recursion depth potentially very deep?
  YES → Tabulation
  NO → Either (preference-based)

Do you need space optimization?
  YES → Tabulation
  NO → Either

In an interview?
  Memoization first (show understanding), then optimize with tabulation
```

---

## The Complete Mental Checklist

**When you see a new DP problem, follow this checklist:**

```
[ ] 1. Understand the problem statement
      - What are we optimizing? (max/min/count)
      - What are the constraints?
      - What are the inputs and outputs?

[ ] 2. Identify if DP applies
      - Does the problem have overlapping subproblems?
      - Does it have optimal substructure?
      - If unsure, think recursively first

[ ] 3. Define the state clearly
      - Write: "dp[i] = ..."
      - Make it so specific that someone reading it understands exactly what you're computing
      - Red flag: If it's vague, rethink

[ ] 4. Write the recurrence relation
      - How do you compute dp[state] from smaller states?
      - Enumerate all possibilities (if-else, min/max, sum, etc.)
      - Verify with examples

[ ] 5. Identify base cases
      - What's the smallest input?
      - What's the answer for that input?
      - Verify that recurrence doesn't apply to base case

[ ] 6. Decide array dimensions
      - How many independent parameters in state?
      - What's the range of each?
      - Calculate space complexity

[ ] 7. Choose approach
      - Memoization or Tabulation?
      - Decision based on recurrence structure and interview context

[ ] 8. Code the solution
      - Implement carefully (off-by-one errors are common)
      - Use clear variable names
      - Add comments for non-obvious logic

[ ] 9. Verify with small examples
      - Dry run through the algorithm
      - Check base cases
      - Check edge cases (n=0, n=1, empty input, etc.)

[ ] 10. Optimize space (if needed)
       - Can you reduce dimensions?
       - Can you use rolling arrays?
       - Is space optimization worth the added complexity?

[ ] 11. Analyze complexity
       - Time: number of states × work per state
       - Space: array size (before optimization)
       - Communicate these clearly
```

---

# PHASE 3: PATTERN MASTERY

## Pattern 1: 1D DP - Linear Sequences

### 1.1 Fibonacci Sequence

**Problem:** Find the n-th Fibonacci number.

**Intuition:**

```
The Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, ...

Each number is the sum of the previous two.
Why? No specific reason - it's just the definition.
But it DOES have overlapping subproblems:
- fib(5) needs fib(4) and fib(3)
- fib(4) needs fib(3) and fib(2)
- fib(3) is computed twice

This is a perfect DP candidate.
```

**Applying the Framework:**

```
State: dp[i] = the i-th Fibonacci number
Recurrence: dp[i] = dp[i-1] + dp[i-2]
Base cases: dp[0] = 0, dp[1] = 1
Array: 1D of size (n+1)
```

**Recursive Solution (for reference):**

```python
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)
# Time: O(2^n) - don't use this
```

**Memoization (Top-Down):**

```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# Time: O(n) - each number computed once
# Space: O(n) - memo size + recursion depth
```

**Tabulation (Bottom-Up):**

```python
def fib_tab(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

# Time: O(n)
# Space: O(n)
```

**Space-Optimized Tabulation:**

```python
def fib_optimized(n):
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    
    return prev1

# Time: O(n)
# Space: O(1) ← only two variables
```

**Interview Answer:**

```
"To find the n-th Fibonacci number:

1. State: dp[i] = the i-th Fibonacci number
2. Recurrence: dp[i] = dp[i-1] + dp[i-2]
3. Base: dp[0] = 0, dp[1] = 1
4. Approach: Tabulation with space optimization

The key insight is that we don't need the entire array - just the last two values.

Time: O(n), Space: O(1)
"
```

---

### 1.2 Climbing Stairs

**Problem:** You're at step 0. Each move, you climb 1 or 2 steps. How many ways to reach step n?

**Intuition:**

```
Ways to reach step n:
- You were at step n-1 and took a 1-step (one option)
- You were at step n-2 and took a 2-step (one option)

Total ways = ways(n-1) + ways(n-2)

Because these two sets of "ways" are mutually exclusive and cover all possibilities.
```

**Applying the Framework:**

```
State: dp[i] = number of ways to reach step i
Recurrence: dp[i] = dp[i-1] + dp[i-2]
Base cases: 
  - dp[0] = 1 (already there, one way: do nothing)
  - dp[1] = 1 (only one way: take one 1-step)
Array: 1D of size (n+1)
```

**Dry Run (n=5):**

```
dp[0] = 1
dp[1] = 1
dp[2] = dp[1] + dp[0] = 1 + 1 = 2 (ways: [1,1], [2])
dp[3] = dp[2] + dp[1] = 2 + 1 = 3 (ways: [1,1,1], [1,2], [2,1])
dp[4] = dp[3] + dp[2] = 3 + 2 = 5
dp[5] = dp[4] + dp[3] = 5 + 3 = 8

Answer: 8 ways
```

**Code (Tabulation with Optimization):**

```python
def climbStairs(n):
    if n == 1:
        return 1
    
    prev2, prev1 = 1, 1
    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    
    return prev1

# Time: O(n)
# Space: O(1)
```

**Variation:** What if you can climb 1, 2, or 3 steps?

```python
def climbStairs_variation(n):
    # dp[i] = ways to reach step i
    # Recurrence: dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
    # Because you can come from (i-1), (i-2), or (i-3)
    
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[0], dp[1], dp[2] = 1, 1, 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
    
    return dp[n]
```

---

### 1.3 Coin Change

**Problem:** Given coins and a target amount, find the minimum number of coins needed.

**Intuition:**

```
To make amount n using minimum coins:
- Try using each coin type
- For coin c: I'd have (n - c) remaining
- Total coins = 1 + minCoins(n - c)
- Take the minimum across all coin types

Recurrence: dp[i] = 1 + min(dp[i - coin] for each coin type)
```

**Applying the Framework:**

```
State: dp[i] = minimum coins needed for amount i
Recurrence: dp[i] = 1 + min(dp[i - coin] for coin in coins if coin <= i)
Base case: dp[0] = 0 (no coins needed for 0 amount)
Array: 1D of size (amount + 1)
```

**Dry Run (coins=[1,2,5], amount=5):**

```
dp[0] = 0
dp[1] = 1 + min(dp[1-1]) = 1 + dp[0] = 1 (coin 1)
dp[2] = 1 + min(dp[2-1], dp[2-2]) = 1 + min(dp[1], dp[0]) = 1 + 0 = 1 (coin 2)
dp[3] = 1 + min(dp[3-1], dp[3-2]) = 1 + min(dp[2], dp[1]) = 1 + 1 = 2 (coins 1,2)
dp[4] = 1 + min(dp[4-1], dp[4-2]) = 1 + min(dp[3], dp[2]) = 1 + 1 = 2 (coins 2,2)
dp[5] = 1 + min(dp[5-1], dp[5-2], dp[5-5]) = 1 + min(dp[4], dp[3], dp[0]) = 1 + 0 = 1 (coin 5)

Answer: 1 coin
```

**Code:**

```python
def coinChange(coins, amount):
    # dp[i] = minimum coins for amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], 1 + dp[i - coin])
    
    return dp[amount] if dp[amount] != float('inf') else -1

# Time: O(amount * len(coins))
# Space: O(amount)
```

**Common Mistake:** Forgetting to handle the case where amount is impossible.

```python
# Check if dp[amount] is still infinity
return -1 if dp[amount] == float('inf') else dp[amount]
```

---

## Pattern 2: 2D DP - Grid and Sequences

### 2.1 Grid Paths (Unique Paths)

**Problem:** In an m×n grid, start at (0,0), end at (m-1,n-1). Can only move right or down. Count unique paths.

**Intuition:**

```
To reach cell (i,j):
- You came from cell (i-1,j) (from above) OR
- You came from cell (i,j-1) (from left)

Total paths to (i,j) = paths_to(i-1,j) + paths_to(i,j-1)

Why? These are mutually exclusive: each path either came from above or left, not both.
```

**Applying the Framework:**

```
State: dp[i][j] = number of unique paths to reach (i,j)
Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1]
Base cases: 
  - dp[0][j] = 1 for all j (only one way: move right)
  - dp[i][0] = 1 for all i (only one way: move down)
Array: 2D of size m × n
```

**Dry Run (m=3, n=3):**

```
Grid indices:
(0,0) (0,1) (0,2)
(1,0) (1,1) (1,2)
(2,0) (2,1) (2,2)

Initial:
dp[0][0]=1  dp[0][1]=1  dp[0][2]=1
dp[1][0]=1  dp[1][1]=?  dp[1][2]=?
dp[2][0]=1  dp[2][1]=?  dp[2][2]=?

Fill:
dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2
dp[1][2] = dp[0][2] + dp[1][1] = 1 + 2 = 3
dp[2][1] = dp[1][1] + dp[2][0] = 2 + 1 = 3
dp[2][2] = dp[1][2] + dp[2][1] = 3 + 3 = 6

Final:
dp[0][0]=1  dp[0][1]=1  dp[0][2]=1
dp[1][0]=1  dp[1][1]=2  dp[1][2]=3
dp[2][0]=1  dp[2][1]=3  dp[2][2]=6

Answer: 6 unique paths
```

**Code:**

```python
def uniquePaths(m, n):
    # dp[i][j] = unique paths to (i,j)
    dp = [[0] * n for _ in range(m)]
    
    # Base cases
    for i in range(m):
        dp[i][0] = 1
    for j in range(n):
        dp[0][j] = 1
    
    # Fill
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[m-1][n-1]

# Time: O(m*n)
# Space: O(m*n)
```

**Space Optimization:**

```python
def uniquePaths_optimized(m, n):
    # We only need the previous row
    prev = [1] * n
    
    for i in range(1, m):
        curr = [1] * n
        for j in range(1, n):
            curr[j] = prev[j] + curr[j-1]
        prev = curr
    
    return prev[n-1]

# Time: O(m*n)
# Space: O(n) ← only one row
```

---

### 2.2 Longest Common Subsequence (LCS)

**Problem:** Given two strings, find the longest subsequence common to both.

**Intuition:**

```
Subsequence: a sequence that appears in the same order, but not necessarily contiguous.

Example:
s1 = "abcde"
s2 = "ace"

LCS = "ace" (length 3)

Why? We need to compare characters:
- If s1[i] == s2[j]: they match, include in LCS
  LCS using both = 1 + LCS(s1[0..i-1], s2[0..j-1])
  
- If s1[i] != s2[j]: don't match, try both options
  LCS = max(LCS(s1[0..i-1], s2[0..j]), LCS(s1[0..i], s2[0..j-1]))
  "Does the match come from the rest of s1 or the rest of s2?"
```

**Applying the Framework:**

```
State: dp[i][j] = length of LCS of s1[0..i-1] and s2[0..j-1]
Recurrence:
  if s1[i-1] == s2[j-1]:
    dp[i][j] = 1 + dp[i-1][j-1]
  else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
Base cases: 
  - dp[0][j] = 0 for all j (empty s1, LCS = 0)
  - dp[i][0] = 0 for all i (empty s2, LCS = 0)
Array: 2D of size (len(s1)+1) × (len(s2)+1)
```

**Dry Run (s1="abc", s2="ac"):**

```
Strings:
s1 = "abc"
s2 = "ac"

DP table (rows = s1, cols = s2):
    ""  "a"  "c"
""   0   0    0
"a"  0   ?    ?
"b"  0   ?    ?
"c"  0   ?    ?

Fill:
Row 1 (s1[0]="a"):
  dp[1][1]: s1[0]="a" == s2[0]="a" ? YES → 1 + dp[0][0] = 1
  dp[1][2]: s1[0]="a" == s2[1]="c" ? NO → max(dp[0][2], dp[1][1]) = max(0, 1) = 1

Row 2 (s1[1]="b"):
  dp[2][1]: s1[1]="b" == s2[0]="a" ? NO → max(dp[1][1], dp[2][0]) = max(1, 0) = 1
  dp[2][2]: s1[1]="b" == s2[1]="c" ? NO → max(dp[1][2], dp[2][1]) = max(1, 1) = 1

Row 3 (s1[2]="c"):
  dp[3][1]: s1[2]="c" == s2[0]="a" ? NO → max(dp[2][1], dp[3][0]) = max(1, 0) = 1
  dp[3][2]: s1[2]="c" == s2[1]="c" ? YES → 1 + dp[2][1] = 1 + 1 = 2

Table:
    ""  "a"  "c"
""   0   0    0
"a"  0   1    1
"b"  0   1    1
"c"  0   1    2

Answer: dp[3][2] = 2, LCS = "ac"
```

**Code:**

```python
def longestCommonSubsequence(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

# Time: O(m*n)
# Space: O(m*n)
```

**Interview Variation:** Also return the LCS string.

```python
def longestCommonSubsequence_withString(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Backtrack to find the string
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            lcs.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return "".join(reversed(lcs))
```

---

## Pattern 3: Subsequence DP

### 3.1 Longest Increasing Subsequence (LIS)

**Problem:** Find the length of the longest strictly increasing subsequence.

**Intuition:**

```
Subsequence: elements in the same order, but not necessarily contiguous.
Increasing: each element is strictly greater than the previous.

Example:
arr = [10, 9, 2, 5, 3, 7, 101, 18]
LIS = [2, 3, 7, 101] or [2, 5, 7, 101] or [2, 5, 7, 18] (length 4)

Key insight:
- dp[i] = LIS length ending at index i
- To compute dp[i], look at all previous elements j < i
- If arr[j] < arr[i], we can extend the LIS ending at j
- Take the maximum extension
```

**Applying the Framework:**

```
State: dp[i] = length of LIS ending at index i
Recurrence: 
  dp[i] = 1 + max(dp[j] for all j < i where arr[j] < arr[i])
  (or 1 if no such j exists)
Base case: dp[i] = 1 for all i (each element alone is a subsequence of length 1)
Array: 1D of size n
```

**Dry Run (arr=[10,9,2,5,3,7,101,18]):**

```
i=0, arr[0]=10:
  No previous elements → dp[0] = 1 (LIS: [10])

i=1, arr[1]=9:
  j=0: arr[0]=10 > arr[1]=9 ? Can't extend
  → dp[1] = 1 (LIS: [9])

i=2, arr[2]=2:
  j=0,1: arr[0]=10 > arr[2]=2, arr[1]=9 > arr[2]=2 ? Can't extend
  → dp[2] = 1 (LIS: [2])

i=3, arr[3]=5:
  j=0: arr[0]=10 > arr[3]=5 ? No
  j=1: arr[1]=9 > arr[3]=5 ? No
  j=2: arr[2]=2 < arr[3]=5 ? YES → can extend dp[2]
  → dp[3] = 1 + dp[2] = 1 + 1 = 2 (LIS: [2,5])

i=4, arr[4]=3:
  j=2: arr[2]=2 < arr[4]=3 ? YES → dp[3] = 1 + 1 = 2
  → dp[4] = 2 (LIS: [2,3])

i=5, arr[5]=7:
  j=0,1: skip (no match)
  j=2: arr[2]=2 < arr[5]=7 ? YES → 1 + 1 = 2
  j=3: arr[3]=5 < arr[5]=7 ? YES → 1 + 2 = 3
  j=4: arr[4]=3 < arr[5]=7 ? YES → 1 + 2 = 3
  → dp[5] = max(2, 3, 3) = 3 (LIS: [2,5,7])

i=6, arr[6]=101:
  j=3: arr[3]=5 < arr[6]=101 ? YES → 1 + 2 = 3
  j=5: arr[5]=7 < arr[6]=101 ? YES → 1 + 3 = 4
  → dp[6] = 4 (LIS: [2,5,7,101])

i=7, arr[7]=18:
  j=5: arr[5]=7 < arr[7]=18 ? YES → 1 + 3 = 4
  → dp[7] = 4 (LIS: [2,5,7,18])

Answer: max(dp) = 4
```

**Code (O(n²)):**

```python
def lengthOfLIS(arr):
    n = len(arr)
    if n == 0:
        return 0
    
    # dp[i] = LIS length ending at index i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], 1 + dp[j])
    
    return max(dp)

# Time: O(n²)
# Space: O(n)
```

**Code (O(n log n) - Binary Search, Advanced):**

```python
def lengthOfLIS_optimized(arr):
    import bisect
    
    # tails[i] = smallest tail of all increasing subsequences of length i+1
    tails = []
    
    for num in arr:
        # Find position where num should go
        pos = bisect.bisect_left(tails, num)
        
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    
    return len(tails)

# Time: O(n log n)
# Space: O(n)
# Tricky to understand, skip in interviews unless asked for optimization
```

---

## Pattern 4: Knapsack DP

### 4.1 0/1 Knapsack

**Problem:** Given items with weights and values, and a weight capacity, maximize value with weight constraint.

**Intuition:**

```
For each item, we have two choices:
1. Include it (if weight allows)
2. Exclude it

Recurrence:
- If we include item i: value = item_value[i] + max_value_with_remaining_capacity
- If we exclude item i: value = max_value_without_item_i

Take the better choice.
```

**Applying the Framework:**

```
State: dp[i][w] = max value using items 0..i-1 with weight limit w
Recurrence:
  dp[i][w] = max(
    dp[i-1][w],                              // exclude item i-1
    item_value[i-1] + dp[i-1][w - weight]   // include item i-1
  ) if weight[i-1] <= w
Base cases:
  - dp[0][w] = 0 for all w (no items)
  - dp[i][0] = 0 for all i (no capacity)
Array: 2D of size (n+1) × (capacity+1)
```

**Dry Run (items=[(value=5,weight=4), (value=6,weight=5), (value=3,weight=2)], capacity=7):**

```
Item:  0(v=5,w=4)  1(v=6,w=5)  2(v=3,w=2)
Capacity: 7

DP table (rows = items, cols = weight):
      0  1  2  3  4  5  6  7
  0   0  0  0  0  0  0  0  0  (no items)
  1   0  0  0  0  5  5  5  5  (item 0)
  2   0  0  0  0  5  6  6  11 (items 0,1)
  3   0  0  3  3  5  6  8  11 (items 0,1,2)

Filling row 1 (item 0: v=5, w=4):
  w=0: capacity=0 < weight=4 → dp[1][0] = dp[0][0] = 0
  w=1,2,3: capacity < weight=4 → dp[1][w] = dp[0][w] = 0
  w=4: capacity≥weight → max(dp[0][4], 5 + dp[0][0]) = max(0, 5) = 5
  w=5,6,7: same → 5

Filling row 2 (item 1: v=6, w=5):
  w=0-4: capacity < weight=5 → copy from dp[1][w]
  w=5: max(dp[1][5], 6 + dp[1][0]) = max(5, 6) = 6
  w=6: max(dp[1][6], 6 + dp[1][1]) = max(5, 6) = 6
  w=7: max(dp[1][7], 6 + dp[1][2]) = max(5, 6) = 6
  
Wait, let me recalculate w=7:
  If we include item 1 (v=6, w=5): remaining capacity = 7-5=2
  Previous best with capacity 2 was: dp[1][2] = 0
  So: 6 + 0 = 6
  
But dp[1][7] = 5 (just item 0)
So: max(5, 6) = 6
  
Hmm, but we should be able to fit both items 0 and 1 (weight = 4+5=9, too heavy).
Let me retry.

Actually:
  w=7: max(dp[1][7], 6 + dp[1][2]) = max(5, 6) = 6

But what if we include both 0 and 1?
Item 0: v=5, w=4
Item 1: v=6, w=5
Total: v=11, w=9 (exceeds capacity=7)

So we can't include both. Let's recalculate:
  w=7: include item 1? → 6 + dp[1][7-5] = 6 + dp[1][2] = 6 + 0 = 6
       exclude item 1? → dp[1][7] = 5
       → max(5, 6) = 6
  
But wait, dp[1][2] means "best value with capacity 2 using only item 0".
Item 0 has weight=4, so it doesn't fit in capacity=2. Hence dp[1][2] = 0. ✓

Ah, but then how do we get 11 at w=7?

Let me reconsider. At w=7, if we include item 1 (w=5):
- Remaining capacity: 7-5=2
- Best value with capacity 2 from items 0 (already computed): 0 (item 0 is too heavy)
- Total: 6 + 0 = 6

But looking at the answer dp[2][7], it shows 11. Let me recalculate the entire table.

Actually, I think I made an error. Let me recompute from scratch.

items = [(v=5,w=4), (v=6,w=5), (v=3,w=2)]

dp[1][4] = item 0 fits → max(dp[0][4], 5+dp[0][0]) = max(0, 5) = 5
dp[1][5] = item 0 fits → max(dp[0][5], 5+dp[0][1]) = max(0, 5) = 5
dp[1][6] = item 0 fits → max(dp[0][6], 5+dp[0][2]) = max(0, 5) = 5
dp[1][7] = item 0 fits → max(dp[0][7], 5+dp[0][3]) = max(0, 5) = 5

dp[2][5] = item 1 fits (w=5) → max(dp[1][5], 6+dp[1][0]) = max(5, 6) = 6
dp[2][6] = item 1 fits (w=5) → max(dp[1][6], 6+dp[1][1]) = max(5, 6) = 6
dp[2][7] = item 1 fits (w=5) → max(dp[1][7], 6+dp[1][2]) = max(5, 6) = 6

Hmm, still getting 6, not 11.

Wait - let me re-examine the recurrence.

dp[2][7] = max(dp[1][7], 6 + dp[1][7-5])
         = max(dp[1][7], 6 + dp[1][2])
         = max(5, 6 + 0)
         = 6

That's correct. We can't fit both items 0 and 1 in capacity 7.

Oh, I see my mistake! Let me recalculate with items 0 and 1 together:
Item 0: w=4, v=5
Item 1: w=5, v=6
Total weight: 9 (exceeds 7), so they don't fit together.

So the table should be:
      0  1  2  3  4  5  6  7
  0   0  0  0  0  0  0  0  0
  1   0  0  0  0  5  5  5  5
  2   0  0  0  0  5  6  6  6
  3   0  0  3  3  5  6  8  8

Let me recalculate row 3 (item 2: v=3, w=2):
dp[3][2] = max(dp[2][2], 3 + dp[2][0]) = max(0, 3) = 3
dp[3][3] = max(dp[2][3], 3 + dp[2][1]) = max(0, 3) = 3
dp[3][4] = max(dp[2][4], 3 + dp[2][2]) = max(5, 3) = 5
dp[3][5] = max(dp[2][5], 3 + dp[2][3]) = max(6, 3) = 6
dp[3][6] = max(dp[2][6], 3 + dp[2][4]) = max(6, 3+5) = max(6, 8) = 8 ✓
dp[3][7] = max(dp[2][7], 3 + dp[2][5]) = max(6, 3+6) = max(6, 9) = 9

So the correct table is:
      0  1  2  3  4  5  6  7
  0   0  0  0  0  0  0  0  0
  1   0  0  0  0  5  5  5  5
  2   0  0  0  0  5  6  6  6
  3   0  0  3  3  5  6  8  9

Answer: dp[3][7] = 9
```

**Code:**

```python
def knapsack01(values, weights, capacity):
    n = len(values)
    # dp[i][w] = max value using items 0..i-1 with weight limit w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Exclude item i-1
            dp[i][w] = dp[i-1][w]
            
            # Include item i-1 (if it fits)
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], values[i-1] + dp[i-1][w - weights[i-1]])
    
    return dp[n][capacity]

# Time: O(n * capacity)
# Space: O(n * capacity)
```

**Space Optimization (1D DP):**

```python
def knapsack01_optimized(values, weights, capacity):
    # dp[w] = max value with weight limit w
    dp = [0] * (capacity + 1)
    
    for i in range(len(values)):
        # Traverse backwards to avoid using the same item twice
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    
    return dp[capacity]

# Time: O(n * capacity)
# Space: O(capacity)
```

**Why backward iteration in 1D?**

```
Forward iteration would use the updated dp[w - weights[i]] from the same iteration.
This would effectively allow using the same item multiple times.

Example (wrong way):
for w in range(weights[i], capacity + 1):
    dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    # dp[w - weights[i]] was JUST updated, so it includes item i
    # This means item i is counted multiple times!

Backward iteration uses the OLD dp[w - weights[i]] from the previous iteration.
This ensures each item is counted at most once.
```

---

## Pattern 5: Partition DP

### 5.1 Partition Equal Subset Sum

**Problem:** Can you partition an array into two subsets with equal sum?

**Intuition:**

```
Partition into two equal subsets:
- Total sum must be even (otherwise impossible)
- We need to find a subset with sum = total_sum / 2
- This reduces to: "Can we achieve target sum = total_sum / 2?"

This is similar to 0/1 Knapsack, but instead of maximizing, we check if a sum is achievable.
```

**Applying the Framework:**

```
State: dp[i][sum] = can we achieve sum using items 0..i-1?
Recurrence:
  dp[i][sum] = dp[i-1][sum]  (don't include item i-1)
               OR
               dp[i-1][sum - arr[i-1]]  (include item i-1, if sum >= arr[i-1])
Base cases:
  - dp[0][0] = True (empty subset has sum 0)
  - dp[0][s] = False for s > 0 (can't achieve positive sum with no items)
Array: 2D of size (n+1) × (target_sum+1)
```

**Dry Run (arr=[1,5,11,5], target=11):**

```
Total sum = 22, target = 11

DP table:
      0   1   2   3   4   5   6   7   8   9  10  11
  0   T   F   F   F   F   F   F   F   F   F   F   F
  1   T   T   F   F   F   F   F   F   F   F   F   F   (item 1)
  2   T   T   F   F   F   T   T   F   F   F   F   F   (item 5)
  3   T   T   F   T   F   T   T   F   T   F   T   T   (item 11)
  4   T   T   F   T   F   T   T   F   T   F   T   T   (item 5)

Filling row 1 (item 0=1):
  dp[1][0] = dp[0][0] = T (include nothing)
  dp[1][1] = dp[0][1] OR dp[0][0] = F OR T = T
  dp[1][2..11] = dp[0][2..11] = F

Filling row 2 (item 1=5):
  dp[2][5] = dp[1][5] OR dp[1][0] = F OR T = T
  dp[2][6] = dp[1][6] OR dp[1][1] = F OR T = T
  others based on whether sum-5 was achievable

Filling row 4 (item 3=5):
  dp[4][11] = dp[3][11] OR dp[3][6]
            = T OR T = T

Answer: dp[n][target] = True
Explanation: [5, 6] has sum 11, and [1, 5, 5] has sum 11 (wait, that's not right)
Actually: one subset [11] and the other [1, 5, 5]
```

**Code:**

```python
def canPartition(arr):
    total_sum = sum(arr)
    
    # Total sum must be even
    if total_sum % 2 != 0:
        return False
    
    target = total_sum // 2
    n = len(arr)
    
    # dp[i][s] = can we achieve sum s using items 0..i-1?
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    
    # Base case: sum 0 is always achievable (empty subset)
    for i in range(n + 1):
        dp[i][0] = True
    
    for i in range(1, n + 1):
        for s in range(target + 1):
            # Don't include item i-1
            dp[i][s] = dp[i-1][s]
            
            # Include item i-1 (if it fits)
            if arr[i-1] <= s:
                dp[i][s] = dp[i][s] or dp[i-1][s - arr[i-1]]
    
    return dp[n][target]

# Time: O(n * target_sum)
# Space: O(n * target_sum)
```

**Space Optimization (1D DP):**

```python
def canPartition_optimized(arr):
    total_sum = sum(arr)
    
    if total_sum % 2 != 0:
        return False
    
    target = total_sum // 2
    
    # dp[s] = can we achieve sum s?
    dp = [False] * (target + 1)
    dp[0] = True
    
    for num in arr:
        # Traverse backwards to avoid using same item twice
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]
    
    return dp[target]

# Time: O(n * target_sum)
# Space: O(target_sum)
```

---

## Pattern 6: DP on Strings

### 6.1 Edit Distance (Levenshtein Distance)

**Problem:** Minimum number of operations (insert, delete, replace) to transform s1 into s2.

**Intuition:**

```
To transform "horse" to "ros":
- Delete 'h' → "orse"
- Delete 'e' → "ors"
- Replace 'r' with 'r' (no-op) → "ors" (wait, this doesn't work)

Let me think recursively:
- At each position, we compare characters
- If they match: no operation needed
- If they don't: try all three operations and pick the best

Three operations:
1. Replace: transform s1[0..i-1] to s2[0..j-1], then replace s1[i] with s2[j]
   Cost = 1 + editDist(s1[0..i-1], s2[0..j-1])

2. Delete from s1: remove s1[i], then transform remaining
   Cost = 1 + editDist(s1[0..i-1], s2[0..j])

3. Insert into s1: insert s2[j], then transform remaining
   Cost = 1 + editDist(s1[0..i], s2[0..j-1])
```

**Applying the Framework:**

```
State: dp[i][j] = edit distance between s1[0..i-1] and s2[0..j-1]
Recurrence:
  if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1]  (no operation needed)
  else:
    dp[i][j] = 1 + min(
      dp[i-1][j],    (delete from s1)
      dp[i][j-1],    (insert into s1)
      dp[i-1][j-1]   (replace)
    )
Base cases:
  - dp[0][j] = j (insert j characters)
  - dp[i][0] = i (delete i characters)
Array: 2D of size (len(s1)+1) × (len(s2)+1)
```

**Dry Run (s1="horse", s2="ros"):**

```
DP table:
      ""  r   o   s
""    0   1   2   3
h     1   ?   ?   ?
o     2   ?   ?   ?
r     3   ?   ?   ?
s     4   ?   ?   ?
e     5   ?   ?   ?

Filling:
[1,1]: s1[0]='h' != s2[0]='r' → 1 + min(dp[0][1]=1, dp[1][0]=1, dp[0][0]=0) = 1
[1,2]: s1[0]='h' != s2[1]='o' → 1 + min(dp[0][2]=2, dp[1][1]=1, dp[0][1]=1) = 2
[1,3]: s1[0]='h' != s2[2]='s' → 1 + min(dp[0][3]=3, dp[1][2]=2, dp[0][2]=2) = 3

[2,1]: s1[1]='o' != s2[0]='r' → 1 + min(dp[1][1]=1, dp[2][0]=2, dp[1][0]=1) = 2
[2,2]: s1[1]='o' == s2[1]='o' → dp[1][1] = 1
[2,3]: s1[1]='o' != s2[2]='s' → 1 + min(dp[1][3]=3, dp[2][2]=1, dp[1][2]=2) = 2

[3,1]: s1[2]='r' == s2[0]='r' → dp[2][0] = 2
[3,2]: s1[2]='r' != s2[1]='o' → 1 + min(dp[2][2]=1, dp[3][1]=2, dp[2][1]=2) = 2
[3,3]: s1[2]='r' != s2[2]='s' → 1 + min(dp[2][3]=2, dp[3][2]=2, dp[2][2]=1) = 2

[4,1]: s1[3]='s' != s2[0]='r' → 1 + min(dp[3][1]=2, dp[4][0]=4, dp[3][0]=3) = 3
[4,2]: s1[3]='s' != s2[1]='o' → 1 + min(dp[3][2]=2, dp[4][1]=3, dp[3][1]=2) = 3
[4,3]: s1[3]='s' == s2[2]='s' → dp[3][2] = 2

[5,1]: s1[4]='e' != s2[0]='r' → 1 + min(dp[4][1]=3, dp[5][0]=5, dp[4][0]=4) = 4
[5,2]: s1[4]='e' != s2[1]='o' → 1 + min(dp[4][2]=3, dp[5][1]=4, dp[4][1]=3) = 4
[5,3]: s1[4]='e' != s2[2]='s' → 1 + min(dp[4][3]=2, dp[5][2]=4, dp[4][2]=3) = 3

Final:
      ""  r   o   s
""    0   1   2   3
h     1   1   2   3
o     2   2   1   2
r     3   2   2   2
s     4   3   3   2
e     5   4   4   3

Answer: dp[5][3] = 3
```

**Code:**

```python
def editDistance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # delete
                    dp[i][j-1],    # insert
                    dp[i-1][j-1]   # replace
                )
    
    return dp[m][n]

# Time: O(m*n)
# Space: O(m*n)
```

---

## Pattern 7: DP on Trees (Intro)

### 7.1 House Robber on Trees

**Problem:** Rob houses in a tree (connected, no cycles). Maximum value with constraint: can't rob adjacent nodes.

**Intuition:**

```
For each node, two choices:
1. Rob this node: can't rob children
   Value = node_value + sum(rob_grandchildren)

2. Don't rob this node: can rob children
   Value = sum(rob_children)

Take the better option.

This is naturally recursive (top-down DP).
```

**Applying the Framework:**

```
State: 
  dp[node][0] = max value if we DON'T rob this node
  dp[node][1] = max value if we DO rob this node

Recurrence:
  if not robbing node:
    dp[node][0] = sum(max(dp[child][0], dp[child][1]) for each child)
  
  if robbing node:
    dp[node][1] = node.value + sum(dp[child][0] for each child)

Base case: leaf nodes
  dp[leaf][0] = 0 (don't rob)
  dp[leaf][1] = leaf.value (rob)
```

**Code:**

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rob(root):
    # memo[node][0] = max value if don't rob node
    # memo[node][1] = max value if rob node
    memo = {}
    
    def dfs(node):
        if not node:
            return (0, 0)
        
        if node in memo:
            return memo[node]
        
        left_not_rob, left_rob = dfs(node.left)
        right_not_rob, right_rob = dfs(node.right)
        
        # Don't rob this node: can rob or not rob children (take max)
        not_rob = max(left_not_rob, left_rob) + max(right_not_rob, right_rob)
        
        # Rob this node: children must not be robbed
        rob_this = node.val + left_not_rob + right_not_rob
        
        memo[node] = (not_rob, rob_this)
        return (not_rob, rob_this)
    
    not_rob, rob_this = dfs(root)
    return max(not_rob, rob_this)

# Time: O(n) - each node visited once
# Space: O(h) - recursion depth (height)
```

---

# PHASE 4: INTERVIEW CONVERSION

## How to Identify DP in Interviews

### Red Flags (DP Problems in Disguise)

**Learn to recognize these patterns:**

```
1. "Maximum/Minimum" + "any way" / "count"
   → Likely DP

2. "Optimal" solution needed with decision at each step
   → DP

3. Recurrence visible in the problem statement
   "Can reuse the result" / "subproblem"
   → DP

4. Constraints allow exponential recursion
   "n <= 20, n <= 100" (small inputs)
   → DP is intended

5. Optimization version of recursive problem
   "Fibonacci", "Subset sum", etc.
   → DP
```

**Interview dialogue example:**

```
Interviewer: "Given an array, find the maximum sum of a subarray."

What you should think:
1. Can I solve this recursively?
   - maxSum(arr) depends on maxSum(arr[0:-1])? Hmm, not directly.
   - maxSum ending at i depends on maxSum ending at i-1? YES!
   - This is Kadane's algorithm → DP

2. Overlapping subproblems?
   - maxEnding(i-1) is computed once, used for maxEnding(i)
   - Actually, we only compute each once, no overlap
   - But the structure is DP

3. Optimal substructure?
   - Best solution ending at i includes best solution ending at i-1
   - YES

→ Recognize: This is DP
```

---

### Interview Answering Strategy

**Step 1: State the approach (Don't jump to code)**

```
"I notice this problem asks for the [maximum/minimum] value given constraints on choices.
This suggests DP: we can break it into subproblems where the optimal solution
depends on optimal solutions to smaller subproblems.

Let me first think about the state definition:
- What would the subproblem be?
- How would smaller subproblems combine?"
```

**Step 2: Define state and recurrence (Before coding)**

```
"I'll define:
- State: dp[i] = the [specific thing we're computing]
- Recurrence: dp[i] = [formula]
- Base cases: [list them]
- Time: O(?)
- Space: O(?)"

Pause here and get interviewer feedback before coding.
```

**Step 3: Code carefully**

```python
# Solution template:
def solve(arr):
    n = len(arr)
    dp = ...  # initialize
    
    # Base cases
    dp[0] = ...
    
    # Fill using recurrence
    for i in range(1, n):
        dp[i] = ...  # recurrence
    
    return dp[n-1]
```

**Step 4: Verify with examples**

```
"Let me trace through a small example to verify:
[example input]
...
Does the output match expected? ✓"
```

**Step 5: Optimize if asked**

```
"Space-wise, I notice dp[i] only depends on dp[i-1] and dp[i-2].
So I can use two variables instead of an array:
[optimized code]"
```

---

## Common Traps and Wrong Approaches

### Trap 1: Confusing Greedy with DP

```python
# WRONG APPROACH (Greedy)
def maxProfit_greedy(prices):
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    return profit

# This works for "buy/sell unlimited times" but NOT for "at most 1 transaction"

# CORRECT APPROACH (DP)
def maxProfit_dp(prices):
    if not prices:
        return 0
    
    # dp[i][0] = max profit after i transactions (not holding)
    # dp[i][1] = max profit after i transactions (holding)
    
    # For "at most k transactions", use DP
    ...
```

**How to avoid:** Greedy only works when local optimal = global optimal. DP is safer.

---

### Trap 2: Off-By-One Errors

```python
# WRONG
for i in range(len(arr)):
    dp[i] = dp[i-1] + ...  # when i=0, dp[-1] is accessed!

# CORRECT
for i in range(1, len(arr)):
    dp[i] = dp[i-1] + ...  # start from i=1

# Also: array indexing
# dp is 1-indexed: dp[i] represents state for arr[0..i-1]
# Make sure you adjust correctly
```

**How to avoid:**
- Initialize base cases explicitly
- Start loops from correct index
- Write out examples by hand first

---

### Trap 3: Wrong Recurrence Relation

```python
# WRONG (for climbing stairs)
def climbStairs(n):
    dp = [0] * n
    dp[0] = 1
    for i in range(1, n):
        dp[i] = dp[i-1] + dp[i-2]  # IndexError when i=1, dp[i-2]=dp[-1]

# CORRECT
def climbStairs(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
```

**How to avoid:**
- Write out base cases explicitly
- Dry run on small examples (n=0, 1, 2, 3)
- Verify recurrence matches your state definition

---

### Trap 4: Not Handling Edge Cases

```python
def solve(arr):
    if not arr:  # EDGE CASE!
        return 0
    
    if len(arr) == 1:  # EDGE CASE!
        return arr[0]
    
    # ... rest of code
```

**Common edge cases to check:**
- Empty input
- Single element
- All negative numbers (for max problems)
- All positive numbers (for min problems)

---

### Trap 5: Choosing Wrong Approach

```python
# Problem: Find LIS
# WRONG: "I'll use memoization recursively"
# (recursive approach might hit stack overflow for large n)

# RIGHT: "I'll use tabulation, and if needed, optimize with binary search"

# Decision factors:
# - Is recursion depth small? → Memoization OK
# - Is n very large (10^5+)? → Tabulation preferred
# - Is recursion structure complex? → Memoization easier to code
# - Need space optimization? → Tabulation better
```

---

## How to Explain DP Clearly to an Interviewer

### The Story Approach

```
"Think of this problem as a journey:
- At each step, I make a decision
- My decision affects what I can do next
- I want the best total outcome

For example, in [problem name]:
- At each position, I choose to [action A] or [action B]
- This affects my options at the next position
- I need to track the best outcome at each position

This is where DP helps: instead of exploring all paths (exponential),
I remember the best outcome at each position.
So when I reach a position from multiple paths, I use the remembered best."
```

### The Recurrence Narrative

```
"Let me explain the recurrence relation:

dp[i] represents [specific thing we're computing at step i]

To compute dp[i], I think: 'What information from previous steps do I need?'

Answer: I need [dp[i-1], dp[i-2], etc.]

And the formula is: dp[i] = [how we combine previous results]

This works because:
1. The problem has optimal substructure: best solution at i uses best solutions before i
2. The recurrence avoids recomputation: each dp[i] computed once
"
```

### Complexity Analysis

```
"Time Complexity:
- Number of states: [how many unique states]
- Work per state: [how much computation]
- Total: O([number of states] * [work per state])

Space Complexity:
- DP array size: [dimensions and ranges]
- Can be optimized to: [if yes, how]
"
```

---

## How to Debug DP Solutions

### The Trace Method

**When your DP code doesn't work:**

```
1. Print the entire DP table/array after filling
   
   Example:
   dp = [[0]*5 for _ in range(5)]
   # ... fill logic ...
   for row in dp:
       print(row)

2. Manually trace a small example by hand

3. Check if your manual trace matches the printed table

4. If they don't match, find the first mismatch
   "Ah, dp[2][3] should be 5 but I got 3"

5. Check the recurrence for this state
   "For dp[2][3], I should do ... but I coded ..."
```

**Example (debugging):**

```python
# My code:
def lis(arr):
    n = len(arr)
    dp = [1] * n
    
    for i in range(n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], 1 + dp[j])
    
    return max(dp)

# Test on arr = [10, 9, 2, 5, 3, 7, 101, 18]
# Let me trace:
arr = [10, 9, 2, 5, 3, 7, 101, 18]
dp = [1, 1, 1, ?, ?, ?, ?, ?]  # After i=3

# Wait, let me run and print:
# dp = [1, 1, 1, 2, 2, 3, 4, 4]
# But dp[5] (arr[5]=7) should be 3 (LIS: [2,5,7])

# Let me trace dp[5]:
# i=5, arr[5]=7
# j=0: arr[0]=10 > 7, skip
# j=1: arr[1]=9 > 7, skip
# j=2: arr[2]=2 < 7, dp[5] = max(1, 1+dp[2]) = max(1, 1+1) = 2
# j=3: arr[3]=5 < 7, dp[5] = max(2, 1+dp[3]) = max(2, 1+2) = 3 ✓
# j=4: arr[4]=3 < 7, dp[5] = max(3, 1+dp[4]) = max(3, 1+2) = 3

# OK so dp[5]=3 is correct. Good!
```

### The Assertion Method

```python
# Add assertions to verify your recurrence
def lis(arr):
    n = len(arr)
    dp = [1] * n
    
    for i in range(n):
        for j in range(i):
            if arr[j] < arr[i]:
                new_val = 1 + dp[j]
                assert new_val >= 1, f"Invalid computation at dp[{i}]"
                assert new_val <= i + 1, f"dp[{i}] can't exceed {i+1}"
                dp[i] = max(dp[i], new_val)
    
    return max(dp)
```

### The Comparison Method

```python
# Implement both memoization and tabulation
# Compare results

def solve_memo(arr):
    memo = {}
    def dfs(i):
        if i in memo:
            return memo[i]
        # ... recurrence ...
        memo[i] = result
        return result
    return dfs(len(arr) - 1)

def solve_tab(arr):
    dp = [0] * len(arr)
    # ... fill logic ...
    return dp[-1]

# Test
assert solve_memo(arr) == solve_tab(arr), "Memoization and tabulation differ!"
```

---

## Final Interview Checklist

**Before you say "I'm done":**

```
[ ] Solution compiles and runs without errors
[ ] Handled all base cases (n=0, n=1, etc.)
[ ] Tested on provided examples (manually trace)
[ ] Tested on edge cases (empty, single element, etc.)
[ ] Tested on largest constraints (if given)
[ ] Explained the state definition clearly
[ ] Explained the recurrence relation
[ ] Explained why DP works (overlapping subproblems + optimal substructure)
[ ] Analyzed time complexity correctly
[ ] Analyzed space complexity correctly
[ ] Considered space optimization (if applicable)
[ ] Verified recurrence is correct (spot-checked values)
[ ] Code is clean and readable
[ ] Variable names are descriptive
[ ] Asked if interviewer wants further optimization
```

---

# QUICK REFERENCE & CHECKLISTS

## Pattern Summary Table

| Pattern | State Definition | Recurrence | Time | Space | Key Example |
|---------|------------------|-----------|------|-------|-----------|
| **Fibonacci** | dp[i] = i-th fibonacci | dp[i]=dp[i-1]+dp[i-2] | O(n) | O(1) | Climb Stairs |
| **1D Array** | dp[i] = [thing at i] | depends on dp[i-1], dp[i-2] | O(n) or O(n²) | O(n) or O(1) | LIS, Coin Change |
| **2D Grid** | dp[i][j] = [thing at i,j] | dp[i][j]=dp[i-1][j]+dp[i][j-1] | O(m*n) | O(m*n) or O(n) | Paths, LCS |
| **Knapsack** | dp[i][w] = max value | combine include/exclude | O(n*W) | O(n*W) or O(W) | 0/1 Knapsack |
| **Subsequence** | dp[i] = [thing ending at i] | compare with previous | O(n²) or O(n log n) | O(n) | LIS |
| **String** | dp[i][j] = [thing for s1[0..i], s2[0..j]] | match/mismatch cases | O(m*n) | O(m*n) | Edit Distance |
| **Tree** | dp[node][choice] = best value | combine child results | O(n) | O(h) | House Robber Tree |

---

## Decision Tree for Choosing DP Type

```
Is the problem recursive?
├─ YES
│  ├─ Can I identify a state clearly?
│  │  ├─ YES
│  │  │  ├─ Does the state depend on few previous states?
│  │  │  │  ├─ YES → Can try memoization or tabulation
│  │  │  │  └─ NO → Maybe not DP
│  │  │  └─ NO → Rethink the problem
│  │  └─ NO → Rethink the problem
│  └─ Probably DP
└─ NO
   └─ Probably not DP
```

---

## Recurrence Relation Patterns

```
Pattern: Linear Combination
dp[i] = dp[i-1] + dp[i-2] + ... + dp[i-k]
Example: Climbing stairs (k=2, climbing 1 or 2 steps)

Pattern: Min/Max Selection
dp[i] = max(option1(dp[...]), option2(dp[...]), ...)
Example: LIS, Coin Change

Pattern: Boolean Achievability
dp[i] = dp[i-1] OR dp[i-2] OR ... (can we achieve state i?)
Example: Partition, Subset Sum

Pattern: Conditional Combination
if condition:
    dp[i] = f(dp[i-1], dp[i-2], ...)
else:
    dp[i] = g(dp[i-1], dp[i-2], ...)
Example: LCS, Edit Distance

Pattern: 2D Movement
dp[i][j] = dp[i-1][j] + dp[i][j-1]  (from above and left)
Example: Grid paths, Unique paths

Pattern: Two Choices
dp[i] = max(
    include_i: ... + dp[i-1],
    exclude_i: ... + dp[i-1]
)
Example: 0/1 Knapsack, House Robber
```

---

## Off-by-One Error Prevention

```
Common mistakes:

1. Array indexing vs state ranges
   dp[i] represents arr[0..i-1] (i elements)
   NOT arr[i]

2. Initialization
   // WRONG
   dp = [0] * n  # Only n elements, index 0 to n-1
   
   // RIGHT
   dp = [0] * (n + 1)  # n+1 elements to represent dp[n]

3. Loop bounds
   // WRONG
   for i in range(n):
       dp[i] = ...  # What about dp[n]?
   
   // RIGHT
   for i in range(1, n + 1):
       dp[i] = ...  # Includes dp[n]

4. Accessing dp[i-1] in loops
   // WRONG
   for i in range(n):
       dp[i] = dp[i-1] + ...  # When i=0, dp[-1] is accessed!
   
   // RIGHT (initialize base case first)
   dp[0] = ...  # base case
   for i in range(1, n):
       dp[i] = dp[i-1] + ...
```

---

## Space Optimization Cheatsheet

**When can you optimize space?**

```
1. If dp[i] only depends on dp[i-1] (and earlier)
   → Use rolling/sliding window
   dp_old = ...
   dp_new = f(dp_old)
   dp_old = dp_new

2. If dp[i][j] only depends on dp[i-1][j] and dp[i][j-1]
   → Use 1D array, iterate backwards for j
   for j in range(W, -1, -1):
       dp[j] = max(dp[j], ...)

3. If you need both dp[i-1] and dp[i-2]
   → Keep two previous values
   prev2, prev1 = ..., ...
   for i in range(2, n):
       curr = f(prev1, prev2)
       prev2, prev1 = prev1, curr
```

---

## Template: Memoization

```python
def solve(arr):
    memo = {}
    
    def dp(state):
        # Check memo
        if state in memo:
            return memo[state]
        
        # Base case
        if is_base_case(state):
            return base_value
        
        # Recurrence
        result = recurrence(dp(state-1), dp(state-2), ...)
        
        # Store and return
        memo[state] = result
        return result
    
    return dp(target_state)
```

---

## Template: Tabulation

```python
def solve(arr):
    n = len(arr)
    dp = [0] * (n + 1)
    
    # Base cases
    dp[0] = ...
    dp[1] = ...
    
    # Fill
    for i in range(2, n + 1):
        dp[i] = recurrence(dp[i-1], dp[i-2], ...)
    
    return dp[n]
```

---

## Quick Debugging Checklist

```
[ ] State definition clear? ("dp[i] = ...")
[ ] Recurrence correct? (Manually verify 2-3 values)
[ ] Base cases covered? (n=0, n=1, etc.)
[ ] Array initialization correct? (size, initial values)
[ ] Loop bounds correct? (off-by-one check)
[ ] Return statement correct? (return dp[n] not dp[n-1])
[ ] Edge cases handled? (empty input, single element)
[ ] Time/space complexity acceptable?
```

---

## Common Interview Follow-Ups

**If you solve it, expect:**

```
1. "Can you optimize space?"
   → Reduce from O(n) to O(1) if possible

2. "What if we add this constraint?"
   → Modify the recurrence

3. "How would you handle this edge case?"
   → Add checks before/after DP

4. "Can you return the actual solution, not just the value?"
   → Backtrack through DP table

5. "What's the actual time/space?"
   → Recalculate based on constraints

6. "How would you parallelize this?"
   → Some DP can't be parallelized (dependencies)

7. "What if constraints increase 10x?"
   → Need optimization or different approach
```

---

This comprehensive guide covers everything from fundamentals to interview mastery. Remember:

1. **Slow down and understand** - Don't memorize patterns
2. **Practice the framework** - Apply it to every problem
3. **Debug carefully** - Trace by hand before coding
4. **Explain clearly** - Your understanding matters more than code speed
5. **Optimize iteratively** - Basic solution first, then optimize

Good luck with your interviews! 🚀

