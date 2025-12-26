"""LeetCode Problem 23: Merge K Sorted Lists
Method: Divide and Conquer / Min Heap
Category: Linked List, Heap, Divide and Conquer
Time Complexity: O(N log k) where N = total nodes, k = number of lists
Space Complexity: O(k) for heap
Link: https://leetcode.com/problems/merge-k-sorted-lists/

-----------------------------------
Problem Description:
You are given an array of k linked-lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

-----------------------------------
Visual Explanation:

Input: 3 sorted lists
    List 1: 1 → 4 → 5
    List 2: 1 → 3 → 4
    List 3: 2 → 6

Output: 1 → 1 → 2 → 3 → 4 → 4 → 5 → 6

-----------------------------------
Three Approaches:

1. BRUTE FORCE: Merge lists one by one
   Time: O(kN) where k = lists, N = total nodes
   
2. MIN HEAP (Priority Queue):
   - Put first node of each list in heap
   - Pop smallest, add its next to heap
   - Time: O(N log k)
   
3. DIVIDE AND CONQUER:
   - Pair up lists and merge each pair
   - Repeat until one list remains
   - Time: O(N log k)

-----------------------------------
Divide and Conquer Visualization:

Round 1: Merge pairs
    [list1, list2, list3, list4, list5]
         ↓     ↓         ↓
    [merged12, merged34, list5]

Round 2: Merge pairs again
    [merged12, merged34, list5]
         ↓         ↓
    [merged1234, list5]

Round 3: Final merge
    [merged1234, list5]
           ↓
    [final_merged]

-----------------------------------
Constraints:
• k == lists.length
• 0 <= k <= 10^4
• 0 <= lists[i].length <= 500
• -10^4 <= lists[i][j] <= 10^4
• lists[i] is sorted in ascending order
• The sum of lists[i].length will not exceed 10^4

-----------------------------------
Examples:

Example 1:
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]

Example 2:
Input: lists = []
Output: []

Example 3:
Input: lists = [[]]
Output: []
"""

from typing import List, Optional
import heapq

# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    # Required for heap comparison when values are equal
    def __lt__(self, other):
        return self.val < other.val


# -------------------------------
# 1. Brute Force: Merge One by One
# Time Complexity: O(kN) - k merges, each up to N nodes
# Space Complexity: O(1)
# -------------------------------
class SolutionBruteForce:
    """
    Approach:
    - Start with first list
    - Merge with second, then third, and so on
    
    Problem: If first list is huge, we traverse it k times!
    """
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        
        result = lists[0]
        for i in range(1, len(lists)):
            result = self.mergeTwoLists(result, lists[i])
        
        return result
    
    def mergeTwoLists(self, l1, l2):
        dummy = ListNode(0)
        current = dummy
        
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        
        current.next = l1 if l1 else l2
        return dummy.next


# -------------------------------
# 2. Optimal: Min Heap (Priority Queue)
# Time Complexity: O(N log k) - N insertions, each log k
# Space Complexity: O(k) - heap stores k nodes
# -------------------------------
class SolutionHeap:
    """
    Min Heap Approach:
    1. Push first node of each list into min heap
    2. Pop smallest node, add to result
    3. Push next node of popped node to heap
    4. Repeat until heap is empty
    
    Why O(N log k)?
    - Each of N nodes is pushed/popped once
    - Heap operations are O(log k) where k = number of lists
    """
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        
        # Min heap: (value, index, node)
        # Index is tie-breaker when values are equal
        heap = []
        
        # Step 1: Add first node of each list to heap
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, (node.val, i, node))
        
        dummy = ListNode(0)
        current = dummy
        
        # Step 2: Process heap
        while heap:
            val, idx, node = heapq.heappop(heap)
            current.next = node
            current = current.next
            
            # Step 3: Add next node to heap
            if node.next:
                heapq.heappush(heap, (node.next.val, idx, node.next))
        
        return dummy.next


# -------------------------------
# 3. Optimal: Divide and Conquer
# Time Complexity: O(N log k)
# Space Complexity: O(log k) for recursion stack
# -------------------------------
class Solution:
    """
    Divide and Conquer:
    - Pair up k lists and merge each pair
    - After first round: k/2 lists
    - After second round: k/4 lists
    - Continue until 1 list remains
    
    Why O(N log k)?
    - log k rounds of merging
    - Each round processes all N nodes
    """
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        
        # Keep merging pairs until one list remains
        while len(lists) > 1:
            merged_lists = []
            
            # Merge pairs: (0,1), (2,3), (4,5), ...
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i + 1] if i + 1 < len(lists) else None
                merged_lists.append(self.mergeTwoLists(l1, l2))
            
            lists = merged_lists
        
        return lists[0]
    
    def mergeTwoLists(self, l1, l2):
        """Merge two sorted linked lists - you already know this!"""
        dummy = ListNode(0)
        current = dummy
        
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        
        current.next = l1 if l1 else l2
        return dummy.next


# -------------------------------
# Dry Run: Divide and Conquer
# -------------------------------
"""
Input: [list1, list2, list3, list4, list5]
       [1→4]  [1→3]  [2→6]  [3→5]  [7→8]

Round 1 (merge pairs):
    merge(list1, list2) → 1→1→3→4
    merge(list3, list4) → 2→3→5→6
    list5 stays alone   → 7→8
    
    Result: [[1→1→3→4], [2→3→5→6], [7→8]]

Round 2:
    merge(merged12, merged34) → 1→1→2→3→3→4→5→6
    list5 stays alone         → 7→8
    
    Result: [[1→1→2→3→3→4→5→6], [7→8]]

Round 3:
    merge → 1→1→2→3→3→4→5→6→7→8
    
    Final Result!
"""


# -------------------------------
# Complexity Comparison
# -------------------------------
"""
| Approach           | Time      | Space    | Notes                    |
|--------------------|-----------|----------|--------------------------|
| Brute Force        | O(kN)     | O(1)     | Merge one by one         |
| Min Heap           | O(N log k)| O(k)     | Best for streaming data  |
| Divide & Conquer   | O(N log k)| O(log k) | Best overall, in-place   |

Where:
- N = total number of nodes across all lists
- k = number of linked lists
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
    lists = [
        create_list([1, 4, 5]),
        create_list([1, 3, 4]),
        create_list([2, 6])
    ]
    result = sol.mergeKLists(lists)
    print("Test 1:", list_to_array(result))
    # Expected: [1, 1, 2, 3, 4, 4, 5, 6]
    
    # Test Case 2: Empty input
    result2 = sol.mergeKLists([])
    print("Test 2:", list_to_array(result2))
    # Expected: []
    
    # Test Case 3: Single list
    lists3 = [create_list([1, 2, 3])]
    result3 = sol.mergeKLists(lists3)
    print("Test 3:", list_to_array(result3))
    # Expected: [1, 2, 3]
