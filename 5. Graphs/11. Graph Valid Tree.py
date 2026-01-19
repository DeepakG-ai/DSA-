"""
Graph Valid Tree (LeetCode 261 / LintCode 178)
https://leetcode.com/problems/graph-valid-tree/
https://www.lintcode.com/problem/178/

===========================================
PROBLEM
===========================================
Given n nodes labeled from 0 to n-1 and a list of undirected edges,
check if these edges make up a valid tree.

A valid tree must satisfy:
    1. Connected: All nodes must be reachable from any node
    2. No Cycle: There should be no cycles

===========================================
KEY INSIGHT
===========================================

For a graph to be a VALID TREE:
    1. Number of edges = n - 1 (exactly!)
    2. All nodes are connected (single component)

WHY n-1 edges?
    - A tree with n nodes always has exactly n-1 edges
    - Less edges = disconnected
    - More edges = definitely has cycle

APPROACH 1: Check edges + BFS/DFS connectivity
    - If edges != n-1, return False
    - Do BFS/DFS from node 0, check if all n nodes visited

APPROACH 2: Union-Find
    - For each edge, union the two nodes
    - If already in same set = cycle!
    - At end, check if all in same component

===========================================
"""

from typing import List
from collections import deque


# ============================================
# DFS SOLUTION
# ============================================
class Solution_DFS:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # Rule 1: Tree must have exactly n-1 edges
        if len(edges) != n - 1:
            return False
        
        # Build adjacency list (undirected)
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        
        # DFS to check connectivity
        vis = set()
        
        def dfs(node):
            vis.add(node)
            for neighbor in adj[node]:
                if neighbor not in vis:
                    dfs(neighbor)
        
        # Start DFS from node 0
        dfs(0)
        
        # Rule 2: All nodes must be connected
        return len(vis) == n


# ============================================
# BFS SOLUTION
# ============================================
class Solution_BFS:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # Rule 1: Tree must have exactly n-1 edges
        if len(edges) != n - 1:
            return False
        
        # Build adjacency list (undirected)
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        
        # BFS to check connectivity
        vis = set([0])
        queue = deque([0])
        
        while queue:
            node = queue.popleft()
            for neighbor in adj[node]:
                if neighbor not in vis:
                    vis.add(neighbor)
                    queue.append(neighbor)
        
        # Rule 2: All nodes must be connected
        return len(vis) == n


# ============================================
# UNION-FIND SOLUTION
# ============================================
class Solution_UnionFind:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # Rule 1: Tree must have exactly n-1 edges
        if len(edges) != n - 1:
            return False
        
        # Union-Find setup
        parent = list(range(n))
        rank = [0] * n
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False  # Already connected = cycle!
            # Union by rank
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True
        
        # Try to union all edges
        for u, v in edges:
            if not union(u, v):
                return False  # Cycle detected!
        
        return True


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    sol_dfs = Solution_DFS()
    sol_bfs = Solution_BFS()
    sol_uf = Solution_UnionFind()
    
    # TEST 1: Valid Tree
    # 0 - 1 - 2 - 3 - 4
    print("=" * 50)
    print("TEST 1: Valid Tree (Chain)")
    print("=" * 50)
    
    n1 = 5
    edges1 = [[0,1], [0,2], [0,3], [1,4]]
    
    print(f"DFS: {sol_dfs.validTree(n1, edges1)}")
    print(f"BFS: {sol_bfs.validTree(n1, edges1)}")
    print(f"UF:  {sol_uf.validTree(n1, edges1)}")
    assert sol_dfs.validTree(n1, edges1) == True
    print("PASSED!\n")
    
    
    # TEST 2: Has Cycle (Not a Tree)
    # 0 - 1
    # |   |
    # 3 - 2
    print("=" * 50)
    print("TEST 2: Has Cycle (Square)")
    print("=" * 50)
    
    n2 = 5
    edges2 = [[0,1], [1,2], [2,3], [1,3], [1,4]]
    
    print(f"DFS: {sol_dfs.validTree(n2, edges2)}")
    print(f"BFS: {sol_bfs.validTree(n2, edges2)}")
    print(f"UF:  {sol_uf.validTree(n2, edges2)}")
    assert sol_dfs.validTree(n2, edges2) == False
    print("PASSED!\n")
    
    
    # TEST 3: Disconnected
    # 0 - 1    2 - 3
    print("=" * 50)
    print("TEST 3: Disconnected")
    print("=" * 50)
    
    n3 = 4
    edges3 = [[0,1], [2,3]]
    
    print(f"DFS: {sol_dfs.validTree(n3, edges3)}")
    print(f"BFS: {sol_bfs.validTree(n3, edges3)}")
    print(f"UF:  {sol_uf.validTree(n3, edges3)}")
    assert sol_dfs.validTree(n3, edges3) == False
    print("PASSED!\n")
    
    
    # TEST 4: Single Node
    print("=" * 50)
    print("TEST 4: Single Node")
    print("=" * 50)
    
    n4 = 1
    edges4 = []
    
    print(f"DFS: {sol_dfs.validTree(n4, edges4)}")
    print(f"BFS: {sol_bfs.validTree(n4, edges4)}")
    print(f"UF:  {sol_uf.validTree(n4, edges4)}")
    assert sol_dfs.validTree(n4, edges4) == True
    print("PASSED!\n")
    
    
    # TEST 5: Two nodes, one edge
    print("=" * 50)
    print("TEST 5: Two Nodes, One Edge")
    print("=" * 50)
    
    n5 = 2
    edges5 = [[0, 1]]
    
    print(f"DFS: {sol_dfs.validTree(n5, edges5)}")
    print(f"BFS: {sol_bfs.validTree(n5, edges5)}")
    print(f"UF:  {sol_uf.validTree(n5, edges5)}")
    assert sol_dfs.validTree(n5, edges5) == True
    print("PASSED!\n")
    
    
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
