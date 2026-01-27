"""
Shortest Path in Directed Acyclic Graph (DAG) using Topological Sort
GFG: https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph/1

===========================================
PROBLEM
===========================================
Given a Directed Acyclic Graph (DAG) with V vertices and E weighted edges.
Find the shortest path from source vertex (0) to all other vertices.
If a vertex is unreachable, its distance is -1.

===========================================
WHY TOPOLOGICAL SORT?
===========================================

In a DAG, topological sort gives us an order where:
    - For every edge u -> v, u comes BEFORE v
    - So when we process u, we can RELAX all edges from u
    - We never need to revisit u again!

This is BETTER than Dijkstra for DAGs:
    - Dijkstra: O((V + E) log V)
    - Topo Sort: O(V + E)  <-- Faster!

===========================================
ALGORITHM
===========================================

Step 1: Create Topological Sort (DFS + Stack)
    - visited array
    - stack (nodes added AFTER all neighbors done)

Step 2: Initialize Distance Array
    - dist = [infinity] * V
    - dist[source] = 0

Step 3: Process nodes in Topological Order (pop from stack)
    - For each node u:
        - For each neighbor (v, weight):
            - If dist[u] + weight < dist[v]:
                - dist[v] = dist[u] + weight  (RELAX!)

Step 4: Return distances (-1 for unreachable)

===========================================
EXAMPLE (Your explanation)
===========================================

Graph:
    6 --> 4 (weight 2)
    6 --> 5 (weight 3)
    5 --> 4 (weight 1)
    
Source = 6 (or 0 in 0-indexed)

Topo Order: [6, 5, 4, ...]

Process node 6 (dist=0):
    - Neighbor 4: dist[4] = 0 + 2 = 2
    - Neighbor 5: dist[5] = 0 + 3 = 3

Process node 5 (dist=3):
    - Neighbor 4: dist[4] = min(2, 3+1) = 2  (no update, already shorter!)

Final: dist[4] = 2, dist[5] = 3

===========================================
"""

from typing import List


class Solution:
    def shortestPath(self, V: int, E: int, edges: List[List[int]]) -> List[int]:
        """
        Shortest path in DAG using Topological Sort (DFS).
        
        Time: O(V + E)
        Space: O(V + E)
        """
        # Build adjacency list (weighted)
        # adj[u] = [(v1, w1), (v2, w2), ...]
        adj = [[] for _ in range(V)]
        for u, v, w in edges:
            adj[u].append((v, w))
        
        # =====================
        # STEP 1: Topological Sort (DFS)
        # =====================
        vis = [0] * V
        stack = []
        
        def dfs(node):
            vis[node] = 1
            for neighbor, weight in adj[node]:
                if not vis[neighbor]:
                    dfs(neighbor)
            # Add to stack AFTER all neighbors done
            stack.append(node)
        
        # Run DFS for all nodes (handle disconnected)
        for i in range(V):
            if not vis[i]:
                dfs(i)
        
        # =====================
        # STEP 2: Initialize Distances
        # =====================
        INF = float('inf')
        dist = [INF] * V
        dist[0] = 0  # Source node = 0
        
        # =====================
        # STEP 3: Process in Topological Order (LIFO)
        # =====================
        while stack:
            node = stack.pop()  # LIFO = Topological Order
            
            # Only process if reachable
            if dist[node] != INF:
                for neighbor, weight in adj[node]:
                    # RELAX the edge
                    if dist[node] + weight < dist[neighbor]:
                        dist[neighbor] = dist[node] + weight
        
        # =====================
        # STEP 4: Convert INF to -1 (unreachable)
        # =====================
        result = []
        for d in dist:
            if d == INF:
                result.append(-1)
            else:
                result.append(d)
        
        return result


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    sol = Solution()
    
    # TEST 1: GFG Example
    print("=" * 50)
    print("TEST 1: GFG Example")
    print("=" * 50)
    
    #     0 --> 1 (w=2)
    #     0 --> 4 (w=1)
    #     1 --> 2 (w=3)
    #     4 --> 2 (w=2)
    #     4 --> 5 (w=4)
    #     2 --> 3 (w=6)
    #     5 --> 3 (w=1)
    
    V1 = 6
    E1 = 7
    edges1 = [
        [0, 1, 2],
        [0, 4, 1],
        [1, 2, 3],
        [4, 2, 2],
        [4, 5, 4],
        [2, 3, 6],
        [5, 3, 1]
    ]
    
    result = sol.shortestPath(V1, E1, edges1)
    print(f"Result:   {result}")
    print(f"Expected: [0, 2, 3, 6, 1, 5]")
    # dist[0]=0, dist[1]=2, dist[2]=3 (via 4), dist[3]=6 (via 5), dist[4]=1, dist[5]=5
    assert result == [0, 2, 3, 6, 1, 5]
    print("PASSED!\n")
    
    
    # TEST 2: Unreachable nodes
    print("=" * 50)
    print("TEST 2: Unreachable Nodes")
    print("=" * 50)
    
    # 0 --> 1 (w=1)
    # 2 --> 3 (w=1)  (disconnected from 0)
    
    V2 = 4
    E2 = 2
    edges2 = [
        [0, 1, 1],
        [2, 3, 1]
    ]
    
    result = sol.shortestPath(V2, E2, edges2)
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
    
    result = sol.shortestPath(V3, E3, edges3)
    print(f"Result:   {result}")
    print(f"Expected: [0]")
    assert result == [0]
    print("PASSED!\n")
    
    
    # TEST 4: Chain
    print("=" * 50)
    print("TEST 4: Simple Chain")
    print("=" * 50)
    
    # 0 --> 1 --> 2 --> 3
    V4 = 4
    E4 = 3
    edges4 = [
        [0, 1, 1],
        [1, 2, 2],
        [2, 3, 3]
    ]
    
    result = sol.shortestPath(V4, E4, edges4)
    print(f"Result:   {result}")
    print(f"Expected: [0, 1, 3, 6]")
    assert result == [0, 1, 3, 6]
    print("PASSED!\n")
    
    
    # TEST 5: Multiple paths
    print("=" * 50)
    print("TEST 5: Multiple Paths (Choose Shortest)")
    print("=" * 50)
    
    # 0 --> 1 (w=10)
    # 0 --> 2 (w=1)
    # 2 --> 1 (w=2)  <-- Shorter path 0->2->1 = 3
    
    V5 = 3
    E5 = 3
    edges5 = [
        [0, 1, 10],
        [0, 2, 1],
        [2, 1, 2]
    ]
    
    result = sol.shortestPath(V5, E5, edges5)
    print(f"Result:   {result}")
    print(f"Expected: [0, 3, 1]")  # 0->2->1 = 1+2 = 3
    assert result == [0, 3, 1]
    print("PASSED!\n")
    
    
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
