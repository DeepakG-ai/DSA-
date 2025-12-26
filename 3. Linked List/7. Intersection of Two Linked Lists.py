"""LeetCode Problem 160: Intersection of Two Linked Lists
Method: Two Pointer / Hash Set
Category: Linked List, Two Pointers
Time Complexity: O(n + m)
Space Complexity: O(1)
Link: https://leetcode.com/problems/intersection-of-two-linked-lists/

-----------------------------------
Problem Description:
Given the heads of two singly linked lists headA and headB, return the node 
at which the two lists intersect. If the two linked lists have no intersection, 
return null.

Note: The intersection is by reference (same node in memory), NOT by value.

-----------------------------------
Visual Explanation:

List A:      a1 → a2 ↘
                      c1 → c2 → c3 → NULL
List B: b1 → b2 → b3 ↗

Intersection node: c1 (both lists point to the SAME c1 node)

NOT intersection (same value but different nodes):
    A: 1 → 2 → 3
    B: 4 → 2 → 5
    Here 2s are DIFFERENT nodes, just same value. No intersection!

-----------------------------------
Key Insight (Two Pointer Magic):

If we traverse A then B, and B then A, we travel the same distance!

    Path 1: a1 → a2 → c1 → c2 → c3 → b1 → b2 → b3 → c1 (total: lenA + lenB)
    Path 2: b1 → b2 → b3 → c1 → c2 → c3 → a1 → a2 → c1 (total: lenB + lenA)

They meet at intersection point c1!

Why it works:
    lenA + lenB = lenB + lenA (same total distance)
    They "sync up" at the intersection!

-----------------------------------
Constraints:
• The number of nodes of listA is in the m
• The number of nodes of listB is in the n
• 1 <= m, n <= 3 * 10^4
• 1 <= Node.val <= 10^5
• 0 <= skipA < m
• 0 <= skipB < n
• intersectVal is 0 if there is no intersection

-----------------------------------
Examples:

Example 1:
Input: listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], intersect at 8
Output: Reference of node with value 8
Explanation: The two lists intersect at node with value 8.

Example 2:
Input: listA = [1,9,1,2,4], listB = [3,2,4], intersect at 2
Output: Reference of node with value 2

Example 3:
Input: listA = [2,6,4], listB = [1,5], no intersection
Output: null
"""

from typing import Optional

# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# -------------------------------
# 1. Brute Force: Hash Set
# Time Complexity: O(n + m)
# Space Complexity: O(n) - store all nodes of list A
# -------------------------------
class SolutionHashSet:
    """
    Store all nodes of list A in a set.
    Traverse list B and check if any node exists in set.
    First match is the intersection!
    """
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        # Store all nodes of list A
        nodes_in_A = set()
        current = headA
        while current:
            nodes_in_A.add(current)  # Add node reference, not value!
            current = current.next
        
        # Check list B for any matching node
        current = headB
        while current:
            if current in nodes_in_A:
                return current  # Found intersection!
            current = current.next
        
        return None  # No intersection


# -------------------------------
# 2. Optimal: Two Pointers
# Time Complexity: O(n + m)
# Space Complexity: O(1) - no extra space!
# -------------------------------
class Solution:
    """
    Two Pointer Technique:
    - Pointer A starts at headA
    - Pointer B starts at headB
    - When A reaches end, redirect to headB
    - When B reaches end, redirect to headA
    - They will meet at intersection (or both become NULL)
    
    Why? Both pointers travel the same total distance: lenA + lenB
    """
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        if not headA or not headB:
            return None
        
        pointerA = headA
        pointerB = headB
        
        # Traverse until they meet or both become NULL
        while pointerA != pointerB:
            # Move A: if end reached, switch to headB
            pointerA = pointerA.next if pointerA else headB
            
            # Move B: if end reached, switch to headA
            pointerB = pointerB.next if pointerB else headA
        
        # Either they meet at intersection, or both are NULL
        return pointerA


# -------------------------------
# Dry Run: Two Pointers
# -------------------------------
"""
List A: 4 → 1 → 8 → 4 → 5 → NULL  (length = 5)
              ↗
List B: 5 → 6 → 1  (length = 6, shares 8 → 4 → 5)

pA path: 4 → 1 → 8 → 4 → 5 → NULL → 5 → 6 → 1 → 8 ← MEET!
pB path: 5 → 6 → 1 → 8 → 4 → 5 → NULL → 4 → 1 → 8 ← MEET!

Step-by-step:
    Step 0: pA=4, pB=5
    Step 1: pA=1, pB=6
    Step 2: pA=8, pB=1
    Step 3: pA=4, pB=8
    Step 4: pA=5, pB=4
    Step 5: pA=NULL, pB=5  → pA switches to headB
    Step 6: pA=5, pB=NULL → pB switches to headA
    Step 7: pA=6, pB=4
    Step 8: pA=1, pB=1
    Step 9: pA=8, pB=8  ← MATCH! Return node 8
"""


# -------------------------------
# Dry Run: No Intersection
# -------------------------------
"""
List A: 1 → 2 → 3 → NULL  (length = 3)
List B: 4 → 5 → NULL      (length = 2)

pA path: 1 → 2 → 3 → NULL → 4 → 5 → NULL
pB path: 4 → 5 → NULL → 1 → 2 → 3 → NULL

After traversing lenA + lenB for both:
    pA = NULL
    pB = NULL
    pA == pB (both NULL) → Return NULL (no intersection)
"""


# -------------------------------
# Why This Works Mathematically
# -------------------------------
"""
Let:
    a = length of list A before intersection
    b = length of list B before intersection
    c = length of common part (after intersection)

Total lengths:
    lenA = a + c
    lenB = b + c

Pointer A travels: a + c + b = a + b + c
Pointer B travels: b + c + a = a + b + c

Same distance! They sync up at intersection.

If no intersection (c = 0):
    Both travel a + b, both end at NULL
    NULL == NULL → return NULL
"""


# -------------------------------
# Helper Functions for Testing
# -------------------------------
def create_intersecting_lists(valsA, valsB, intersect_vals):
    """Create two lists that intersect at a common node."""
    if not intersect_vals:
        # No intersection
        headA = create_list(valsA)
        headB = create_list(valsB)
        return headA, headB, None
    
    # Create intersection part
    intersect = create_list(intersect_vals)
    
    # Create list A prefix
    headA = create_list(valsA)
    if headA:
        curr = headA
        while curr.next:
            curr = curr.next
        curr.next = intersect
    else:
        headA = intersect
    
    # Create list B prefix
    headB = create_list(valsB)
    if headB:
        curr = headB
        while curr.next:
            curr = curr.next
        curr.next = intersect
    else:
        headB = intersect
    
    return headA, headB, intersect

def create_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


if __name__ == "__main__":
    sol = Solution()
    
    # Test Case 1: Lists intersect at node with value 8
    headA, headB, intersect = create_intersecting_lists([4, 1], [5, 6, 1], [8, 4, 5])
    result = sol.getIntersectionNode(headA, headB)
    print("Test 1:", result.val if result else None)
    # Expected: 8
    
    # Test Case 2: No intersection
    headA2 = create_list([2, 6, 4])
    headB2 = create_list([1, 5])
    result2 = sol.getIntersectionNode(headA2, headB2)
    print("Test 2:", result2.val if result2 else None)
    # Expected: None
    
    # Test Case 3: Same starting point
    headA3, headB3, intersect3 = create_intersecting_lists([], [], [1, 2, 3])
    result3 = sol.getIntersectionNode(headA3, headB3)
    print("Test 3:", result3.val if result3 else None)
    # Expected: 1
