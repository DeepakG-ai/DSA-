"""
Clone Graph (133. LeetCode)
https://leetcode.com/problems/clone-graph/

===========================================
PROBLEM
===========================================
Given a reference of a node in a connected undirected graph.
Return a DEEP COPY (clone) of the graph.

Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

===========================================
WORKFLOW (Deep Copy)
===========================================
Key Challenge: Graph has cycles! A node might point back to an already visited node.
Solution: Use a Hash Map (Dictionary) to track visited nodes.

Map: { Original_Node : Clone_Node }

ALGORITHM (DFS Recursive):
1. If node is None, return None.
2. If node is already in map (visited), return map[node] (the clone).
3. Create a NEW clone node with same value.
4. Add (node : new_node) to map.
5. For each neighbor of node:
   - Recursively call cloneGraph(neighbor)
   - Append the returned clone neighbor to new_node.neighbors
6. Return new_node

===========================================
"""

from collections import deque

# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
    
    def __repr__(self):
        return f"Node({self.val})"


def cloneGraph_DFS(node: 'Node') -> 'Node':
    """
    Deep copy using DFS (Recursive).
    Time: O(V + E) - Visit every vertex and edge once.
    Space: O(V) - Map + Recursion stack.
    """
    if not node:
        return None
    
    old_to_new = {}
    
    def dfs(curr):
        # 1. Base Case: If already cloned, return the clone
        if curr in old_to_new:
            return old_to_new[curr]
        
        # 2. Create copy
        copy = Node(curr.val)
        old_to_new[curr] = copy
        
        # 3. Clone neighbors
        for neighbor in curr.neighbors:
            # Recursively clone and add to neighbors list
            copy.neighbors.append(dfs(neighbor))
            
        return copy
    
    return dfs(node)


def cloneGraph_BFS(node: 'Node') -> 'Node':
    """
    Deep copy using BFS (Iterative).
    Time: O(V + E)
    Space: O(V) - Map + Queue
    """
    if not node:
        return None
    
    old_to_new = {}
    
    # 1. Create start copy and map it
    copy = Node(node.val)
    old_to_new[node] = copy
    
    queue = deque([node])
    
    while queue:
        curr = queue.popleft()
        
        for neighbor in curr.neighbors:
            # If not visited/cloned yet
            if neighbor not in old_to_new:
                # Create clone
                new_neighbor = Node(neighbor.val)
                old_to_new[neighbor] = new_neighbor
                queue.append(neighbor)
            
            # Link the clone (curr's clone -> neighbor's clone)
            old_to_new[curr].neighbors.append(old_to_new[neighbor])
            
    return copy


# ============================================
# HELPER FOR TESTING
# ============================================
def build_graph(adj_list):
    """Factory to build graph from adj list [[2,4],[1,3]...]"""
    if not adj_list: return None
    
    nodes = [Node(i+1) for i in range(len(adj_list))]
    for i, neighbors in enumerate(adj_list):
        for n_idx in neighbors:
            nodes[i].neighbors.append(nodes[n_idx-1])
    return nodes[0] # Return node 1

def get_adj_list(node):
    """Convert graph back to adj list for verification"""
    if not node: return []
    
    result = {}
    visited = set()
    queue = deque([node])
    visited.add(node)
    
    while queue:
        curr = queue.popleft()
        # Store sorted neighbor values (1-based index logic from LeetCode)
        result[curr.val] = sorted([n.val for n in curr.neighbors])
        
        for n in curr.neighbors:
            if n not in visited:
                visited.add(n)
                queue.append(n)
    
    # Sort by node val to match input format [[2,4],[1,3]...]
    output = []
    if not result: return []
    max_val = max(result.keys())
    for i in range(1, max_val + 1):
        output.append(result.get(i, []))
    return output


# ============================================
# TEST CASES
# ============================================
if __name__ == "__main__":
    
    # TEST 1: LeetCode Example 1
    # 1 -- 2
    # |    |
    # 4 -- 3
    adj1 = [[2,4],[1,3],[2,4],[1,3]]
    
    print("--- TEST 1: Simple Cycle ---")
    original_node = build_graph(adj1)
    
    # Run DFS Clone
    cloned_node_dfs = cloneGraph_DFS(original_node)
    print("DFS Clone Result:", get_adj_list(cloned_node_dfs))
    assert get_adj_list(cloned_node_dfs) == adj1
    assert cloned_node_dfs is not original_node # Important: Must be new object!
    
    # Run BFS Clone
    cloned_node_bfs = cloneGraph_BFS(original_node)
    print("BFS Clone Result:", get_adj_list(cloned_node_bfs))
    assert get_adj_list(cloned_node_bfs) == adj1
    assert cloned_node_bfs is not original_node
    
    print("TEST 1 PASSED! \n")


    # TEST 2: Single Node
    adj2 = [[]]
    print("--- TEST 2: Single Node ---")
    original_node2 = build_graph(adj2)
    
    cloned_node2 = cloneGraph_DFS(original_node2)
    print("DFS Clone Result:", get_adj_list(cloned_node2))
    assert get_adj_list(cloned_node2) == adj2
    
    cloned_node2_bfs = cloneGraph_BFS(original_node2)
    print("BFS Clone Result:", get_adj_list(cloned_node2_bfs))
    assert get_adj_list(cloned_node2_bfs) == adj2
    
    print("TEST 2 PASSED! \n")


    # TEST 3: Empty
    adj3 = []
    print("--- TEST 3: Empty Graph ---")
    original_node3 = build_graph(adj3)
    assert cloneGraph_DFS(original_node3) is None
    assert cloneGraph_BFS(original_node3) is None
    print("TEST 3 PASSED! (None returned)")
