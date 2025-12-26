"""
Binary Tree Fundamentals in Python
===================================
Complete guide to understanding Binary Trees before solving LeetCode problems.

This file covers:
1. Tree Node Structure
2. Tree Terminology
3. Types of Binary Trees
4. Tree Traversals (DFS & BFS)
5. Building Trees from Arrays (like LeetCode)
"""

from collections import deque
from typing import Optional, List


# ================================================
# 1. TREE NODE STRUCTURE
# ================================================
class TreeNode:
    """
    Binary Tree Node - similar to LinkedList node but with TWO pointers!
    
    LinkedList:           Binary Tree:
    ┌─────┬──────┐       ┌──────┬─────┬───────┐
    │ val │ next │       │ left │ val │ right │
    └─────┴──────┘       └──────┴─────┴───────┘
    
    Visual from your image:
        ┌─────┬─────┬─────┐
        │  ←  │  5  │  →  │
        └──┬──┴─────┴──┬──┘
           ↓           ↓
          [6]         [7]
    """
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left    # Pointer to left child
        self.right = right  # Pointer to right child


# ================================================
# 2. TREE TERMINOLOGY
# ================================================
"""
Example Tree:
                    5        ← ROOT (no parent)
                   / \
                  6   7      ← INTERNAL NODES (have children)
                 / \   \
                8   9   10   ← LEAF NODES (no children)
               /
              1

TERMINOLOGY:
-----------
• Root: Top node (5) - has no parent
• Parent: 6 is parent of 8 and 9
• Children: 8 and 9 are children of 6
• Siblings: 8 and 9 are siblings (same parent)
• Leaf: Node with no children (1, 9, 10)
• Internal Node: Node with at least one child (5, 6, 7, 8)
• Subtree: Any node and all its descendants
• Edge: Connection between parent and child
• Depth: Distance from root (root depth = 0)
• Height: Two conventions exist:
    - Count NODES on longest path → height = 4 (5→6→8→1 = 4 nodes) ← LeetCode uses this!
    - Count EDGES on longest path → height = 3 (3 edges)           ← Some CS textbooks and Graph theory
• Level: All nodes at same depth (Level 0, 1, 2, 3)

NOTE: LeetCode Definition (Problem 104):
  "Maximum depth is the NUMBER OF NODES along the longest path 
   from the root node down to the farthest leaf node."
  So for LeetCode problems, always COUNT NODES!

RELATIONSHIPS in above tree:
---------------------------
• Root = 5
• Leaves = 1, 9, 10
• Height = 3 (longest path: 5 → 6 → 8 → 1)
• Depth of node 8 = 2
• Parent of 8 = 6
• Children of 6 = [8, 9]
• Siblings of 8 = [9]
"""


# ================================================
# 3. TYPES OF BINARY TREES
# ================================================
"""
1. FULL BINARY TREE
   Every node has 0 or 2 children (never 1)
   
       1              1
      / \           / \
     2   3         2   3
                  / \
                 4   5
   
   ✅ Full        ✅ Full


2. COMPLETE BINARY TREE
   All levels filled except last, which fills left to right
   
       1              1
      / \           / \
     2   3         2   3
    / \           / \   \
   4   5         4   5   6
   
   ✅ Complete    ❌ Not Complete (gap before 6)


3. PERFECT BINARY TREE
   All internal nodes have 2 children, all leaves at same level
   
         1
        / \
       2   3
      / \ / \
     4  5 6  7
   
   ✅ Perfect (also Full and Complete)


4. BINARY SEARCH TREE (BST)
   Left child < Parent < Right child
   
         8
        / \
       3   10
      / \    \
     1   6    14
   
   ✅ BST: 1 < 3 < 6 < 8 < 10 < 14
"""


# ================================================
# 4. TREE TRAVERSALS
# ================================================

# ----- DFS: Depth First Search -----
# Go as deep as possible before backtracking
# Uses: Stack (or recursion which uses call stack)

def preorder_dfs(root: TreeNode) -> List[int]:
    """
    PREORDER: Root → Left → Right
    Process root BEFORE children
    
    Use case: Copy/clone a tree, prefix expression
    
         5
        / \
       6   7
      / \
     8   9
    
    Order: 5 → 6 → 8 → 9 → 7
    """
    result = []
    
    def dfs(node):
        if not node:
            return
        result.append(node.val)  # Process ROOT first
        dfs(node.left)           # Then LEFT
        dfs(node.right)          # Then RIGHT
    
    dfs(root)
    return result


