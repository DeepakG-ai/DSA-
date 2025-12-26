"""LeetCode Problem 226: Invert Binary Tree
Method: DFS / BFS
Category: Trees, DFS, BFS, Recursion
Time Complexity: O(n)
Space Complexity: O(h) for DFS, O(n) for BFS
Link: https://leetcode.com/problems/invert-binary-tree/

-----------------------------------
Problem Description:
Given the root of a binary tree, invert the tree, and return its root.

This is the famous problem that Homebrew's author couldn't solve!
(Max Howell was rejected by Google for not solving this in 2015)

-----------------------------------
Visual Explanation:

Original:           Inverted:
        4                   4
       / \                 / \
      2   7     →         7   2
     / \ / \             / \ / \
    1  3 6  9           9  6 3  1

Every node's left and right children are SWAPPED!

-----------------------------------
Key Insight:

For EVERY node:
    swap(node.left, node.right)

That's it! Recursively or iteratively swap all children.

-----------------------------------
Constraints:
• The number of nodes in the tree is in the range [0, 100]
• -100 <= Node.val <= 100

-----------------------------------
Examples:

Example 1:
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]

Example 2:
Input: root = [2,1,3]
Output: [2,3,1]

Example 3:
Input: root = []
Output: []
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
# 1. DFS Recursive (Most Elegant)
# ⭐ BEST FOR INTERVIEW - Simple, clean, shows recursion mastery
# Time: O(n), Space: O(h)
# -------------------------------
class Solution:
    """
    Recursive approach:
    1. If node is None, return None
    2. Swap left and right children
    3. Recursively invert left and right subtrees
    """
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        
        # Swap children
        root.left, root.right = root.right, root.left
        
        # Recursively invert subtrees
        self.invertTree(root.left)
        self.invertTree(root.right)
        
        return root


# -------------------------------
# 2. DFS Recursive (Alternative)
# Time: O(n), Space: O(h)
# -------------------------------
class SolutionDFS2:
    """
    Alternative: Invert subtrees first, then swap.
    Same result, different order.
    """
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        
        # Invert subtrees first
        left = self.invertTree(root.left)
        right = self.invertTree(root.right)
        
        # Then swap
        root.left = right
        root.right = left
        
        return root


# -------------------------------
# 3. BFS Iterative (Queue)
# Time: O(n), Space: O(n)
# -------------------------------
class SolutionBFS:
    """
    BFS approach:
    - Use queue to process nodes level by level
    - For each node, swap its children
    """
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            
            # Swap children
            node.left, node.right = node.right, node.left
            
            # Add children to queue for processing
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return root


# -------------------------------
# 4. DFS Iterative (Stack)
# Time: O(n), Space: O(h)
# -------------------------------
class SolutionDFSIterative:
    """
    DFS using stack instead of recursion.
    """
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        
        stack = [root]
        
        while stack:
            node = stack.pop()
            
            # Swap children
            node.left, node.right = node.right, node.left
            
            # Add children to stack
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        
        return root


# -------------------------------
# Dry Run: DFS Recursive
# -------------------------------
"""
Original:
        4
       / \
      2   7

invertTree(4):
    swap: 4.left=7, 4.right=2
    Tree now:
        4
       / \
      7   2
    
    invertTree(7): (no children, returns)
    invertTree(2): (no children, returns)
    
    return 4

Result:
        4
       / \
      7   2
"""


# -------------------------------
# The Famous Tweet
# -------------------------------
"""
Max Howell (@mxcl) - June 10, 2015:

"Google: 90% of our engineers use the software you wrote (Homebrew), 
but you can't invert a binary tree on a whiteboard so f*** off."

This became one of the most famous tweets in tech history!

The irony: This is one of the EASIEST tree problems.
Just swap left and right recursively!
"""


# -------------------------------
# One-liner (For Fun)
# -------------------------------
class SolutionOneLiner:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root:
            root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root


# -------------------------------
# Helper Functions
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


def tree_to_array(root):
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


def print_tree(root, level=0, prefix="Root: "):
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


if __name__ == "__main__":
    sol = Solution()
    
    # Test Case 1
    #        4              4
    #       / \            / \
    #      2   7    →     7   2
    #     / \ / \        / \ / \
    #    1  3 6  9      9  6 3  1
    root1 = array_to_tree([4, 2, 7, 1, 3, 6, 9])
    print("Original:")
    print_tree(root1)
    
    inverted1 = sol.invertTree(root1)
    print("\nInverted:")
    print_tree(inverted1)
    print(f"Array: {tree_to_array(inverted1)}")
    # Expected: [4, 7, 2, 9, 6, 3, 1]
    
    # Test Case 2: Empty
    root2 = None
    print(f"\nEmpty tree inverted: {sol.invertTree(root2)}")
    # Expected: None
    
    # Test Case 3: Single node
    root3 = TreeNode(1)
    print(f"\nSingle node inverted: {tree_to_array(sol.invertTree(root3))}")
    # Expected: [1]
