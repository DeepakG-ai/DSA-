"""LeetCode Problem 88: Merge Sorted Array
Method: Two-Pointer (Backwards)
Category: Arrays, Two Pointers
Time Complexity: O(m + n)
Space Complexity: O(1)  (in-place)
Link: https://leetcode.com/problems/merge-sorted-array/

-----------------------------------
Problem Description:
Given two sorted arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.
Note: nums1 has a size of m + n where the first m elements are the actual elements
and the last n positions are set to 0 to accommodate nums2.

-----------------------------------
Constraints:
• nums1.length == m + n
• nums2.length == n
• 0 <= m, n <= 200
• 1 <= m + n <= 200
• -10^9 <= nums1[i], nums2[j] <= 10^9

-----------------------------------
Examples:

Example 1:
Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
The result should be [1,2,2,3,5,6].

Example 2:
Input: nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
Explanation: We are merging nums2=[] into nums1=[1].
The result is still [1].

Example 3:
Input: nums1 = [0], m = 0, nums2 = [1], n = 1
Output: [1]
Explanation: We are merging nums2=[1] into nums1=[0].
The result is [1].
"""

from typing import List

# Brute Force Solution (Using Extra Space)
class SolutionBruteForce:
    """Time Complexity: O(m + n)
    Space Complexity: O(m + n) - Uses extra array nums3 to store result"""
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        # Create extra array to store merged result
        nums3 = []
        left = right = 0

        # Compare and merge elements from both arrays
        while left < m and right < n:
            if nums1[left] < nums2[right]:
                nums3.append(nums1[left])
                left += 1
            else:
                nums3.append(nums2[right])
                right += 1

        # Add remaining elements from nums1 if any
        while left < m:
            nums3.append(nums1[left])
            left += 1

        # Add remaining elements from nums2 if any
        while right < n:
            nums3.append(nums2[right])
            right += 1

        # Copy back merged result to nums1
        for i in range(m + n):
            nums1[i] = nums3[i]


# Optimal Solution (Without Extra Space)
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        # Pointers for nums1, nums2, and the end of nums1
        p1, p2, p = m - 1, n - 1, m + n - 1

        # Merge from the back
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]
                p1 -= 1
            else:
                nums1[p] = nums2[p2]
                p2 -= 1
            p -= 1

        # If nums2 still has elements, copy them
        while p2 >= 0:
            nums1[p] = nums2[p2]
            p2 -= 1
            p -= 1
