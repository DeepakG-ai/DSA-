"""
Word Ladder II (LeetCode 126)
https://leetcode.com/problems/word-ladder-ii/

===========================================
PROBLEM
===========================================
Given beginWord, endWord, and wordList.
Find ALL the shortest transformation sequences from beginWord to endWord.

Return empty list if no transformation exists.

===========================================
KEY DIFFERENCES FROM WORD LADDER I
===========================================

Word Ladder I:  Return LENGTH of shortest path
Word Ladder II: Return ALL SHORTEST PATHS

Changes needed:
1. Track the PATH, not just visited
2. Store ALL paths that reach endWord at shortest level
3. Don't remove word from set immediately (multiple paths may use same word at same level)

===========================================
ALGORITHM
===========================================

1. BFS to find shortest paths
2. Instead of storing just word, store (word, path_so_far)
3. Key insight: Remove words from wordSet only AFTER processing entire level
   (Multiple paths at same level can use same word)

4. When we find endWord, add path to result and continue 
   (to find other paths at same level)

===========================================
"""

from typing import List
from collections import deque


class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        wordSet = set(wordList)
        
        # Edge case
        if endWord not in wordSet:
            return []
        
        result = []
        
        # BFS: queue stores (current_word, path_to_current_word)
        queue = deque([(beginWord, [beginWord])])
        
        # Track words used at current level (remove AFTER level completes)
        visited_this_level = set()
        
        found = False  # Flag to stop after finding shortest level
        
        while queue and not found:
            # Process entire level
            level_size = len(queue)
            
            # Words to remove after this level
            words_to_remove = set()
            
            for _ in range(level_size):
                word, path = queue.popleft()
                
                # Try changing each position
                for i in range(len(word)):
                    for c in 'abcdefghijklmnopqrstuvwxyz':
                        if c == word[i]:
                            continue
                        
                        new_word = word[:i] + c + word[i+1:]
                        
                        if new_word in wordSet:
                            new_path = path + [new_word]
                            
                            # Found endWord!
                            if new_word == endWord:
                                result.append(new_path)
                                found = True  # Mark to stop after this level
                            else:
                                # Add to queue for next level
                                queue.append((new_word, new_path))
                                words_to_remove.add(new_word)
            
            # Remove used words AFTER processing entire level
            wordSet -= words_to_remove
        
        return result


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    sol = Solution()
    
    # TEST 1: LeetCode Example 1
    print("=" * 50)
    print("TEST 1: hit -> cog (multiple paths)")
    print("=" * 50)
    
    beginWord1 = "hit"
    endWord1 = "cog"
    wordList1 = ["hot", "dot", "dog", "lot", "log", "cog"]
    
    result = sol.findLadders(beginWord1, endWord1, wordList1)
    print(f"Paths found: {len(result)}")
    for path in result:
        print(f"  {' -> '.join(path)}")
    
    # Two paths of length 5:
    # hit -> hot -> dot -> dog -> cog
    # hit -> hot -> lot -> log -> cog
    assert len(result) == 2
    assert len(result[0]) == 5
    print("PASSED!\n")
    
    
    # TEST 2: No path
    print("=" * 50)
    print("TEST 2: No path exists")
    print("=" * 50)
    
    beginWord2 = "hit"
    endWord2 = "cog"
    wordList2 = ["hot", "dot", "dog", "lot", "log"]  # No "cog"
    
    result = sol.findLadders(beginWord2, endWord2, wordList2)
    print(f"Paths found: {result}")
    assert result == []
    print("PASSED!\n")
    
    
    # TEST 3: Direct path
    print("=" * 50)
    print("TEST 3: Direct transformation")
    print("=" * 50)
    
    beginWord3 = "hit"
    endWord3 = "hot"
    wordList3 = ["hot"]
    
    result = sol.findLadders(beginWord3, endWord3, wordList3)
    print(f"Paths: {result}")
    assert result == [["hit", "hot"]]
    print("PASSED!\n")
    
    
    # TEST 4: Multiple same-length paths
    print("=" * 50)
    print("TEST 4: red -> tax")
    print("=" * 50)
    
    beginWord4 = "red"
    endWord4 = "tax"
    wordList4 = ["ted", "tex", "red", "tax", "tad", "den", "rex", "pee"]
    
    result = sol.findLadders(beginWord4, endWord4, wordList4)
    print(f"Paths found: {len(result)}")
    for path in result:
        print(f"  {' -> '.join(path)}")
    print("PASSED!\n")
    
    
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
