"""
LeetCode Problem: Trapping Rain Water
Problem Link: https://leetcode.com/problems/trapping-rain-water/

This file contains:
1. Brute Force Approach
2. Optimal Two Pointer Approach

Category: Arrays, Two Pointers
Algorithm Explanation (Two Pointer Approach):
    - Initialize two pointers l and r at the start and end of the array.
    - Keep track of left_max and right_max (the tallest bars seen so far from left and right).
    - At each step:
    - Compare height[l] and height[r].
    - Move the pointer with the smaller height inward.
    - If the current height is smaller than the max seen from that side, water can be trapped: total += left_max - height[l] or right_max - height[r].
    - Otherwise, update the max for that side.

Continue until l < r.
Example 1:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
"""

from typing import List

# -------------------------------
# 1. Brute Force Approach
# Time Complexity: O(n^2)
# Space Complexity: O(1)
# -------------------------------
class SolutionBruteForce:
    def trap(self, height: List[int]) -> int:
        total = 0
        n = len(height)
        for i in range(1, n-1):
            left_max = max(height[:i])      # maximum height to the left of i
            right_max = max(height[i+1:])   # maximum height to the right of i
            water_level = min(left_max, right_max)
            if water_level > height[i]:
                total += water_level - height[i]
        return total

# -------------------------------
# 2. Optimal Two Pointer Approach
# Time Complexity: O(n)
# Space Complexity: O(1)
# -------------------------------
class SolutionOptimal:
    def trap(self, height: List[int]) -> int:
        left_max = right_max = total = 0
        l, r = 0, len(height) - 1

        while l < r:
            if height[l] <= height[r]:
                if left_max > height[l]:
                    total += left_max - height[l]
                else:
                    left_max = height[l]
                l += 1
            else:
                if right_max >= height[r]:
                    total += right_max - height[r]
                else:
                    right_max = height[r]
                r -= 1

        return total

# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    heights = [0,1,0,2,1,0,1,3,2,1,2,1]

    bf = SolutionBruteForce()
    print("Brute Force Total Water Trapped:", bf.trap(heights))

    opt = SolutionOptimal()
    print("Optimal Total Water Trapped:", opt.trap(heights))
