"""
Dijkstra's Algorithm - Shortest Path (Weighted Graph)
GFG: https://www.geeksforgeeks.org/problems/implementing-dijkstra-set-1-adjacency-matrix/1

===========================================
DEFINITION
===========================================
Dijkstra's Algorithm finds the shortest path from a source vertex 
to ALL other vertices in a weighted graph with NON-NEGATIVE weights.

It uses a GREEDY approach:
    - Always pick the unvisited vertex with MINIMUM distance
    - Relax all its edges (update shorter paths)
    - Mark as visited (distance is now final)

===========================================
WHEN TO USE DIJKSTRA
===========================================

| Algorithm           | When to Use                              |
|---------------------|------------------------------------------|
| BFS                 | Unweighted graph (all edges = 1)         |
| Topo Sort + Relax   | DAG (Directed Acyclic Graph)             |
| Dijkstra            | Weighted graph (NON-NEGATIVE weights)    |
| Bellman-Ford        | Weighted graph (can have NEGATIVE weights)|

===========================================
TWO IMPLEMENTATIONS: SET vs PRIORITY QUEUE
===========================================

Both use Min-Heap concept to get minimum distance node.
BUT they handle "finding a better path" differently!

-------------------------------------------
PRIORITY QUEUE (Python - heapq)
-------------------------------------------
    - Can't remove arbitrary elements!
    - When we find better path: push new entry, keep old one
    - Queue may have DUPLICATES: (10, 5) and (8, 5) for same node 5
    - Solution: "LAZY DELETION" - skip outdated entries
    
    if d > dist[node]:
        continue  # Skip! We already found shorter path

-------------------------------------------
SET (C++ set<pair<int,int>>)
-------------------------------------------
    - CAN remove and insert in O(log N)
    - When we find better path: REMOVE old, INSERT new
    - st.erase({10, 5})  // Remove old distance
    - st.insert({8, 5})  // Insert new distance
    - No duplicates ever!
    - No skip check needed

-------------------------------------------
EXAMPLE: Node 5 with distances 10 and 8
-------------------------------------------

PRIORITY QUEUE:
    PQ = [..., (10, 5), ...]   # Initial path with dist=10
    Found better path dist=8
    PQ = [..., (10, 5), (8, 5), ...]  # BOTH exist!
    
    Pop (8, 5) first (min-heap)
    Process node 5 with dist=8
    dist[5] = 8
    
    Later, pop (10, 5)
    Check: 10 > dist[5] (which is 8)
    SKIP IT! (Lazy Deletion)

SET:
    Set = {..., (10, 5), ...}
    Found better path dist=8
    Set.erase({10, 5})   # REMOVE old
    Set.insert({8, 5})   # INSERT new
    Set = {..., (8, 5), ...}  # Only one entry!
    
    No duplicates, no skip needed

-------------------------------------------
SUMMARY
-------------------------------------------
| Aspect              | Priority Queue    | Set               |
|---------------------|-------------------|-------------------|
| Remove old entry?   | NO (lazy delete)  | YES               |
| Duplicates?         | YES               | NO                |
| Skip check needed?  | YES               | NO                |
| Python support?     | heapq (easy)      | No native support |

For Python interviews: Use Priority Queue with Lazy Deletion!

===========================================
ALGORITHM
===========================================

1. Initialize:
    - dist = [infinity] * V
    - dist[source] = 0
    - pq = [(0, source)]  # (distance, node)

2. While pq not empty:
    - Pop (d, node) with minimum distance
    - If d > dist[node]: continue (LAZY DELETION - skip outdated!)
    - For each neighbor:
        - If dist[node] + weight < dist[neighbor]:
            - Update dist[neighbor]
            - Push (new_dist, neighbor) to pq

3. Return dist array

Time: O((V + E) log V)
Space: O(V)

===========================================
"""

import heapq
from typing import List


