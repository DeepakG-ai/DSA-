"""LeetCode Problem 206: Reverse Linked List
Method: Iterative / Recursive
Category: Linked List
Time Complexity: O(n)
Space Complexity: O(1) iterative, O(n) recursive
Link: https://leetcode.com/problems/reverse-linked-list/

-----------------------------------
Problem Description:
Given the head of a singly linked list, reverse the list, and return the reversed list.

-----------------------------------
Visual Explanation:

Input:  1 → 2 → 3 → 4 → 5 → NULL
Output: 5 → 4 → 3 → 2 → 1 → NULL

The Trick: Reverse the direction of arrows!
    Before: 1 → 2
    After:  1 ← 2

-----------------------------------
Iterative Approach (Main Idea):

Use 3 pointers: prev, curr, temp

Step 1: Save next node (temp = curr.next)
Step 2: Reverse the arrow (curr.next = prev)
Step 3: Move prev forward (prev = curr)
Step 4: Move curr forward (curr = temp)

Visual:
    NULL   1 → 2 → 3 → NULL
     ↑     ↑
    prev  curr

    NULL ← 1   2 → 3 → NULL   (reversed arrow)
           ↑   ↑
          prev curr

    NULL ← 1 ← 2   3 → NULL
               ↑   ↑
              prev curr

    NULL ← 1 ← 2 ← 3   NULL
                   ↑    ↑
                  prev curr (curr is NULL, stop!)

Return prev (new head)

-----------------------------------
Constraints:
• The number of nodes in the list is in range [0, 5000]
• -5000 <= Node.val <= 5000

-----------------------------------
Examples:

Example 1:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:
Input: head = [1,2]
Output: [2,1]

Example 3:
Input: head = []
Output: []
"""

from typing import Optional

# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# -------------------------------
# 1. Iterative Approach (Recommended)
# Time Complexity: O(n)
# Space Complexity: O(1) - only 3 pointers
# -------------------------------
class Solution:
    """
    Three pointer technique:
    - prev: tracks the reversed portion
    - curr: current node being processed
    - temp: saves next node before we break the link
    """
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        
        while curr:
            temp = curr.next      # Save next node
            curr.next = prev      # Reverse the arrow
            prev = curr           # Move prev forward
            curr = temp           # Move curr forward
        
        return prev  # prev is now the new head


# -------------------------------
# 2. Recursive Approach
# Time Complexity: O(n)
# Space Complexity: O(n) - call stack
# -------------------------------
class SolutionRecursive:
    """
    Recursive intuition:
    1. Recurse to the end of the list
    2. On the way back, reverse each link
    
    Example: 1 → 2 → 3 → NULL
    
    Call stack going down:
        reverse(1) → reverse(2) → reverse(3) [base case, return 3]
    
    Coming back up:
        At node 2: 2.next.next = 2  →  3.next = 2  →  3 → 2
        At node 1: 1.next.next = 1  →  2.next = 1  →  2 → 1
    """
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Base case: empty list or single node
        if not head or not head.next:
            return head
        
        # Recurse to end, get new head
        new_head = self.reverseList(head.next)
        
        # Reverse the link
        head.next.next = head  # Point next node back to current
        head.next = None       # Break forward link
        
        return new_head


# -------------------------------
# Dry Run: Iterative
# -------------------------------
"""
Input: 1 → 2 → 3 → NULL

Initial: prev=NULL, curr=1

Step 1:
    temp = 2
    curr.next = NULL  (1 → NULL)
    prev = 1
    curr = 2
    
    State: NULL ← 1   2 → 3 → NULL

Step 2:
    temp = 3
    curr.next = 1  (2 → 1)
    prev = 2
    curr = 3
    
    State: NULL ← 1 ← 2   3 → NULL

Step 3:
    temp = NULL
    curr.next = 2  (3 → 2)
    prev = 3
    curr = NULL  ← STOP!
    
    State: NULL ← 1 ← 2 ← 3

Return prev (3) as new head
Output: 3 → 2 → 1 → NULL
"""


# -------------------------------
# Helper Functions
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
    sol_rec = SolutionRecursive()
    
    # Test Case 1: Regular list
    head1 = create_list([1, 2, 3, 4, 5])
    result1 = sol.reverseList(head1)
    print("Test 1 (Iterative):", list_to_array(result1))
    # Expected: [5, 4, 3, 2, 1]
    
    # Test Case 2: Two nodes (Recursive)
    head2 = create_list([1, 2])
    result2 = sol_rec.reverseList(head2)
    print("Test 2 (Recursive):", list_to_array(result2))
    # Expected: [2, 1]
    
    # Test Case 3: Empty list
    head3 = create_list([])
    result3 = sol.reverseList(head3)
    print("Test 3 (Empty):", list_to_array(result3))
    # Expected: []
