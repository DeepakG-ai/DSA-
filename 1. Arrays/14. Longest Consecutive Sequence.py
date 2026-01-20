"""
Longest Consecutive Sequence (LeetCode 128)
https://leetcode.com/problems/longest-consecutive-sequence/

===========================================
PROBLEM
===========================================
Given an unsorted array of integers nums,
return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Example:
Input: nums = [100, 4, 200, 1, 3, 2]
Output: 4  (sequence: [1, 2, 3, 4])

===========================================
"""

# ============================================
# APPROACH 1: SORTING
# Time: O(n log n) - sorting
# Space: O(1) or O(n) depending on sort
# ============================================
def longestConsecutive_sorting(nums: list) -> int:
    """
    Sort the array, then count consecutive elements.
    """
    if not nums:
        return 0
    
    nums = sorted(set(nums))  # Remove duplicates and sort
    
    longest = 1
    current_length = 1
    
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1] + 1:
            # Consecutive
            current_length += 1
        else:
            # Not consecutive, reset
            longest = max(longest, current_length)
            current_length = 1
    
    return max(longest, current_length)


# ============================================
# APPROACH 2: HASHSET (OPTIMAL)
# Time: O(n) - each number visited at most twice
# Space: O(n) - for the set
# ============================================
def longestConsecutive(nums):
    # 1. Convert to set for O(1) lookups
    num_set = set(nums)
    max_len = 0

    for n in num_set:
        # 2. Only start counting if 'n' is the START of a sequence
        # (Check if n-1 exists. If it does, 'n' is not the start, so skip it)
        if (n - 1) not in num_set:
            length = 0
            while (n + length) in num_set:
                length += 1
            max_len = max(max_len, length)
            
    return max_len


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    
    # TEST 1: LeetCode Example 1
    nums1 = [100, 4, 200, 1, 3, 2]
    assert longestConsecutive_sorting(nums1) == 4
    assert longestConsecutive(nums1) == 4
    print("TEST 1 PASSED: [100,4,200,1,3,2] -> 4")
    
    # TEST 2: LeetCode Example 2
    nums2 = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
    assert longestConsecutive_sorting(nums2) == 9
    assert longestConsecutive(nums2) == 9
    print("TEST 2 PASSED: [0,3,7,2,5,8,4,6,0,1] -> 9")
    
    # TEST 3: Empty array
    nums3 = []
    assert longestConsecutive(nums3) == 0
    print("TEST 3 PASSED: [] -> 0")
    
    # TEST 4: Single element
    nums4 = [5]
    assert longestConsecutive(nums4) == 1
    print("TEST 4 PASSED: [5] -> 1")
    
    # TEST 5: All same
    nums5 = [1, 1, 1, 1]
    assert longestConsecutive(nums5) == 1
    print("TEST 5 PASSED: [1,1,1,1] -> 1")
    
    # TEST 6: Negative numbers
    nums6 = [-2, -1, 0, 1]
    assert longestConsecutive(nums6) == 4
    print("TEST 6 PASSED: [-2,-1,0,1] -> 4")
    
    print("\n" + "=" * 40)
    print("ALL 6 TESTS PASSED!")
    print("=" * 40)
