# Complete Guide to Time & Space Complexity for MAANG Interviews

## Table of Contents
1. [Foundation Concepts](#foundation-concepts)
2. [Big O Notation Explained](#big-o-notation-explained)
3. [Time Complexity Analysis](#time-complexity-analysis)
4. [Space Complexity Analysis](#space-complexity-analysis)
5. [Complexity Classes](#complexity-classes)
6. [Input Size vs Complexity](#input-size-vs-complexity)
7. [Advanced Techniques](#advanced-techniques)
8. [Interview Patterns](#interview-patterns)
9. [Practice Problems](#practice-problems)

---

## Foundation Concepts

### What is Complexity Analysis?

Complexity analysis helps us understand:
- **Time Complexity**: How execution time grows as input size increases
- **Space Complexity**: How memory usage grows as input size increases

### Why Does It Matter?

In interviews, you need to:
1. Analyze your solution's efficiency
2. Compare different approaches
3. Optimize when needed
4. Understand scalability

---

## Big O Notation Explained

### What is Big O?

Big O describes the **worst-case scenario** upper bound of an algorithm's growth rate.

### Common Notations

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Array access by index |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Single loop through array |
| O(n log n) | Linearithmic | Merge sort, heap sort |
| O(n²) | Quadratic | Nested loops |
| O(n³) | Cubic | Triple nested loops |
| O(2ⁿ) | Exponential | Recursive fibonacci |
| O(n!) | Factorial | Generating all permutations |

### Visualization of Growth

```
Operations for n = 10:
O(1)      = 1
O(log n)  = 3
O(n)      = 10
O(n log n)= 30
O(n²)     = 100
O(2ⁿ)     = 1,024
O(n!)     = 3,628,800

Operations for n = 100:
O(1)      = 1
O(log n)  = 7
O(n)      = 100
O(n log n)= 700
O(n²)     = 10,000
O(2ⁿ)     = 1.27 × 10³⁰
O(n!)     = 9.33 × 10¹⁵⁷
```

---

## Time Complexity Analysis

### Rule 1: Drop Constants

```python
# Both are O(n), not O(2n) or O(3n)
def example1(arr):
    for i in arr:  # n operations
        print(i)
    for i in arr:  # n operations
        print(i)
    # Total: 2n → O(n)

def example2(arr):
    for i in arr:
        print(i)
        print(i)
        print(i)
    # Total: 3n → O(n)
```

### Rule 2: Drop Non-Dominant Terms

```python
# O(n² + n) → O(n²)
def example(arr):
    # O(n²) dominates
    for i in arr:
        for j in arr:
            print(i, j)
    
    # O(n) is dropped
    for i in arr:
        print(i)
```

### Rule 3: Different Inputs = Different Variables

```python
# This is O(a + b), NOT O(n)
def process_two_arrays(arr1, arr2):
    for i in arr1:  # O(a)
        print(i)
    for j in arr2:  # O(b)
        print(j)

# This is O(a * b), NOT O(n²)
def nested_different(arr1, arr2):
    for i in arr1:
        for j in arr2:
            print(i, j)
```

### Analyzing Loops

#### Single Loop
```python
# O(n)
for i in range(n):
    print(i)
```

#### Nested Loops (Same Size)
```python
# O(n²)
for i in range(n):
    for j in range(n):
        print(i, j)
```

#### Nested Loops (Different Sizes)
```python
# O(n * m)
for i in range(n):
    for j in range(m):
        print(i, j)
```

#### Consecutive Loops
```python
# O(a + b)
for i in range(a):
    print(i)
for j in range(b):
    print(j)
```

#### Loop with Increment Changes
```python
# O(log n) - dividing by 2 each time
i = 1
while i < n:
    print(i)
    i *= 2  # 1, 2, 4, 8, 16...

# O(log n) - halving each time
i = n
while i > 0:
    print(i)
    i //= 2
```

#### Partial Iterations
```python
# O(n²) - still quadratic even though not full n*n
for i in range(n):
    for j in range(i):  # Goes from 0 to i
        print(i, j)
# Total: 0 + 1 + 2 + ... + (n-1) = n(n-1)/2 → O(n²)
```

### Common Algorithm Complexities

#### Sorting Algorithms
```python
# O(n²) - Bubble, Insertion, Selection Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# O(n log n) - Merge Sort, Quick Sort (average), Heap Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

#### Searching Algorithms
```python
# O(n) - Linear Search
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# O(log n) - Binary Search (sorted array)
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

#### Recursive Algorithms
```python
# O(2ⁿ) - Fibonacci (naive)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# O(n) - Fibonacci (with memoization)
def fibonacci_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]
```

### Master Theorem for Recursion

For recurrences of the form: **T(n) = aT(n/b) + f(n)**

```python
# T(n) = 2T(n/2) + O(n) → O(n log n)
# Example: Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])      # T(n/2)
    right = merge_sort(arr[mid:])     # T(n/2)
    return merge(left, right)          # O(n)

# T(n) = 2T(n/2) + O(1) → O(n)
# Example: Binary tree traversal per level
```

---

## Space Complexity Analysis

### What Counts as Space?

1. **Auxiliary Space**: Extra space used by algorithm (excluding input)
2. **Input Space**: Space used to store input
3. **Total Space**: Auxiliary + Input

In interviews, we usually discuss **auxiliary space**.

### Components of Space Complexity

```python
def example(arr):
    # 1. Variables: O(1)
    count = 0
    max_val = float('-inf')
    
    # 2. Data Structures: O(n)
    result = []  # Size grows with input
    visited = set()  # Size grows with input
    
    # 3. Recursion Stack: O(depth)
    # Each recursive call adds to stack
    
    # 4. Input: Not counted in auxiliary space
    # arr is given, not created by us
```

### Space Complexity Examples

#### O(1) - Constant Space
```python
def sum_array(arr):
    total = 0  # Single variable
    for num in arr:
        total += num
    return total
# Only 'total' variable, independent of input size
```

#### O(n) - Linear Space
```python
def create_copy(arr):
    result = []  # New array of size n
    for num in arr:
        result.append(num)
    return result

def use_set(arr):
    seen = set()  # Can grow up to size n
    for num in arr:
        seen.add(num)
    return len(seen)
```

#### O(n) - Recursion Stack
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
# Stack depth = n calls
# Space: O(n) for recursion stack
```

#### O(log n) - Logarithmic Space
```python
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, left, mid-1)
    else:
        return binary_search_recursive(arr, target, mid+1, right)
# Stack depth = log n calls
```

#### O(n²) - Quadratic Space
```python
def create_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    return matrix
# n × n matrix = n² space
```

### In-Place vs Out-of-Place

```python
# In-place: O(1) space - modifies input
def reverse_in_place(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

# Out-of-place: O(n) space - creates new array
def reverse_new_array(arr):
    return arr[::-1]
```

---

## Complexity Classes

### Performance Hierarchy (Best to Worst)

```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
```

### When Each Complexity is Acceptable

| Complexity | Max Input Size | Use Case |
|------------|----------------|----------|
| O(1) | Any | Constant operations |
| O(log n) | 10¹⁸ | Binary search, balanced trees |
| O(n) | 10⁸ | Single pass algorithms |
| O(n log n) | 10⁶ | Efficient sorting |
| O(n²) | 10⁴ | Small inputs, nested iterations |
| O(n³) | 500 | Dynamic programming with 3D arrays |
| O(2ⁿ) | 20 | Backtracking, subsets |
| O(n!) | 11 | Permutations |

---

## Input Size vs Complexity

### The 1-Second Rule

Modern computers: ~10⁸ to 10⁹ operations per second

### Constraint Guidelines

| Constraint | Expected Complexity | Example Algorithms |
|------------|---------------------|-------------------|
| n ≤ 10 | O(n!) | Permutations |
| n ≤ 20 | O(2ⁿ) | Subset generation, backtracking |
| n ≤ 500 | O(n³) | Floyd-Warshall, DP with 3 dimensions |
| n ≤ 5,000 | O(n²) | Bubble sort, nested loops |
| n ≤ 10⁶ | O(n log n) | Merge sort, heap operations |
| n ≤ 10⁸ | O(n) | Linear scan, hash operations |
| n ≤ 10¹⁸ | O(log n) | Binary search, GCD |

### Real Interview Constraints

```python
# Constraint: n ≤ 10⁴
# ✅ O(n²) will work - 10⁴ × 10⁴ = 10⁸ operations
def two_sum_brute_force(arr, target):
    n = len(arr)
    for i in range(n):
        for j in range(i+1, n):
            if arr[i] + arr[j] == target:
                return [i, j]

# Constraint: n ≤ 10⁶
# ❌ O(n²) will TLE - 10⁶ × 10⁶ = 10¹² operations
# ✅ O(n) or O(n log n) needed
def two_sum_optimal(arr, target):
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

---

## Advanced Techniques

### Amortized Analysis

Some operations are expensive occasionally but cheap on average.

```python
# Dynamic Array (like Python list)
# append() is O(1) amortized
arr = []
for i in range(n):
    arr.append(i)  # Occasionally O(n) when resizing, but O(1) amortized
# Total: O(n) for n operations → O(1) per operation
```

### Best, Average, Worst Case

```python
# Quick Sort
# Best Case: O(n log n) - balanced partitions
# Average Case: O(n log n)
# Worst Case: O(n²) - already sorted with bad pivot

# Linear Search
# Best Case: O(1) - found at first position
# Average Case: O(n/2) → O(n)
# Worst Case: O(n) - element at end or not present
```

### Multi-variable Complexity

```python
# O(V + E) - Graph traversal
def bfs(graph):
    # V = vertices, E = edges
    visited = set()
    queue = [start]
    
    while queue:  # O(V) - visit each vertex once
        node = queue.pop(0)
        for neighbor in graph[node]:  # O(E) total across all vertices
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

---

## Interview Patterns

### Pattern 1: Two Pointers - O(n) Time, O(1) Space

```python
# Find pair that sums to target in sorted array
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]
# Time: O(n), Space: O(1)
```

### Pattern 2: Sliding Window - O(n) Time, O(k) Space

```python
# Maximum sum subarray of size k
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i-k] + arr[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
# Time: O(n), Space: O(1)
```

### Pattern 3: Hash Map - O(n) Time, O(n) Space

```python
# Find first non-repeating character
def first_unique_char(s):
    freq = {}
    for char in s:  # O(n)
        freq[char] = freq.get(char, 0) + 1
    
    for char in s:  # O(n)
        if freq[char] == 1:
            return char
    return None
# Time: O(n), Space: O(n) - at most 26 chars for lowercase English
```

### Pattern 4: Binary Search - O(log n) Time, O(1) Space

```python
# Find element in rotated sorted array
def search_rotated(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        
        # Left half is sorted
        if arr[left] <= arr[mid]:
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
# Time: O(log n), Space: O(1)
```

### Pattern 5: DFS/BFS - O(V+E) Time, O(V) Space

```python
# Graph traversal
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited
# Time: O(V + E), Space: O(V) for recursion stack and visited set
```

### Pattern 6: Dynamic Programming

```python
# Fibonacci - Top Down (Memoization)
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]
# Time: O(n), Space: O(n)

# Fibonacci - Bottom Up (Tabulation)
def fib_dp(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
# Time: O(n), Space: O(n)

# Fibonacci - Space Optimized
def fib_optimized(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    return prev1
# Time: O(n), Space: O(1)
```

---

## Practice Problems

### Beginner Level

1. **Array Sum** - O(n) time, O(1) space
2. **Find Maximum** - O(n) time, O(1) space
3. **Reverse Array** - O(n) time, O(1) space in-place
4. **Linear Search** - O(n) time, O(1) space
5. **Remove Duplicates** - O(n) time, O(n) space with set

### Intermediate Level

6. **Two Sum** - O(n) time, O(n) space with hash map
7. **Valid Anagram** - O(n) time, O(1) space (26 letters)
8. **Merge Two Sorted Arrays** - O(n+m) time, O(n+m) space
9. **Binary Search** - O(log n) time, O(1) space
10. **Longest Substring Without Repeating** - O(n) time, O(min(n,m)) space

### Advanced Level

11. **Median of Two Sorted Arrays** - O(log(min(n,m))) time, O(1) space
12. **Merge K Sorted Lists** - O(n log k) time, O(k) space
13. **Trapping Rain Water** - O(n) time, O(1) space
14. **Word Break** - O(n²) time, O(n) space with DP
15. **LRU Cache** - O(1) time for get/put, O(capacity) space

---

## How to Analyze in Interviews

### Step-by-Step Process

1. **Identify loops and their iterations**
   - Single loop → O(n)
   - Nested loops → multiply complexities
   - Sequential loops → add complexities

2. **Check for recursion**
   - Draw recursion tree
   - Count levels (depth)
   - Count nodes at each level
   - Apply Master Theorem if applicable

3. **Identify data structures used**
   - Arrays, strings → count their size
   - Hash maps, sets → what's stored?
   - Stacks, queues → max size?

4. **Consider best/average/worst cases**
   - Always state which case you're analyzing
   - In interviews, worst case is default

5. **Simplify using rules**
   - Drop constants
   - Drop non-dominant terms
   - Use different variables for different inputs

### Example Analysis

```python
def find_duplicates(arr):
    seen = set()           # Space: O(n) in worst case
    duplicates = []        # Space: O(n) in worst case
    
    for num in arr:        # Time: O(n)
        if num in seen:    # Time: O(1) average for set lookup
            duplicates.append(num)
        else:
            seen.add(num)  # Time: O(1) average
    
    return duplicates

# Analysis:
# Time: O(n) - single loop with O(1) operations inside
# Space: O(n) - seen set can hold up to n elements
```

---

## Interview Tips

### What Interviewers Want to Hear

1. **State your complexity clearly**
   - "This solution has O(n) time complexity and O(1) space complexity"

2. **Explain your reasoning**
   - "We iterate through the array once, so that's O(n). We only use two pointers, so space is O(1)"

3. **Mention trade-offs**
   - "We can solve this in O(n²) time with O(1) space, or O(n) time with O(n) space using a hash map"

4. **Optimize when asked**
   - Start with brute force, then optimize
   - Explain why optimizations work

### Common Mistakes to Avoid

❌ Saying O(n) when you have nested loops
❌ Forgetting to count space for data structures
❌ Confusing O(log n) with O(n)
❌ Not considering the recursion stack space
❌ Using O(n²) when n ≤ 10⁶

### Quick Reference Card

```
Loop Types:
- for i in range(n): → O(n)
- while i < n: i *= 2 → O(log n)
- for i in range(n): for j in range(n): → O(n²)
- for i in range(n): for j in range(i): → O(n²)

Data Structures:
- Array/String → O(n) space
- Hash Map/Set → O(n) space
- Fixed variables → O(1) space
- Recursion depth d → O(d) space

Common Algorithms:
- Binary Search → O(log n)
- Sorting → O(n log n)
- DFS/BFS → O(V + E)
- Two Pointers → O(n)
- Sliding Window → O(n)
```

---

## Final Checklist for Interviews

Before you finish analyzing:

- [ ] Did I count all loops correctly?
- [ ] Did I account for nested operations?
- [ ] Did I consider recursion stack space?
- [ ] Did I count auxiliary data structures?
- [ ] Did I use the right variables for different inputs?
- [ ] Did I mention trade-offs if multiple approaches exist?
- [ ] Can I explain why this complexity is acceptable for given constraints?

---

## Additional Resources

### Key Formulas to Remember

```
Sum of first n numbers: 1 + 2 + 3 + ... + n = n(n+1)/2 → O(n²)

Sum of powers of 2: 1 + 2 + 4 + 8 + ... + 2ⁿ = 2ⁿ⁺¹ - 1 → O(2ⁿ)

Height of complete binary tree: log₂(n) → O(log n)

Number of leaf nodes in complete binary tree: n/2 → O(n)
```

Good luck with your MAANG interviews! Remember, practice is key. Analyze the complexity of every problem you solve.