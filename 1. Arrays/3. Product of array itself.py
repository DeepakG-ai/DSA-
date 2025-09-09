"""
LeetCode Problem: 238. Product of Array Except Self
Method: Prefix and Suffix Multiplication (no division)
Category: Arrays
Time Complexity: O(n)
Space Complexity: O(1) excluding the output array
Link: https://leetcode.com/problems/product-of-array-except-self/
"""

def product_except_self(nums):
    n = len(nums)
    answer = [1] * n

    # Step 1: Prefix product pass
    left_product = 1
    for i in range(n):
        answer[i] = left_product  # product of all elements before i
        left_product *= nums[i]   # update running prefix

    # Step 2: Suffix product pass
    right_product = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= right_product  # multiply by product of all elements after i
        right_product *= nums[i]    # update running suffix

    return answer

# Example usage
nums = [1, 2, 3, 4]
print(product_except_self(nums))  # Output: [24, 12, 8, 6]
