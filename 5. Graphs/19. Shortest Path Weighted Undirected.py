"""
Shortest Path in Weighted Undirected Graph (GFG)
https://www.geeksforgeeks.org/problems/shortest-path-in-weighted-undirected-graph/1

===========================================
PROBLEM
===========================================
Given a weighted undirected graph with V vertices and E edges.
Find the shortest path from vertex 1 to vertex V.
Return the PATH (not just distance).
If no path exists, return [-1].

===========================================
KEY INSIGHT
===========================================
This is Dijkstra + Path Reconstruction!

Two parts:
1. Run Dijkstra to find shortest distances
2. Track PARENT of each node to reconstruct path

===========================================
ALGORITHM
===========================================

1. Initialize:
    - dist = [infinity] * V
    - parent = [-1] * V  (to track path)
    - dist[source] = 0
    - pq = [(0, source)]

2. Dijkstra:
    - When relaxing edge u -> v:
        - Update dist[v]
        - parent[v] = u  (track where we came from!)

3. Path Reconstruction:
    - Start from destination (V)
    - Keep going to parent[current] until source
    - Reverse the path

===========================================
"""

import heapq
from typing import List


class Solution:
    def shortestPath(self, n: int, m: int, edges: List[List[int]]) -> List[int]:
        """
        Shortest path from node 1 to node n with path reconstruction.
        
        Args:
            n: Number of vertices
            m: Number of edges
            edges: List of [u, v, weight] (1-indexed)
        
        Returns:
            Path from 1 to n, or [-1] if no path
        """
        # Build adjacency list (1-indexed)
        adj = [[] for _ in range(n + 1)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))  # Undirected!
        
        # Initialize
        dist = [float('inf')] * (n + 1)
        parent = [-1] * (n + 1)
        
        dist[1] = 0  # Source is node 1
        pq = [(0, 1)]  # (distance, node)
        
        # Dijkstra
        while pq:
            d, node = heapq.heappop(pq)
            
            # Lazy deletion
            if d > dist[node]:
                continue
            
            for neighbor, weight in adj[node]:
                if dist[node] + weight < dist[neighbor]:
                    dist[neighbor] = dist[node] + weight
                    parent[neighbor] = node  # Track parent!
                    heapq.heappush(pq, (dist[neighbor], neighbor))
        
        # If destination unreachable
        if dist[n] == float('inf'):
            return [-1]
        
        # Path Reconstruction
        path = []
        current = n  # Start from destination
        
        while current != -1:
            path.append(current)
            current = parent[current]
        
        path.reverse()  # Reverse to get 1 -> n order
        
        return path


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    sol = Solution()
    
    # TEST 1: GFG Example
    print("=" * 50)
    print("TEST 1: GFG Example")
    print("=" * 50)
    
    n1 = 5
    m1 = 6
    edges1 = [
        [1, 2, 2],
        [2, 5, 5],
        [2, 3, 4],
        [1, 4, 1],
        [4, 3, 3],
        [3, 5, 1]
    ]
    
    result = sol.shortestPath(n1, m1, edges1)
    print(f"Path: {result}")
    print(f"Expected: [1, 4, 3, 5] (cost = 1+3+1 = 5)")
    # Path: 1 -> 4 -> 3 -> 5 (cost = 1 + 3 + 1 = 5)
    # vs 1 -> 2 -> 5 (cost = 2 + 5 = 7)
    assert result == [1, 4, 3, 5]
    print("PASSED!\n")
    
    
    # TEST 2: Direct path
    print("=" * 50)
    print("TEST 2: Direct Path")
    print("=" * 50)
    
    n2 = 2
    m2 = 1
    edges2 = [[1, 2, 5]]
    
    result = sol.shortestPath(n2, m2, edges2)
    print(f"Path: {result}")
    print(f"Expected: [1, 2]")
    assert result == [1, 2]
    print("PASSED!\n")
    
    
    # TEST 3: No path
    print("=" * 50)
    print("TEST 3: No Path Exists")
    print("=" * 50)
    
    n3 = 3
    m3 = 1
    edges3 = [[1, 2, 1]]  # Node 3 is disconnected
    
    result = sol.shortestPath(n3, m3, edges3)
    print(f"Path: {result}")
    print(f"Expected: [-1]")
    assert result == [-1]
    print("PASSED!\n")
    
    
    # TEST 4: Multiple paths, choose shortest
    print("=" * 50)
    print("TEST 4: Multiple Paths")
    print("=" * 50)
    
    #     1
    #    /|\
    #   2 | 10
    #  /  |  \
    # 2   1   3
    #  \  |  /
    #   3 2  
    #    \|/
    #     4
    
    n4 = 4
    m4 = 4
    edges4 = [
        [1, 2, 2],
        [1, 3, 10],
        [2, 4, 3],
        [3, 4, 1]
    ]
    
    result = sol.shortestPath(n4, m4, edges4)
    print(f"Path: {result}")
    # Path 1->2->4 = 2+3 = 5
    # Path 1->3->4 = 10+1 = 11
    assert result == [1, 2, 4]
    print("PASSED!\n")
    
    
    # TEST 5: Single node (source = destination)
    print("=" * 50)
    print("TEST 5: Single Node")
    print("=" * 50)
    
    n5 = 1
    m5 = 0
    edges5 = []
    
    result = sol.shortestPath(n5, m5, edges5)
    print(f"Path: {result}")
    print(f"Expected: [1]")
    assert result == [1]
    print("PASSED!\n")
    
    
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
