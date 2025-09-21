"""
LeetCode 20: Valid Parentheses
https://leetcode.com/problems/valid-parentheses/

Problem: Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', 
determine if the input string is valid. The string is valid if all open brackets are closed 
in the correct order.

Method: Stack-based Approach
- Time Complexity: O(n) where n is length of string
- Space Complexity: O(n) for stack in worst case

Constraints:
- 1 <= s.length <= 104
- s consists of parentheses only '()[]{}'
- Each opening bracket must have corresponding closing bracket
- Brackets must be closed in correct order

Examples:
1. Input: s = "()"
   Output: true
   Explanation: Simple pair of matching brackets

2. Input: s = "()[]{}"
   Output: true
   Explanation: Multiple pairs, each closed in correct order

3. Input: s = "(]"
   Output: false
   Explanation: Closing bracket doesn't match opening bracket

"""
"""

Algorithm Explanation:
-------------------
Stack-based approach to validate matching parentheses

Initialize:
- Create empty stack to store opening brackets

For each character in string:
1. If opening bracket ( { [ :
   - Push onto stack
   
2. If closing bracket ) } ] :
   - If stack is empty:
     * Return False (no matching opening bracket)
   - Pop top element from stack
   - If popped bracket doesn't match current closing bracket:
     * Return False (wrong order)
   - If matches:
     * Continue to next character

Final Check:
- If stack is empty:
  * Return True (all brackets matched)
- If stack not empty:
  * Return False (some opening brackets not closed)

Time: O(n) - single pass through string
Space: O(n) - stack can grow up to string length
"""


def isValid(s: str) -> bool:
    # Initialize empty stack and mapping of brackets
    stack = []
    mapping = {')':'(', '}':'{', ']':'['}

    # Process each character in string
    for ch in s:
        if ch in mapping:  # closing bracket
            top = stack.pop() if stack else '#'
            if mapping[ch] != top:
                return False
        else:  # opening bracket
            stack.append(ch)

    # Valid if all brackets are matched (stack is empty)
    return not stack

