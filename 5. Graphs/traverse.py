"""
Graph Traversal: BFS and DFS
Following Striver's A2Z DSA Course

LeetCode-style input:
- V = number of vertices (0-indexed)
- adj = adjacency list where adj[i] contains all neighbors of node i

===========================================
BFS WORKFLOW (Striver's Approach)
===========================================

1. Create visited array: vis = [0] * V  (all False initially)

2. Add starting node to queue AND mark it as visited:
   - queue.append(start)
   - vis[start] = 1

3. While queue is NOT empty:
   a. Pop front node from queue
   b. Add this node to result/BFS list
   
   c. For each neighbor of this node:
      - IF neighbor is NOT in queue (i.e., vis[neighbor] == 0):
        * Add neighbor to queue
        * Mark vis[neighbor] = 1 (True)

Key Point: vis[i] = 1 means node i is IN the queue or already processed.
           So checking "not visited" is same as "not in queue".
===========================================
"""

from collections import deque

# ============================================
# BFS (Breadth-First Search)
# ============================================
def bfs_of_graph(V: int, adj: list) -> list:
    """
    BFS traversal starting from node 0.
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    vis = [0] * V           # visited array
    vis[0] = 1              # mark starting node as visited
    q = deque([0])          # queue for BFS
    bfs = []                # result: traversal order
    
    while q:
        node = q.popleft()  # get front of queue
        bfs.append(node)    # add to result
        
        # Visit all neighbors
        for neighbor in adj[node]:
            if not vis[neighbor]:
                vis[neighbor] = 1    # mark visited BEFORE adding to queue
                q.append(neighbor)
    
    return bfs


# ============================================
# TEST CASES
# ============================================

def run_test(name, V, adj, description):
    """Helper function to run and display a test case."""
    print("\n" + "=" * 50)
    print(f"TEST: {name}")
    print(f"Description: {description}")
    print("=" * 50)
    print(f"V = {V}")
    print("Adjacency List:")
    for i in range(V):
        print(f"  {i}: {adj[i]}")
    result = bfs_of_graph(V, adj)
    print(f"\nBFS Result: {result}")
    return result


if __name__ == "__main__":
    
    # ----------------------------------------
    # TEST CASE 1: Tree Structure
    # ----------------------------------------
    """
          0
         / \
        1   2
        |   |
        3   4
    """
    V1 = 5
    adj1 = [
        [1, 2],     # 0 -> 1, 2
        [0, 3],     # 1 -> 0, 3
        [0, 4],     # 2 -> 0, 4
        [1],        # 3 -> 1
        [2]         # 4 -> 2
    ]
    run_test("Tree Structure", V1, adj1, "Simple tree with 5 nodes")
    # Expected: [0, 1, 2, 3, 4]
    
    # ----------------------------------------
    # TEST CASE 2: Graph with Cycle
    # ----------------------------------------
    """
        0 --- 1
        |     |
        3 --- 2
    """
    V2 = 4
    adj2 = [
        [1, 3],     # 0 -> 1, 3
        [0, 2],     # 1 -> 0, 2
        [1, 3],     # 2 -> 1, 3
        [0, 2]      # 3 -> 0, 2
    ]
    run_test("Graph with Cycle", V2, adj2, "Square graph (has cycle)")
    # Expected: [0, 1, 3, 2]
    
    # ----------------------------------------
    # TEST CASE 3: Linear Chain
    # ----------------------------------------
    """
        0 --- 1 --- 2 --- 3 --- 4
    """
    V3 = 5
    adj3 = [
        [1],        # 0 -> 1
        [0, 2],     # 1 -> 0, 2
        [1, 3],     # 2 -> 1, 3
        [2, 4],     # 3 -> 2, 4
        [3]         # 4 -> 3
    ]
    run_test("Linear Chain", V3, adj3, "Nodes connected in a line")
    # Expected: [0, 1, 2, 3, 4]
    
    # ----------------------------------------
    # TEST CASE 4: Star Graph
    # ----------------------------------------
    """
          1
          |
      2 - 0 - 3
          |
          4
    """
    V4 = 5
    adj4 = [
        [1, 2, 3, 4],   # 0 -> all others
        [0],            # 1 -> 0
        [0],            # 2 -> 0
        [0],            # 3 -> 0
        [0]             # 4 -> 0
    ]
    run_test("Star Graph", V4, adj4, "Center node connected to all others")
    # Expected: [0, 1, 2, 3, 4]
    
    # ----------------------------------------
    # TEST CASE 5: Single Node
    # ----------------------------------------
    """
        0 (alone)
    """
    V5 = 1
    adj5 = [
        []          # 0 has no neighbors
    ]
    run_test("Single Node", V5, adj5, "Only one node, no edges")
    # Expected: [0]
    
    # ----------------------------------------
    # SUMMARY
    # ----------------------------------------
