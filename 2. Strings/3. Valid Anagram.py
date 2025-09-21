"""
LeetCode 242: Valid Anagram
https://leetcode.com/problems/valid-anagram/

Problem: Given two strings s and t, return true if t is an anagram of s, and false otherwise.
An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, 
typically using all the original letters exactly once.

Method: 
1. Using HashMap (Dictionary)
   - Time Complexity: O(n)
   - Space Complexity: O(k) where k is the number of unique characters
2. Using Counter (Built-in)
   - Time Complexity: O(n)
   - Space Complexity: O(k)

Constraints:
- 1 <= s.length, t.length <= 5 * 10^4
- s and t consist of lowercase English letters
- Both strings must be of equal length to be anagrams

Examples:
1. Input: s = "anagram", t = "nagaram"
   Output: true
   Explanation: Both strings have same characters with same frequencies

2. Input: s = "rat", t = "car"
   Output: false
   Explanation: Different characters in both strings

3. Input: s = "ab", t = "a"
   Output: false
   Explanation: Different lengths, can't be anagrams
"""

# Solution using HashMap
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s)!= len(t):
            return False

        count = {}

        for i in s:
            count[i]=count.get(i,0)+1

        for i in t:
            if i not in count or count[i]==0:
                return False
            count[i]-=1
        return True

# Solution using Counter (more concise)
from collections import Counter 
def isAnagram (self,s,t):
    if len(s)!=len(t):
        return False
    return Counter(s)==Counter(t)

"""
Example Usage:
s1, t1 = "anagram", "nagaram"
solution = Solution()
print(solution.isAnagram(s1, t1))  # Output: True

s2, t2 = "rat", "car"
print(solution.isAnagram(s2, t2))  # Output: False
"""