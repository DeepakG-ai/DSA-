"""LeetCode Problem 297: Serialize and Deserialize Binary Tree
Method: BFS / DFS with String Encoding
Category: Trees, BFS, DFS, Design
Time Complexity: O(n)
Space Complexity: O(n)
Link: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/

Difficulty: HARD

-----------------------------------
Problem Description:
Design an algorithm to serialize and deserialize a binary tree. 
Serialization is converting a tree to a string.
Deserialization is reconstructing the tree from the string.

You must ensure the tree can be reconstructed from the serialized string.

-----------------------------------
Visual Explanation:

Original Tree:
        1
       / \
      2   3
         / \
        4   5

Serialized (BFS): "1,2,3,null,null,4,5"
Serialized (DFS): "1,2,null,null,3,4,null,null,5,null,null"

Deserialized: Same tree back!

-----------------------------------
Key Insight:

We need to store NULL nodes to preserve tree structure!

Without nulls:
    [1, 2, 3, 4, 5] - Can't tell which nodes are children of which!

With nulls (BFS level-order):
    [1, 2, 3, null, null, 4, 5]
    Level 0: 1
    Level 1: 2, 3
    Level 2: null, null (children of 2), 4, 5 (children of 3)

-----------------------------------
Constraints:
• The number of nodes in the tree is in the range [0, 10^4]
• -1000 <= Node.val <= 1000
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
# BFS Approach (Level Order)
# ⭐ BEST FOR INTERVIEW - Easier to explain and debug than DFS
# Time: O(n), Space: O(n)
# -------------------------------
class Codec:
    """
    BFS Serialization:
    - Use level-order traversal
    - Store 'null' for missing nodes
    - Join with comma delimiter
    
    BFS Deserialization:
    - Split string by comma
    - Use queue to rebuild level by level
    """
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string."""
        if not root:
            return ""
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")
        
        # Remove trailing nulls for cleaner string
        while result and result[-1] == "null":
            result.pop()
        
        return ",".join(result)
    
    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree."""
        if not data:
            return None
        
        values = data.split(",")
        root = TreeNode(int(values[0]))
        queue = deque([root])
        i = 1
        
        while queue and i < len(values):
            node = queue.popleft()
            
            # Left child
            if i < len(values) and values[i] != "null":
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1
            
            # Right child
            if i < len(values) and values[i] != "null":
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1
        
        return root


# -------------------------------
# DFS Approach (Preorder)
# Time: O(n), Space: O(n)
# -------------------------------
class CodecDFS:
    """
    DFS Serialization (Preorder: Root → Left → Right):
    - Process root, then recursively process left, then right
    - Use 'null' for missing nodes
    
    DFS Deserialization:
    - Use iterator/index to consume values in order
    - Recursively build left subtree, then right
    """
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes using preorder DFS."""
        result = []
        
        def dfs(node):
            if not node:
                result.append("null")
                return
            result.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        
        dfs(root)
        return ",".join(result)
    
    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes using preorder DFS."""
        if not data:
            return None
        
        values = iter(data.split(","))
        
        def dfs():
            val = next(values)
            if val == "null":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node
        
        return dfs()


# -------------------------------
# Dry Run: BFS Serialize
# -------------------------------
"""
Tree:
        1
       / \
      2   3
         / \
        4   5

Queue processing:
    Process 1 → result = ["1"], add 2, 3 to queue
    Process 2 → result = ["1","2"], add null, null
    Process 3 → result = ["1","2","3"], add 4, 5
    Process null → result = ["1","2","3","null"]
    Process null → result = ["1","2","3","null","null"]
    Process 4 → result = ["1","2","3","null","null","4"]
    Process 5 → result = ["1","2","3","null","null","4","5"]

Final: "1,2,3,null,null,4,5"
"""


# -------------------------------
# Dry Run: DFS Serialize
# -------------------------------
"""
Tree:
        1
       / \
      2   3
         / \
        4   5

Preorder traversal:
    dfs(1) → "1"
        dfs(2) → "2"
            dfs(null) → "null"
            dfs(null) → "null"
        dfs(3) → "3"
            dfs(4) → "4"
                dfs(null) → "null"
                dfs(null) → "null"
            dfs(5) → "5"
                dfs(null) → "null"
                dfs(null) → "null"

Final: "1,2,null,null,3,4,null,null,5,null,null"
"""


# -------------------------------
# Helper: Print Tree
# -------------------------------
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
    # Build original tree
    #        1
    #       / \
    #      2   3
    #         / \
    #        4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(5)
    
    print("Original Tree:")
    print_tree(root)
    
    # Test BFS Codec
    codec_bfs = Codec()
    serialized_bfs = codec_bfs.serialize(root)
    print(f"\nBFS Serialized: {serialized_bfs}")
    
    deserialized_bfs = codec_bfs.deserialize(serialized_bfs)
    print("\nBFS Deserialized Tree:")
    print_tree(deserialized_bfs)
    
    # Test DFS Codec
    codec_dfs = CodecDFS()
    serialized_dfs = codec_dfs.serialize(root)
    print(f"\nDFS Serialized: {serialized_dfs}")
    
    deserialized_dfs = codec_dfs.deserialize(serialized_dfs)
    print("\nDFS Deserialized Tree:")
    print_tree(deserialized_dfs)
    
    # Test empty tree
    empty_serialized = codec_bfs.serialize(None)
    print(f"\nEmpty tree serialized: '{empty_serialized}'")
    empty_deserialized = codec_bfs.deserialize("")
    print(f"Empty tree deserialized: {empty_deserialized}")
