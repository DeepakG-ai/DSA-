"""
Rotten Oranges (994. LeetCode)
https://leetcode.com/problems/rotting-oranges/

===========================================
PROBLEM
===========================================
Given a grid:
- 0 = Empty cell
- 1 = Fresh orange
- 2 = Rotten orange

Every minute, any fresh orange adjacent (4-directional) to a rotten orange becomes rotten.
Return the minimum number of minutes until no cell has a fresh orange.
If this is impossible, return -1.

===========================================
WORKFLOW (Multi-Source BFS)
===========================================

1. Create queue
2. Create vis = [[0]*m for _ in range(n)]   (copy of grid)
3. Initial time = 0, fresh_count = 0

4. First Pass - Find all starting points:
   for row in range(n):
       for col in range(m):
           - IF grid[row][col] == 2:   (rotten)
             * Add (row, col, time=0) to queue
             * Mark vis[row][col] = 2
           - ELIF grid[row][col] == 1: (fresh)
             * Count fresh oranges
             * Mark vis[row][col] = 1

5. BFS - Process queue level by level:
   while queue:
       - Pop (row, col, t) from queue
       - For each 4 neighbors:
         * Skip if out of bounds
         * Skip if vis[nrow][ncol] != 1 (not fresh)
         * IF fresh (vis == 1):
           - Mark vis[nrow][ncol] = 2 (now rotten)
           - Add (nrow, ncol, t+1) to queue
           - Decrease fresh_count
           - Update max_time = t+1

6. Return:
   - If fresh_count > 0: return -1 (impossible)
   - Else: return max_time

===========================================
"""

from collections import deque


def orangesRotting(grid: list) -> int:
    """
    Multi-Source BFS to find minimum time for all oranges to rot.
    
    Time: O(n * m) - Visit every cell once
    Space: O(n * m) - Queue + Visited matrix
    """
    if not grid:
        return 0
    
    n = len(grid)       # rows
    m = len(grid[0])    # cols
    
    vis = [[0] * m for _ in range(n)]
    queue = deque()
    fresh_count = 0
    
    # 4 directions: UP, DOWN, LEFT, RIGHT
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Step 1: Find all rotten oranges and fresh oranges
    for row in range(n):
        for col in range(m):
            if grid[row][col] == 2:
                # Rotten orange - add to queue with time=0
                queue.append((row, col, 0))
                vis[row][col] = 2
            elif grid[row][col] == 1:
                # Fresh orange - count it
                fresh_count += 1
                vis[row][col] = 1
            # 0 = empty, vis stays 0
    
    max_time = 0
    
    # Step 2: BFS - rot adjacent fresh oranges
    while queue:
        row, col, t = queue.popleft()
        
        for dr, dc in directions:
            nrow = row + dr
            ncol = col + dc
            
            # Check bounds AND is fresh (vis == 1)
            if 0 <= nrow < n and 0 <= ncol < m and vis[nrow][ncol] == 1:
                # Rot this orange
                vis[nrow][ncol] = 2
                fresh_count -= 1
                queue.append((nrow, ncol, t + 1))
                max_time = t + 1
    
    # Step 3: Check if any fresh oranges remain
    if fresh_count > 0:
        return -1
    
    return max_time




















# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    
    # TEST 1: LeetCode Example 1
    # [[2,1,1],
    #  [1,1,0],
    #  [0,1,1]]
    # Answer: 4 minutes
    grid1 = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1]
    ]
    result1 = orangesRotting([row[:] for row in grid1])
    print(f"TEST 1: {result1}")
    assert result1 == 4, f"Expected 4, got {result1}"
    print("TEST 1 PASSED: 4 minutes\n")
    
    # TEST 2: LeetCode Example 2 (Impossible)
    # [[2,1,1],
    #  [0,1,1],
    #  [1,0,1]]  <- Corner orange cannot be reached
    # Answer: -1
    grid2 = [
        [2, 1, 1],
        [0, 1, 1],
        [1, 0, 1]
    ]
    result2 = orangesRotting([row[:] for row in grid2])
    print(f"TEST 2: {result2}")
    assert result2 == -1, f"Expected -1, got {result2}"
    print("TEST 2 PASSED: -1 (impossible)\n")
    
    # TEST 3: No fresh oranges
    # [[0,2]]
    # Answer: 0 (already done)
    grid3 = [[0, 2]]
    result3 = orangesRotting([row[:] for row in grid3])
    print(f"TEST 3: {result3}")
    assert result3 == 0, f"Expected 0, got {result3}"
    print("TEST 3 PASSED: 0 minutes (no fresh)\n")
    
    # TEST 4: All fresh, no rotten
    # [[1,1]]
    # Answer: -1 (no way to rot)
    grid4 = [[1, 1]]
    result4 = orangesRotting([row[:] for row in grid4])
    print(f"TEST 4: {result4}")
    assert result4 == -1, f"Expected -1, got {result4}"
    print("TEST 4 PASSED: -1 (no rotten source)\n")
    
    # TEST 5: Empty grid
    grid5 = [[0]]
    result5 = orangesRotting([row[:] for row in grid5])
    print(f"TEST 5: {result5}")
    assert result5 == 0, f"Expected 0, got {result5}"
    print("TEST 5 PASSED: 0 (empty grid)\n")
    
    # TEST 6: Multiple rotten sources (Multi-Source BFS)
    # [[2,1,1],
    #  [1,1,1],
    #  [1,1,2]]
    # Rotten at (0,0) and (2,2) spread simultaneously
    grid6 = [
        [2, 1, 1],
        [1, 1, 1],
        [1, 1, 2]
    ]
    result6 = orangesRotting([row[:] for row in grid6])
    print(f"TEST 6: {result6}")
    assert result6 == 2, f"Expected 2, got {result6}"
    print("TEST 6 PASSED: 2 minutes (multi-source)\n")
    
    print("=" * 40)
    print("ALL 6 TESTS PASSED!")
    print("=" * 40)