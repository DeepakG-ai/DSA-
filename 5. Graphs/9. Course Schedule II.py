"""
Course Schedule II (LeetCode 210)
https://leetcode.com/problems/course-schedule-ii/

===========================================
PROBLEM
===========================================
There are numCourses courses (0 to numCourses-1).
Prerequisites given as [course, prerequisite].

Return the ORDER in which to take courses.
If impossible (cycle exists), return empty array [].

===========================================
KEY INSIGHT
===========================================

This is EXACTLY "Topological Sort"!

    - If valid order exists → return topological order
    - If cycle exists      → return []

Using Kahn's Algorithm (BFS):
    Topological Sort:  return result
    Course Schedule II: return result if len(result) == V else []

===========================================
"""

from collections import deque


def findOrder(numCourses: int, prerequisites: list) -> list:
    """
    Return the order to take courses (Topological Sort).
    
    LOGIC: Standard Kahn's Algorithm, return result or [] if cycle.
    
    Time: O(V + E)
    Space: O(V + E)
    """
    # Build adjacency list (prereq → course)
    adj = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Start with courses having no prerequisites
    queue = deque()
    for i in range(numCourses):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []  # This will be our course order
    
    while queue:
        course = queue.popleft()
        result.append(course)  # Take this course!
        
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # If we got all courses → return order
    # If not all courses → cycle exists → return []
    return result if len(result) == numCourses else []


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    
    # TEST 1: Simple order
    # 0 → 1 (Take 0 first, then 1)
    print("TEST 1: 2 courses, [1,0]")
    result = findOrder(2, [[1, 0]])
    print(f"Order: {result}")  # [0, 1]
    assert result == [0, 1]
    print("PASSED!\n")
    
    
    # TEST 2: Complex valid order
    #    0
    #   / \
    #  v   v
    #  1   2
    #   \ /
    #    v
    #    3
    print("TEST 2: 4 courses, complex DAG")
    result = findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    print(f"Order: {result}")
    # Valid orders: [0,1,2,3] or [0,2,1,3]
    assert len(result) == 4
    assert result[0] == 0  # 0 must be first
    assert result[-1] == 3  # 3 must be last
    print("PASSED!\n")
    
    
    # TEST 3: Cycle - impossible
    print("TEST 3: Cycle [1,0], [0,1]")
    result = findOrder(2, [[1, 0], [0, 1]])
    print(f"Order: {result}")  # []
    assert result == []
    print("PASSED!\n")
    
    
    # TEST 4: No prerequisites (all independent)
    print("TEST 4: No prerequisites")
    result = findOrder(3, [])
    print(f"Order: {result}")  # Any order, e.g., [0, 1, 2]
    assert len(result) == 3
    print("PASSED!\n")
    
    
    # TEST 5: Single course
    print("TEST 5: Single course")
    result = findOrder(1, [])
    print(f"Order: {result}")  # [0]
    assert result == [0]
    print("PASSED!\n")
    
    
    # TEST 6: Longer chain
    # 0 → 1 → 2 → 3
    print("TEST 6: Chain 0->1->2->3")
    result = findOrder(4, [[1, 0], [2, 1], [3, 2]])
    print(f"Order: {result}")  # Expected: [0, 1, 2, 3]
    assert result == [0, 1, 2, 3]
    print("PASSED!\n")
    
    
    print("=" * 40)
    print("ALL TESTS PASSED!")
    print("=" * 40)
