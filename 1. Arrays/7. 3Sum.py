"""LeetCode Problem 15: 3Sum
Method: Two Pointers + Sorting
Category: Arrays, Two Pointers
Time Complexity: O(n^2) - nested loop with two pointers
Space Complexity: O(1) - excluding the space required for output
Link: https://leetcode.com/problems/3sum/

-----------------------------------
Constraints:
• 3 <= nums.length <= 3000
• -10^5 <= nums[i] <= 10^5
• Solutions must not contain duplicate triplets

-----------------------------------
Examples:

Example 1:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[2] + nums[4] = (-1) + 1 + (-1) = -1
nums[1] + nums[2] + nums[3] = 0 + 1 + 2 = 3

Example 2:
Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:
Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.
"""

from typing import List

#Optimal Solution 

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()  # Step 1: Sort array
        res = []
        n = len(nums)

        for i in range(n):
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]

                if total < 0:
                    left += 1

                elif total > 0:
                    right -= 1

                else :
                    res.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1

                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1

        return res


#Brute force solution 
#O(n^3) --> time complexity
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result = set()   # use set to avoid duplicates
        n = len(nums)
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                        result.add(triplet)  # set ensures uniqueness
        
        return [list(triplet) for triplet in result]


