"""
Number of Islands (200. LeetCode)
https://leetcode.com/problems/number-of-islands/

===========================================
PROBLEM
===========================================
Given a 2D grid of '1's (land) and '0's (water).
Count the number of islands.
An island is surrounded by water and formed by connecting lands horizontally/vertically.

===========================================
WORKFLOW
===========================================

1. Create visited = [[0]*m for _ in range(n)]   (same size as grid)
2. count = 0

3. Iterate through ALL cells in grid:
   for row in range(n):
       for col in range(m):
           - IF grid[row][col] == '1' AND not visited[row][col]:
             * count += 1                  (found new island!)
             * BFS/DFS from (row, col)     (mark all connected land as visited)

4. Return count

===========================================
8 DIRECTIONS (Striver's approach)
===========================================

From cell (row, col), check all 8 neighbors:

        (row-1,col-1)  (row-1,col)  (row-1,col+1)
                   \\       |       /
                    \\      |      /
        (row,col-1) --- (row,col) --- (row,col+1)
                    /       |      \\
                   /        |       \\
        (row+1,col-1)  (row+1,col)  (row+1,col+1)

Using nested loop: delrow = -1 to 1, delcol = -1 to 1
Skip when delrow == 0 AND delcol == 0 (that's the cell itself)

===========================================
4 DIRECTIONS (Standard LeetCode)
===========================================

For THIS problem, LeetCode says "horizontally or vertically"
So we use only 4 directions: UP, DOWN, LEFT, RIGHT

        (row-1, col)       # UP
            |
(row, col-1) - (row, col) - (row, col+1)
            |
        (row+1, col)       # DOWN

===========================================
"""

from collections import deque


def numIslands(grid: list) -> int:
    """
    Count number of islands using BFS (4 directions).
    """
    if not grid:
        return 0
    
    n = len(grid)       # rows
    m = len(grid[0])    # cols
    vis = [[0] * m for _ in range(n)]
    count = 0
    
    # 4 directions: UP, DOWN, LEFT, RIGHT
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def bfs(row, col):
        queue = deque([(row, col)])
        vis[row][col] = 1
        
        while queue:
            r, c = queue.popleft()
            
            # Check all 4 directions
            for dr, dc in directions:
                nrow = r + dr
                ncol = c + dc
                
                # Check bounds AND is land AND not visited
                if (0 <= nrow < n and 0 <= ncol < m and 
                    grid[nrow][ncol] == '1' and not vis[nrow][ncol]):
                    vis[nrow][ncol] = 1
                    queue.append((nrow, ncol))
    
    # Iterate through ALL cells
    for row in range(n):
        for col in range(m):
            if grid[row][col] == '1' and not vis[row][col]:
                count += 1      # Found new island!
                bfs(row, col)   # Mark all connected land
    
    return count


def numIslands_DFS(grid: list) -> int: # Recommended for
    """
    Count islands using DFS (recursive, 4 directions).
    """
    if not grid:
        return 0
    
    n = len(grid)
    m = len(grid[0])
    vis = [[0] * m for _ in range(n)]
    count = 0
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def dfs(row, col):
        vis[row][col] = 1
        
        for dr, dc in directions:
            nrow = row + dr
            ncol = col + dc
            
            if (0 <= nrow < n and 0 <= ncol < m and 
                grid[nrow][ncol] == '1' and not vis[nrow][ncol]):
                dfs(nrow, ncol)
    
    for row in range(n):
        for col in range(m):
            if grid[row][col] == '1' and not vis[row][col]:
                count += 1
                dfs(row, col)
    
    return count



def numIslands_SinkDFS(grid: list) -> int:
    """
    Count islands using DFS (Space Optimized).
    Instead of 'vis' array, we turn '1' to '0' (Sink the island).
    """
    if not grid:
        return 0
    
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    def dfs(r, c):
        grid[r][c] = '0'  # Mark as visited (Sink it)
        
        # UP
        if r > 0 and grid[r-1][c] == '1':
            dfs(r-1, c)
        # DOWN
        if r+1 < rows and grid[r+1][c] == '1':
            dfs(r+1, c)
        # LEFT
        if c > 0 and grid[r][c-1] == '1':
            dfs(r, c-1)
        # RIGHT
        if c+1 < cols and grid[r][c+1] == '1':
            dfs(r, c+1)
            
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
    
    return count

























# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    
    # TEST 1: LeetCode Example 1
    grid1 = [
        ['1', '1', '1', '1', '0'],
        ['1', '1', '0', '1', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '0', '0', '0']
    ]
    assert numIslands([row[:] for row in grid1]) == 1
    assert numIslands_DFS([row[:] for row in grid1]) == 1
    # Use deep copy because SinkDFS modifies the grid
    assert numIslands_SinkDFS([row[:] for row in grid1]) == 1
    print("TEST 1 PASSED: 1 island")
    
    # TEST 2: LeetCode Example 2
    grid2 = [
        ['1', '1', '0', '0', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '1', '0', '0'],
        ['0', '0', '0', '1', '1']
    ]
    assert numIslands([row[:] for row in grid2]) == 3
    assert numIslands_DFS([row[:] for row in grid2]) == 3
    assert numIslands_SinkDFS([row[:] for row in grid2]) == 3
    print("TEST 2 PASSED: 3 islands")
    
    # TEST 3: All water
    grid3 = [
        ['0', '0', '0'],
        ['0', '0', '0']
    ]
    assert numIslands([row[:] for row in grid3]) == 0
    assert numIslands_DFS([row[:] for row in grid3]) == 0
    assert numIslands_SinkDFS([row[:] for row in grid3]) == 0
    print("TEST 3 PASSED: 0 islands (all water)")
    
    # TEST 4: All land
    grid4 = [
        ['1', '1'],
        ['1', '1']
    ]
    assert numIslands([row[:] for row in grid4]) == 1
    assert numIslands_DFS([row[:] for row in grid4]) == 1
    assert numIslands_SinkDFS([row[:] for row in grid4]) == 1
    print("TEST 4 PASSED: 1 island (all land)")
    
    # TEST 5: Single cell land
    grid5 = [['1']]
    assert numIslands([row[:] for row in grid5]) == 1
    assert numIslands_SinkDFS([row[:] for row in grid5]) == 1
    print("TEST 5 PASSED: 1 island (single cell)")
    
    # TEST 6: Diagonal islands (4-dir = 2 islands, 8-dir = 1 island)
    grid6 = [
        ['1', '0'],
        ['0', '1']
    ]
    assert numIslands([row[:] for row in grid6]) == 2  # 4 directions
    # Note: numIslands_8Dir was removed based on previous content
    assert numIslands_SinkDFS([row[:] for row in grid6]) == 2
    print("TEST 6 PASSED: 4-dir=2 islands")

    
    print("\n" + "=" * 40)
    print("ALL 6 TESTS PASSED!")
    print("=" * 40)
