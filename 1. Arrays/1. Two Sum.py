"""
LeetCode Problem: 1. Two Sum
Method: Hash Map
Category: Arrays
Time Complexity: O(n)
Space Complexity: O(n)
Link: https://leetcode.com/problems/two-sum/
"""
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return -1
    
print(TwoSum([2, 3, 7, 9], 7))


"""
# Time complexity - O(n^2)
def TwoSum(arr,target):
        for i in range(0,len(arr)):
            for j in range(i+1,len(arr)):
                sum=arr[i]+arr[j]
                if sum==target:
                    return i,j
        return -1      
                  
    print(TwoSum([2, 3, 7, 9], 7))           
"""

