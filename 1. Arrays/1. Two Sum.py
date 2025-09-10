"""LeetCode Problem 1: Two Sum
Method: Hash Map
Category: Arrays
Time Complexity: O(n)
Space Complexity: O(n)
Link: https://leetcode.com/problems/two-sum/

-----------------------------------
Constraints:
• 2 <= nums.length <= 10^4
• -10^9 <= nums[i] <= 10^9
• -10^9 <= target <= 10^9
• Only one valid answer exists
• The same element cannot be used twice

-----------------------------------
Examples:

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1]

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]
Explanation: Because nums[1] + nums[2] == 6

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 6
"""

def two_sum(nums, target):
    # Using hashmap to store number:index pairs
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []  # No solution found

# Test cases
def test_two_sum():
    # Test case 1
    nums1 = [2,7,11,15]
    assert two_sum(nums1, 9) == [0,1], "Test case 1 failed"
    
    # Test case 2
    nums2 = [3,2,4]
    assert two_sum(nums2, 6) == [1,2], "Test case 2 failed"
    
    # Test case 3
    nums3 = [3,3]
    assert two_sum(nums3, 6) == [0,1], "Test case 3 failed"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_two_sum()

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

