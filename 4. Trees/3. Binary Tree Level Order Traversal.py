"""LeetCode Problem 102: Binary Tree Level Order Traversal
Method: BFS (Breadth First Search) with Queue
Category: Trees, BFS, Queue
Time Complexity: O(n)
Space Complexity: O(n)
Link: https://leetcode.com/problems/binary-tree-level-order-traversal/

-----------------------------------
Problem Description:
Given the root of a binary tree, return the level order traversal of its nodes' values.
(i.e., from left to right, level by level).

-----------------------------------
Visual Explanation:

        3          ← Level 0
       / \
      9  20        ← Level 1
        /  \
       15   7      ← Level 2

Output: [[3], [9, 20], [15, 7]]

-----------------------------------
Key Insight:

BFS = Level Order Traversal!

Use a QUEUE (FIFO):
1. Start with root in queue
2. Process all nodes at current level
3. Add their children to queue for next level
4. Repeat until queue is empty

-----------------------------------
Constraints:
• The number of nodes in the tree is in the range [0, 2000]
• -1000 <= Node.val <= 1000

-----------------------------------
Examples:

Example 1:
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]

Example 2:
Input: root = [1]
Output: [[1]]

Example 3:
Input: root = []
Output: []
"""

from typing import Optional, List
from collections import deque

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# -------------------------------
# BFS Solution (Standard)
# ⭐ BEST FOR INTERVIEW - Interviewers expect BFS for level-order problems
# Time: O(n), Space: O(n)
# -------------------------------
class Solution:
    """
    BFS with Queue:
    1. Add root to queue
    2. While queue not empty:
       - Get size of current level
       - Process all nodes in this level
       - Add their children to queue
    """
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            level_size = len(queue)  # Number of nodes at current level
            current_level = []
            
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)
                
                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(current_level)
        
        return result


# -------------------------------
# DFS Solution (Alternative)
# Time: O(n), Space: O(n)
# -------------------------------
class SolutionDFS:
    """
    DFS approach: Track level while traversing.
    Less intuitive but works!
    """
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        result = []
        self.dfs(root, 0, result)
        return result
    
    def dfs(self, node, level, result):
        if not node:
            return
        
        # If this level doesn't exist in result, create it
        if level == len(result):
            result.append([])
        
        # Add current node to its level
        result[level].append(node.val)
        
        # Recurse with level + 1
        self.dfs(node.left, level + 1, result)
        self.dfs(node.right, level + 1, result)


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

Initial: queue = [3], result = []

Iteration 1 (Level 0):
    level_size = 1
    Process 3, add to current_level
    Add 9, 20 to queue
    queue = [9, 20]
    result = [[3]]

Iteration 2 (Level 1):
    level_size = 2
    Process 9 → no children
    Process 20 → add 15, 7 to queue
    queue = [15, 7]
    result = [[3], [9, 20]]

Iteration 3 (Level 2):
    level_size = 2
    Process 15 → no children
    Process 7 → no children
    queue = []
    result = [[3], [9, 20], [15, 7]]

Queue empty → return result
"""


# -------------------------------
# Why Use level_size?
# -------------------------------
"""
Critical! Without level_size, we can't separate levels.

queue = [3]

# Wrong way (no level separation):
while queue:
    node = queue.popleft()
    process(node)
    queue.append(node.left)
    queue.append(node.right)
# Output: [3, 9, 20, 15, 7] ← All in one list!

# Right way (with level_size):
while queue:
    level_size = len(queue)  ← Capture current level size
    for _ in range(level_size):
        # Only process nodes from THIS level
# Output: [[3], [9, 20], [15, 7]] ← Separated by levels!
"""


# -------------------------------
# Helper: Array to Tree
# -------------------------------
def array_to_tree(arr):
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
    sol_dfs = SolutionDFS()
    
    # Test Case 1
    root1 = array_to_tree([3, 9, 20, None, None, 15, 7])
    print("Test 1 (BFS):", sol.levelOrder(root1))
    # Expected: [[3], [9, 20], [15, 7]]
    
    print("Test 1 (DFS):", sol_dfs.levelOrder(root1))
    # Expected: [[3], [9, 20], [15, 7]]
    
    # Test Case 2: Single node
    root2 = array_to_tree([1])
    print("Test 2:", sol.levelOrder(root2))
    # Expected: [[1]]
    
    # Test Case 3: Empty tree
    root3 = None
    print("Test 3 (Empty):", sol.levelOrder(root3))
    # Expected: []
    
    # Test Case 4: Left-skewed
    root4 = array_to_tree([1, 2, None, 3])
    print("Test 4 (Left-skewed):", sol.levelOrder(root4))
    # Expected: [[1], [2], [3]]
