"""
LeetCode Problem: 2. Add Two Numbers
Method: Linked List Traversal + Carry
Category: Linked List / Math
Time Complexity: O(max(m, n)) 
    → m = length of l1, n = length of l2
Space Complexity: O(max(m, n)) 
    → for the output linked list
Link: https://leetcode.com/problems/add-two-numbers/
"""

# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode()  # dummy node for result list
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            total = val1 + val2 + carry

            carry = total // 10
            current.next = ListNode(total % 10)  # new digit node
            current = current.next

            if l1: 
                l1 = l1.next
            if l2: 
                l2 = l2.next

        return dummy.next
