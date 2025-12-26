"""LeetCode Problem 235: Lowest Common Ancestor of a Binary Search Tree
Method: BST Property Traversal
Category: Trees, BST
Time Complexity: O(h) where h = height of tree
Space Complexity: O(1) iterative, O(h) recursive
Link: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/

-----------------------------------
Problem Description:
Given a binary search tree (BST), find the lowest common ancestor (LCA) 
of two given nodes in the BST.

The lowest common ancestor is defined as the lowest node in the tree 
that has both p and q as descendants (a node can be a descendant of itself).

-----------------------------------
Visual Explanation:

        6
       / \
      2   8
     / \ / \
    0  4 7  9
      / \
     3   5

LCA(2, 8) = 6  (6 is the first node where 2 and 8 split)
LCA(2, 4) = 2  (2 is ancestor of 4, so 2 itself is LCA)
LCA(3, 5) = 4  (4 is where 3 and 5 diverge)

-----------------------------------
Key Insight (BST Property):

For any node:
- Left subtree has values < node.val
- Right subtree has values > node.val

So for finding LCA of p and q:
1. If both p, q < current → LCA is in LEFT subtree
2. If both p, q > current → LCA is in RIGHT subtree
3. Otherwise, current node IS the LCA (they split here!)

-----------------------------------
Constraints:
• The number of nodes in the tree is in the range [2, 10^5]
• -10^9 <= Node.val <= 10^9
• All Node.val are unique
• p != q
• p and q will exist in the BST

-----------------------------------
Examples:

Example 1:
Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
Output: 6
Explanation: The LCA of nodes 2 and 8 is 6.

Example 2:
Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
Output: 2
Explanation: The LCA of nodes 2 and 4 is 2, since a node can be 
a descendant of itself.
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
# 1. Iterative Solution (Optimal)
# ⭐ BEST FOR INTERVIEW - O(1) space, shows BST property understanding
# Time: O(h), Space: O(1)
# -------------------------------
class Solution:
    """
    Use BST property to navigate:
    - Both p, q < current → go LEFT
    - Both p, q > current → go RIGHT
    - Otherwise → current is LCA (split point)
    """
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        current = root
        
        while current:
            # Both p and q are in LEFT subtree
            if p.val < current.val and q.val < current.val:
                current = current.left
            
            # Both p and q are in RIGHT subtree
            elif p.val > current.val and q.val > current.val:
                current = current.right
            
            # Split point found - this is the LCA!
            else:
                return current
        
        return None  # Should never reach here if p, q exist


# -------------------------------
# 2. Recursive Solution
# Time: O(h), Space: O(h) - call stack
# -------------------------------
class SolutionRecursive:
    """
    Same logic as iterative, but using recursion.
    """
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        # Base case check
        if not root:
            return None
        
        # Both in left subtree
        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)
        
        # Both in right subtree
        elif p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)
        
        # Split point - current node is LCA
        else:
            return root


# -------------------------------
# Dry Run Example
# -------------------------------
"""
Tree:
        6
       / \
      2   8
     / \
    0   4

Find LCA(2, 8):

Step 1: current = 6
    p=2 < 6 and q=8 > 6 → SPLIT!
    Return 6

Find LCA(0, 4):

Step 1: current = 6
    p=0 < 6 and q=4 < 6 → Both LEFT
    Go left

Step 2: current = 2
    p=0 < 2 and q=4 > 2 → SPLIT!
    Return 2
"""


# -------------------------------
# Why This Works (Only for BST!)
# -------------------------------
"""
BST Property:
    Left < Root < Right

When we find a node where p and q are on DIFFERENT sides 
(or one equals the node), that's the LCA!

      6      ← p=2 goes left, q=8 goes right → LCA is 6
     / \
    2   8

Note: This ONLY works for BST! 
For regular binary tree, you need a different approach 
(check both subtrees and compare).
"""


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


def find_node(root, val):
    """Find and return node with given value."""
    if not root:
        return None
    if root.val == val:
        return root
    if val < root.val:
        return find_node(root.left, val)
    return find_node(root.right, val)


if __name__ == "__main__":
    sol = Solution()
    sol_rec = SolutionRecursive()
    
    # Build tree: [6,2,8,0,4,7,9,null,null,3,5]
    #         6
    #        / \
    #       2   8
    #      / \ / \
    #     0  4 7  9
    #       / \
    #      3   5
    root = array_to_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    
    # Test Case 1: LCA of 2 and 8
    p1 = find_node(root, 2)
    q1 = find_node(root, 8)
    result1 = sol.lowestCommonAncestor(root, p1, q1)
    print(f"LCA(2, 8) = {result1.val}")  # Expected: 6
    
    # Test Case 2: LCA of 2 and 4
    p2 = find_node(root, 2)
    q2 = find_node(root, 4)
    result2 = sol.lowestCommonAncestor(root, p2, q2)
    print(f"LCA(2, 4) = {result2.val}")  # Expected: 2
    
    # Test Case 3: LCA of 3 and 5
    p3 = find_node(root, 3)
    q3 = find_node(root, 5)
    result3 = sol_rec.lowestCommonAncestor(root, p3, q3)
    print(f"LCA(3, 5) = {result3.val}")  # Expected: 4
    
    # Test Case 4: LCA of 0 and 9
    p4 = find_node(root, 0)
    q4 = find_node(root, 9)
    result4 = sol.lowestCommonAncestor(root, p4, q4)
    print(f"LCA(0, 9) = {result4.val}")  # Expected: 6
