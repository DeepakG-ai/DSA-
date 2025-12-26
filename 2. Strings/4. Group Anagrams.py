"""LeetCode Problem 49: Group Anagrams
Method: Hash Map with Sorted Key / Character Count Key
Category: Strings, Hash Table, Sorting
Time Complexity: O(n * k log k) or O(n * k)
Space Complexity: O(n * k)
Link: https://leetcode.com/problems/group-anagrams/

-----------------------------------
Problem Description:
Given an array of strings strs, group the anagrams together. 
You can return the answer in any order.

An Anagram is a word formed by rearranging the letters of another word,
using all the original letters exactly once.

-----------------------------------
Visual Explanation:

Input: ["eat", "tea", "tan", "ate", "nat", "bat"]

Anagram groups:
    "eat", "tea", "ate"  → all have letters: a, e, t
    "tan", "nat"         → all have letters: a, n, t
    "bat"                → letters: a, b, t

Output: [["eat","tea","ate"], ["tan","nat"], ["bat"]]

-----------------------------------
Key Insight:

Two strings are anagrams if:
    sorted("eat") == sorted("tea")  →  "aet" == "aet"  ✓

Or if they have the same character frequency:
    "eat" → {a:1, e:1, t:1}
    "tea" → {a:1, e:1, t:1}  ✓

-----------------------------------
Approach 1: Sorted String as Key
    Group by sorted version of each string
    "eat" → key "aet"
    "tea" → key "aet"  (same key, same group!)

Approach 2: Character Count as Key
    Use tuple of character counts as key
    "eat" → (1,0,0,0,1,0,...,1,...) (a=1, e=1, t=1)
    Faster for long strings (no sorting needed)

-----------------------------------
Constraints:
• 1 <= strs.length <= 10^4
• 0 <= strs[i].length <= 100
• strs[i] consists of lowercase English letters

-----------------------------------
Examples:

Example 1:
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Example 2:
Input: strs = [""]
Output: [[""]]

Example 3:
Input: strs = ["a"]
Output: [["a"]]
"""

from typing import List
from collections import defaultdict


# -------------------------------
# 1. Sorted String as Key
# Time Complexity: O(n * k log k) - n strings, k = max length
# Space Complexity: O(n * k)
# -------------------------------
class SolutionSorted:
    """
    Use sorted string as hash map key.
    All anagrams will have the same sorted form.
    
    "eat" → sorted → "aet" (key)
    "tea" → sorted → "aet" (same key!)
    "ate" → sorted → "aet" (same key!)
    """
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Dictionary: sorted_string → list of anagrams
        anagram_groups = defaultdict(list)
        
        for s in strs:
            # Sort the string to create key
            key = ''.join(sorted(s))  # "eat" → "aet"
            anagram_groups[key].append(s)
        
        return list(anagram_groups.values())


# -------------------------------
# 2. Character Count as Key (Optimal)
# Time Complexity: O(n * k) - no sorting!
# Space Complexity: O(n * k)
# -------------------------------
class Solution:
    """
    Use character frequency tuple as key.
    Each position in tuple represents count of a-z.
    
    "eat" → (1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0)
            a=1                   e=1                         t=1
    
    Why tuple? Because lists can't be dictionary keys (unhashable),
    but tuples can!
    """
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Dictionary: char_count_tuple → list of anagrams
        anagram_groups = defaultdict(list)
        
        for s in strs:
            # Create character count array for a-z (26 letters)
            count = [0] * 26
            for char in s:
                count[ord(char) - ord('a')] += 1
            
            # Convert to tuple (hashable) as key
            key = tuple(count)
            anagram_groups[key].append(s)
        
        return list(anagram_groups.values())


# -------------------------------
# Dry Run Example
# -------------------------------
"""
Input: ["eat", "tea", "tan", "ate", "nat", "bat"]

Using Sorted Key:
    "eat" → sorted → "aet" → groups["aet"] = ["eat"]
    "tea" → sorted → "aet" → groups["aet"] = ["eat", "tea"]
    "tan" → sorted → "ant" → groups["ant"] = ["tan"]
    "ate" → sorted → "aet" → groups["aet"] = ["eat", "tea", "ate"]
    "nat" → sorted → "ant" → groups["ant"] = ["tan", "nat"]
    "bat" → sorted → "abt" → groups["abt"] = ["bat"]

Final groups:
    {
        "aet": ["eat", "tea", "ate"],
        "ant": ["tan", "nat"],
        "abt": ["bat"]
    }

Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
"""


# -------------------------------
# Why defaultdict?
# -------------------------------
"""
Without defaultdict:
    groups = {}
    if key not in groups:
        groups[key] = []
    groups[key].append(s)

With defaultdict:
    groups = defaultdict(list)
    groups[key].append(s)  # Automatically creates empty list if key doesn't exist!

Much cleaner and more Pythonic!
"""


# -------------------------------
# Complexity Comparison
# -------------------------------
"""
| Approach         | Time        | Space   | Best For              |
|------------------|-------------|---------|----------------------|
| Sorted Key       | O(n*k*logk) | O(n*k)  | Short strings        |
| Char Count Key   | O(n*k)      | O(n*k)  | Long strings         |

Where:
- n = number of strings
- k = maximum length of a string
"""


if __name__ == "__main__":
    sol = Solution()
    sol_sorted = SolutionSorted()
    
    # Test Case 1
    strs1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print("Test 1 (Char Count):", sol.groupAnagrams(strs1))
    # Expected: [["eat","tea","ate"], ["tan","nat"], ["bat"]]
    
    # Test Case 2: Empty string
    strs2 = [""]
    print("Test 2 (Empty):", sol.groupAnagrams(strs2))
    # Expected: [[""]]
    
    # Test Case 3: Single character
    strs3 = ["a"]
    print("Test 3 (Single):", sol.groupAnagrams(strs3))
    # Expected: [["a"]]
    
    # Test Case 4: Using sorted approach
    strs4 = ["abc", "bca", "cab", "xyz", "zyx"]
    print("Test 4 (Sorted):", sol_sorted.groupAnagrams(strs4))
    # Expected: [["abc","bca","cab"], ["xyz","zyx"]]
