# Complete Guide to Time & Space Complexity for MAANG Interviews

## Table of Contents
1. [Fundamentals](#fundamentals)
2. [Big O Notation Deep Dive](#big-o-notation-deep-dive)
3. [Time Complexity Analysis](#time-complexity-analysis)
4. [Space Complexity Analysis](#space-complexity-analysis)
5. [Common Complexities & Examples](#common-complexities--examples)
6. [Input Size vs Time Complexity (The Math Behind It)](#input-size-vs-time-complexity)
7. [Advanced Techniques](#advanced-techniques)
8. [Interview Tips & Tricks](#interview-tips--tricks)

---

## Fundamentals

### What is Algorithmic Complexity?

**Time Complexity**: How the runtime of an algorithm grows as input size increases.

**Space Complexity**: How much extra memory an algorithm needs as input size increases.

### Why It Matters in MAANG Interviews
- Determines if your solution will scale
- Shows your understanding of algorithm efficiency
- Often the difference between accepted and rejected solutions

---

## Big O Notation Deep Dive

### The Three Notations

1. **Big O (O)** - Upper bound (worst case) ← *Most used in interviews*
2. **Big Omega (Ω)** - Lower bound (best case)
3. **Big Theta (Θ)** - Tight bound (average case)

### Rules of Big O

#### Rule 1: Drop Constants
```
O(2n) → O(n)
O(500) → O(1)
O(13n²) → O(n²)
```

#### Rule 2: Drop Non-Dominant Terms
```
O(n² + n) → O(n²)
O(n + log n) → O(n)
O(n! + n³) → O(n!)
```

#### Rule 3: Different Inputs = Different Variables
```python
# Wrong: O(n)
def process(arr1, arr2):
    for i in arr1: pass
    for j in arr2: pass

# Correct: O(n + m) where n = len(arr1), m = len(arr2)
```

#### Rule 4: Add for Sequential, Multiply for Nested
```python
# Sequential: O(a + b)
for i in a: pass
for j in b: pass

# Nested: O(a * b)
for i in a:
    for j in b: pass
```

---

## Time Complexity Analysis

### Complexity Hierarchy (Fastest to Slowest)
```
O(1) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
```

### Common Patterns

#### O(1) - Constant Time
```python
# Array access
def get_first(arr):
    return arr[0]  # O(1)

# Hash map operations
def check_key(d, key):
    return key in d  # O(1) average

# Arithmetic operations
def add(a, b):
    return a + b  # O(1)
```

#### O(log n) - Logarithmic Time
```python
# Binary Search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:  # O(log n) - halving each time
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Finding power (divide and conquer)
def power(x, n):
    if n == 0: return 1
    half = power(x, n // 2)  # O(log n)
    return half * half if n % 2 == 0 else half * half * x
```

**Why log n?** Each iteration reduces problem size by half (or some constant factor).

#### O(√n) - Square Root Time
```python
# Check if number is prime
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):  # O(√n)
        if n % i == 0:
            return False
    return True

# Count divisors
def count_divisors(n):
    count = 0
    for i in range(1, int(n**0.5) + 1):  # O(√n)
        if n % i == 0:
            count += 2 if i != n // i else 1
    return count
```

#### O(n) - Linear Time
```python
# Single loop
def find_max(arr):
    max_val = arr[0]
    for num in arr:  # O(n)
        if num > max_val:
            max_val = num
    return max_val

# Two sequential loops (still O(n))
def process(arr):
    total = sum(arr)  # O(n)
    for x in arr:     # O(n)
        print(x / total)
    # Total: O(n) + O(n) = O(2n) = O(n)
```

#### O(n log n) - Linearithmic Time
```python
# Merge Sort / Quick Sort (average)
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # T(n/2)
    right = merge_sort(arr[mid:])  # T(n/2)
    return merge(left, right)      # O(n)
    # Total: O(n log n)

# Sorting then processing
def find_closest_pair(arr):
    arr.sort()  # O(n log n)
    min_diff = float('inf')
    for i in range(len(arr) - 1):  # O(n)
        min_diff = min(min_diff, arr[i+1] - arr[i])
    return min_diff
    # Total: O(n log n)
```

#### O(n²) - Quadratic Time
```python
# Nested loops (same array)
def has_duplicate(arr):
    for i in range(len(arr)):       # O(n)
        for j in range(i+1, len(arr)):  # O(n)
            if arr[i] == arr[j]:
                return True
    return False
    # Total: O(n²)

# Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):              # O(n)
        for j in range(n - i - 1):  # O(n)
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    # Total: O(n²)
```

#### O(2ⁿ) - Exponential Time
```python
# Naive Fibonacci (recursive)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)  # O(2ⁿ)
    # Each call makes 2 more calls

# Generate all subsets
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i+1, path)  # Branching factor = 2
            path.pop()
    backtrack(0, [])
    return result
    # Total: O(2ⁿ) - 2^n subsets
```

#### O(n!) - Factorial Time
```python
# Generate all permutations
def permute(nums):
    result = []
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i in range(len(remaining)):  # n choices, then n-1, then n-2...
            backtrack(path + [remaining[i]], 
                     remaining[:i] + remaining[i+1:])
    backtrack([], nums)
    return result
    # Total: O(n!)

# Traveling Salesman (brute force)
def tsp_brute_force(cities):
    # Try all possible orders: O(n!)
    pass
```

---

## Space Complexity Analysis

### What Counts as Space?

1. **Input space** - Usually NOT counted
2. **Auxiliary space** - Extra space used ← *This is what we analyze*
3. **Output space** - Sometimes counted, clarify in interview

### Common Patterns

#### O(1) - Constant Space
```python
# Only using fixed variables
def sum_array(arr):
    total = 0  # O(1) space
    for num in arr:
        total += num
    return total

# In-place swap
def reverse_array(arr):
    left, right = 0, len(arr) - 1  # O(1) space
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

#### O(n) - Linear Space
```python
# Creating new array
def double_values(arr):
    result = []  # O(n) space
    for num in arr:
        result.append(num * 2)
    return result

# Using hash map
def two_sum(nums, target):
    seen = {}  # O(n) space in worst case
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Using set for duplicates
def has_duplicate(arr):
    seen = set()  # O(n) space
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False
```

#### O(n²) - Quadratic Space
```python
# 2D matrix
def create_matrix(n):
    matrix = [[0] * n for _ in range(n)]  # O(n²) space
    return matrix

# Dynamic programming table
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n+1) for _ in range(m+1)]  # O(m*n) space
    # ... rest of algorithm
    return dp[m][n]
```

#### Recursion and Stack Space
```python
# Recursive DFS
def dfs(node):
    if not node: return
    dfs(node.left)   # O(h) space on call stack
    dfs(node.right)
    # Space: O(h) where h = height of tree
    # Worst case: O(n) for skewed tree
    # Best case: O(log n) for balanced tree

# Fibonacci with memoization
def fib(n, memo={}):
    if n in memo: return memo[n]  # O(n) space for memo
    if n <= 1: return n
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]
    # Space: O(n) for memo + O(n) for recursion stack = O(n)
```

### Space Optimization Techniques

#### Technique 1: In-Place Modification
```python
# Before: O(n) space
def remove_duplicates(arr):
    return list(set(arr))

# After: O(1) space (modifies input)
def remove_duplicates_inplace(arr):
    if not arr: return 0
    write_idx = 1
    for read_idx in range(1, len(arr)):
        if arr[read_idx] != arr[read_idx-1]:
            arr[write_idx] = arr[read_idx]
            write_idx += 1
    return write_idx
```

#### Technique 2: Reuse Variables
```python
# Before: O(n) space for all states
def climb_stairs_space(n):
    dp = [0] * (n+1)
    dp[0] = 1
    dp[1] = 1
    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# After: O(1) space - only track last 2 states
def climb_stairs_optimized(n):
    if n <= 1: return 1
    prev2, prev1 = 1, 1
    for i in range(2, n+1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1
```

---

## Input Size vs Time Complexity

### The Critical Math: Operations per Second

Modern computers: ~10⁸ to 10⁹ operations per second (1 second time limit)

### Constraint → Complexity Table

| Input Size (n) | Max Complexity | Operations | Examples |
|----------------|----------------|------------|----------|
| n ≤ 10 | O(n!) | 3,628,800 | Permutations, TSP |
| n ≤ 20 | O(2ⁿ) | 1,048,576 | Subsets, combinations |
| n ≤ 100 | O(n⁴) | 100,000,000 | 4 nested loops |
| n ≤ 500 | O(n³) | 125,000,000 | 3 nested loops |
| n ≤ 5,000 | O(n²) | 25,000,000 | 2 nested loops |
| n ≤ 100,000 | O(n log n) | ~1,660,000 | Sorting algorithms |
| n ≤ 1,000,000 | O(n) | 1,000,000 | Single pass |
| n ≤ 10⁹ | O(log n) | ~30 | Binary search |
| Any n | O(1) | 1 | Direct access |

### Real Interview Examples

```python
# Example 1: n = 10⁴
# Need O(n) or O(n log n)
def solve(arr):  # len(arr) = 10,000
    arr.sort()  # O(n log n) = 10⁴ * 13 = 130,000 ✓
    # O(n²) = 10⁸ operations ✗ Too slow!

# Example 2: n = 10⁵
# Need O(n) or O(n log n), no O(n²)
def two_sum(arr, target):  # len(arr) = 100,000
    seen = {}
    for i, num in enumerate(arr):  # O(n) = 10⁵ ✓
        if target - num in seen:
            return [seen[target-num], i]
        seen[num] = i
    # Nested loop O(n²) = 10¹⁰ ✗ Way too slow!

# Example 3: n = 20
# Can use O(2ⁿ) or O(n!)
def subsets(nums):  # len(nums) = 20
    # O(2ⁿ) = 2²⁰ = 1,048,576 ✓
    pass
```

### How to Estimate in Interview

**Step 1**: Ask about constraints
- "What's the maximum size of the input?"
- "Are there any time/space constraints?"

**Step 2**: Calculate acceptable complexity
```
If n ≤ 100:     O(n³) is fine
If n ≤ 10,000:  Need O(n log n) or better
If n ≤ 10⁶:     Need O(n) or O(log n)
```

**Step 3**: Choose algorithm accordingly

---

## Advanced Techniques

### Amortized Analysis

**Definition**: Average time per operation over a sequence of operations

#### Example: Dynamic Array (ArrayList)
```python
class DynamicArray:
    def __init__(self):
        self.arr = [None] * 1
        self.size = 0
        self.capacity = 1
    
    def append(self, val):
        if self.size == self.capacity:
            # Resize: O(n)
            self.capacity *= 2
            new_arr = [None] * self.capacity
            for i in range(self.size):
                new_arr[i] = self.arr[i]
            self.arr = new_arr
        
        self.arr[self.size] = val
        self.size += 1

# Individual append: O(n) worst case (during resize)
# Amortized: O(1) because resize happens rarely
# n appends: Total cost = O(n), so O(1) per append
```

### Master Theorem (For Recurrences)

For recurrence: `T(n) = aT(n/b) + f(n)`

```
Case 1: f(n) = O(n^c) where c < log_b(a)
        → T(n) = O(n^(log_b(a)))

Case 2: f(n) = O(n^c) where c = log_b(a)
        → T(n) = O(n^c * log n)

Case 3: f(n) = O(n^c) where c > log_b(a)
        → T(n) = O(f(n))
```

#### Examples:
```python
# Merge Sort: T(n) = 2T(n/2) + O(n)
# a=2, b=2, f(n)=n, c=1
# log_b(a) = log_2(2) = 1 = c
# Case 2: O(n log n)

# Binary Search: T(n) = T(n/2) + O(1)
# a=1, b=2, f(n)=1, c=0
# log_b(a) = log_2(1) = 0 = c
# Case 2: O(log n)

# Strassen's Matrix Mult: T(n) = 7T(n/2) + O(n²)
# a=7, b=2, f(n)=n², c=2
# log_b(a) = log_2(7) ≈ 2.807 > 2
# Case 1: O(n^2.807)
```

### Analyzing Tricky Code

#### Nested Loops with Dependencies
```python
# How complex is this?
for i in range(n):
    for j in range(i, n):
        print(i, j)

# Analysis:
# i=0: n iterations
# i=1: n-1 iterations
# i=2: n-2 iterations
# ...
# Total: n + (n-1) + (n-2) + ... + 1 = n(n+1)/2 = O(n²)
```

#### Logarithmic Decrements
```python
# How complex is this?
i = n
while i > 0:
    print(i)
    i //= 2

# Analysis:
# n → n/2 → n/4 → n/8 → ... → 1
# Number of iterations: log₂(n)
# Time: O(log n)
```

#### String Building
```python
# Bad: O(n²)
def build_string_bad(n):
    s = ""
    for i in range(n):
        s += "a"  # String concatenation creates new string each time
    return s

# Good: O(n)
def build_string_good(n):
    s = []
    for i in range(n):
        s.append("a")  # List append is O(1)
    return "".join(s)  # Join is O(n)
```

---

## Interview Tips & Tricks

### Common Pitfalls

#### ❌ Mistake 1: Forgetting Hidden Operations
```python
# Looks O(n) but is O(n²)
def process(arr):
    result = []
    for i in range(len(arr)):
        result.append(arr[:i])  # Slicing is O(i)!
    return result
# Actual: O(n²)
```

#### ❌ Mistake 2: Ignoring Library Function Costs
```python
# Looks O(n) but might not be
def has_common(list1, list2):
    for item in list1:
        if item in list2:  # O(n) for list, O(1) for set!
            return True
    return False
# Actual with list: O(n * m)
# With set: O(n + m) if you convert list2 to set first
```

#### ❌ Mistake 3: Confusing Average and Worst Case
```python
# Hash map operations
d = {}
d[key] = value  # O(1) average, O(n) worst (hash collisions)

# QuickSort
# O(n log n) average
# O(n²) worst case (already sorted)
```

### Interview Framework

**Step 1: Understand & Clarify**
- What's the input size?
- Any duplicates?
- Is the input sorted?
- Time/space constraints?

**Step 2: Brute Force First**
```
State brute force solution + complexity
"The brute force would be O(n²) with nested loops,
but given n can be 10⁵, we need something faster."
```

**Step 3: Optimize**
- Can we sort? (O(n log n))
- Can we use hash map? (O(1) lookups)
- Can we use two pointers? (O(n) instead of O(n²))
- Is there a mathematical pattern?

**Step 4: State Your Complexity**
```
"My solution is O(n log n) time because of sorting,
and O(n) space for the hash map.
Given the constraints of n ≤ 10⁵, this should pass."
```

### Quick Reference: Data Structure Complexities

| Operation | Array | LinkedList | Stack | Queue | Hash Map | Heap | BST (balanced) |
|-----------|-------|------------|-------|-------|----------|------|----------------|
| Access | O(1) | O(n) | - | - | O(1)* | - | O(log n) |
| Search | O(n) | O(n) | O(n) | O(n) | O(1)* | O(n) | O(log n) |
| Insert | O(n) | O(1)** | O(1) | O(1) | O(1)* | O(log n) | O(log n) |
| Delete | O(n) | O(1)** | O(1) | O(1) | O(1)* | O(log n) | O(log n) |

*Average case, can be O(n) worst case  
**At known position

### Practice Problems by Complexity

**O(1)**: Valid Parentheses (with counter), Linked List cycle detection (Floyd's)

**O(log n)**: Binary Search, First Bad Version, Search in Rotated Sorted Array

**O(n)**: Two Sum, Valid Anagram, Maximum Subarray, Merge Two Sorted Lists

**O(n log n)**: Merge Intervals, Meeting Rooms, Kth Largest Element

**O(n²)**: 3Sum, Longest Palindromic Substring

**O(2ⁿ)**: Subsets, Permutations, Combination Sum

---

## Final Interview Checklist

✅ **Always ask about constraints first**  
✅ **State your approach and complexity before coding**  
✅ **Don't forget to analyze space complexity too**  
✅ **Consider trade-offs** (time vs space)  
✅ **Remember the math**: n ≤ 10⁴ → O(n log n), n ≤ 10⁶ → O(n)  
✅ **Watch for hidden costs**: slicing, sorting, hash operations  
✅ **Optimize only when asked** - brute force first is okay!  
✅ **Think out loud** - explain your complexity analysis  

---

## Quick Complexity Cheat Sheet

```
O(1)      → Direct access, math operations
O(log n)  → Binary search, balanced tree ops
O(n)      → Single loop, linear scan
O(n log n)→ Sorting, divide and conquer
O(n²)     → Two nested loops
O(2ⁿ)     → Subsets, recursion with 2 branches
O(n!)     → Permutations
```

**Golden Rule**: When in doubt, test with the constraint boundaries!

Good luck with your MAANG interviews! 🚀