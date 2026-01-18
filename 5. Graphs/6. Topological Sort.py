"""
Topological Sort
GFG: https://www.geeksforgeeks.org/problems/topological-sort/1

===========================================
WHAT IS TOPOLOGICAL SORT?
===========================================

LINEAR ORDERING of vertices (nodes) such that:
    If there is an edge from U → V, then U must appear BEFORE V in the ordering.

Simple Rule: "Dependencies come first!"

===========================================
EXAMPLE 1: The Graph
===========================================

    5 ──→ 0 ←── 4
    │           │
    ↓           ↓
    2 ──→ 3 ──→ 1

Edges:
    5 → 0    (5 must come before 0)
    5 → 2    (5 must come before 2)
    4 → 0    (4 must come before 0)
    4 → 1    (4 must come before 1)
    2 → 3    (2 must come before 3)
    3 → 1    (3 must come before 1)

Let's trace through:
    - Node 5: No incoming edges → Can start with 5
    - Node 4: No incoming edges → Can also start with 4
    - Node 0: Needs 5 and 4 first
    - Node 2: Needs 5 first
    - Node 3: Needs 2 first
    - Node 1: Needs 4 and 3 first (comes last!)

VALID Topological Orders:
    ✓ 5 → 4 → 0 → 2 → 3 → 1
    ✓ 4 → 5 → 2 → 3 → 1 → 0
    ✓ 5 → 4 → 2 → 3 → 0 → 1
    (Multiple valid answers exist!)

INVALID Order:
    ✗ 0 → 5 → 4 → 2 → 3 → 1  (0 came before 5, but 5→0 exists!)

===========================================
REAL-LIFE ANALOGY: Getting Dressed 👔
===========================================

You CAN'T wear shoes before socks!
You CAN'T wear shirt before bra (if applicable)!

Dependencies:
    Underwear  →  Pants     (underwear before pants)
    Pants      →  Belt      (pants before belt)
    Pants      →  Shoes     (pants before shoes)
    Socks      →  Shoes     (socks before shoes)
    Shirt      →  Belt      (shirt before belt, tucked in)
    Shirt      →  Watch     (sleeves first!)

        Underwear ──→ Pants ──→ Belt
                        │         ↑
                        ↓         │
        Socks ──────→ Shoes    Shirt ──→ Watch

Valid Order:
    Underwear → Socks → Pants → Shirt → Belt → Watch → Shoes
    Socks → Underwear → Shirt → Pants → Belt → Watch → Shoes
    
Invalid Order:
    Shoes → Socks → Pants → ... (WRONG! Can't wear shoes before socks!)

===========================================
WHY ONLY DAG (Directed Acyclic Graph)?
===========================================

TOPOLOGICAL SORT ONLY WORKS ON DAG!
    - D = Directed  (edges have direction)
    - A = Acyclic   (no cycles)
    - G = Graph

-------------------------------------------
WHY NOT UNDIRECTED GRAPH?
-------------------------------------------

In undirected graph: A --- B means BOTH:
    A → B  AND  B → A

This creates a CONTRADICTION:
    - A must come before B (because A → B)
    - B must come before A (because B → A)
    
    IMPOSSIBLE! Both can't be true at the same time.

Example:
    A --- B (undirected)
    
    Rule says: "A before B" AND "B before A"
    
    ? → ?   ← Which comes first? IMPOSSIBLE!

-------------------------------------------
WHY NOT CYCLIC GRAPH?
-------------------------------------------

If there's a cycle: A → B → C → A

Then:
    - A must come before B (A → B)
    - B must come before C (B → C)
    - C must come before A (C → A)
    
    So: A < B < C < A
    
    This means: A < A  (A before A itself?)
    
    CONTRADICTION! A node can't come before itself!

Example:
    A → B
    ↑   ↓
    └── C
    
    A → B → C → A (cycle!)
    
    Order attempt: A → B → C → ... but C needs to go before A!
    But A is already placed! IMPOSSIBLE!

-------------------------------------------
SUMMARY: Why DAG Only?
-------------------------------------------

| Graph Type      | Why Topo Sort Fails?                    |
|-----------------|----------------------------------------|
| Undirected      | Both directions = contradiction         |
| Cyclic          | A < A is impossible (self-dependency)   |
| DAG ✓           | Clear direction, no circular dependency |

===========================================
TWO APPROACHES
===========================================

1. DFS Approach (Using Stack)
   - Do DFS, add node to stack AFTER visiting all neighbors
   - Reverse the stack = Topological Order

2. BFS Approach (Kahn's Algorithm - Using In-degree)
   - Start with nodes having in-degree = 0
   - Process them, reduce in-degree of neighbors
   - Add neighbors with in-degree 0 to queue

===========================================
"""

from collections import deque, defaultdict


