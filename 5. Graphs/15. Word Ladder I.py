"""
Word Ladder I (LeetCode 127)
https://leetcode.com/problems/word-ladder/

===========================================
PROBLEM
===========================================
Given two words (beginWord and endWord), and a wordList.
Find the length of the shortest transformation sequence from beginWord to endWord.

Rules:
    - Only one letter can be changed at a time
    - Each transformed word must exist in the wordList

Return 0 if no such transformation sequence exists.

===========================================
KEY INSIGHT (BFS)
===========================================

This is a SHORTEST PATH problem!
    - Each word is a NODE
    - Edge exists between words that differ by 1 letter
    - Find shortest path from beginWord to endWord

BFS gives shortest path in unweighted graph!

===========================================
TWO APPROACHES FOR FINDING NEIGHBORS
===========================================

1. a-z Approach (Faster for large wordList):
    - For each position, try all 26 letters
    - Check if new word exists in wordSet (O(1) lookup)
    - Time per word: O(26 × M) = O(26M)

2. WordList Approach (Simpler, but slower):
    - Compare current word with every word in wordList
    - Check if they differ by exactly 1 letter
    - Time per word: O(N × M)

When N > 26, a-z approach is faster!

===========================================
ALGORITHM (BFS)
===========================================

1. Convert wordList to Set (for O(1) lookup)
2. Check if endWord exists in wordList
3. Initialize queue with (beginWord, level=1)
4. BFS:
    - Pop word from queue
    - If word == endWord: return level
    - For each neighbor (differs by 1 letter):
        - If in wordSet: add to queue, remove from wordSet
5. Return 0 if not found

===========================================
"""

from typing import List
from collections import deque


# ============================================
# APPROACH 1: a-z Traversal (Faster)
# ============================================
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # Convert to set for O(1) lookup
        wordSet = set(wordList)
        
        # Edge case: endWord not in wordList
        if endWord not in wordSet:
            return 0
        
        # BFS
        queue = deque([(beginWord, 1)])  # (word, level)
        visited = set([beginWord])
        
        while queue:
            word, level = queue.popleft()
            
            # Found!
            if word == endWord:
                return level
            
            # Try changing each position to a-z
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    if c == word[i]:
                        continue  # Skip same letter
                    
                    # Create new word
                    new_word = word[:i] + c + word[i+1:]
                    
                    # If valid and not visited
                    if new_word in wordSet and new_word not in visited:
                        visited.add(new_word)
                        queue.append((new_word, level + 1))
        
        return 0  # No path found


# ============================================
# APPROACH 2: WordList Traversal (Your approach!)
# ============================================
class Solution_WordList:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        wordSet = set(wordList)
        
        if endWord not in wordSet:
            return 0
        
        def differs_by_one(word1, word2):
            """Check if two words differ by exactly 1 letter."""
            if len(word1) != len(word2):
                return False
            diff = 0
            for c1, c2 in zip(word1, word2):
                if c1 != c2:
                    diff += 1
                    if diff > 1:
                        return False
            return diff == 1
        
        # BFS
        queue = deque([(beginWord, 1)])
        visited = set([beginWord])
        
        while queue:
            word, level = queue.popleft()
            
            if word == endWord:
                return level
            
            # Check all words in wordList
            for next_word in wordList:
                if next_word not in visited and differs_by_one(word, next_word):
                    visited.add(next_word)
                    queue.append((next_word, level + 1))
        
        return 0


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    sol = Solution()
    sol2 = Solution_WordList()
    
    # TEST 1: LeetCode Example 1
    print("=" * 50)
    print("TEST 1: hit -> cog")
    print("=" * 50)
    
    beginWord1 = "hit"
    endWord1 = "cog"
    wordList1 = ["hot", "dot", "dog", "lot", "log", "cog"]
    
    # Path: hit -> hot -> dot -> dog -> cog (length 5)
    result1 = sol.ladderLength(beginWord1, endWord1, wordList1)
    result1_v2 = sol2.ladderLength(beginWord1, endWord1, wordList1)
    
    print(f"a-z approach:       {result1}")
    print(f"WordList approach:  {result1_v2}")
    print(f"Expected: 5")
    assert result1 == 5
    assert result1_v2 == 5
    print("PASSED!\n")
    
    
    # TEST 2: No path exists
    print("=" * 50)
    print("TEST 2: hit -> cog (no 'cog' in wordList)")
    print("=" * 50)
    
    beginWord2 = "hit"
    endWord2 = "cog"
    wordList2 = ["hot", "dot", "dog", "lot", "log"]  # No "cog"!
    
    result2 = sol.ladderLength(beginWord2, endWord2, wordList2)
    result2_v2 = sol2.ladderLength(beginWord2, endWord2, wordList2)
    
    print(f"a-z approach:       {result2}")
    print(f"WordList approach:  {result2_v2}")
    print(f"Expected: 0")
    assert result2 == 0
    assert result2_v2 == 0
    print("PASSED!\n")
    
    
    # TEST 3: Direct transformation
    print("=" * 50)
    print("TEST 3: hit -> hot (direct)")
    print("=" * 50)
    
    beginWord3 = "hit"
    endWord3 = "hot"
    wordList3 = ["hot"]
    
    result3 = sol.ladderLength(beginWord3, endWord3, wordList3)
    result3_v2 = sol2.ladderLength(beginWord3, endWord3, wordList3)
    
    print(f"a-z approach:       {result3}")
    print(f"WordList approach:  {result3_v2}")
    print(f"Expected: 2")
    assert result3 == 2
    assert result3_v2 == 2
    print("PASSED!\n")
    
    
    # TEST 4: Same word
    print("=" * 50)
    print("TEST 4: Same begin and end (but end not in list)")
    print("=" * 50)
    
    beginWord4 = "hit"
    endWord4 = "hit"
    wordList4 = ["hot"]
    
    result4 = sol.ladderLength(beginWord4, endWord4, wordList4)
    
    print(f"Result: {result4}")
    print(f"Expected: 0 (endWord not in wordList)")
    assert result4 == 0
    print("PASSED!\n")
    
    
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
