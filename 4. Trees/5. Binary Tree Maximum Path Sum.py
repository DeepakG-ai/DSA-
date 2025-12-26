"""LeetCode Problem 124: Binary Tree Maximum Path Sum
Method: DFS with Global Maximum Tracking
Category: Trees, DFS, Dynamic Programming
Time Complexity: O(n)
Space Complexity: O(h) - recursion stack
Link: https://leetcode.com/problems/binary-tree-maximum-path-sum/

Difficulty: HARD

-----------------------------------
Problem Description:
A path in a binary tree is a sequence of nodes where each pair of adjacent 
nodes has an edge connecting them. A node can only appear in the sequence at most once. 
The path does not need to pass through the root.

The path sum is the sum of the node's values in the path.
Given the root of a binary tree, return the maximum path sum of any non-empty path.

-----------------------------------
Visual Explanation:

Example 1:
       1
      / \
     2   3

Paths:
- 2 → 1 → 3 = 6  ← Maximum!
- 1 → 2 = 3
- 1 → 3 = 4
- Just 2 = 2
- Just 3 = 3
- Just 1 = 1

Answer: 6

Example 2 (with negative):
       -10
       /  \
      9   20
         /  \
        15   7

Best path: 15 → 20 → 7 = 42
(We ignore -10 and 9 because they reduce the sum!)

-----------------------------------
Key Insight:

For each node, we calculate TWO things:

1. MAX_GAIN: Maximum contribution this node can give to its PARENT
   - Can only go ONE direction (either left OR right, not both)
   - = node.val + max(left_gain, right_gain, 0)

2. LOCAL_MAX: Maximum path sum THROUGH this node (potential answer)
   - Can use BOTH children (since path doesn't continue up)
   - = node.val + left_gain + right_gain

We track global maximum while returning only max_gain upward.

-----------------------------------
Constraints:
• The number of nodes in the tree is in the range [1, 3 * 10^4]
• -1000 <= Node.val <= 1000

-----------------------------------
Examples:

Example 1:
Input: root = [1,2,3]
Output: 6
Explanation: The path 2 → 1 → 3 has maximum sum 6.

Example 2:
Input: root = [-10,9,20,null,null,15,7]
Output: 42
Explanation: The path 15 → 20 → 7 has maximum sum 42.
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
# DFS Solution
# ⭐ BEST FOR INTERVIEW - Only approach, must know this pattern
# Time: O(n), Space: O(h)
# -------------------------------
class Solution:
    """
    Key idea:
    - At each node, calculate max path THROUGH this node (could be answer)
    - Return max gain this node can contribute to parent (one direction only)
    - Use global variable to track overall maximum
    """
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float('-inf')  # Global maximum
        self.dfs(root)
        return self.max_sum
    
    def dfs(self, node) -> int:
        """
        Returns: Maximum gain this node can contribute to its parent
        Side effect: Updates self.max_sum with local maximum
        """
        if not node:
            return 0
        
        # Get max gain from left and right children
        # Use max(0, ...) to ignore negative contributions!
        left_gain = max(0, self.dfs(node.left))
        right_gain = max(0, self.dfs(node.right))
        
        # Calculate local maximum (path through this node)
        # This path uses BOTH left and right
        local_max = node.val + left_gain + right_gain
        
        # Update global maximum
        self.max_sum = max(self.max_sum, local_max)
        
        # Return max gain to parent (can only use ONE child)
        # Path to parent is: node + (left OR right), not both!
        return node.val + max(left_gain, right_gain)


# -------------------------------
# Alternative: Without Global Variable
# -------------------------------
class SolutionClean:
    """
    Same logic but using list to avoid global variable.
    """
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        result = [float('-inf')]
        
        def dfs(node):
            if not node:
                return 0
            
            left_gain = max(0, dfs(node.left))
            right_gain = max(0, dfs(node.right))
            
            # Path through this node
            result[0] = max(result[0], node.val + left_gain + right_gain)
            
            # Contribution to parent
            return node.val + max(left_gain, right_gain)
        
        dfs(root)
        return result[0]


# -------------------------------
# Dry Run Example
# -------------------------------
"""
Tree:
       -10
       /  \
      9   20
         /  \
        15   7

DFS traversal (post-order style):

1. dfs(9):
   - left_gain = 0, right_gain = 0
   - local_max = 9 + 0 + 0 = 9
   - max_sum = max(-inf, 9) = 9
   - return 9 + 0 = 9

2. dfs(15):
   - left_gain = 0, right_gain = 0
   - local_max = 15 + 0 + 0 = 15
   - max_sum = max(9, 15) = 15
   - return 15 + 0 = 15

3. dfs(7):
   - left_gain = 0, right_gain = 0
   - local_max = 7 + 0 + 0 = 7
   - max_sum = max(15, 7) = 15 (no change)
   - return 7 + 0 = 7

4. dfs(20):
   - left_gain = max(0, 15) = 15
   - right_gain = max(0, 7) = 7
   - local_max = 20 + 15 + 7 = 42  ← New maximum!
   - max_sum = max(15, 42) = 42
   - return 20 + max(15, 7) = 35

5. dfs(-10):
   - left_gain = max(0, 9) = 9
   - right_gain = max(0, 35) = 35
   - local_max = -10 + 9 + 35 = 34
   - max_sum = max(42, 34) = 42 (no change)
   - return -10 + max(9, 35) = 25

Final answer: 42 ✓
"""


# -------------------------------
# Why max(0, gain)?
# -------------------------------
"""
Critical! If a subtree has negative sum, we IGNORE it!

Example:
      5
     /
   -10
   /
  20

Path 20 → -10 → 5 = 15
vs
Path 5 alone = 5? No!
Path 5 (ignoring left) = 5
But what about 20?

Actually, we check local_max at each node:
- At node 20: local_max = 20 (best so far)
- At node -10: left_gain = max(0, 20) = 20
              local_max = -10 + 20 = 10 (worse than 20)
- At node 5: left_gain = max(0, -10+20) = max(0, 10) = 10
            local_max = 5 + 10 = 15

Hmm, but best path is 20 → -10 → 5 = 15? No wait:
20 alone = 20 is actually the best!

The algorithm catches this because we compute local_max at EVERY node.
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
    
    # Test Case 1
    root1 = array_to_tree([1, 2, 3])
    print("Test 1:", sol.maxPathSum(root1))  # Expected: 6
    
    # Test Case 2
    root2 = array_to_tree([-10, 9, 20, None, None, 15, 7])
    print("Test 2:", sol.maxPathSum(root2))  # Expected: 42
    
    # Test Case 3: Single negative node
    root3 = TreeNode(-3)
    print("Test 3:", sol.maxPathSum(root3))  # Expected: -3
    
    # Test Case 4: All negative
    root4 = array_to_tree([-1, -2, -3])
    print("Test 4:", sol.maxPathSum(root4))  # Expected: -1
