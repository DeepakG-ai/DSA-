"""LeetCode Problem 11: Container With Most Water
Method: Two Pointer Approach
Category: Arrays, Two Pointers
Time Complexity: O(n)
Space Complexity: O(1)
Link: https://leetcode.com/problems/container-with-most-water/

-----------------------------------
Problem Description:
Given n non-negative integers height[1...n] where each represents a point at coordinate (i, height[i]).
n vertical lines are drawn at points where ith line has endpoints at (i, height[i]) and (i, 0).
Find two lines that together with the x-axis forms a container that can hold the most water.

-----------------------------------
Example Calculation:
For height = [1,8,6,2,5,4,8,3,7]

Consider two lines:
- Left line at index 1 with height = 8
- Right line at index 8 with height = 7

width = right - left = 8 - 1 = 7 (number of positions between the lines)
height = min(8, 7) = 7 (limited by shorter line to avoid water spilling)
area = width * height = 7 * 7 = 49 square units

This turns out to be the maximum area possible with any two lines in this array.

-----------------------------------
Algorithm Explanation:
1. Use two pointers (left and right) starting from array ends
2. Width is calculated as (right - left) representing positions between lines
3. Height is minimum of the two lines (water can't be higher than shorter line)
4. Area = width * height
5. Move the pointer with shorter height inward (trying to find a taller line)
6. Keep track of maximum area seen so far

-----------------------------------
Constraints:
• n == height.length
• 2 <= n <= 10^5
• 0 <= height[i] <= 10^4

-----------------------------------
Examples:

Example 1:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. 
The maximum area of water that can be contained is 49.

Example 2:
Input: height = [1,1]
Output: 1
"""

from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height)-1
        max_area = 0
        while left<right:
            width=right-left
            area = width * min(height[left],height[right])
            max_area = max(max_area,area)

            if height[left]<height[right]:
                left+=1
            else:
                right-=1

        return max_area