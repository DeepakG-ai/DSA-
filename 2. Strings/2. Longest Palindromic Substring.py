"""
LeetCode 5: Longest Palindromic Substring
https://leetcode.com/problems/longest-palindromic-substring/

Problem: Given a string s, return the longest palindromic substring in s.

Method: 
1. Optimal Solution - Expand Around Center
   - Time Complexity: O(n²)
   - Space Complexity: O(1)
2. Brute Force Solution - Check all substrings
   - Time Complexity: O(n³)
   - Space Complexity: O(1)

Constraints:
- 1 <= s.length <= 1000
- s consist of only digits and English letters
- s contains at least one character

Examples:
1. Input: s = "babad"
   Output: "bab"
   Explanation: "aba" is also a valid answer

2. Input: s = "cbbd"
   Output: "bb"
   Explanation: Only palindrome of length 2

3. Input: s = "ac"
   Output: "a"
   Explanation: Single character is also a palindrome
"""

class Solution:
    def longestPalindrome(self, s: str) -> str:
        result =""
        longest = 0 

        for i in range(len(s)):
            left , right = i, i 
            # odd length 
            while left >=0 and right <len(s) and s[left]==s[right]:
                if (right - left + 1)>longest:
                    result = s[left:right+1] #s[0:1] so it will skip the last index 1. python slicing techinque
                    longest = right - left + 1
                left-=1
                right +=1

            left, right = i , i+1
            #even length 
            while left >=0 and right <len(s) and s[left]==s[right]:
                if (right - left + 1)>longest:
                    result = s[left:right+1]
                    longest = right - left + 1
                left-=1
                right +=1
            
        return result

# Brute Force Solution - Check all possible substrings
class SolutionBruteForce:
    def longestPalindrome(self, s: str) -> str:
        def isPalindrome(start: int, end: int) -> bool:
            while start < end:
                if s[start] != s[end]:
                    return False
                start += 1
                end -= 1
            return True
        
        n = len(s)
        longest = 1
        result = s[0]
        
        # Check all possible substrings
        for i in range(n):
            for j in range(i + 1, n):
                length = j - i + 1
                if length > longest and isPalindrome(i, j):
                    longest = length
                    result = s[i:j + 1]
        return result

"""
Example Usage:
s = "babad"
sol = Solution()
print(sol.longestPalindrome(s))  # Output: "bab"

s = "cbbd"
sol_brute = SolutionBruteForce()
print(sol_brute.longestPalindrome(s))  # Output: "bb"
"""