"""LeetCode Problem 53: Maximum Subarray
Method: Kadane's Algorithm
Category: Arrays, Dynamic Programming
Time Complexity: O(n)
Space Complexity: O(1)
Link: https://leetcode.com/problems/maximum-subarray/

-----------------------------------
Constraints:
• 1 <= nums.length <= 10^5
• -10^4 <= nums[i] <= 10^4
• Follow up: If you have figured out the O(n) solution, try coding another 
  solution using the divide and conquer approach, which is more subtle

-----------------------------------
Examples:

Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum = 6.

Example 2:
Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum = 1.

Example 3:
Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum = 23.
"""

class Solution(object):
    def maxSubArray(self,nums): #kadanes algorithm
        maxsub=nums[0]
        cursum=0

        for i in nums:
            if cursum<0: #when current sum is negative, reset it to 0
                cursum=0
            cursum+=i   # i is the element not index. adding every element to current sum
            maxsub=max(maxsub,cursum)
        return maxsub
    

    def maxSubArray_dp(self, nums):
        """
        Dynamic Programming Approach:
        dp[i] = max(dp[i-1] + nums[i], nums[i])
        where dp[i] is the maximum subarray sum ending at index i.
        """
        dp = [0] * len(nums)
        dp[0] = nums[0]
        max_sum = dp[0]

        for i in range(1, len(nums)):
            dp[i] = max(dp[i-1] + nums[i], nums[i])
            max_sum = max(max_sum, dp[i])

        return max_sum

    """for i in range(len(nums)):
            if cursum<0:
                cursum=0
            cursum+=nums[i]
            maxsub=max(maxsub,cursum)
        return maxsub"""  # both are same
    
    # for understanding the loop
    """for i in nums:
            print(i) #output : 3,5,7,3
            
        for i in range(len(nums)):
            print(i,nums[i]) #output : 0 3,1 5,2 7,3 3 

        for i, val in enumerate(nums):
            print(i,val) #output : 0 3,1 5,2 7,3 3
        
    """