# ============================================
# APPROACH 1: DFS (Stack-based)
# ============================================
def topological_sort_dfs(V: int, adj: list) -> list:
    """
    Topological Sort using DFS.
    
    IDEA: 
        - After visiting ALL neighbors of a node, push it to stack
        - This ensures all dependencies are processed before the node
        - Finally, reverse the stack for topological order
    
    Time: O(V + E)
    Space: O(V) for visited + stack
    """
    vis = [0] * V
    stack = []  # Will store reverse topological order
    
    def dfs(node):
        vis[node] = 1
        
        # Visit all neighbors first
        for neighbor in adj[node]:
            if not vis[neighbor]:
                dfs(neighbor)
        
        # AFTER all neighbors done, push this node
        # (This node's dependencies are all processed)
        stack.append(node)
    
    # Handle disconnected components
    for node in range(V):
        if not vis[node]:
            dfs(node)
    
    # Reverse stack = Topological Order
    return stack[::-1]


# ============================================
# APPROACH 2: BFS (Kahn's Algorithm)
# ============================================
def topological_sort_bfs(V: int, adj: list) -> list:
    """
    Topological Sort using BFS (Kahn's Algorithm).
    
    IDEA:
        - Calculate in-degree of each node
        - Start with nodes having in-degree = 0 (no dependencies)
        - Process them, reduce in-degree of their neighbors
        - When neighbor's in-degree becomes 0, add to queue
    
    IN-DEGREE = Number of incoming edges to a node
    
    Time: O(V + E)
    Space: O(V) for in-degree array + queue
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
    
    result = []
    
    # Step 3: BFS - process nodes level by level
    while queue:
        node = queue.popleft()
        result.append(node)
        
        # Reduce in-degree of neighbors
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            
            # If in-degree becomes 0, add to queue
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Step 4: Check if topological sort is possible
    # If result doesn't contain all nodes = CYCLE EXISTS!
    if len(result) != V:
        return []  # Cycle detected, no valid topological order
    
    return result


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
    
    # TEST 1: The example from the explanation
    #     5 ──→ 0 ←── 4
    #     │           │
    #     ↓           ↓
    #     2 ──→ 3 ──→ 1
    
    print("=" * 50)
    print("TEST 1: Main Example")
    print("=" * 50)
    
    V1 = 6
    edges1 = [
        [5, 0],  # 5 → 0
        [5, 2],  # 5 → 2
        [4, 0],  # 4 → 0
        [4, 1],  # 4 → 1
        [2, 3],  # 2 → 3
        [3, 1],  # 3 → 1
    ]
    adj1 = build_adj(V1, edges1)
    
    print(f"Graph edges: {edges1}")
    print(f"\nDFS Topological Order: {topological_sort_dfs(V1, adj1)}")
    print(f"BFS Topological Order: {topological_sort_bfs(V1, adj1)}")
    
    # Verify: For each edge u→v, u appears before v
    def verify_topo_order(order, edges):
        pos = {node: i for i, node in enumerate(order)}
        for u, v in edges:
            if pos[u] > pos[v]:
                return False, f"Failed: {u} should come before {v}"
        return True, "Valid topological order!"
    
    dfs_order = topological_sort_dfs(V1, adj1)
    valid, msg = verify_topo_order(dfs_order, edges1)
    print(f"Verification: {msg}")
    
    
    # TEST 2: Simple chain
    #   0 → 1 → 2 → 3
    print("\n" + "=" * 50)
    print("TEST 2: Simple Chain")
    print("=" * 50)
    
    V2 = 4
    edges2 = [[0, 1], [1, 2], [2, 3]]
    adj2 = build_adj(V2, edges2)
    
    print(f"DFS: {topological_sort_dfs(V2, adj2)}")  # Expected: [0, 1, 2, 3]
    print(f"BFS: {topological_sort_bfs(V2, adj2)}")  # Expected: [0, 1, 2, 3]
    
    
    # TEST 3: Multiple starting points
    #   0    1    2
    #   ↓    ↓    ↓
    #   3 ←──4 ←──5
    print("\n" + "=" * 50)
    print("TEST 3: Multiple Starting Points")
    print("=" * 50)
    
    V3 = 6
    edges3 = [[0, 3], [1, 4], [2, 5], [4, 3], [5, 4]]
    adj3 = build_adj(V3, edges3)
    
    print(f"DFS: {topological_sort_dfs(V3, adj3)}")
    print(f"BFS: {topological_sort_bfs(V3, adj3)}")
    
    
    # TEST 4: Single Node (Edge case)
    print("\n" + "=" * 50)
    print("TEST 4: Single Node")
    print("=" * 50)
    
    V4 = 1
    adj4 = [[]]
    
    print(f"DFS: {topological_sort_dfs(V4, adj4)}")  # Expected: [0]
    print(f"BFS: {topological_sort_bfs(V4, adj4)}")  # Expected: [0]
    
    
    # TEST 5: No edges (disconnected nodes)
    print("\n" + "=" * 50)
    print("TEST 5: No Edges (All Independent)")
    print("=" * 50)
    
    V5 = 4
    adj5 = [[], [], [], []]  # No edges
    
    print(f"DFS: {topological_sort_dfs(V5, adj5)}")  # Any order valid
    print(f"BFS: {topological_sort_bfs(V5, adj5)}")  # Any order valid
    
    
    print("\n" + "=" * 50)
    print("ALL TESTS COMPLETED!")
    print("=" * 50)
