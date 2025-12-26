"""LeetCode Problem 104: Maximum Depth of Binary Tree
Method: DFS (Recursive) / BFS (Iterative)
Category: Trees, DFS, BFS, Recursion
Time Complexity: O(n)
Space Complexity: O(h) where h = height of tree
Link: https://leetcode.com/problems/maximum-depth-of-binary-tree/

-----------------------------------
Problem Description:
Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the NUMBER OF NODES along the longest path 
from the root node down to the farthest leaf node.

-----------------------------------
Visual Explanation:

        3          ← Level 1 (depth 1)
       / \
      9  20        ← Level 2 (depth 2)
        /  \
       15   7      ← Level 3 (depth 3)

Maximum Depth = 3 (counting nodes: 3 → 20 → 15 or 3 → 20 → 7)

-----------------------------------
Key Insight (Recursive):

max_depth(node) = 1 + max(max_depth(left), max_depth(right))

"My depth = 1 (myself) + whichever child is deeper"

Base case: if node is None, return 0

-----------------------------------
Constraints:
• The number of nodes in the tree is in the range [0, 10^4]
• -100 <= Node.val <= 100

-----------------------------------
Examples:

Example 1:
Input: root = [3,9,20,null,null,15,7]
Output: 3

Example 2:
Input: root = [1,null,2]
Output: 2
"""

from typing import Optional
from collections import deque

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# -------------------------------
# 1. DFS Recursive (Most Intuitive)
# ⭐ BEST FOR INTERVIEW - Simple, clean, easy to explain
# Time: O(n), Space: O(h) - call stack
# -------------------------------
class Solution:
    """
    Recursion approach:
    - If node is None, depth is 0
    - Otherwise, depth = 1 + max(left_depth, right_depth)
    
    Think of it as asking each node:
    "What's the deepest path starting from you?"
    """
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        
        return 1 + max(left_depth, right_depth)


# -------------------------------
# 2. DFS Recursive (One-liner)
# Same logic, compact form
# -------------------------------
class SolutionOneLiner:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


# -------------------------------
# 3. BFS (Level Order) Approach
# Time: O(n), Space: O(w) - w = max width
# -------------------------------
class SolutionBFS:
    """
    Count number of levels using BFS.
    Each level = depth increases by 1.
    """
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        queue = deque([root])
        depth = 0
        
        while queue:
            depth += 1  # Each level = +1 depth
            level_size = len(queue)
            
            for _ in range(level_size):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return depth


# -------------------------------
# 4. DFS Iterative (Stack)
# Time: O(n), Space: O(h)
# -------------------------------
class SolutionDFSIterative:
    """
    Use stack to simulate recursion.
    Store (node, current_depth) pairs.
    """
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        stack = [(root, 1)]  # (node, depth)
        max_depth = 0
        
        while stack:
            node, depth = stack.pop()
            max_depth = max(max_depth, depth)
            
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
        
        return max_depth


# -------------------------------
# Dry Run: Recursive DFS
# -------------------------------
"""
Tree:
        3
       / \
      9  20
        /  \
       15   7

maxDepth(3):
    ├── maxDepth(9):
    │   ├── maxDepth(None) → 0
    │   └── maxDepth(None) → 0
    │   └── return 1 + max(0, 0) = 1
    │
    └── maxDepth(20):
        ├── maxDepth(15):
        │   ├── maxDepth(None) → 0
        │   └── maxDepth(None) → 0
        │   └── return 1 + max(0, 0) = 1
        │
        └── maxDepth(7):
            ├── maxDepth(None) → 0
            └── maxDepth(None) → 0
            └── return 1 + max(0, 0) = 1
        
        └── return 1 + max(1, 1) = 2
    
    └── return 1 + max(1, 2) = 3

Answer: 3 ✓
"""


# -------------------------------
# Dry Run: BFS
# -------------------------------
"""
Tree:
        3
       / \
      9  20
        /  \
       15   7

Initial: queue = [3], depth = 0

Level 1: depth = 1, process [3], add [9, 20]
Level 2: depth = 2, process [9, 20], add [15, 7]
Level 3: depth = 3, process [15, 7], add nothing

Queue empty → return depth = 3 ✓
"""


# -------------------------------
# Complexity Comparison
# -------------------------------
"""
| Approach       | Time  | Space     | When to Use            |
|---------------|-------|-----------|------------------------|
| DFS Recursive | O(n)  | O(h)      | Most intuitive         |
| DFS Iterative | O(n)  | O(h)      | Avoid stack overflow   |
| BFS           | O(n)  | O(w)      | Level-by-level needed  |

h = height of tree (worst case n for skewed tree)
w = max width of tree (worst case n/2 for complete tree)
"""


# -------------------------------
# Helper Functions
# -------------------------------
def array_to_tree(arr):
    """Convert LeetCode array to tree."""
    if not arr or arr[0] is None:
        return None
    
    root = TreeNode(arr[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(arr):
        node = queue.popleft()
        
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    
    return root


if __name__ == "__main__":
    sol = Solution()
    sol_bfs = SolutionBFS()
    
    # Test Case 1
    root1 = array_to_tree([3, 9, 20, None, None, 15, 7])
    print("Test 1 (DFS):", sol.maxDepth(root1))      # Expected: 3
    print("Test 1 (BFS):", sol_bfs.maxDepth(root1))  # Expected: 3
    
    # Test Case 2
    root2 = array_to_tree([1, None, 2])
    print("Test 2:", sol.maxDepth(root2))  # Expected: 2
    
    # Test Case 3: Empty tree
    root3 = None
    print("Test 3 (Empty):", sol.maxDepth(root3))  # Expected: 0
    
    # Test Case 4: Single node
    root4 = TreeNode(1)
    print("Test 4 (Single):", sol.maxDepth(root4))  # Expected: 1
