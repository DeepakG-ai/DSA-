"""
Number of Provinces (Connected Components)
LeetCode 547: https://leetcode.com/problems/number-of-provinces/

===========================================
PROBLEM
===========================================
Given n cities. Some cities are connected directly, some are not.
A province is a group of directly or indirectly connected cities.
Return the number of provinces.

Input: Adjacency matrix (isConnected[i][j] = 1 if city i and j are connected)
Output: Number of provinces (connected components)

===========================================
WORKFLOW
===========================================

1. Create vis = [0] * n           (visited array)
2. count = 0                      (number of provinces)

3. For each node from 0 to n-1:
   - IF node NOT visited:
     * count += 1                 (found new province!)
     * Run BFS/DFS from this node (mark all connected nodes as visited)

4. Return count

===========================================
"""

from collections import deque


def findCircleNum(isConnected: list) -> int:
    """
    Find number of provinces using BFS.
    
    Args:
        isConnected: Adjacency matrix (n x n)
    
    Returns:
        Number of connected components (provinces)
    """
    n = len(isConnected)
    vis = [0] * n
    count = 0
    
    def bfs(start):
        queue = deque([start])
        vis[start] = 1
        
        while queue:
            node = queue.popleft()
            
            # Check all possible neighbors (0 to n-1)
            for neighbor in range(n):
                # If connected AND not visited
                if isConnected[node][neighbor] == 1 and not vis[neighbor]:
                    vis[neighbor] = 1
                    queue.append(neighbor)
    
    # Loop through ALL nodes
    for node in range(n):
        if not vis[node]:
            count += 1      # Found new province!
            bfs(node)       # Mark all nodes in this province
    
    return count


def findCircleNum_DFS(isConnected: list) -> int:
    """
    Find number of provinces using DFS (recursive).
    """
    n = len(isConnected)
    vis = [0] * n
    count = 0
    
    def dfs(node):
        vis[node] = 1
        for neighbor in range(n):
            if isConnected[node][neighbor] == 1 and not vis[neighbor]:
                dfs(neighbor)
    
    for node in range(n):
        if not vis[node]:
            count += 1
            dfs(node)
    
    return count


# ============================================
# TEST CASES WITH ASSERT
# ============================================

if __name__ == "__main__":
    
    # TEST 1: LeetCode Example 1
    # Cities: 0 - 1, 2 is alone
    # [[1,1,0],
    #  [1,1,0],
    #  [0,0,1]]
    # Two provinces: {0,1} and {2}
    isConnected1 = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 1]
    ]
    assert findCircleNum(isConnected1) == 2
    assert findCircleNum_DFS(isConnected1) == 2
    print("TEST 1 PASSED: 2 provinces")
    
    # TEST 2: LeetCode Example 2
    # Cities: 0, 1, 2 all separate
    # [[1,0,0],
    #  [0,1,0],
    #  [0,0,1]]
    # Three provinces: {0}, {1}, {2}
    isConnected2 = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    assert findCircleNum(isConnected2) == 3
    assert findCircleNum_DFS(isConnected2) == 3
    print("TEST 2 PASSED: 3 provinces (all separate)")
    
    # TEST 3: All connected
    # [[1,1,1],
    #  [1,1,1],
    #  [1,1,1]]
    # One province: {0,1,2}
    isConnected3 = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    assert findCircleNum(isConnected3) == 1
    assert findCircleNum_DFS(isConnected3) == 1
    print("TEST 3 PASSED: 1 province (all connected)")
    
    # TEST 4: Single city
    isConnected4 = [[1]]
    assert findCircleNum(isConnected4) == 1
    assert findCircleNum_DFS(isConnected4) == 1
    print("TEST 4 PASSED: 1 city = 1 province")
    
    # TEST 5: Two separate pairs
    # 0-1 connected, 2-3 connected
    isConnected5 = [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 1]
    ]
    assert findCircleNum(isConnected5) == 2
    assert findCircleNum_DFS(isConnected5) == 2
    print("TEST 5 PASSED: 2 provinces (two pairs)")
    
    # TEST 6: Chain connection (0-1-2-3)
    isConnected6 = [
        [1, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 1, 1, 1],
        [0, 0, 1, 1]
    ]
    assert findCircleNum(isConnected6) == 1
    assert findCircleNum_DFS(isConnected6) == 1
    print("TEST 6 PASSED: 1 province (chain)")
    
    print("\n" + "=" * 40)
    print("ALL 6 TESTS PASSED!")
    print("=" * 40)
