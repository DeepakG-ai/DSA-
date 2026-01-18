"""
Detect Cycle in Directed Graph
GFG: https://www.geeksforgeeks.org/problems/detect-cycle-in-a-directed-graph/1

===========================================
PROBLEM
===========================================
Given a directed graph with V vertices and E edges.
Check whether it contains any cycle or not.

===========================================
KEY INSIGHT (Striver's Approach)
===========================================

TOPOLOGICAL SORT only exists for DAG (Directed Acyclic Graph).

If we can't complete topological sort = CYCLE EXISTS!

Using BFS (Kahn's Algorithm):
    - If len(topo_result) != V → Cycle detected!
    - Why? Some nodes never reach in-degree 0 (stuck in cycle)

===========================================
WHY DOES THIS WORK?
===========================================

In Kahn's Algorithm:
    1. We start with nodes having in-degree = 0
    2. We process them and reduce in-degree of neighbors
    3. When neighbor's in-degree becomes 0, we add it to queue

IF THERE'S A CYCLE:
    - Nodes in the cycle will NEVER have in-degree = 0
    - Why? Each node in cycle has at least 1 incoming edge from cycle
    - They're "waiting" for each other forever!

Example with cycle:
    A → B → C → A  (cycle)
    
    in-degree: A=1, B=1, C=1
    
    No node has in-degree 0!
    Queue stays empty.
    Result = [] (length 0, not V)
    → CYCLE DETECTED!

Example without cycle:
    A → B → C
    
    in-degree: A=0, B=1, C=1
    
    Start with A (in-degree 0)
    Process A → B's in-degree becomes 0
    Process B → C's in-degree becomes 0
    Process C
    Result = [A, B, C] (length 3 = V)
    → NO CYCLE!

===========================================
"""

from collections import deque


# ============================================
# APPROACH 1: BFS (Kahn's Algorithm)
# ============================================
def isCyclic_BFS(V: int, adj: list) -> bool:
    """
    Detect cycle using Kahn's Algorithm (Topological Sort BFS).
    
    LOGIC:
        - Try to do topological sort
        - If we can't include all V nodes → Cycle exists!
    
    Time: O(V + E)
    Space: O(V)
    """
    # Step 1: Calculate in-degree of each node
    in_degree = [0] * V
    for node in range(V):
        for neighbor in adj[node]:
            in_degree[neighbor] += 1
    
    # Step 2: Add all nodes with in-degree 0 to queue
    queue = deque()
    for node in range(V):
        if in_degree[node] == 0:
            queue.append(node)
    
    # Step 3: Process nodes (Kahn's Algorithm)
    count = 0  # Count of processed nodes
    
    while queue:
        node = queue.popleft()
        count += 1  # Node processed
        
        # Reduce in-degree of neighbors
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            
            # If in-degree becomes 0, add to queue
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Step 4: Check if all nodes were processed
    # If count != V → Some nodes stuck in cycle → CYCLE EXISTS!
    return count != V


