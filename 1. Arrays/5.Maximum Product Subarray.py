"""LeetCode Problem 152: Maximum Product Subarray
Method: Dynamic Programming
Category: Arrays, Dynamic Programming
Time Complexity: O(n)
Space Complexity: O(1)
Link: https://leetcode.com/problems/maximum-product-subarray/

-----------------------------------
Constraints:
• 1 <= nums.length <= 2 * 10^4
• -10 <= nums[i] <= 10
• The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer

-----------------------------------
Examples:

Example 1:
Input: nums = [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.

Example 2:
Input: nums = [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
"""

def maxProduct(nums):
    """
    Calculate the maximum product of any contiguous subarray.
    Key idea: Keep track of both max and min products because
    a negative number can turn min product into max product.
    """
    if not nums:
        return 0
        
    max_prod = nums[0]  # Global maximum product
    cur_max = nums[0]   # Maximum product ending at current position
    cur_min = nums[0]   # Minimum product ending at current position
    
    for i in range(1, len(nums)):
        n = nums[i]
        # When multiplying by a negative number, max becomes min and min becomes max
        if n < 0:
            cur_max, cur_min = cur_min, cur_max
            
        # Either start new subarray from current number or extend previous subarray
        cur_max = max(n, cur_max * n)
        cur_min = min(n, cur_min * n)
        
        # Update global maximum if current maximum is larger
        max_prod = max(max_prod, cur_max)
    
    return max_prod

def test_max_product():
    """Test cases for maximum product subarray"""
    
    # Test case 1: Basic case with positive and negative numbers
    nums1 = [2,3,-2,4]
    assert maxProduct(nums1) == 6, "Test case 1 failed"
    
    # Test case 2: Array with zero
    nums2 = [-2,0,-1]
    assert maxProduct(nums2) == 0, "Test case 2 failed"
    
    # Test case 3: All negative numbers
    nums3 = [-2,-3,-4]
    assert maxProduct(nums3) == 12, "Test case 3 failed"  # -3 * -4 = 12
    
    # Test case 4: Mix of positive, negative and zeros
    nums4 = [-2,3,-4,0,5,-2]
    assert maxProduct(nums4) == 24, "Test case 4 failed"  # -2 * 3 * -4 = 24
    
    # Test case 5: Single element array
    nums5 = [5]
    assert maxProduct(nums5) == 5, "Test case 5 failed"
    
    # Test case 6: Two negative numbers make positive
    nums6 = [-4,-3]
    assert maxProduct(nums6) == 12, "Test case 6 failed"
    
    # Test case 7: Complex case with alternating signs
    nums7 = [1,-2,3,-4,5,-6]
    assert maxProduct(nums7) == 120, "Test case 7 failed"  # 3 * -4 * 5 * -6 = 360
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_max_product()