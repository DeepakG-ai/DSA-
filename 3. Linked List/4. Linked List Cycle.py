"""LeetCode Problem 141: Linked List Cycle
Method: Floyd's Tortoise and Hare (Two Pointers)
Category: Linked List, Two Pointers
Time Complexity: O(n)
Space Complexity: O(1)
Link: https://leetcode.com/problems/linked-list-cycle/

-----------------------------------
Problem Description:
Given head, the head of a linked list, determine if the linked list has a cycle in it.
A cycle exists if some node in the list can be reached again by continuously following 
the next pointer. Return True if there is a cycle, otherwise return False.

-----------------------------------
Visual Explanation:

Normal Linked List (No Cycle):
    1 → 2 → 3 → 4 → 5 → NULL
    (Ends at NULL, no cycle)

Linked List WITH Cycle:
    1 → 2 → 3 → 4 → 5
            ↑       ↓
            └───────┘
    (5 points back to 3, infinite loop!)

-----------------------------------
Why Two Pointers Work (Tortoise & Hare Analogy):

Imagine two runners on a circular track:
- 🐢 Slow runner (tortoise): moves 1 step at a time
- 🐇 Fast runner (hare): moves 2 steps at a time

If the track is circular:
    Fast runner will eventually LAP the slow runner → They MEET!
    
If the track is straight (no cycle):
    Fast runner reaches the END first → No meeting

Mathematically:
- Fast gains 1 step on slow each iteration
- If cycle exists, gap eventually becomes 0 → collision

-----------------------------------
Constraints:
• The number of nodes in the list is in the range [0, 10^4]
• -10^5 <= Node.val <= 10^5
• pos is -1 or a valid index in the linked-list

-----------------------------------
Examples:

Example 1:
Input: head = [3,2,0,-4], pos = 1  (tail connects to node index 1)
Output: True
Explanation: There is a cycle where tail connects to the second node.

Example 2:
Input: head = [1,2], pos = 0  (tail connects to node index 0)
Output: True
Explanation: There is a cycle where tail connects to the first node.

Example 3:
Input: head = [1], pos = -1  (no cycle)
Output: False
Explanation: There is no cycle in the linked list.
"""

from typing import Optional

# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# -------------------------------
# 1. Brute Force Approach (HashSet)
# Time Complexity: O(n)
# Space Complexity: O(n) - stores all visited nodes
# -------------------------------
class SolutionBruteForce:
    """
    Approach: Store every visited node in a set.
    If we see the same node again → Cycle found!
    If we reach NULL → No cycle.
    
    Drawback: Uses O(n) extra space.
    """
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited = set()
        current = head
        
        while current:
            if current in visited:
                return True  # Cycle detected! Same node visited twice
            visited.add(current)
            current = current.next
        
        return False  # Reached NULL, no cycle


# -------------------------------
# 2. Optimal Solution (Floyd's Cycle Detection)
# Time Complexity: O(n)
# Space Complexity: O(1) - no extra space!
# -------------------------------
class Solution:
    """
    Floyd's Tortoise and Hare Algorithm:
    - Slow pointer moves 1 step
    - Fast pointer moves 2 steps
    - If they meet → Cycle exists
    - If fast reaches NULL → No cycle
    
    Why it works:
    - If cycle exists, fast will eventually catch up to slow
    - Fast gains 1 step per iteration, so gap closes to 0
    """
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head
        
        while fast and fast.next:
            slow = slow.next        # Move 1 step
            fast = fast.next.next   # Move 2 steps
            
            if slow == fast:
                return True  # They met! Cycle exists
        
        return False  # Fast reached NULL, no cycle


# -------------------------------
# Dry Run Example
# -------------------------------
"""
Input: 1 → 2 → 3 → 4 (4 points back to 2)

Step 0: slow=1, fast=1 (start)
Step 1: slow=2, fast=3
Step 2: slow=3, fast=2 (fast wrapped around!)
Step 3: slow=4, fast=4 → MATCH! Return True

If no cycle (1 → 2 → 3 → NULL):
Step 0: slow=1, fast=1
Step 1: slow=2, fast=3
Step 2: fast.next = NULL → Exit loop → Return False
"""


# -------------------------------
# Test Helper Functions
# -------------------------------
def create_cycle_list(values, pos):
    """Create a linked list with a cycle at position 'pos'"""
    if not values:
        return None
    
    nodes = [ListNode(val) for val in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    if pos >= 0 and pos < len(nodes):
        nodes[-1].next = nodes[pos]  # Create cycle
    
    return nodes[0]


if __name__ == "__main__":
    # Test Case 1: Has cycle
    head1 = create_cycle_list([3, 2, 0, -4], pos=1)
    sol = Solution()
    print("Test 1 (Has Cycle):", sol.hasCycle(head1))  # Expected: True
    
    # Test Case 2: No cycle
    head2 = create_cycle_list([1, 2, 3, 4, 5], pos=-1)
    print("Test 2 (No Cycle):", sol.hasCycle(head2))  # Expected: False
    
    # Test Case 3: Single node, no cycle
    head3 = ListNode(1)
    print("Test 3 (Single Node):", sol.hasCycle(head3))  # Expected: False