# ============================================
# APPROACH 2: DFS (3-Color Method)
# ============================================
def isCyclic_DFS(V: int, adj: list) -> bool:
    """
    Detect cycle using DFS with 3 colors.
    
    Colors:
        WHITE (0) = Not visited
        GRAY  (1) = Currently in recursion stack (being processed)
        BLACK (2) = Completely processed (all descendants done)
    
    CYCLE = If we find a GRAY node while exploring!
            (We reached a node that's still being processed = back edge!)
    
    Time: O(V + E)
    Space: O(V)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * V
    
    def dfs(node):
        # Mark as currently exploring (GRAY)
        color[node] = GRAY
        
        for neighbor in adj[node]:
            # If neighbor is GRAY → We found a back edge → CYCLE!
            if color[neighbor] == GRAY:
                return True
            
            # If neighbor is WHITE (not visited), explore it
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True
            
            # If neighbor is BLACK → Already fully processed, skip
        
        # Done with this node, mark as BLACK
        color[node] = BLACK
        return False
    
    # Check all components (handle disconnected graph)
    for node in range(V):
        if color[node] == WHITE:
            if dfs(node):
                return True
    
    return False


# ============================================
# HELPER: Build adjacency list
# ============================================
def build_adj(V: int, edges: list) -> list:
    """Build adjacency list for DIRECTED graph."""
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)  # Only u → v (directed!)
    return adj


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    
    # TEST 1: Simple cycle (triangle)
    #   0 → 1
    #   ↑   ↓
    #   └── 2
    print("=" * 50)
    print("TEST 1: Simple Cycle (Triangle)")
    print("=" * 50)
    
    V1 = 3
    edges1 = [[0, 1], [1, 2], [2, 0]]  # 0→1→2→0 (cycle!)
    adj1 = build_adj(V1, edges1)
    
    result_bfs = isCyclic_BFS(V1, adj1)
    result_dfs = isCyclic_DFS(V1, adj1)
    
    print(f"BFS: {result_bfs}")  # True
    print(f"DFS: {result_dfs}")  # True
    assert result_bfs == True
    assert result_dfs == True
    print("PASSED: Cycle detected!\n")
    
    
    # TEST 2: No cycle (chain)
    #   0 → 1 → 2 → 3
    print("=" * 50)
    print("TEST 2: No Cycle (Chain)")
    print("=" * 50)
    
    V2 = 4
    edges2 = [[0, 1], [1, 2], [2, 3]]
    adj2 = build_adj(V2, edges2)
    
    result_bfs = isCyclic_BFS(V2, adj2)
    result_dfs = isCyclic_DFS(V2, adj2)
    
    print(f"BFS: {result_bfs}")  # False
    print(f"DFS: {result_dfs}")  # False
    assert result_bfs == False
    assert result_dfs == False
    print("PASSED: No cycle!\n")
    
    
    # TEST 3: Cycle in one component
    #   0 → 1    3 → 4
    #       ↓    ↑   ↓
    #       2 ───┘   5
    #              ↓ ↑
    #              └─┘ (4→5→4 NOT a cycle, just 5→4 doesn't exist)
    # Actually: 3 → 4 → 5 → 3 (cycle!)
    print("=" * 50)
    print("TEST 3: Cycle with Multiple Components")
    print("=" * 50)
    
    V3 = 6
    edges3 = [[0, 1], [1, 2], [3, 4], [4, 5], [5, 3]]  # 3→4→5→3 cycle
    adj3 = build_adj(V3, edges3)
    
    result_bfs = isCyclic_BFS(V3, adj3)
    result_dfs = isCyclic_DFS(V3, adj3)
    
    print(f"BFS: {result_bfs}")  # True
    print(f"DFS: {result_dfs}")  # True
    assert result_bfs == True
    assert result_dfs == True
    print("PASSED: Cycle in component!\n")
    
    
    # TEST 4: Self-loop
    #   0 → 0 (points to itself)
    print("=" * 50)
    print("TEST 4: Self-loop")
    print("=" * 50)
    
    V4 = 1
    edges4 = [[0, 0]]  # 0 → 0
    adj4 = build_adj(V4, edges4)
    
    result_bfs = isCyclic_BFS(V4, adj4)
    result_dfs = isCyclic_DFS(V4, adj4)
    
    print(f"BFS: {result_bfs}")  # True
    print(f"DFS: {result_dfs}")  # True
    assert result_bfs == True
    assert result_dfs == True
    print("PASSED: Self-loop is a cycle!\n")
    
    
    # TEST 5: DAG (from topological sort example)
    #     5 ──→ 0 ←── 4
    #     │           │
    #     ↓           ↓
    #     2 ──→ 3 ──→ 1
    print("=" * 50)
    print("TEST 5: DAG (No Cycle)")
    print("=" * 50)
    
    V5 = 6
    edges5 = [[5, 0], [5, 2], [4, 0], [4, 1], [2, 3], [3, 1]]
    adj5 = build_adj(V5, edges5)
    
    result_bfs = isCyclic_BFS(V5, adj5)
    result_dfs = isCyclic_DFS(V5, adj5)
    
    print(f"BFS: {result_bfs}")  # False
    print(f"DFS: {result_dfs}")  # False
    assert result_bfs == False
    assert result_dfs == False
    print("PASSED: DAG has no cycle!\n")
    
    
    # TEST 6: Single node, no edges
    print("=" * 50)
    print("TEST 6: Single Node, No Edges")
    print("=" * 50)
    
    V6 = 1
    adj6 = [[]]
    
    result_bfs = isCyclic_BFS(V6, adj6)
    result_dfs = isCyclic_DFS(V6, adj6)
    
    print(f"BFS: {result_bfs}")  # False
    print(f"DFS: {result_dfs}")  # False
    assert result_bfs == False
    assert result_dfs == False
    print("PASSED: No cycle!\n")
    
    
    print("=" * 50)
    print("ALL 6 TESTS PASSED!")
    print("=" * 50)
