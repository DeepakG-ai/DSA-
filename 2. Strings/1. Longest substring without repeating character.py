"""
LeetCode Problem 3: Longest Substring Without Repeating Characters
Method: Sliding Window (Optimal)
Category: Strings, Sliding Window, Hashing
Time Complexity (Optimal): O(n)
Space Complexity (Optimal): O(min(n, charset))  ~ O(n)
Link: https://leetcode.com/problems/longest-substring-without-repeating-characters/

-----------------------------------
Problem Description:
Given a string s, find the length of the longest substring 
without repeating characters.

-----------------------------------
Constraints:
• 0 <= s.length <= 5 * 10^4
• s consists of English letters, digits, symbols, and spaces.

-----------------------------------
Examples:

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Note that the answer must be a substring, "pwke" is a subsequence not a substring.
"""

# Brute Force Solution (Check all substrings)
class SolutionBruteForce:
    """Time Complexity: O(n^3)
    Space Complexity: O(min(n, charset)) - extra set for uniqueness check"""
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        longest = 0

        # Generate all substrings
        for i in range(n):
            for j in range(i, n):
                substring = s[i:j+1]
                # Check if substring has all unique characters
                if len(set(substring)) == len(substring):
                    longest = max(longest, j - i + 1)

        return longest


# Optimal Solution (Sliding Window)
class Solution:
    """Time Complexity: O(n)
    Space Complexity: O(min(n, charset))"""
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = 0
        sett = set()
        longest = 0

        for right in range(len(s)):
            # Shrink window until duplicate is removed
            while s[right] in sett:
                sett.remove(s[left])
                left += 1

            # Expand window
            sett.add(s[right])
            longest = max(longest, right - left + 1)

        return longest
