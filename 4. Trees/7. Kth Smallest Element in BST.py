"""LeetCode Problem 230: Kth Smallest Element in a BST
Method: Inorder Traversal (DFS)
Category: Trees, BST, DFS
Time Complexity: O(H + k) where H = height
Space Complexity: O(H) for recursion stack
Link: https://leetcode.com/problems/kth-smallest-element-in-a-bst/

-----------------------------------
Problem Description:
Given the root of a binary search tree, and an integer k, return the kth 
smallest value (1-indexed) of all the values of the nodes in the tree.

-----------------------------------
Visual Explanation:

BST Property: Left < Root < Right

So INORDER traversal gives SORTED order!

        5
       / \
      3   6
     / \
    2   4
   /
  1

Inorder: [1, 2, 3, 4, 5, 6] ← Sorted!

k=1 → return 1 (smallest)
k=3 → return 3 (3rd smallest)

-----------------------------------
Key Insight:

Inorder traversal of BST = Sorted order!

Just do inorder and return the k-th element.

Optimization: Stop early once we've found k-th element.

-----------------------------------
Constraints:
• The number of nodes in the tree is n
• 1 <= k <= n <= 10^4
• 0 <= Node.val <= 10^4

-----------------------------------
Examples:

Example 1:
Input: root = [3,1,4,null,2], k = 1
Output: 1

Example 2:
Input: root = [5,3,6,2,4,null,null,1], k = 3
Output: 3
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
# 1. Collect All + Return k-th
# Time: O(n), Space: O(n)
# -------------------------------
class SolutionSimple:
    """
    Simple approach:
    1. Do full inorder traversal
    2. Return element at index k-1
    """
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        values = []
        self.inorder(root, values)
        return values[k - 1]  # 1-indexed, so k-1
    
    def inorder(self, node, values):
        if not node:
            return
        self.inorder(node.left, values)
        values.append(node.val)
        self.inorder(node.right, values)


# -------------------------------
# 2. Early Stop (Optimal)
# ⭐ BEST FOR INTERVIEW - O(H+k) time, shows optimization thinking
# Time: O(H + k), Space: O(H)
# -------------------------------
class Solution:
    """
    Optimization: Stop as soon as we find k-th element!
    No need to traverse entire tree.
    
    Use counter to track how many elements we've visited.
    """
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        self.k = k
        self.result = None
        self.inorder(root)
        return self.result
    
    def inorder(self, node):
        if not node or self.result is not None:
            return
        
        # Go left first (smaller elements)
        self.inorder(node.left)
        
        # Process current node
        self.k -= 1
        if self.k == 0:
            self.result = node.val
            return
        
        # Go right (larger elements)
        self.inorder(node.right)


# -------------------------------
# 3. Iterative with Stack
# Time: O(H + k), Space: O(H)
# -------------------------------
class SolutionIterative:
    """
    Iterative inorder using stack.
    More explicit control over traversal.
    """
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        current = root
        
        while stack or current:
            # Go left as far as possible
            while current:
                stack.append(current)
                current = current.left
            
            # Process node
            current = stack.pop()
            k -= 1
            if k == 0:
                return current.val
            
            # Move to right subtree
            current = current.right
        
        return -1  # Should never reach here


# -------------------------------
# Dry Run Example
# -------------------------------
"""
Tree:
        5
       / \
      3   6
     / \
    2   4
   /
  1

k = 3 (find 3rd smallest)

Inorder traversal with early stop:

1. Go left: 5 → 3 → 2 → 1 → null
2. Process 1: k = 3-1 = 2
3. Back to 2, process: k = 2-1 = 1
4. Go right from 2: null
5. Back to 3, process: k = 1-1 = 0 ← Found!
6. Return 3 ✓

We stopped early - didn't need to visit 4, 5, 6!
"""


# -------------------------------
# Why Inorder = Sorted for BST?
# -------------------------------
"""
BST Property:
    Left subtree < Root < Right subtree

Inorder: Left → Root → Right

So we visit:
    All smaller values (left) → Current → All larger values (right)
    
This naturally gives sorted order!

        5
       / \
      3   6

Inorder: 3 → 5 → 6 ✓ (sorted!)
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


if __name__ == "__main__":
    sol = Solution()
    sol_iter = SolutionIterative()
    
    # Test Case 1
    #     3
    #    / \
    #   1   4
    #    \
    #     2
    root1 = array_to_tree([3, 1, 4, None, 2])
    print("Test 1 (k=1):", sol.kthSmallest(root1, 1))  # Expected: 1
    
    # Test Case 2
    #         5
    #        / \
    #       3   6
    #      / \
    #     2   4
    #    /
    #   1
    root2 = array_to_tree([5, 3, 6, 2, 4, None, None, 1])
    print("Test 2 (k=3):", sol.kthSmallest(root2, 3))  # Expected: 3
    
    # Test Case 3: Iterative approach
    root3 = array_to_tree([5, 3, 6, 2, 4, None, None, 1])
    print("Test 3 (k=4, iterative):", sol_iter.kthSmallest(root3, 4))  # Expected: 4
    
    # Test Case 4: k = n (largest element)
    root4 = array_to_tree([3, 1, 4, None, 2])
    print("Test 4 (k=4, largest):", sol.kthSmallest(root4, 4))  # Expected: 4