def inorder_dfs(root: TreeNode) -> List[int]:
    """
    INORDER: Left → Root → Right
    Process root BETWEEN children
    
    Use case: BST gives sorted order!
    
         5
        / \
       6   7
      / \
     8   9
    
    Order: 8 → 6 → 9 → 5 → 7
    """
    result = []
    
    def dfs(node):
        if not node:
            return
        dfs(node.left)           # Process LEFT first
        result.append(node.val)  # Then ROOT
        dfs(node.right)          # Then RIGHT
    
    dfs(root)
    return result


def postorder_dfs(root: TreeNode) -> List[int]:
    """
    POSTORDER: Left → Right → Root
    Process root AFTER children
    
    Use case: Delete tree, postfix expression
    
         5
        / \
       6   7
      / \
     8   9
    
    Order: 8 → 9 → 6 → 7 → 5
    """
    result = []
    
    def dfs(node):
        if not node:
            return
        dfs(node.left)           # Process LEFT first
        dfs(node.right)          # Then RIGHT
        result.append(node.val)  # Then ROOT last
    
    dfs(root)
    return result


# ----- BFS: Breadth First Search -----
# Process level by level
# Uses: Queue

def bfs_level_order(root: TreeNode) -> List[List[int]]:
    """
    BFS: Level by Level (Breadth First)
    Uses Queue (FIFO)
    
         5
        / \
       6   7
      / \
     8   9
    
    Level 0: [5]
    Level 1: [6, 7]
    Level 2: [8, 9]
    
    Output: [[5], [6, 7], [8, 9]]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result


# ================================================
# 5. BUILDING TREES (Like LeetCode Does)
# ================================================

def array_to_tree(arr: List[Optional[int]]) -> Optional[TreeNode]:
    """
    Convert LeetCode-style array to actual tree.
    LeetCode uses level-order representation with None for missing nodes.
    
    Input:  [5, 6, 7, 8, 9, None, None]
    Output:
              5
             / \
            6   7
           / \
          8   9
    
    This is what LeetCode hides from you! (Like LinkedList utils)
    """
    if not arr or arr[0] is None:
        return None
    
    root = TreeNode(arr[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(arr):
        node = queue.popleft()
        
        # Left child
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        
        # Right child
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    
    return root


def tree_to_array(root: TreeNode) -> List[Optional[int]]:
    """
    Convert tree back to LeetCode-style array.
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    
    # Remove trailing Nones
    while result and result[-1] is None:
        result.pop()
    
    return result


def print_tree(root: TreeNode, level=0, prefix="Root: "):
    """Pretty print tree structure."""
    if root is not None:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left or root.right:
            if root.left:
                print_tree(root.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if root.right:
                print_tree(root.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")


# ================================================
# 6. MEMORY TIP: DFS Order Mnemonics
# ================================================
"""
Remember the traversal orders:

PRE-order:   ROOT comes PRE (before) children
             Root → Left → Right

IN-order:    ROOT comes IN (between) children
             Left → Root → Right

POST-order:  ROOT comes POST (after) children
             Left → Right → Root

Visual:
         ①
        / \
       ②   ③

PRE:  ① → ② → ③  (Root first)
IN:   ② → ① → ③  (Root in middle)
POST: ② → ③ → ①  (Root last)
"""


# ================================================
# DEMO / TEST
# ================================================
if __name__ == "__main__":
    print("=" * 60)
    print("BINARY TREE FUNDAMENTALS DEMO")
    print("=" * 60)
    
    # Create tree from your image: 5 → 6,7 → 8,9
    #       5
    #      / \
    #     6   7
    #    / \
    #   8   9
    #  /
    # 1
    
    # Method 1: Manual creation
    root = TreeNode(5)
    root.left = TreeNode(6)
    root.right = TreeNode(7)
    root.left.left = TreeNode(8)
    root.left.right = TreeNode(9)
    root.left.left.left = TreeNode(1)
    
    print("\n1. Tree Structure:")
    print_tree(root)
    
    print("\n2. DFS Traversals:")
    print(f"   Preorder  (Root→L→R): {preorder_dfs(root)}")
    print(f"   Inorder   (L→Root→R): {inorder_dfs(root)}")
    print(f"   Postorder (L→R→Root): {postorder_dfs(root)}")
    
    print("\n3. BFS Traversal:")
    print(f"   Level Order: {bfs_level_order(root)}")
    
    # Method 2: From LeetCode-style array
    print("\n4. Building tree from array (like LeetCode):")
    arr = [5, 6, 7, 8, 9]
    tree_from_arr = array_to_tree(arr)
    print(f"   Input array: {arr}")
    print(f"   Tree structure:")
    print_tree(tree_from_arr)
    
    print("\n5. Converting tree back to array:")
    back_to_arr = tree_to_array(root)
    print(f"   Output: {back_to_arr}")
    
    print("\n" + "=" * 60)
    print("Now you're ready for LeetCode Tree problems! 🌳")
    print("=" * 60)
