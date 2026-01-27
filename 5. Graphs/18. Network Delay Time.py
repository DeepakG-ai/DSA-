"""
Network Delay Time (LeetCode 743)
https://leetcode.com/problems/network-delay-time/

===========================================
PROBLEM
===========================================
You are given a network of n nodes (labeled 1 to n).
Given times[i] = (ui, vi, wi): time to send signal from ui to vi is wi.

Send a signal from node k.
Return the MINIMUM time for all nodes to receive the signal.
Return -1 if impossible for all nodes to receive.

===========================================
KEY INSIGHT
===========================================
This is a classic Dijkstra problem!

We need to find the shortest path from source (k) to ALL nodes.
The answer is the MAXIMUM of all shortest paths.

Why maximum?
    - Signal reaches each node at different times
    - ALL nodes must receive = wait for the LAST one
    - Last one = node with MAXIMUM shortest distance

===========================================
ALGORITHM
===========================================

1. Build adjacency list from times array
2. Run Dijkstra from source k
3. Find maximum distance among all nodes
4. If any node has distance = infinity, return -1

===========================================
"""

import heapq
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # Build adjacency list
        # Note: Nodes are 1-indexed in this problem!
        adj = [[] for _ in range(n + 1)]
        for u, v, w in times:
            adj[u].append((v, w))
        
        # Dijkstra's Algorithm
        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        
        pq = [(0, k)]  # (distance, node)
        
        while pq:
            d, node = heapq.heappop(pq)
            
            # Lazy deletion: skip outdated entries
            if d > dist[node]:
                continue
            
            for neighbor, weight in adj[node]:
                if dist[node] + weight < dist[neighbor]:
                    dist[neighbor] = dist[node] + weight
                    heapq.heappush(pq, (dist[neighbor], neighbor))
        
        # Find maximum distance (ignoring index 0 since nodes are 1-indexed)
        max_dist = max(dist[1:])
        # Example: Striver's graph, source = 0
        # dist = [0, 4, 4, 7, 5, 8]
        # 0  1  2  3  4  5  ← nodes

        
        # If any node unreachable, return -1
        return max_dist if max_dist != float('inf') else -1
        #output 8 , max([4, 4, 7, 5, 8]) = 8

# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    sol = Solution()
    
    # TEST 1: LeetCode Example 1
    print("=" * 50)
    print("TEST 1: LeetCode Example")
    print("=" * 50)
    
    times1 = [[2,1,1], [2,3,1], [3,4,1]]
    n1 = 4
    k1 = 2
    
    result = sol.networkDelayTime(times1, n1, k1)
    print(f"times = {times1}")
    print(f"n = {n1}, k = {k1}")
    print(f"Result: {result}")
    print(f"Expected: 2")
    # From node 2: reach 1 and 3 in time 1, reach 4 in time 2
    assert result == 2
    print("PASSED!\n")
    
    
    # TEST 2: Unreachable node
    print("=" * 50)
    print("TEST 2: Unreachable Node")
    print("=" * 50)
    
    times2 = [[1,2,1]]
    n2 = 2
    k2 = 2  # Start from 2, but no edge from 2!
    
    result = sol.networkDelayTime(times2, n2, k2)
    print(f"Result: {result}")
    print(f"Expected: -1")
    assert result == -1
    print("PASSED!\n")
    
    
    # TEST 3: Single node
    print("=" * 50)
    print("TEST 3: Single Node")
    print("=" * 50)
    
    times3 = []
    n3 = 1
    k3 = 1
    
    result = sol.networkDelayTime(times3, n3, k3)
    print(f"Result: {result}")
    print(f"Expected: 0 (signal is already at the only node)")
    assert result == 0
    print("PASSED!\n")
    
    
    # TEST 4: Multiple paths, choose shortest
    print("=" * 50)
    print("TEST 4: Multiple Paths")
    print("=" * 50)
    
    # 1 -> 2 (direct: 10)
    # 1 -> 3 -> 2 (via 3: 1+1=2)
    times4 = [[1,2,10], [1,3,1], [3,2,1]]
    n4 = 3
    k4 = 1
    
    result = sol.networkDelayTime(times4, n4, k4)
    print(f"Result: {result}")
    print(f"Expected: 2 (path 1->3->2 = 1+1)")
    assert result == 2
    print("PASSED!\n")
    
    
    # TEST 5: Star graph
    print("=" * 50)
    print("TEST 5: Star Graph from Center")
    print("=" * 50)
    
    # 1 is center, connects to 2,3,4,5
    times5 = [[1,2,1], [1,3,2], [1,4,3], [1,5,4]]
    n5 = 5
    k5 = 1
    
    result = sol.networkDelayTime(times5, n5, k5)
    print(f"Result: {result}")
    print(f"Expected: 4 (max distance to node 5)")
    assert result == 4
    print("PASSED!\n")
    
    
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
