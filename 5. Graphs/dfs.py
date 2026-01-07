"""
DFS (Depth-First Search) - Recursive
===========================================
DFS WORKFLOW
===========================================

INITIAL SETUP:
--------------
1. Create vis = [0] * V           (visited array)
2. Create empty result list:      dfs = []
3. Call dfs(start_node)

DFS FUNCTION (recursive):
-------------------------
def dfs(node):
    1. Mark node as visited:      vis[node] = 1
    2. Add node to result:        dfs.append(node)
    3. For each neighbor of node:
       - IF neighbor NOT visited:
         * Call dfs(neighbor)     # Go deeper!

===========================================
EXAMPLE: Undirected Graph with Cycle
===========================================

        1
       / |
      2  3 --- 4
     /|   |    |
    5 6   7 -- 8

Cycle: 3 - 4 - 8 - 7 - 3

adj = {
    1: [2, 3],
    2: [1, 5, 6],
    3: [1, 4, 7],
    4: [3, 8],
    5: [2],
    6: [2],
    7: [3, 8],
    8: [4, 7]
}

Starting from node 1:

dfs(1):
  vis[1] = 1, result = [1]
  neighbors of 1: [2, 3]
  
  -> dfs(2):
       vis[2] = 1, result = [1, 2]
       neighbors of 2: [1, 5, 6]
       1 visited, skip
       
       -> dfs(5):
            vis[5] = 1, result = [1, 2, 5]
            neighbors of 5: [2]
            2 visited, skip
            return to dfs(2)
       
       -> dfs(6):
            vis[6] = 1, result = [1, 2, 5, 6]
            neighbors of 6: [2]
            2 visited, skip
            return to dfs(2)
       
       return to dfs(1)
  
  -> dfs(3):
       vis[3] = 1, result = [1, 2, 5, 6, 3]
       neighbors of 3: [1, 4, 7]
       1 visited, skip
       
       -> dfs(4):
            vis[4] = 1, result = [1, 2, 5, 6, 3, 4]
            neighbors of 4: [3, 8]
            3 visited, skip
            
            -> dfs(8):
                 vis[8] = 1, result = [1, 2, 5, 6, 3, 4, 8]
                 neighbors of 8: [4, 7]
                 4 visited, skip
                 
                 -> dfs(7):
                      vis[7] = 1, result = [1, 2, 5, 6, 3, 4, 8, 7]
                      neighbors of 7: [3, 8]
                      3 visited, skip
                      8 visited, skip
                      return
                 
                 return to dfs(8)
            
            return to dfs(4)
       
       7 already visited, skip
       return to dfs(3)
  
  return

DONE! Result: [1, 2, 5, 6, 3, 4, 8, 7]

===========================================
"""

from collections import defaultdict


def dfs_of_graph(V: int, adj: list, start: int = 0) -> list:
    """
    DFS traversal using recursion.
    
    Args:
        V: Number of vertices
        adj: Adjacency list
        start: Starting node
    
    Returns:
        List of nodes in DFS order
    """
    vis = [0] * V
    result = []
    
    def dfs(node):
        vis[node] = 1
        result.append(node)
        
        for neighbor in adj[node]:
            if not vis[neighbor]:
                dfs(neighbor)
    
    dfs(start)
    return result


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
    assert dfs_of_graph(V1, adj1, 0) == [0, 1, 3, 2, 4]
    print("TEST 1 PASSED: Tree from node 0")
    
    # TEST 2: Tree Structure (start from 3)
    assert dfs_of_graph(V1, adj1, 3) == [3, 1, 0, 2, 4]
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
    assert dfs_of_graph(V2, adj2, 0) == [0, 1, 2, 3]
    print("TEST 3 PASSED: Cycle graph from node 0")
    
    # TEST 4: Cycle graph (start from 2)
    assert dfs_of_graph(V2, adj2, 2) == [2, 1, 0, 3]
    print("TEST 4 PASSED: Cycle graph from node 2")
    
    # TEST 5: Linear Chain
    V3 = 5
    adj3 = [
        [1],
        [0, 2],
        [1, 3],
        [2, 4],
        [3]
    ]
    assert dfs_of_graph(V3, adj3, 0) == [0, 1, 2, 3, 4]
    print("TEST 5 PASSED: Linear chain from node 0")
    
    # TEST 6: Linear Chain (start from 2)
    assert dfs_of_graph(V3, adj3, 2) == [2, 1, 0, 3, 4]
    print("TEST 6 PASSED: Linear chain from node 2")
    
    # TEST 7: Star Graph
    V4 = 5
    adj4 = [
        [1, 2, 3, 4],
        [0],
        [0],
        [0],
        [0]
    ]
    assert dfs_of_graph(V4, adj4, 0) == [0, 1, 2, 3, 4]
    print("TEST 7 PASSED: Star graph from center")
    
    # TEST 8: Star Graph (start from 3)
    assert dfs_of_graph(V4, adj4, 3) == [3, 0, 1, 2, 4]
    print("TEST 8 PASSED: Star graph from node 3")
    
    # TEST 9: Single Node
    V5 = 1
    adj5 = [[]]
    assert dfs_of_graph(V5, adj5, 0) == [0]
    print("TEST 9 PASSED: Single node")
    
    # TEST 10: Your example graph (1-indexed converted to 0-indexed)
    #     0 ---- 1 ---- 4
    #    / \      \
    #   2   \      5
    #  / \   \
    # 3   6   \
    # |        \
    # 7 --------+
    V6 = 8
    adj6 = [
        [1, 2],       # 0 (was 1): [2, 3] -> [1, 2]
        [0, 4, 5],    # 1 (was 2): [1, 5, 6] -> [0, 4, 5]
        [0, 3, 6],    # 2 (was 3): [1, 4, 7] -> [0, 3, 6]
        [2, 7],       # 3 (was 4): [3, 8] -> [2, 7]
        [1],          # 4 (was 5): [2] -> [1]
        [1],          # 5 (was 6): [2] -> [1]
        [2, 7],       # 6 (was 7): [3, 8] -> [2, 7]
        [3, 6]        # 7 (was 8): [4, 7] -> [3, 6]
    ]
    result = dfs_of_graph(V6, adj6, 0)
    print(f"TEST 10: Your graph DFS = {result}")
    assert result == [0, 1, 4, 5, 2, 3, 7, 6]
    print("TEST 10 PASSED: Your example graph")
    
    print("\n" + "=" * 40)
    print("ALL 10 TESTS PASSED!")
    print("=" * 40)
