"""
Detect Cycle in Undirected Graph (BFS)
GFG: https://www.geeksforgeeks.org/problems/detect-cycle-in-an-undirected-graph/1

===========================================
PROBLEM
===========================================
Given an undirected graph with V vertices and E edges.
Check whether it contains any cycle or not.

===========================================
WORKFLOW (BFS with Parent Tracking)
===========================================

1. Create visited array: vis = [0] * V

2. Loop through all nodes (for disconnected components):
   for node in range(V):
       if not vis[node]:
           if bfs(node) returns True:
               return True (cycle found!)

3. BFS Function:
   - Queue stores: (node, parent)
   - Start: queue.append((start, -1)), vis[start] = 1
   
   - While queue not empty:
     * Pop (node, parent)
     * For each neighbor:
       - If NOT visited: mark, add (neighbor, node) to queue
       - If VISITED and neighbor != parent: CYCLE FOUND!

4. If all components checked and no cycle: return False

===========================================
KEY INSIGHT
===========================================
In undirected graph: A -- B means B is also connected to A.
When at B, we'll see A as neighbor (visited).
But that's just the edge we came from (parent), NOT a cycle!

CYCLE = visited neighbor that is NOT the parent

===========================================
"""

from collections import deque


def isCycle_BFS(V: int, adj: list) -> bool:
    """
    Detect cycle using BFS with parent tracking.
    
    Args:
        V: Number of vertices
        adj: Adjacency list (already built)
    
    Returns:
        True if cycle exists, False otherwise
    
    Time: O(V + E)
    Space: O(V)
    """
    vis = [0] * V
    
    def bfs(start):
        # Queue: (node, parent)
        queue = deque([(start, -1)])
        vis[start] = 1
        
        while queue:
            node, parent = queue.popleft()
            
            for neighbor in adj[node]:
                if not vis[neighbor]:
                    vis[neighbor] = 1
                    queue.append((neighbor, node))
                
                elif neighbor != parent:
                    # Visited AND not parent = CYCLE!
                    return True
        
        return False
    
    # Check all components (handles disconnected graphs)
    for node in range(V):
        if not vis[node]:
            if bfs(node):
                return True
    
    return False


def isCycle_DFS(V: int, adj: list) -> bool:
    """
    Detect cycle using DFS with parent tracking (recursive).
    """
    vis = [0] * V
    
    def dfs(node, parent):
        vis[node] = 1
        
        for neighbor in adj[node]:
            if not vis[neighbor]:
                if dfs(neighbor, node):  # node becomes parent
                    return True
            
            elif neighbor != parent:
                return True  # Cycle!
        
        return False
    
    for node in range(V):
        if not vis[node]:
            if dfs(node, -1):
                return True
    
    return False


# ============================================
# HELPER: Build adjacency list from edges
# ============================================
def build_adj(V, edges):
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)  # Undirected
    return adj


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    
    # TEST 1: Simple cycle (square)
    #   0 --- 1
    #   |     |
    #   3 --- 2
    V1 = 4
    edges1 = [[0,1], [1,2], [2,3], [3,0]]
    adj1 = build_adj(V1, edges1)
    
    assert isCycle_BFS(V1, adj1) == True
    assert isCycle_DFS(V1, adj1) == True
    print("TEST 1 PASSED: Cycle detected (square)")
    
    
    # TEST 2: No cycle (line)
    #   0 --- 1 --- 2 --- 3
    V2 = 4
    edges2 = [[0,1], [1,2], [2,3]]
    adj2 = build_adj(V2, edges2)
    
    assert isCycle_BFS(V2, adj2) == False
    assert isCycle_DFS(V2, adj2) == False
    print("TEST 2 PASSED: No cycle (line)")
    
    
    # TEST 3: Triangle (cycle)
    #     0
    #    / \
    #   1---2
    V3 = 3
    edges3 = [[0,1], [1,2], [2,0]]
    adj3 = build_adj(V3, edges3)
    
    assert isCycle_BFS(V3, adj3) == True
    assert isCycle_DFS(V3, adj3) == True
    print("TEST 3 PASSED: Cycle detected (triangle)")
    
    
    # TEST 4: Disconnected - one component has cycle
    #   Component 1: 0 --- 1
    #   Component 2: 2 --- 3
    #                |     |
    #                4 --- 5
    V4 = 6
    edges4 = [[0,1], [2,3], [3,5], [5,4], [4,2]]  # Cycle in component 2
    adj4 = build_adj(V4, edges4)
    
    assert isCycle_BFS(V4, adj4) == True
    assert isCycle_DFS(V4, adj4) == True
    print("TEST 4 PASSED: Cycle in disconnected component")
    
    
    # TEST 5: Tree (no cycle)
    #       0
    #      /|\
    #     1 2 3
    #    /|
    #   4 5
    V5 = 6
    edges5 = [[0,1], [0,2], [0,3], [1,4], [1,5]]
    adj5 = build_adj(V5, edges5)
    
    assert isCycle_BFS(V5, adj5) == False
    assert isCycle_DFS(V5, adj5) == False
    print("TEST 5 PASSED: Tree structure (no cycle)")
    
    
    # TEST 6: Single node
    V6 = 1
    adj6 = [[]]
    
    assert isCycle_BFS(V6, adj6) == False
    assert isCycle_DFS(V6, adj6) == False
    print("TEST 6 PASSED: Single node (no cycle)")
    
    
    print("\n" + "=" * 40)
    print("ALL 6 TESTS PASSED!")
    print("=" * 40)
