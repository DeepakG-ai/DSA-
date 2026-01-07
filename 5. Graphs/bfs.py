"""
BFS (Breadth-First Search)

INITIAL SETUP:
--------------
1. Create vis = [0] * V           (visited array)
2. Mark starting node as visited: vis[start] = 1
3. Add starting node to queue:    q = deque([start])
4. Create empty result list:      bfs = []

MAIN LOOP (while queue is not empty):
-------------------------------------
Step 1: Remove node from FRONT of queue
        node = q.popleft()

Step 2: Add this node to result
        bfs.append(node)

Step 3: Visit all neighbors
        for neighbor in adj[node]:
            if not vis[neighbor]:       # Check if NOT visited
                vis[neighbor] = 1       # Mark as visited IMMEDIATELY
                q.append(neighbor)      # Add to queue

===========================================
EXAMPLE: Graph with Cycle
===========================================

    0 --- 1
    |     |
    3 --- 2

adj = [[1,3], [0,2], [1,3], [0,2]]

Initial: vis=[1,0,0,0], q=[0], bfs=[]

Iteration 1:
  node = 0              # pop from queue
  bfs = [0]             # add to result
  neighbors of 0: [1,3]
    1 not visited -> vis[1]=1, q=[1]
    3 not visited -> vis[3]=1, q=[1,3]

Iteration 2:
  node = 1              # pop from queue
  bfs = [0,1]           # add to result
  neighbors of 1: [0,2]
    0 already visited -> skip
    2 not visited -> vis[2]=1, q=[3,2]

Iteration 3:
  node = 3              # pop from queue
  bfs = [0,1,3]         # add to result
  neighbors of 3: [0,2]
    0 already visited -> skip
    2 already visited -> skip

Iteration 4:
  node = 2              # pop from queue
  bfs = [0,1,3,2]       # add to result
  neighbors of 2: [1,3]
    1 already visited -> skip
    3 already visited -> skip

Queue empty -> DONE
Result: [0,1,3,2]

===========================================
"""

from collections import deque


def bfs_of_graph(V: int, adj: list, start: int = 0) -> list:
    """
    BFS traversal starting from given node.
    
    Args:
        V: Number of vertices (0-indexed)
        adj: Adjacency list
        start: Starting node (default 0)
    
    Returns:
        List of nodes in BFS order
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    vis = [0] * V
    vis[start] = 1
    q = deque([start])
    bfs = []
    
    while q:
        node = q.popleft()
        bfs.append(node)
        
        for neighbor in adj[node]:
            if not vis[neighbor]:
                vis[neighbor] = 1
                q.append(neighbor)
    
    return bfs


# ============================================
# TEST CASES WITH ASSERT
# ============================================

if __name__ == "__main__":
    
    # TEST 1: Tree Structure (start from 0)
    #       0
    #      / \
    #     1   2
    #     |   |
    #     3   4
    V1 = 5
    adj1 = [
        [1, 2],
        [0, 3],
        [0, 4],
        [1],
        [2]
    ]
    assert bfs_of_graph(V1, adj1, 0) == [0, 1, 2, 3, 4]
    print("TEST 1 PASSED: Tree from node 0")
    
    # TEST 2: Tree Structure (start from 3)
    assert bfs_of_graph(V1, adj1, 3) == [3, 1, 0, 2, 4]
    print("TEST 2 PASSED: Tree from node 3")
    
    # TEST 3: Graph with Cycle
    #     0 --- 1
    #     |     |
    #     3 --- 2
    V2 = 4
    adj2 = [
        [1, 3],
        [0, 2],
        [1, 3],
        [0, 2]
    ]
    assert bfs_of_graph(V2, adj2, 0) == [0, 1, 3, 2]
    print("TEST 3 PASSED: Cycle graph from node 0")
    
    # TEST 4: Cycle graph (start from 2)
    assert bfs_of_graph(V2, adj2, 2) == [2, 1, 3, 0]
    print("TEST 4 PASSED: Cycle graph from node 2")
    
    # TEST 5: Linear Chain
    #     0 --- 1 --- 2 --- 3 --- 4
    V3 = 5
    adj3 = [
        [1],
        [0, 2],
        [1, 3],
        [2, 4],
        [3]
    ]
    assert bfs_of_graph(V3, adj3, 0) == [0, 1, 2, 3, 4]
    print("TEST 5 PASSED: Linear chain from node 0")
    
    # TEST 6: Linear Chain (start from middle)
    assert bfs_of_graph(V3, adj3, 2) == [2, 1, 3, 0, 4]
    print("TEST 6 PASSED: Linear chain from node 2")
    
    # TEST 7: Star Graph
    #       1
    #       |
    #   2 - 0 - 3
    #       |
    #       4
    V4 = 5
    adj4 = [
        [1, 2, 3, 4],
        [0],
        [0],
        [0],
        [0]
    ]
    assert bfs_of_graph(V4, adj4, 0) == [0, 1, 2, 3, 4]
    print("TEST 7 PASSED: Star graph from center")
    
    # TEST 8: Star Graph (start from leaf)
    assert bfs_of_graph(V4, adj4, 3) == [3, 0, 1, 2, 4]
    print("TEST 8 PASSED: Star graph from leaf node 3")
    
    # TEST 9: Single Node
    V5 = 1
    adj5 = [[]]
    assert bfs_of_graph(V5, adj5, 0) == [0]
    print("TEST 9 PASSED: Single node")
    
    # TEST 10: Two Nodes
    V6 = 2
    adj6 = [[1], [0]]
    assert bfs_of_graph(V6, adj6, 1) == [1, 0]
    print("TEST 10 PASSED: Two nodes from node 1")
    
    print("\n" + "=" * 40)
    print("ALL 10 TESTS PASSED!")
    print("=" * 40)
