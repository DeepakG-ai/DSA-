"""LeetCode Problem 19: Remove Nth Node From End of List
Method: Two Pointer Approach (One Pass)
Category: Linked List, Two Pointers
Time Complexity: O(n)
Space Complexity: O(1)
Link: https://leetcode.com/problems/remove-nth-node-from-end-of-list/

-----------------------------------
Problem Description:
Given the head of a linked list, remove the nth node from the END of the list
and return its head.

-----------------------------------
Visual Explanation:

Input: 1 → 2 → 3 → 4 → 5, n = 2
                   ↑
              Remove this (2nd from end)

Output: 1 → 2 → 3 → 5

-----------------------------------
The Key Insight:

How do we find "nth from end" in ONE PASS?

Trick: Create a GAP of n nodes between two pointers!

    1 → 2 → 3 → 4 → 5 → NULL
    ↑       ↑
   left   right  (gap = 2)

When right reaches NULL, left is at the node BEFORE the one to delete!

Step by step:
1. Move right pointer n steps ahead first
2. Then move both pointers together
3. When right hits NULL, left.next is the node to remove

-----------------------------------
Why Use Dummy Node?

Edge case: What if we need to remove the FIRST node?
    Input: 1 → 2 → 3, n = 3 (remove node 1)
    
Without dummy: left would need to be BEFORE head (impossible!)
With dummy:    dummy → 1 → 2 → 3
               ↑
              left can be here

-----------------------------------
Constraints:
• The number of nodes in the list is sz
• 1 <= sz <= 30
• 0 <= Node.val <= 100
• 1 <= n <= sz

-----------------------------------
Examples:

Example 1:
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
Explanation: Remove 4 (2nd from end)

Example 2:
Input: head = [1], n = 1
Output: []
Explanation: Remove the only node

Example 3:
Input: head = [1,2], n = 1
Output: [1]
Explanation: Remove 2 (last node)
"""

from typing import Optional

# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# -------------------------------
# 1. Brute Force Approach (Two Pass)
# Time Complexity: O(n) - two traversals
# Space Complexity: O(1)
# -------------------------------
class SolutionBruteForce:
    """
    Approach:
    Pass 1: Count total nodes (length)
    Pass 2: Go to (length - n)th node and remove next
    
    Example: [1,2,3,4,5], n=2
    Length = 5
    Position to stop = 5 - 2 = 3 (stop at node 3)
    Remove node 3's next (which is 4)
    """
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Pass 1: Count length
        length = 0
        current = head
        while current:
            length += 1
            current = current.next
        
        # Edge case: removing first node
        if length == n:
            return head.next
        
        # Pass 2: Go to (length - n)th node
        current = head
        for _ in range(length - n - 1):
            current = current.next
        
        # Remove the next node
        current.next = current.next.next
        
        return head


# -------------------------------
# 2. Optimal Solution (One Pass with Two Pointers)
# Time Complexity: O(n) - single traversal
# Space Complexity: O(1)
# -------------------------------
class Solution:
    """
    Two Pointer Technique:
    1. Create dummy node before head (handles edge cases)
    2. Move right pointer n steps ahead
    3. Move both pointers until right reaches NULL
    4. left.next is the node to remove
    
    Why this works:
    - Gap between left and right is always n
    - When right = NULL, left is exactly n+1 positions from end
    - So left.next is nth from end
    """
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Create dummy node pointing to head
        dummy = ListNode(0, head)
        left = dummy
        right = head
        
        # Step 1: Move right pointer n steps ahead
        while n > 0 and right:
            right = right.next
            n -= 1
        
        # Step 2: Move both pointers until right reaches NULL
        while right:
            left = left.next
            right = right.next
        
        # Step 3: Remove the nth node
        left.next = left.next.next
        
        return dummy.next


# -------------------------------
# Dry Run Example
# -------------------------------
"""
Input: 1 → 2 → 3 → 4 → 5, n = 2

Initial:
    dummy → 1 → 2 → 3 → 4 → 5 → NULL
    ↑       ↑
   left   right

After moving right n=2 steps:
    dummy → 1 → 2 → 3 → 4 → 5 → NULL
    ↑               ↑
   left           right

Move both until right = NULL:
    dummy → 1 → 2 → 3 → 4 → 5 → NULL
                    ↑           ↑
                   left       right

Now left.next = 4 (the node to remove!)
left.next = left.next.next → skip node 4

Result: 1 → 2 → 3 → 5
"""


# -------------------------------
# Edge Cases
# -------------------------------
"""
1. Remove first node: [1,2,3], n=3
   dummy → 1 → 2 → 3 → NULL
           ↑           ↑
          left       right (after n steps)
   Result: [2,3]

2. Single node: [1], n=1
   dummy → 1 → NULL
   ↑           ↑
  left       right
   Result: []

3. Remove last node: [1,2], n=1
   dummy → 1 → 2 → NULL
           ↑       ↑
          left   right
   Result: [1]
"""


# -------------------------------
# Helper Functions for Testing
# -------------------------------
def create_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

def list_to_array(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    sol = Solution()
    
    # Test Case 1
    head1 = create_list([1, 2, 3, 4, 5])
    result1 = sol.removeNthFromEnd(head1, 2)
    print("Test 1:", list_to_array(result1))  # Expected: [1, 2, 3, 5]
    
    # Test Case 2: Single node
    head2 = create_list([1])
    result2 = sol.removeNthFromEnd(head2, 1)
    print("Test 2:", list_to_array(result2))  # Expected: []
    
    # Test Case 3: Remove first node
    head3 = create_list([1, 2])
    result3 = sol.removeNthFromEnd(head3, 2)
    print("Test 3:", list_to_array(result3))  # Expected: [2]
