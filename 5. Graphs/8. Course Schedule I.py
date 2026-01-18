"""
Course Schedule I (LeetCode 207)
https://leetcode.com/problems/course-schedule/

===========================================
PROBLEM
===========================================
There are numCourses courses (0 to numCourses-1).
Prerequisites given as [course, prerequisite].
    Example: [1, 0] means "to take course 1, you must first take course 0"

Return TRUE if you can finish all courses, FALSE otherwise.

===========================================
KEY INSIGHT
===========================================

This is EXACTLY "Detect Cycle in Directed Graph" with INVERTED return!

    - If NO cycle  → Can finish all courses  → return TRUE
    - If cycle     → Stuck in dependencies   → return FALSE

Using Kahn's Algorithm (BFS):
    - Detect Cycle:     return count != V  (True if cycle)
    - Course Schedule:  return count == V  (True if NO cycle)

===========================================
BUILDING THE GRAPH
===========================================

prerequisites = [[1,0], [2,0], [3,1], [3,2]]

[course, prereq] means: prereq → course (prereq must come first!)

So we build: adj[prereq].append(course)

       0
      / \
     v   v
     1   2
      \ /
       v
       3

===========================================
"""

from collections import deque


def canFinish(numCourses: int, prerequisites: list) -> bool:
    """
    Can we finish all courses? (Is the graph cycle-free?)
    
    LOGIC: Same as Detect Cycle, just return opposite!
           count == V means no cycle, so return True.
    
    Time: O(V + E)
    Space: O(V + E)
    """
    # Build adjacency list (prereq → course)
    adj = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)  # prereq → course
        in_degree[course] += 1
    
    # Start with courses having no prerequisites (in-degree = 0)
    queue = deque()
    for i in range(numCourses):
        if in_degree[i] == 0:
            queue.append(i)
    
    count = 0  # Count of courses we can complete
    
    while queue:
        course = queue.popleft()
        count += 1
        
        # "Complete" this course - reduce in-degree of dependent courses
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # If we completed all courses → No cycle → return True
    # Detect Cycle: return count != V
    # Course Sched: return count == V  ← Opposite!
    return count == numCourses


# ============================================
# TEST CASES
# ============================================

if __name__ == "__main__":
    
    # TEST 1: Can finish (no cycle)
    # 0 → 1
    print("TEST 1: [1,0] - Course 1 needs Course 0")
    result = canFinish(2, [[1, 0]])
    print(f"Can finish? {result}")  # True
    assert result == True
    print("PASSED!\n")
    
    
    # TEST 2: Cannot finish (cycle)
    # 0 → 1 → 0 (cycle!)
    print("TEST 2: [1,0], [0,1] - Mutual dependency (cycle)")
    result = canFinish(2, [[1, 0], [0, 1]])
    print(f"Can finish? {result}")  # False
    assert result == False
    print("PASSED!\n")
    
    
    # TEST 3: Complex graph, no cycle
    #    0
    #   / \
    #  v   v
    #  1   2
    #   \ /
    #    v
    #    3
    print("TEST 3: Complex DAG")
    result = canFinish(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    print(f"Can finish? {result}")  # True
    assert result == True
    print("PASSED!\n")
    
    
    # TEST 4: No prerequisites
    print("TEST 4: No prerequisites")
    result = canFinish(3, [])
    print(f"Can finish? {result}")  # True (all independent)
    assert result == True
    print("PASSED!\n")
    
    
    # TEST 5: Single course
    print("TEST 5: Single course")
    result = canFinish(1, [])
    print(f"Can finish? {result}")  # True
    assert result == True
    print("PASSED!\n")
    
    
    # TEST 6: Longer cycle
    # 0 → 1 → 2 → 0 (cycle)
    print("TEST 6: Longer cycle (0->1->2->0)")
    result = canFinish(3, [[1, 0], [2, 1], [0, 2]])
    print(f"Can finish? {result}")  # False
    assert result == False
    print("PASSED!\n")
    
    
    print("=" * 40)
    print("ALL TESTS PASSED!")
    print("=" * 40)
