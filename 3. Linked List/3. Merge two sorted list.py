"""LeetCode Problem 21: Merge Two Sorted Lists
Method: Iterative / Recursive
Category: Linked List
Time Complexity: O(n + m)
Space Complexity: O(1) iterative, O(n + m) recursive
Link: https://leetcode.com/problems/merge-two-sorted-lists/

-----------------------------------
Problem Description:
You are given the heads of two sorted linked lists list1 and list2.
Merge the two lists into one sorted list by splicing together the nodes 
of the first two lists. Return the head of the merged linked list.

-----------------------------------
Visual Explanation:

Input:
    list1: 1 → 2 → 4 → NULL
    list2: 1 → 3 → 4 → NULL

Process (compare heads, pick smaller):
    Compare 1 vs 1 → pick 1 (from list1)
    Compare 2 vs 1 → pick 1 (from list2)
    Compare 2 vs 3 → pick 2 (from list1)
    Compare 4 vs 3 → pick 3 (from list2)
    Compare 4 vs 4 → pick 4 (from list1)
    Remaining: 4 → attach rest of list2

Output: 1 → 1 → 2 → 3 → 4 → 4 → NULL

-----------------------------------
Why Use Dummy Node?

Without dummy:
    - Need special logic for setting head
    - More edge case handling

With dummy:
    dummy → (result will be built here)
    Return dummy.next as the merged head

-----------------------------------
Constraints:
• The number of nodes in both lists is in range [0, 50]
• -100 <= Node.val <= 100
• Both list1 and list2 are sorted in non-decreasing order

-----------------------------------
Examples:

Example 1:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:
Input: list1 = [], list2 = []
Output: []

Example 3:
Input: list1 = [], list2 = [0]
Output: [0]
"""

from typing import Optional

# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# -------------------------------
# 1. Iterative Approach (Recommended)
# Time Complexity: O(n + m)
# Space Complexity: O(1)
# -------------------------------
class Solution:
    """
    Use dummy node and current pointer.
    Compare values, attach smaller node to result.
    When one list is exhausted, attach remaining of other list.
    """
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # Dummy node to simplify edge cases
        dummy = ListNode(0)
        current = dummy
        
        # Compare and merge while both lists have nodes
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        
        # Attach remaining nodes (one list might still have nodes)
        current.next = list1 if list1 else list2
        
        return dummy.next


# -------------------------------
# 2. Recursive Approach
# Time Complexity: O(n + m)
# Space Complexity: O(n + m) - call stack
# -------------------------------
class SolutionRecursive:
    """
    Recursive intuition:
    - If either list is empty, return the other
    - Compare heads, pick smaller
    - Recursively merge the rest
    - Return the smaller node with its next pointing to merged result
    """
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # Base cases
        if not list1:
            return list2
        if not list2:
            return list1
        
        # Pick smaller head and recurse
        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2


# -------------------------------
# Dry Run: Iterative
# -------------------------------
"""
Input:
    list1: 1 → 2 → 4
    list2: 1 → 3 → 4

dummy → NULL
current = dummy

Step 1: 1 vs 1 → pick list1's 1
    dummy → 1
    list1 = 2 → 4
    current = node(1)

Step 2: 2 vs 1 → pick list2's 1
    dummy → 1 → 1
    list2 = 3 → 4
    current = node(1)

Step 3: 2 vs 3 → pick list1's 2
    dummy → 1 → 1 → 2
    list1 = 4
    current = node(2)

Step 4: 4 vs 3 → pick list2's 3
    dummy → 1 → 1 → 2 → 3
    list2 = 4
    current = node(3)

Step 5: 4 vs 4 → pick list1's 4
    dummy → 1 → 1 → 2 → 3 → 4
    list1 = NULL
    current = node(4)

list1 is NULL, attach rest of list2:
    dummy → 1 → 1 → 2 → 3 → 4 → 4

Return dummy.next
Output: 1 → 1 → 2 → 3 → 4 → 4
"""


# -------------------------------
# Dry Run: Recursive
# -------------------------------
"""
Input: list1 = [1,2,4], list2 = [1,3,4]

merge(1→2→4, 1→3→4)
    1 <= 1, so: 1.next = merge(2→4, 1→3→4)
    
    merge(2→4, 1→3→4)
        2 > 1, so: 1.next = merge(2→4, 3→4)
        
        merge(2→4, 3→4)
            2 <= 3, so: 2.next = merge(4, 3→4)
            
            merge(4, 3→4)
                4 > 3, so: 3.next = merge(4, 4)
                
                merge(4, 4)
                    4 <= 4, so: 4.next = merge(NULL, 4)
                    
                    merge(NULL, 4) → return 4
                    
                    4.next = 4, return 4
                
                3.next = 4→4, return 3
            
            2.next = 3→4→4, return 2
        
        1.next = 2→3→4→4, return 1
    
    1.next = 1→2→3→4→4, return 1

Result: 1 → 1 → 2 → 3 → 4 → 4
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
    
    # Test Case 1: Normal case
    l1 = create_list([1, 2, 4])
    l2 = create_list([1, 3, 4])
    result1 = sol.mergeTwoLists(l1, l2)
    print("Test 1 (Iterative):", list_to_array(result1))
    # Expected: [1, 1, 2, 3, 4, 4]
    
    # Test Case 2: Both empty
    l3 = create_list([])
    l4 = create_list([])
    result2 = sol.mergeTwoLists(l3, l4)
    print("Test 2 (Empty lists):", list_to_array(result2))
    # Expected: []
    
    # Test Case 3: One empty (Recursive)
    l5 = create_list([])
    l6 = create_list([0])
    result3 = sol_rec.mergeTwoLists(l5, l6)
    print("Test 3 (Recursive):", list_to_array(result3))
    # Expected: [0]
    
    # Test Case 4: Different lengths
    l7 = create_list([1, 3, 5, 7])
    l8 = create_list([2, 4])
    result4 = sol.mergeTwoLists(l7, l8)
    print("Test 4 (Different lengths):", list_to_array(result4))
    # Expected: [1, 2, 3, 4, 5, 7]
