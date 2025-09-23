"""
LeetCode 8: String to Integer (atoi)
https://leetcode.com/problems/string-to-integer-atoi/

Problem: 
Implement the atoi (string to integer) function that converts a string to a 32-bit signed integer.

Method: Linear Scan
- Time Complexity: O(n) where n is length of string
- Space Complexity: O(1) as we only use a few variables

Constraints:
- 0 <= s.length <= 200
- s consists of English letters (lower-case and upper-case), digits (0-9), ' ', '+', '-', and '.'
- Output must be within 32-bit signed integer range [-2^31, 2^31 - 1]

Examples:
1. Input: s = "42"
   Output: 42
   Explanation: The number "42" is directly converted to integer 42

2. Input: s = "   -42"
   Output: -42
   Explanation: Leading whitespace is removed, "-" indicates negative number

3. Input: s = "4193 with words"
   Output: 4193
   Explanation: Conversion stops at first non-digit after numbers

Algorithm:
1. Initialize:
   - Set up int32 boundaries (INT_MAX, INT_MIN)
   - Initialize result, sign, and index variables

2. Skip Whitespace:
   - Move index past any leading spaces

3. Handle Sign:
   - Check for '+' or '-'
   - Set sign accordingly and move index

4. Process Digits:
   - Convert each digit while checking for overflow
   - Stop at first non-digit character
   - Apply mathematical formula: result = result * 10 + digit

5. Return:
   - Apply sign to result
   - Ensure result is within int32 bounds
"""

# LeetCode 8: String to Integer (atoi)
# Time: O(n), Space: O(1)

class Solution:
    def myAtoi(self, s: str) -> int:
        # Define int32 boundaries
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        i = 0
        n = len(s)
        result= 0
        sign = 1

        # 1. Skip leading spaces
        while i < n and s[i] == " ":
            i += 1

        # 2. Handle sign
        if i < n and (s[i] == "+" or s[i] == "-"):
            sign = -1 if s[i] == "-" else 1
            i += 1

        # 3. Convert digits
        while i < n and s[i].isdigit():
            digit = int(s[i])

            # Check overflow before adding digit
            if result > (INT_MAX - digit) // 10:
                return INT_MAX if sign == 1 else INT_MIN

            result = result * 10 + digit
            i += 1

        return result * sign

"""
Example Usage:
sol = Solution()
print(sol.myAtoi("42"))          # Output: 42
print(sol.myAtoi("   -42"))      # Output: -42
print(sol.myAtoi("4193 words"))  # Output: 4193
print(sol.myAtoi("words 987"))   # Output: 0
print(sol.myAtoi("-91283472332"))# Output: -2147483648 (INT_MIN clamping)
"""
