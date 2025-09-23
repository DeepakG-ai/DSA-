"""
LeetCode 76: Minimum Window Substring
https://leetcode.com/problems/minimum-window-substring/

Problem:
Given two strings s and t, return the minimum window substring of s that contains 
all characters of t in their original frequency. Return empty string if no such 
window exists.

Method: Sliding Window with HashMap
- Time Complexity: O(|S| + |T|) where |S| and |T| are lengths of strings
- Space Complexity: O(|T|) for storing character frequencies

Constraints:
- 1 <= s.length, t.length <= 105
- s and t consist of uppercase and lowercase English letters
- Answer is unique (if it exists)
- All characters in t must be included with their frequencies

Examples:
1. Input: s = "ADOBECODEBANC", t = "ABC"
   Output: "BANC"
   Explanation: Minimum substring containing all characters of "ABC"

2. Input: s = "a", t = "a"
   Output: "a"
   Explanation: Single character match

3. Input: s = "a", t = "aa"
   Output: ""
   Explanation: Cannot match frequency requirement

Algorithm:
1. Initialize:
   - Create frequency map for string t (need)
   - Create window map for current window (window)
   - Track count of matched characters (have)
   - Track minimum window length and indices

2. Expand Window:
   - Iterate through s with right pointer
   - Add characters to window
   - Update have count when frequency matches

3. Shrink Window:
   - When all characters are matched (have == need_count)
   - Try to minimize window by moving left pointer
   - Update minimum length and indices if smaller window found

4. Return Result:
   - Extract minimum window using stored indices
   - Return empty string if no valid window found
"""

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t:
            return ""

        # Step 1: Build frequency map of t
        need = {}
        for c in t:
            need[c] = need.get(c, 0) + 1

        window = {}
        have, need_count = 0, len(need)
        min_len, index = float("inf"), [-1, -1]

        l = 0
        #"ADOBECODEBANC"
        for i in range(len(s)):
            # Step 2: expand window
            if s[i] in need:
                window[s[i]] = window.get(s[i], 0) + 1
                if window[s[i]] == need[s[i]]:
                    have += 1

            #print(f"i={i}, s[i]={s[i]}, window={window}, have={have}")

            # Step 3: shrink window when valid
            while have == need_count:
                #print(f"  Shrinking: l={l}, window={window}, min_len={min_len}")

                if (i - l + 1) < min_len:
                    min_len = i - l + 1
                    index = [l, i]
                    #print(f"    Updated min_len={min_len}, index={index}")

                if s[l] in need:
                    window[s[l]] -= 1
                    if window[s[l]] < need[s[l]]:
                        have -= 1
                        #print(f"    Decreased have={have} because {s[l]} count < need")
                l += 1

        l, r = index
        return s[l:r+1] if min_len != float("inf") else ""

# Create object
sol = Solution()

# Test example
s = "ADOBECODEBANC"
t = "ABC"
result = sol.minWindow(s, t)
print("\nFinal Result:", result)


