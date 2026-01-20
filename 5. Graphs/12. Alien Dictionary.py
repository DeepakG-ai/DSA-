"""
Alien Dictionary (LeetCode 269 / GFG)
https://leetcode.com/problems/alien-dictionary/

===========================================
PROBLEM
===========================================
There is a new alien language that uses the English alphabet.
The order among letters is unknown.

Given a list of words from the alien dictionary SORTED in lexicographical order,
derive the order of letters in this language.

===========================================
WORKFLOW
===========================================

1. Build adjacency list and in-degree:
   - For loop: compare adjacent words (s1 = words[i], s2 = words[i+1])
   - Find FIRST different character
   - Add edge: s1[j] → s2[j] (s1[j] comes before s2[j])
   - Only compare up to min(len(s1), len(s2))

2. Edge Case - INVALID:
   - If s1 is longer than s2 AND s1 starts with s2
   - Example: ["abc", "ab"] → INVALID (prefix should come first)

3. Topological Sort (Kahn's BFS):
   - Start with all nodes with in-degree = 0
   - Process queue, decrement in-degree of neighbors
   - If result length != number of unique chars → CYCLE (invalid)

===========================================
"""

from collections import deque, defaultdict


def alienOrder(words: list) -> str:
    """
    Find order of characters in alien language.
    
    Args:
        words: List of words sorted in alien dictionary order
    
    Returns:
        String of characters in correct order, or "" if invalid
    
    Time: O(C) where C = total characters in all words
    Space: O(1) or O(26) for alphabet
    """
    # Step 1: Initialize graph
    # adj[char] = list of characters that come AFTER char
    adj = defaultdict(set)
    
    # in_degree[char] = count of characters that come BEFORE char
    in_degree = {char: 0 for word in words for char in word}


    """in_degree = {}

       for word in words:
           for char in word:
               in_degree[char] = 0
               
    adj = {
        'b': ['d', 'a'],   # b comes before d and a
        'd': ['a'],        # d comes before a
        'a': ['c']         # a comes before c
    }

    in_degree = {
        'b': 0,   # Nothing before b → START HERE
        'a': 2,   # b and d both before a
        'c': 1,   # a before c
        'd': 1    # b before d
    }

"""
    
    # Step 2: Build edges from adjacent word pairs
    for i in range(len(words) - 1):
        s1 = words[i]
        s2 = words[i + 1]
        
        # Compare up to min length
        min_len = min(len(s1), len(s2))
        
        # Edge Case: s1 is longer AND s1 starts with s2 → INVALID
        if len(s1) > len(s2) and s1[:min_len] == s2[:min_len]:
            return ""
        
        # Find first different character
        for j in range(min_len):
            if s1[j] != s2[j]:
                # s1[j] comes before s2[j]
                # Add edge only if not already added
                if s2[j] not in adj[s1[j]]:
                    adj[s1[j]].add(s2[j])
                    in_degree[s2[j]] += 1
                break  # Only first difference matters!
    
    # Step 3: Topological Sort (Kahn's Algorithm)
    queue = deque()
    
    # Start with all chars having in-degree 0
    for char in in_degree:
        if in_degree[char] == 0:  # 99 - 97 = 2
            queue.append(char)
    
    result = []
    
    while queue:
        char = queue.popleft()
        result.append(char)
        
        for neighbor in adj[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Step 4: Check for cycle
    # If we couldn't process all characters → cycle exists → invalid
    if len(result) != len(in_degree):
        return ""
    
    return "".join(result)


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    
    # TEST 1: Basic example
    # From "wrt", "wrf" → t comes before f
    # From "wrf", "er" → w comes before e
    # From "er", "ett" → r comes before t
    # From "ett", "rftt" → e comes before r
    # Order: w -> e -> r -> t -> f
    words1 = ["wrt", "wrf", "er", "ett", "rftt"]
    result1 = alienOrder(words1)
    print(f"TEST 1: {result1}")
    assert result1 == "wertf", f"Expected 'wertf', got '{result1}'"
    print("TEST 1 PASSED: wertf\n")
    
    
    # TEST 2: Simple two words
    # "z" comes before "x"
    words2 = ["z", "x"]
    result2 = alienOrder(words2)
    print(f"TEST 2: {result2}")
    assert result2 == "zx", f"Expected 'zx', got '{result2}'"
    print("TEST 2 PASSED: zx\n")
    
    
    # TEST 3: Same prefix, longer first → INVALID
    words3 = ["abc", "ab"]
    result3 = alienOrder(words3)
    print(f"TEST 3: {result3}")
    assert result3 == "", f"Expected '', got '{result3}'"
    print("TEST 3 PASSED: '' (invalid - prefix rule)\n")
    
    
    # TEST 4: Single word
    words4 = ["abc"]
    result4 = alienOrder(words4)
    print(f"TEST 4: {result4}")
    # Any order of a, b, c is valid since no constraints
    assert set(result4) == {'a', 'b', 'c'}
    print("TEST 4 PASSED: Single word (any order of abc)\n")
    
    
    # TEST 5: Cycle detection
    # z → x → z creates a cycle
    words5 = ["z", "x", "z"]
    result5 = alienOrder(words5)
    print(f"TEST 5: {result5}")
    assert result5 == "", f"Expected '', got '{result5}'"
    print("TEST 5 PASSED: '' (cycle detected)\n")
    
    
    print("=" * 40)
    print("ALL 5 TESTS PASSED!")
    print("=" * 40)
