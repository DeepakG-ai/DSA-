"""
Pacific Atlantic Water Flow (LeetCode 417)
https://leetcode.com/problems/pacific-atlantic-water-flow/

===========================================
PROBLEM
===========================================
Given an m x n matrix of heights representing an island:
    - Pacific Ocean touches LEFT and TOP edges
    - Atlantic Ocean touches RIGHT and BOTTOM edges

Water can flow from a cell to adjacent cells (up, down, left, right)
only if the adjacent cell's height is LESS THAN OR EQUAL to current cell.

Find all cells where water can flow to BOTH oceans.

===========================================
VISUALIZATION
===========================================

         Pacific Ocean (TOP)
              |
              v
    Pacific   +---+---+---+---+---+
    Ocean --> | 1 | 2 | 2 | 3 | 5 |
    (LEFT)    +---+---+---+---+---+
              | 3 | 2 | 3 | 4 | 4 |
              +---+---+---+---+---+
              | 2 | 4 | 5 | 3 | 1 |
              +---+---+---+---+---+
              | 6 | 7 | 1 | 4 | 5 |
              +---+---+---+---+---+
              | 5 | 1 | 1 | 2 | 4 | --> Atlantic Ocean (RIGHT)
              +---+---+---+---+---+
                              |
                              v
                    Atlantic Ocean (BOTTOM)

===========================================
KEY INSIGHT (Reverse Thinking!)
===========================================

NORMAL APPROACH (Hard):
    - From each cell, check if water can reach both oceans
    - Very complex path tracking!

REVERSE APPROACH (Smart!):
    - Start from ocean edges and go UPHILL (find cells that can drain TO ocean)
    - Atlantic: Start from RIGHT and BOTTOM edges
    - Pacific: Start from LEFT and TOP edges
    - Find INTERSECTION of both sets!

Why reverse works?
    - If water from cell A can flow TO Pacific, then
      starting from Pacific and going UPHILL, we can reach A!

===========================================
WORKFLOW (Multi-Source DFS)
===========================================

1. Create two visited sets:
   - pac_vis = set()
   - atl_vis = set()

2. Start DFS from Pacific edges (LEFT column + TOP row):
   - Go to neighbors if neighbor height >= current height (uphill)
   - Mark all reachable cells

3. Start DFS from Atlantic edges (RIGHT column + BOTTOM row):
   - Same logic, mark all reachable cells

4. Return INTERSECTION of both sets!

===========================================
"""

from typing import List


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights: return []
        
        rows, cols = len(heights), len(heights[0])
        
        # 1. Create two sets to track reachability
        pac_vis, atl_vis = set(), set()
        
        # 2. DFS Helper (Climbing UP logic)
        def dfs(r, c, visit_set, prev_height):
            # Check Bounds & Already Visited
            if ((r, c) in visit_set or 
                r < 0 or c < 0 or r == rows or c == cols or 
                heights[r][c] < prev_height): # CONSTRAINT: Must be Higher or Equal
                return
            
            visit_set.add((r, c))
            
            # Go to all 4 neighbors
            dfs(r + 1, c, visit_set, heights[r][c])
            dfs(r - 1, c, visit_set, heights[r][c])
            dfs(r, c + 1, visit_set, heights[r][c])
            dfs(r, c - 1, visit_set, heights[r][c])
            
        # 3. Launch DFS from the Coastlines
        for c in range(cols):
            dfs(0, c, pac_vis, heights[0][c])           # Top Row (Pacific)
            dfs(rows - 1, c, atl_vis, heights[rows-1][c]) # Bottom Row (Atlantic)
            
        for r in range(rows):
            dfs(r, 0, pac_vis, heights[r][0])           # Left Col (Pacific)
            dfs(r, cols - 1, atl_vis, heights[r][cols-1]) # Right Col (Atlantic)
            
        # 4. Find the Intersection (Cells in BOTH sets)
        res = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) in pac_vis and (r, c) in atl_vis:
                    res.append([r, c])
                    
        return res


# ============================================
# BFS SOLUTION (Same Logic, Different Traversal)
# ============================================
from collections import deque

class Solution_BFS:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights: return []
        
        rows, cols = len(heights), len(heights[0])
        
        # 1. Create two sets to track reachability
        pac_vis, atl_vis = set(), set()
        
        # 2. BFS Helper (Climbing UP logic)
        def bfs(queue, visit_set):
            while queue:
                r, c = queue.popleft()
                
                # Go to all 4 neighbors
                for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                    nr, nc = r + dr, c + dc
                    
                    # Check Bounds & Already Visited & Height Constraint
                    if (nr < 0 or nc < 0 or nr == rows or nc == cols or
                        (nr, nc) in visit_set or
                        heights[nr][nc] < heights[r][c]):  # Must be Higher or Equal
                        continue
                    
                    visit_set.add((nr, nc))
                    queue.append((nr, nc))
        
        # 3. Initialize queues with coastline cells
        pac_queue = deque()
        atl_queue = deque()
        
        for c in range(cols):
            pac_vis.add((0, c))                    # Top Row (Pacific)
            pac_queue.append((0, c))
            atl_vis.add((rows - 1, c))             # Bottom Row (Atlantic)
            atl_queue.append((rows - 1, c))
            
        for r in range(rows):
            pac_vis.add((r, 0))                    # Left Col (Pacific)
            pac_queue.append((r, 0))
            atl_vis.add((r, cols - 1))             # Right Col (Atlantic)
            atl_queue.append((r, cols - 1))
        
        # 4. Launch BFS from the Coastlines
        bfs(pac_queue, pac_vis)
        bfs(atl_queue, atl_vis)
            
        # 5. Find the Intersection (Cells in BOTH sets)
        res = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) in pac_vis and (r, c) in atl_vis:
                    res.append([r, c])
                    
        return res


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    sol = Solution()
    
    # TEST 1: LeetCode Example 1
    print("=" * 50)
    print("TEST 1: LeetCode Example")
    print("=" * 50)
    
    heights1 = [
        [1, 2, 2, 3, 5],
        [3, 2, 3, 4, 4],
        [2, 4, 5, 3, 1],
        [6, 7, 1, 4, 5],
        [5, 1, 1, 2, 4]
    ]
    
    result = sol.pacificAtlantic(heights1)
    expected = [[0,4], [1,3], [1,4], [2,2], [3,0], [3,1], [4,0]]
    
    print(f"Result:   {result}")
    print(f"Expected: {expected}")
    print("PASSED!\n")
    
    
    # TEST 2: Single cell
    print("=" * 50)
    print("TEST 2: Single Cell")
    print("=" * 50)
    
    heights2 = [[1]]
    result = sol.pacificAtlantic(heights2)
    print(f"Result: {result}")  # [[0, 0]]
    print("PASSED!\n")
    
    
    # TEST 3: All same height
    print("=" * 50)
    print("TEST 3: All Same Height")
    print("=" * 50)
    
    heights3 = [
        [1, 1],
        [1, 1]
    ]
    result = sol.pacificAtlantic(heights3)
    print(f"Result: {result}")  # All 4 cells
    print("PASSED!\n")
    
    
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
