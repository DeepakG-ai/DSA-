"""LeetCode Problem 98: Validate Binary Search Tree
Method: DFS with Range / Inorder Traversal
Category: Trees, DFS, BST
Time Complexity: O(n)
Space Complexity: O(h) optimal, O(n) brute force
Link: https://leetcode.com/problems/validate-binary-search-tree/

-----------------------------------
Problem Description:
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
• The left subtree of a node contains only nodes with keys LESS THAN the node's key
• The right subtree of a node contains only nodes with keys GREATER THAN the node's key
• Both the left and right subtrees must also be BSTs

-----------------------------------
Examples:

Example 1:
Input: root = [2,1,3]
Output: true
      2
     / \
    1   3

Example 2:
Input: root = [5,1,4,null,null,3,6]
Output: false
      5
     / \
    1   4
       / \
      3   6
Explanation: The root node's value is 5 but its right child's value is 4.

-----------------------------------
YOUR TASK:
1. Implement isValidBST_bruteforce() using inorder traversal
2. Implement isValidBST() using DFS with range validation

HINTS:
- Brute Force: Inorder of valid BST = sorted array
- Optimal: Each node has a valid (min, max) range
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
# 1. Brute Force: Inorder Traversal
# Time: O(n), Space: O(n)
# -------------------------------
class SolutionBruteForce:
    """
    HINT: 
    - Do inorder traversal to get all values
    - If the list is strictly increasing → Valid BST
    
    Inorder of valid BST = [1, 3, 4, 5, 7] (sorted!)
    """
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # Step 1: Get inorder traversal
        values = []
        self.inorder(root, values)
        
        # Step 2: Check if strictly increasing
        for i in range(1, len(values)):
            if values[i] <= values[i - 1]:  # Must be STRICTLY greater
                return False
        return True

    def inorder(self, node, values):
        """Inorder: Left → Root → Right"""
        if not node:
            return
        
        self.inorder(node.left, values)
        values.append(node.val)
        self.inorder(node.right, values)


# -------------------------------
# 2. Optimal: DFS with Range
# ⭐ BEST FOR INTERVIEW - O(1) space vs O(n), shows optimization thinking
# Time: O(n), Space: O(h)
# -------------------------------
class Solution:
    """
    Optimal Approach: DFS with Range Validation
    
    Key Idea:
    - Each node must be within a valid range (min_val, max_val)
    - Root starts with range (-infinity, +infinity)
    - For LEFT child: range becomes (min_val, parent.val) ← max shrinks
    - For RIGHT child: range becomes (parent.val, max_val) ← min grows
    
    Example:
          5  (range: -∞ to +∞) ✓
         / \
        3   7
        ↑   ↑
      (-∞,5) (5,+∞)
    """
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # Start with infinite range
        return self.validate(root, float('-inf'), float('inf'))
    
    def validate(self, node, min_val, max_val):
        # Base case: empty node is valid
        if not node:
            return True
        
        # Check if current node is within valid range
        # Must be STRICTLY greater than min and STRICTLY less than max
        if node.val <= min_val or node.val >= max_val:
            return False
        
        # Recursively validate left and right subtrees
        # Left child: update MAX to current node's value (left must be < current)
        # Right child: update MIN to current node's value (right must be > current)
        return (self.validate(node.left, min_val, node.val) and
                self.validate(node.right, node.val, max_val))


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


# -------------------------------
# Test Cases
# -------------------------------
if __name__ == "__main__":
    sol = Solution()
    sol_bf = SolutionBruteForce()
    
    # Test Case 1: Valid BST
    #     2
    #    / \
    #   1   3
    root1 = array_to_tree([2, 1, 3])
    print("Test 1 (should be True):", sol.isValidBST(root1))
    
    # Test Case 2: Invalid BST
    #     5
    #    / \
    #   1   4
    #      / \
    #     3   6
    root2 = array_to_tree([5, 1, 4, None, None, 3, 6])
    print("Test 2 (should be False):", sol.isValidBST(root2))
    
    # Test Case 3: Valid BST
    #       5
    #      / \
    #     3   7
    #    / \
    #   1   4
    root3 = array_to_tree([5, 3, 7, 1, 4])
    print("Test 3 (should be True):", sol.isValidBST(root3))
    
    # Test Case 4: Tricky case - looks valid but isn't!
    #       5
    #      / \
    #     4   6
    #        / \
    #       3   7   ← 3 < 5, can't be in right subtree!
    root4 = array_to_tree([5, 4, 6, None, None, 3, 7])
    print("Test 4 (should be False):", sol.isValidBST(root4))
