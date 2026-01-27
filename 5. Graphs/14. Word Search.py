"""
Word Search (LeetCode 79)
https://leetcode.com/problems/word-search/

===========================================
PROBLEM
===========================================
Given an m x n grid of characters and a string word.
Return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells,
where adjacent cells are horizontally or vertically neighboring.
The same letter cell may not be used more than once.

===========================================
KEY INSIGHT (Backtracking)
===========================================

1. Try each cell as starting point
2. DFS with backtracking:
   - If current char matches, mark as visited
   - Explore 4 directions
   - If path doesn't work, UNMARK (backtrack!)
3. Return True if complete word found

Why Backtracking?
    - We need to explore ALL possible paths
    - If one path fails, we UNDO and try another
    - Same cell can be used in different paths (but not same path)

===========================================
ALGORITHM
===========================================

1. For each cell (r, c):
    - If board[r][c] == word[0]:
        - Start DFS from (r, c) with index 0

2. DFS(r, c, index):
    - Base case: index == len(word) -> Found! Return True
    - Bounds check: Out of bounds -> Return False
    - Char mismatch: board[r][c] != word[index] -> Return False
    - Already visited: Return False
    
    - Mark cell as visited (temp change)
    - Explore 4 directions with index + 1
    - BACKTRACK: Unmark cell
    - Return result

===========================================
"""

from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        if not board or not board[0]:
            return False
        
        rows, cols = len(board), len(board[0])
        
        def dfs(r, c, index):
            # Base case: Found complete word!
            if index == len(word):
                return True
            
            # Bounds check + Char match + Already visited
            if (r < 0 or r >= rows or 
                c < 0 or c >= cols or 
                board[r][c] != word[index]):
                return False
            
            # Mark as visited (temporarily change the cell)
            temp = board[r][c]
            board[r][c] = '#'  # Mark visited
            
            # Explore 4 directions
            found = (dfs(r + 1, c, index + 1) or  # Down
                     dfs(r - 1, c, index + 1) or  # Up
                     dfs(r, c + 1, index + 1) or  # Right
                     dfs(r, c - 1, index + 1))    # Left
            
            # BACKTRACK: Restore the cell
            board[r][c] = temp
            
            return found
        
        # Try each cell as starting point
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == word[0]:  # Optimization: Only start if first char matches
                    if dfs(r, c, 0):
                        return True
        
        return False


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    sol = Solution()
    
    # TEST 1: LeetCode Example 1 - ABCCED
    print("=" * 50)
    print("TEST 1: Word 'ABCCED'")
    print("=" * 50)
    
    board1 = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    word1 = "ABCCED"
    
    result = sol.exist([row[:] for row in board1], word1)
    print(f"Board: {board1}")
    print(f"Word: '{word1}'")
    print(f"Result: {result}")
    assert result == True
    print("PASSED!\n")
    
    
    # TEST 2: LeetCode Example 2 - SEE
    print("=" * 50)
    print("TEST 2: Word 'SEE'")
    print("=" * 50)
    
    board2 = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    word2 = "SEE"
    
    result = sol.exist([row[:] for row in board2], word2)
    print(f"Word: '{word2}'")
    print(f"Result: {result}")
    assert result == True
    print("PASSED!\n")
    
    
    # TEST 3: LeetCode Example 3 - ABCB (False - can't reuse)
    print("=" * 50)
    print("TEST 3: Word 'ABCB' (Can't reuse cell)")
    print("=" * 50)
    
    board3 = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    word3 = "ABCB"
    
    result = sol.exist([row[:] for row in board3], word3)
    print(f"Word: '{word3}'")
    print(f"Result: {result}")
    assert result == False
    print("PASSED!\n")
    
    
    # TEST 4: Single cell match
    print("=" * 50)
    print("TEST 4: Single Cell")
    print("=" * 50)
    
    board4 = [['A']]
    word4 = "A"
    
    result = sol.exist(board4, word4)
    print(f"Word: '{word4}'")
    print(f"Result: {result}")
    assert result == True
    print("PASSED!\n")
    
    
    # TEST 5: Word not found
    print("=" * 50)
    print("TEST 5: Word Not Found")
    print("=" * 50)
    
    board5 = [
        ['A', 'B'],
        ['C', 'D']
    ]
    word5 = "XYZ"
    
    result = sol.exist(board5, word5)
    print(f"Word: '{word5}'")
    print(f"Result: {result}")
    assert result == False
    print("PASSED!\n")
    
    
    # TEST 6: Backtracking needed
    print("=" * 50)
    print("TEST 6: Backtracking Required")
    print("=" * 50)
    
    # Need to backtrack because first path fails
    board6 = [
        ['A', 'B', 'C'],
        ['D', 'E', 'F'],
        ['G', 'H', 'I']
    ]
    word6 = "ABEF"  # A(0,0) -> B(0,1) -> E(1,1) -> F(1,2)
    
    result = sol.exist([row[:] for row in board6], word6)
    print(f"Word: '{word6}'")
    print(f"Result: {result}")
    assert result == True
    print("PASSED!\n")
    
    
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
