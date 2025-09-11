"""LeetCode Problem 18: 4Sum
Method: Two Pointers + Sorting (Similar to 3Sum but with one more loop)
Category: Arrays, Two Pointers
Time Complexity: O(n^3) - nested loops with two pointers
Space Complexity: O(1) - excluding the space required for output
Link: https://leetcode.com/problems/4sum/

-----------------------------------
Constraints:
• 1 <= nums.length <= 200
• -10^9 <= nums[i] <= 10^9
• -10^9 <= target <= 10^9
• Solutions must not contain duplicate quadruplets

-----------------------------------
Examples:

Example 1:
Input: nums = [1,0,-1,0,-2,2], target = 0
Output: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
Explanation: All unique quadruplets that sum to target

Example 2:
Input: nums = [2,2,2,2,2], target = 8
Output: [[2,2,2,2]]
Explanation: The only possible quadruplet that sums to 8

Example 3:
Input: nums = [1,2,3,4], target = 10
Output: [[1,2,3,4]]
Explanation: Sum of all elements equals target
"""

class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        result = []
        n=len(nums)

        #fixed i and j pointers
        for i in range(n):
            if i>0 and nums[i] == nums[i-1]:  
                continue

            for j in range(i+1,n):
                if j!=i+1 and nums[j]==nums[j-1]:
                    continue

                k = j+1
                l = n-1

                while k<l:
                    total = nums[i]+nums[j]+nums[k]+nums[l]

                    if total == target:
                        result.append([nums[i],nums[j],nums[k],nums[l]])
                        k+=1
                        l-=1

                        while k<l and nums[k]==nums[k-1]:
                            k+=1
                        while k<l and nums[l]==nums[l+1]:
                            l-=1
                    elif total < target:
                        k+=1
                    else:
                        l-=1
        return result

# Brute Force Solution using 4 nested loops
class SolutionBruteForce:
    """
    Brute Force approach using 4 nested loops
    Time Complexity: O(n^4) - four nested loops
    Space Complexity: O(1) - excluding the space required for output
    """
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        n = len(nums)
        result = set()  # Using set to automatically handle duplicates
        
        # Four nested loops to try all possible combinations
        for i in range(n-3):
            for j in range(i+1, n-2):
                for k in range(j+1, n-1):
                    for l in range(k+1, n):
                        # Check if the current combination sums to target
                        curr_sum = nums[i] + nums[j] + nums[k] + nums[l]
                        if curr_sum == target:
                            # Sort the quadruplet to handle duplicates when adding to set
                            quad = tuple(sorted([nums[i], nums[j], nums[k], nums[l]]))
                            result.add(quad)
        
        # Convert tuples back to lists for the final result
        return [list(quad) for quad in result]

# Example usage:
# solution = Solution()  # Optimal solution using two pointers
# solution_bf = SolutionBruteForce()  # Brute force solution
# nums = [1,0,-1,0,-2,2]
# target = 0
# print("Optimal solution:", solution.fourSum(nums, target))
# print("Brute force solution:", solution_bf.fourSum(nums, target))

                while k<l:
                    total = nums[i]+nums[j]+nums[k]+nums[l]

                    if total == target:
                        result.append([nums[i],nums[j],nums[k],nums[l]])
                        k+=1
                        l-=1

                        while k<l and nums[k]==nums[k-1]:
                            k+=1
                        while k<l and nums[l]==nums[l+1]:
                            l-=1
                        
                    elif total<target:
                        k+=1
                    else:
                        l-=1
        return result

            