class Solution:
    def dijkstra(self, V: int, adj: List[List[List[int]]], S: int) -> List[int]:
        """
        Dijkstra's Algorithm using Min-Heap (Priority Queue).
        
        Args:
            V: Number of vertices
            adj: Adjacency list where adj[u] = [[v1, w1], [v2, w2], ...]
            S: Source vertex (can be ANY node, not just 0!)
        
        Returns:
            List of shortest distances from S to all vertices
        
        Time: O((V + E) log V)
        Space: O(V)
        """
        # 1. Initialize distances with Infinity
        dist = [float('inf')] * V
        dist[S] = 0
        
        # 2. Min-Heap: stores (distance, node)
        # We start with the source node at distance 0
        pq = [(0, S)]
        
        while pq:
            # Pop the node with the shortest distance
            d, node = heapq.heappop(pq)
            
            # LAZY DELETION: 
            # If the popped distance is greater than what we already found, 
            # it means this is an "outdated" path. Skip it.
            if d > dist[node]:
                continue
            
            # Traverse neighbors
            for neighbor, weight in adj[node]:
                if dist[node] + weight < dist[neighbor]:
                    # Update distance
                    dist[neighbor] = dist[node] + weight
                    # Push new pair to PQ (We do NOT remove the old pair)
                    heapq.heappush(pq, (dist[neighbor], neighbor))
                    
        return dist


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    sol = Solution()
    
    # TEST 1: GFG Example
    print("=" * 50)
    print("TEST 1: Source = 0")
    print("=" * 50)
    
    #       1
    #   0 ----- 1
    #   |       |
    #  4|       |2
    #   |       |
    #   2 ----- 3
    #       3
    
    V1 = 4
    adj1 = [
        [[1, 1], [2, 4]],  # 0 -> (1, w=1), (2, w=4)
        [[0, 1], [3, 2]],  # 1 -> (0, w=1), (3, w=2)
        [[0, 4], [3, 3]],  # 2 -> (0, w=4), (3, w=3)
        [[1, 2], [2, 3]]   # 3 -> (1, w=2), (2, w=3)
    ]
    
    result = sol.dijkstra(V1, adj1, 0)
    print(f"Distances from 0: {result}")
    print(f"Expected:         [0, 1, 4, 3]")
    # dist[0]=0, dist[1]=1, dist[2]=4 (direct or via 1->3->2 = 1+2+3=6, direct is shorter)
    # dist[3]=3 (0->1->3 = 1+2 = 3)
    assert result == [0, 1, 4, 3]
    print("PASSED!\n")
    
    
    # TEST 2: Different source (not 0!)
    print("=" * 50)
    print("TEST 2: Source = 2 (not 0!)")
    print("=" * 50)
    
    result = sol.dijkstra(V1, adj1, 2)  # Start from node 2
    print(f"Distances from 2: {result}")
    print(f"Expected:         [4, 5, 0, 3]")
    # From node 2: dist[2]=0, dist[0]=4, dist[3]=3, dist[1]=5 (2->3->1)
    assert result == [4, 5, 0, 3]
    print("PASSED!\n")
    
    
    # TEST 3: Larger graph
    print("=" * 50)
    print("TEST 3: Larger Graph, Source = 0")
    print("=" * 50)
    
    #     0 --1-- 1 --2-- 2
    #     |       |       |
    #     4       3       1
    #     |       |       |
    #     3 --2-- 4 --1-- 5
    
    V3 = 6
    adj3 = [
        [[1, 1], [3, 4]],           # 0
        [[0, 1], [2, 2], [4, 3]],   # 1
        [[1, 2], [5, 1]],           # 2
        [[0, 4], [4, 2]],           # 3
        [[1, 3], [3, 2], [5, 1]],   # 4
        [[2, 1], [4, 1]]            # 5
    ]
    
    result = sol.dijkstra(V3, adj3, 0)
    print(f"Distances from 0: {result}")
    print(f"Expected:         [0, 1, 3, 4, 4, 4]")
    assert result == [0, 1, 3, 4, 4, 4]
    print("PASSED!\n")
    
    
    # TEST 4: Single node
    print("=" * 50)
    print("TEST 4: Single Node")
    print("=" * 50)
    
    V4 = 1
    adj4 = [[]]
    
    result = sol.dijkstra(V4, adj4, 0)
    print(f"Distances: {result}")
    print(f"Expected:  [0]")
    assert result == [0]
    print("PASSED!\n")
    
    
    # TEST 5: Disconnected graph
    print("=" * 50)
    print("TEST 5: Disconnected Graph")
    print("=" * 50)
    
    # 0 -- 1    2 -- 3 (two separate components)
    V5 = 4
    adj5 = [
        [[1, 1]],      # 0
        [[0, 1]],      # 1
        [[3, 1]],      # 2
        [[2, 1]]       # 3
    ]
    
    result = sol.dijkstra(V5, adj5, 0)
    print(f"Distances from 0: {result}")
    print(f"Expected:         [0, 1, inf, inf]")
    assert result[0] == 0
    assert result[1] == 1
    assert result[2] == float('inf')
    assert result[3] == float('inf')
    print("PASSED!\n")
    
    
    # TEST 6: Striver's Video Example (demonstrates lazy deletion)
    print("=" * 50)
    print("TEST 6: Striver's Graph Example")
    print("=" * 50)

    # 6 Vertices (0 to 5)
    V_striver = 6
    adj_striver = [[] for _ in range(V_striver)]

    # Helper to add undirected edges
    def add_edge(u, v, w):
        adj_striver[u].append([v, w])
        adj_striver[v].append([u, w])

    # Adding edges as shown in Striver's video
    add_edge(0, 1, 4)
    add_edge(0, 2, 4)
    add_edge(1, 2, 2)
    add_edge(2, 3, 3)
    add_edge(2, 4, 1)
    add_edge(2, 5, 6)
    add_edge(3, 5, 2)
    add_edge(4, 5, 3)

    # Run Dijkstra from Source 0
    result = sol.dijkstra(V_striver, adj_striver, 0)
    
    print(f"Distances: {result}")
    
    # Expected:
    # 0->0: 0
    # 0->1: 4
    # 0->2: 4
    # 0->3: 0->2->3 = 4+3 = 7
    # 0->4: 0->2->4 = 4+1 = 5
    # 0->5: 0->2->4->5 = 4+1+3 = 8 (NOT 0->2->5 which is 4+6=10)
    #       This is where (10,5) gets skipped by lazy deletion!
    
    expected = [0, 4, 4, 7, 5, 8]
    print(f"Expected:  {expected}")
    
    assert result == expected
    print("PASSED: Matches Striver's example!")
    print("Note: Node 5 had (10,5) and (8,5) - lazy deletion skipped (10,5)!\n")
    
    
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
