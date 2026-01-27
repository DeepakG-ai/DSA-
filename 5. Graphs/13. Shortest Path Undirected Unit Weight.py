"""
Shortest Path in Undirected Graph with Unit Weight
GFG: https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph-having-unit-distance/1

===========================================
PROBLEM
===========================================
Given an undirected graph with V vertices and E edges.
Each edge has weight = 1 (unit weight).
Find shortest path from source (0) to all vertices.

===========================================
WHY BFS? (Not DFS or Dijkstra)
===========================================

BFS naturally finds shortest path when all weights are equal!

Why?
    - BFS explores level by level
    - Level 1 = distance 1 from source
    - Level 2 = distance 2 from source
    - First time we reach a node = shortest path!

No need for Dijkstra because all weights are same.

===========================================
ALGORITHM
===========================================

1. Initialize:
    - dist = [-1] * V  (-1 means unreachable)
    - dist[source] = 0
    - queue = [source]

2. BFS:
    - Pop node from queue
    - For each neighbor:
        - If dist[neighbor] == -1 (not visited):
            - dist[neighbor] = dist[node] + 1
            - queue.append(neighbor)

3. Return dist array

===========================================
"""

from typing import List
from collections import deque


class Solution:
    def shortestPath(self, edges: List[List[int]], V: int, E: int, src: int) -> List[int]:
        """
        Shortest path using BFS (unit weight edges).
        
        Time: O(V + E)
        Space: O(V)
        """
        # Build adjacency list (undirected)
        adj = [[] for _ in range(V)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)  # Undirected!
        
        # Initialize distances (-1 = unreachable)
        dist = [-1] * V
        dist[src] = 0
        
        # BFS
        queue = deque([src])
        
        while queue:
            node = queue.popleft()
            
            for neighbor in adj[node]:
                # If not visited yet
                if dist[neighbor] == -1:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        
        return dist


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    sol = Solution()
    
    # TEST 1: GFG Example
    print("=" * 50)
    print("TEST 1: Connected Graph")
    print("=" * 50)
    
    #     0 --- 1 --- 2
    #     |     |
    #     3 --- 4 --- 5 --- 6
    #                 |
    #                 7 --- 8
    
    V1 = 9
    E1 = 10
    edges1 = [
        [0, 1], [0, 3],
        [1, 2], [1, 4],
        [3, 4],
        [4, 5],
        [5, 6], [5, 7],
        [7, 8]
    ]
    
    result = sol.shortestPath(edges1, V1, E1, 0)
    print(f"Result:   {result}")
    print(f"Expected: [0, 1, 2, 1, 2, 3, 4, 4, 5]")
    assert result == [0, 1, 2, 1, 2, 3, 4, 4, 5]
    print("PASSED!\n")
    
    
    # TEST 2: Disconnected
    print("=" * 50)
    print("TEST 2: Disconnected Graph")
    print("=" * 50)
    
    # 0 --- 1    2 --- 3 (separate components)
    
    V2 = 4
    E2 = 2
    edges2 = [[0, 1], [2, 3]]
    
    result = sol.shortestPath(edges2, V2, E2, 0)
    print(f"Result:   {result}")
    print(f"Expected: [0, 1, -1, -1]")
    assert result == [0, 1, -1, -1]
    print("PASSED!\n")
    
    
    # TEST 3: Single Node
    print("=" * 50)
    print("TEST 3: Single Node")
    print("=" * 50)
    
    V3 = 1
    E3 = 0
    edges3 = []
    
    result = sol.shortestPath(edges3, V3, E3, 0)
    print(f"Result:   {result}")
    print(f"Expected: [0]")
    assert result == [0]
    print("PASSED!\n")
    
    
    # TEST 4: Star Graph
    print("=" * 50)
    print("TEST 4: Star Graph (0 is center)")
    print("=" * 50)
    
    #       1
    #       |
    #   2 - 0 - 3
    #       |
    #       4
    
    V4 = 5
    E4 = 4
    edges4 = [[0, 1], [0, 2], [0, 3], [0, 4]]
    
    result = sol.shortestPath(edges4, V4, E4, 0)
    print(f"Result:   {result}")
    print(f"Expected: [0, 1, 1, 1, 1]")
    assert result == [0, 1, 1, 1, 1]
    print("PASSED!\n")
    
    
    # TEST 5: Chain
    print("=" * 50)
    print("TEST 5: Chain Graph")
    print("=" * 50)
    
    # 0 --- 1 --- 2 --- 3 --- 4
    
    V5 = 5
    E5 = 4
    edges5 = [[0, 1], [1, 2], [2, 3], [3, 4]]
    
    result = sol.shortestPath(edges5, V5, E5, 0)
    print(f"Result:   {result}")
    print(f"Expected: [0, 1, 2, 3, 4]")
    assert result == [0, 1, 2, 3, 4]
    print("PASSED!\n")
    
    
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
