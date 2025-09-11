"""LeetCode Problem 33: Search in Rotated Sorted Array
Method: Linear Search (Basic) / Binary Search (Optimal)
Category: Arrays, Binary Search
Time Complexity: O(n) for linear search, O(log n) for binary search
Space Complexity: O(1)
Link: https://leetcode.com/problems/search-in-rotated-sorted-array/

-----------------------------------
Constraints:
• 1 <= nums.length <= 5000
• -10^4 <= nums[i] <= 10^4
• All values of nums are unique
• nums is guaranteed to be rotated at some pivot
• -10^4 <= target <= 10^4

-----------------------------------
Examples:

Example 1:
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
Explanation: Target 0 is found at index 4

Example 2:
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1
Explanation: Target 3 is not in nums

Example 3:
Input: nums = [1], target = 0
Output: -1
Explanation: Single element array, target not found
"""

class Solution:
    def search(self, nums: List[int], target: int) -> int:
       for i in range(len(nums)):
            if target not in nums:
                return -1
            if target == nums[i]:
                return i




class Solution:
    def search(self, nums: List[int], target: int) -> int:
        for i in range(len(nums)):
            if target == nums[i]:
                return i   
        return -1
            
