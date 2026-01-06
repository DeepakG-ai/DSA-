# Graph Fundamentals - Complete Interview Guide

> **From Zero to MAANG-Ready**
> 
> This guide covers everything you need to know about graphs for technical interviews.

---

## Table of Contents

1. [What is a Graph?](#1-what-is-a-graph)
2. [Graph Terminology](#2-graph-terminology)
3. [Types of Graphs](#3-types-of-graphs)
4. [Graph Representations](#4-graph-representations)
5. [Graph Traversals (BFS & DFS)](#5-graph-traversals)
6. [Common Graph Algorithms](#6-common-graph-algorithms)
7. [Pattern Recognition for Interviews](#7-pattern-recognition)
8. [Python Code Templates](#8-python-code-templates)
9. [Interview Tips](#9-interview-tips)

---

## 1. What is a Graph?

### Definition
A **graph** is a data structure consisting of:
- **Vertices (Nodes)**: The entities/objects
- **Edges**: Connections between vertices

### Real-World Examples

| Example | Vertices | Edges |
|---------|----------|-------|
| Social Network | Users | Friendships |
| Maps/Roads | Cities | Roads |
| Web Pages | Pages | Hyperlinks |
| Computer Network | Computers | Cables |
| WhatsApp | Users | Contacts |
| LinkedIn | Professionals | Connections |

### Graph vs Tree

| Aspect | Tree | Graph |
|--------|------|-------|
| Cycles | No cycles allowed | Cycles allowed |
| Root | Has a root node | No root concept |
| Parent | Each node has 1 parent | No parent concept |
| Hierarchy | Hierarchical | Non-hierarchical |
| Edges | n-1 edges for n nodes | Any number of edges |

> **Key Insight**: A tree is a special type of graph (connected, acyclic graph).

### Visual Representation

```
TREE:                   GRAPH:
    1                   A --- B
   / \                  |   / |
  2   3                 |  /  |
 / \                    C --- D
4   5                   
                        (Has cycle: A-B-D-C-A)
```

---

## 2. Graph Terminology

### Basic Terms

| Term | Definition | Example |
|------|------------|---------|
| **Vertex (Node)** | A point in the graph | User in social network |
| **Edge** | Connection between two vertices | Friendship |
| **Adjacent** | Two vertices connected by an edge | A and B if edge (A,B) exists |
| **Neighbor** | All vertices connected to a vertex | Friends of a user |
| **Degree** | Number of edges connected to a vertex | Number of friends |
| **Path** | Sequence of vertices connected by edges | Route from A to B |
| **Cycle** | Path that starts and ends at same vertex | A→B→C→A |
| **Connected** | Path exists between all vertex pairs | All users can reach each other |
| **Component** | Maximal connected subgraph | Isolated friend groups |

### Degree in Directed Graphs

```
    A → B → C
    ↓   ↓
    D   E

In-degree of B = 1 (one incoming edge from A)
Out-degree of B = 2 (edges to C and E)
Total degree of B = 3
```

| Vertex | In-Degree | Out-Degree |
|--------|-----------|------------|
| A | 0 | 2 |
| B | 1 | 2 |
| C | 1 | 0 |
| D | 1 | 0 |
| E | 1 | 0 |

### Path vs Walk vs Trail

```
Graph: A - B - C - D
           |   |
           E - F

Walk: A → B → C → B → E (can repeat vertices/edges)
Trail: A → B → C → F → E → B (can repeat vertices, NOT edges)
Path: A → B → C → D (no repetition)
Simple Path: A → B → E → F → C → D (no repetition, visits all possible)
```

---

## 3. Types of Graphs

### 3.1 Directed vs Undirected

```
UNDIRECTED:              DIRECTED:
A --- B                  A → B
|     |                  ↓   ↓
C --- D                  C ← D

Edge (A,B) = Edge (B,A)  Edge A→B ≠ Edge B→A
```

| Type | Edge Notation | Real Example |
|------|---------------|--------------|
| Undirected | (A, B) = (B, A) | Facebook friend |
| Directed | A → B ≠ B → A | Twitter follow |

### 3.2 Weighted vs Unweighted

```
UNWEIGHTED:              WEIGHTED:
A --- B                  A --5-- B
|     |                  |       |
C --- D                  3       7
                         |       |
                         C --2-- D

All edges equal          Edges have different costs
```

| Type | Use Case |
|------|----------|
| Unweighted | Social connections, reachability |
| Weighted | Maps (distance), networks (bandwidth) |

### 3.3 Cyclic vs Acyclic

```
CYCLIC:                  ACYCLIC (DAG):
A → B                    A → B
↑   ↓                        ↓
D ← C                    C → D

Has cycle: A→B→C→D→A     No cycles (Directed Acyclic Graph)
```

> **DAG (Directed Acyclic Graph)**: Very important for interviews!
> - Used in: Task scheduling, dependency resolution, topological sort

### 3.4 Connected vs Disconnected

```
CONNECTED:               DISCONNECTED:
A - B - C                A - B    D - E
|       |                |        |
D - E - F                C        F

One component            Two components
```

### 3.5 Complete Graph

Every vertex is connected to every other vertex.

```
Complete Graph K4:
    A
   /|\
  B-+-C
   \|/
    D

Edges = n(n-1)/2 = 4(3)/2 = 6 edges
```

### 3.6 Bipartite Graph

Vertices can be divided into two sets where edges only connect vertices from different sets.

```
Set 1: {A, B, C}
Set 2: {1, 2, 3}

A----1
 \  /
  \/
  /\
 /  \
B----2
 \  /
  \/
  /\
 /  \
C----3

No edges within same set!
```

> **Interview Tip**: A graph is bipartite if and only if it has no odd-length cycles.

### Summary Table

| Property | Interview Frequency | Key Algorithm |
|----------|--------------------| --------------|
| Directed | Very High | BFS, DFS |
| Weighted | High | Dijkstra, Bellman-Ford |
| DAG | High | Topological Sort |
| Cyclic | High | Cycle Detection |
| Bipartite | Medium | Graph Coloring |

---

## 4. Graph Representations

### 4.1 Edge List

Simply a list of all edges.

```python
# Directed graph edges: [(from, to), ...]
edges = [
    (0, 1), (1, 2), (0, 3),
    (3, 4), (3, 6), (3, 7),
    (4, 2), (4, 5), (5, 2)
]

# Weighted edges: [(from, to, weight), ...]
weighted_edges = [
    ('A', 'B', 5),
    ('A', 'C', 3),
    ('B', 'D', 7)
]
```

| Pros | Cons |
|------|------|
| Simple to implement | Slow to check if edge exists: O(E) |
| Easy to iterate all edges | Slow to find neighbors: O(E) |
| Good for edge-centric algorithms | Not good for vertex-centric |

**Best for**: Kruskal's algorithm, when you only need to iterate edges.

### 4.2 Adjacency Matrix

2D array where `matrix[i][j] = 1` if edge exists from i to j.

```python
# For graph: 0→1, 1→2, 0→3
#     0  1  2  3
# 0 [[0, 1, 0, 1],
# 1  [0, 0, 1, 0],
# 2  [0, 0, 0, 0],
# 3  [0, 0, 0, 0]]

def create_adjacency_matrix(n, edges):
    matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        matrix[u][v] = 1
        # For undirected: matrix[v][u] = 1
    return matrix
```

| Pros | Cons |
|------|------|
| O(1) edge lookup | O(n²) space even for sparse graphs |
| Simple implementation | O(n) to find all neighbors |
| Good for dense graphs | Wasteful for sparse graphs |

**Best for**: Dense graphs, when you need O(1) edge existence check.

### 4.3 Adjacency List ⭐ (Most Common in Interviews)

Each vertex stores a list of its neighbors.

```python
from collections import defaultdict

def create_adjacency_list(edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        # For undirected: graph[v].append(u)
    return graph

# Result for edges [(0,1), (0,3), (1,2), (3,4)]
# {
#     0: [1, 3],
#     1: [2],
#     3: [4]
# }
```

| Pros | Cons |
|------|------|
| O(degree) to find neighbors | O(degree) edge lookup |
| Space efficient: O(V + E) | Not constant time edge check |
| Good for sparse graphs | - |

**Best for**: Most interview problems! Default choice.

### 4.4 Comparison Table

| Operation | Edge List | Adj Matrix | Adj List |
|-----------|-----------|------------|----------|
| Space | O(E) | O(V²) | O(V + E) |
| Add Edge | O(1) | O(1) | O(1) |
| Remove Edge | O(E) | O(1) | O(degree) |
| Edge Exists? | O(E) | O(1) | O(degree) |
| Find Neighbors | O(E) | O(V) | O(degree) |
| Iterate All Edges | O(E) | O(V²) | O(V + E) |

> **Interview Default**: Use **Adjacency List** unless told otherwise!

### 4.5 Building Graph from Problem Input

LeetCode typically gives edges as:
```python
# Format 1: List of edges
edges = [[0,1], [1,2], [2,0]]

# Format 2: Number of nodes + edges
n = 3
edges = [[0,1], [1,2], [2,0]]

# Your standard template:
from collections import defaultdict

def build_graph(n, edges, directed=False):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph
```

---

## 5. Graph Traversals

### 5.1 BFS (Breadth-First Search)

**Explore level by level** - visit all neighbors before going deeper.

```
       A
      /|\
     B C D
    /|   |
   E F   G

BFS from A: A → B → C → D → E → F → G
Level 0: A
Level 1: B, C, D
Level 2: E, F, G
```

#### BFS Template

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result
```

#### BFS with Level Tracking

```python
def bfs_levels(graph, start):
    visited = set()
    queue = deque([(start, 0)])  # (node, level)
    visited.add(start)
    
    while queue:
        node, level = queue.popleft()
        print(f"Node {node} at level {level}")
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))
```

#### When to Use BFS

| Problem Type | Why BFS? |
|--------------|----------|
| Shortest path (unweighted) | Finds shortest path first |
| Level order traversal | Natural level tracking |
| Nearest neighbor | Explores closest first |
| Connected components | Visits all connected nodes |
| Bipartite check | Level-based coloring |

> **Key Insight**: BFS finds the **shortest path** in unweighted graphs!

### 5.2 DFS (Depth-First Search)

**Go as deep as possible** before backtracking.

```
       A
      /|\
     B C D
    /|   |
   E F   G

DFS from A: A → B → E → F → C → D → G
(Goes deep first: A→B→E, backtrack, B→F, backtrack...)
```

#### DFS Template (Recursive)

```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(node)
    result = [node]
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            result.extend(dfs(graph, neighbor, visited))
    
    return result
```

#### DFS Template (Iterative with Stack)

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            
            # Add neighbors in reverse for correct order
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result
```

#### When to Use DFS

| Problem Type | Why DFS? |
|--------------|----------|
| Path finding | Explores complete paths |
| Cycle detection | Can track back edges |
| Topological sort | Natural ordering |
| Connected components | Visits all connected |
| Maze solving | Explores all paths |
| Backtracking | Try all possibilities |

### 5.3 BFS vs DFS Comparison

| Aspect | BFS | DFS |
|--------|-----|-----|
| Data Structure | Queue (FIFO) | Stack (LIFO) / Recursion |
| Space | O(width) | O(height) |
| Shortest Path | ✅ Yes (unweighted) | ❌ No |
| Complete | ✅ Yes | ✅ Yes |
| Use When | Shortest path, levels | Paths, cycles, backtrack |

### 5.4 Traversal Visualization

```
Graph:
    1 --- 2
    |     |
    3 --- 4 --- 5

BFS from 1:
  Queue: [1] → [2,3] → [3,4] → [4] → [5]
  Visit: 1 → 2 → 3 → 4 → 5

DFS from 1:
  Stack: [1] → [2,3] → [4,3] → [5,3] → [3] → []
  Visit: 1 → 2 → 4 → 5 → 3
```

---

## 6. Common Graph Algorithms

### 6.1 Cycle Detection

#### Undirected Graph (DFS)

```python
def has_cycle_undirected(graph, n):
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:  # Back edge found!
                return True
        return False
    
    # Check all components
    for i in range(n):
        if i not in visited:
            if dfs(i, -1):
                return True
    return False
```

#### Directed Graph (Colors: White/Gray/Black)

```python
def has_cycle_directed(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    
    def dfs(node):
        color[node] = GRAY  # Currently exploring
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:  # Back edge!
                return True
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True
        color[node] = BLACK  # Finished
        return False
    
    for i in range(n):
        if color[i] == WHITE:
            if dfs(i):
                return True
    return False
```

> **Interview Tip**: For directed graphs, use 3 colors (White=unvisited, Gray=in-progress, Black=done).

### 6.2 Topological Sort

Order nodes so that for every edge u→v, u comes before v.

**Only possible for DAG (Directed Acyclic Graph)!**

```
        5 → 0 ← 4
        ↓       ↓
        2 → 3 → 1

Topological Order: 4 → 5 → 0 → 2 → 3 → 1
(or: 5 → 4 → 0 → 2 → 3 → 1, etc.)
```

#### Kahn's Algorithm (BFS)

```python
from collections import deque

def topological_sort_bfs(graph, n):
    in_degree = [0] * n
    
    # Calculate in-degrees
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
    
    # Start with nodes having in-degree 0
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we processed all nodes, no cycle exists
    return result if len(result) == n else []  # Empty = has cycle
```

#### DFS Approach (Reverse Post-order)

```python
def topological_sort_dfs(graph, n):
    visited = set()
    stack = []
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)  # Add after all descendants
    
    for i in range(n):
        if i not in visited:
            dfs(i)
    
    return stack[::-1]  # Reverse the stack
```

**Use Cases**:
- Course prerequisites
- Build systems (Makefile)
- Task scheduling
- Package dependency resolution

### 6.3 Shortest Path Algorithms

#### Dijkstra's Algorithm (Weighted, Non-negative)

```python
import heapq

def dijkstra(graph, start, n):
    distances = [float('inf')] * n
    distances[start] = 0
    
    # Min heap: (distance, node)
    heap = [(0, start)]
    
    while heap:
        dist, node = heapq.heappop(heap)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    return distances
```

**Time Complexity**: O((V + E) log V) with binary heap

#### BFS for Unweighted Graphs

```python
def shortest_path_bfs(graph, start, end):
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        node, path = queue.popleft()
        
        if node == end:
            return path
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []  # No path found
```

### 6.4 Union-Find (Disjoint Set Union)

For managing connected components efficiently.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already connected
        
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**Use Cases**:
- Number of connected components
- Cycle detection (undirected)
- Kruskal's MST algorithm
- Account merge problems

### 6.5 Connected Components

A **connected component** is a maximal set of vertices where every vertex is reachable from every other vertex in that set.

#### Visual Example: 4 Connected Components

```
Component 1:  1 ─── 2       Component 2:  5
              │     │                    / \
              │     │                   6 ─ 7
              3 ─── 4

Component 3:  8             Component 4:  10 (alone)
              │
              9
```

#### Key Insight: All Components in ONE Data Structure

**They're NOT connected to each other by edges!** But they're stored in **ONE dictionary**:

```python
# ONE dictionary holds ALL components
graph = {
    # Component 1
    1: [2, 3],
    2: [1, 4],
    3: [1, 4],
    4: [2, 3],
    # Component 2
    5: [6, 7],
    6: [5, 7],
    7: [5, 6],
    # Component 3
    8: [9],
    9: [8],
    # Component 4
    10: []  # Isolated node - no neighbors
}
```

> **Note**: The adjacency list (dictionary) is itself an object that stores lists.
> So technically, graph uses **object (dict) + lists** stored in one data structure.
> The "nodes" are just integer labels, not separate Node objects.

#### Counting Connected Components (BFS/DFS)

```python
from collections import defaultdict, deque

def count_components(n, edges):
    """Count the number of connected components in an undirected graph."""
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = [False] * (n + 1)
    count = 0
    
    def bfs(start):
        queue = deque([start])
        visited[start] = True
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
    
    # Loop through ALL nodes
    for node in range(1, n + 1):
        if not visited[node]:
            count += 1       # Found a new component!
            bfs(node)        # Mark all nodes in this component
    
    return count

# Example usage
edges = [(1,2), (1,3), (2,4), (3,4), (5,6), (5,7), (6,7), (8,9)]
n = 10
print(count_components(n, edges))  # Output: 4
```

#### Why This Works

1. **Loop through ALL nodes** (1 to n)
2. If a node is **unvisited**, it's a **new component** → increment count
3. **BFS/DFS marks all reachable nodes** from that starting point
4. Nodes in **other components** remain unvisited until we reach them in the loop
5. Isolated nodes (like node 10) form their own component

#### Comparison: Tree vs Graph Node Storage

| Aspect | Tree / Linked List | Graph (Adjacency List) |
|--------|-------------------|------------------------|
| Node | Object with data + pointers | Just a number/label |
| Edge | Pointer stored inside object | Entry in adjacency list |
| Storage | Objects scattered in memory | One dict/array holds all |
| Disconnected parts | Cannot have | ✅ Multiple components in ONE structure |

### 6.6 Algorithm Selection Guide

| Problem | Algorithm | Time |
|---------|-----------|------|
| Shortest path (unweighted) | BFS | O(V + E) |
| Shortest path (weighted, positive) | Dijkstra | O((V+E) log V) |
| Shortest path (weighted, negative) | Bellman-Ford | O(VE) |
| Shortest path (all pairs) | Floyd-Warshall | O(V³) |
| Cycle detection | DFS | O(V + E) |
| Topological sort | Kahn's / DFS | O(V + E) |
| Connected components | BFS/DFS/Union-Find | O(V + E) |
| MST | Kruskal's / Prim's | O(E log V) |
| Bipartite check | BFS/DFS coloring | O(V + E) |

---

## 7. Pattern Recognition for Interviews

### Pattern 1: Grid as Graph

Many matrix problems are graph problems in disguise!

```python
# 4 directions
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# 8 directions (including diagonals)
directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

def bfs_grid(grid, start_row, start_col):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([(start_row, start_col)])
    visited.add((start_row, start_col))
    
    while queue:
        r, c = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) not in visited and grid[nr][nc] == 1:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
```

**Grid Problems (Graph in Disguise)**:
- Number of Islands
- Flood Fill
- Rotting Oranges
- Shortest Path in Binary Matrix
- Word Search

### Pattern 2: Clone Graph

Deep copy a graph - need to handle cycles!

```python
def cloneGraph(node):
    if not node:
        return None
    
    visited = {}
    
    def dfs(node):
        if node in visited:
            return visited[node]
        
        clone = Node(node.val)
        visited[node] = clone
        
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)
```

### Pattern 3: Course Schedule (Topological Sort)

```python
# Can finish all courses?
# courses = [[1,0]] means course 1 requires course 0

def canFinish(numCourses, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    completed = 0
    
    while queue:
        course = queue.popleft()
        completed += 1
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return completed == numCourses
```

### Pattern 4: Connected Components

```python
def countComponents(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set()
    count = 0
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
    
    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1
    
    return count
```

### Pattern 5: Bipartite Check

```python
def isBipartite(graph):
    n = len(graph)
    color = [-1] * n
    
    def bfs(start):
        queue = deque([start])
        color[start] = 0
        
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
        return True
    
    for i in range(n):
        if color[i] == -1:
            if not bfs(i):
                return False
    return True
```

---

## 8. Python Code Templates

### Complete Graph Class

```python
from collections import defaultdict, deque

class Graph:
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u, v, weight=1):
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))
    
    def bfs(self, start):
        visited = set([start])
        queue = deque([start])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result
    
    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        
        visited.add(start)
        result = [start]
        
        for neighbor, _ in self.graph[start]:
            if neighbor not in visited:
                result.extend(self.dfs(neighbor, visited))
        return result
    
    def has_cycle(self):
        WHITE, GRAY, BLACK = 0, 1, 2
        color = defaultdict(int)
        
        def dfs(node):
            color[node] = GRAY
            for neighbor, _ in self.graph[node]:
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE and dfs(neighbor):
                    return True
            color[node] = BLACK
            return False
        
        return any(dfs(node) for node in self.graph if color[node] == WHITE)
```

### Quick Templates for Interviews

```python
# 1. Build graph from edges
def build_graph(edges, directed=False):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph

# 2. BFS shortest path
def shortest_path(graph, start, end):
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1

# 3. DFS all paths
def all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    
    paths = []
    for neighbor in graph[start]:
        if neighbor not in path:
            paths.extend(all_paths(graph, neighbor, end, path))
    return paths

# 4. Connected components
def count_components(n, edges):
    graph = build_graph(edges)
    visited = set()
    count = 0
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
    
    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1
    return count
```

---

## 9. Interview Tips

### ⭐ The 5-Step Approach

1. **Clarify the problem**
   - Directed or undirected?
   - Weighted or unweighted?
   - Are there cycles?
   - Can there be disconnected components?

2. **Identify the graph type**
   - Is it given as a graph or disguised (matrix, string)?
   - How is input provided (adjacency list, edge list)?

3. **Choose the right algorithm**
   - BFS for shortest path (unweighted)
   - DFS for paths, cycles, backtracking
   - Topological sort for ordering with dependencies
   - Union-Find for component problems

4. **Consider edge cases**
   - Empty graph
   - Single node
   - Disconnected components
   - Cycles
   - Self-loops

5. **Optimize**
   - Use visited set to avoid repeating work
   - Consider space vs time tradeoffs
   - Early termination when possible

### Common Mistakes to Avoid

| Mistake | Solution |
|---------|----------|
| Forgetting visited set | Always track visited nodes! |
| Not handling disconnected graphs | Loop through all nodes to start DFS/BFS |
| Wrong direction in directed graph | Check if u→v or v→u |
| Using adjacency matrix for sparse graphs | Use adjacency list |
| Infinite loop in cyclic graphs | Use visited set |
| Not considering negative weights | Use Bellman-Ford instead of Dijkstra |

### Complexity Quick Reference

| Algorithm | Time | Space |
|-----------|------|-------|
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |
| Dijkstra (heap) | O((V+E) log V) | O(V) |
| Bellman-Ford | O(VE) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Topological Sort | O(V + E) | O(V) |
| Union-Find | O(α(n)) ≈ O(1) | O(V) |

### MAANG-Specific Tips

1. **Amazon**: Loves connected components, shortest path
2. **Google**: Graph traversals, topological sort
3. **Meta**: Grid problems (islands, regions)
4. **Microsoft**: BFS/DFS basics, cycle detection
5. **Apple**: Shortest path, graph representation

---

## Summary: Graph Problem Checklist

Before solving any graph problem, ask yourself:

- [ ] What are the vertices? What are the edges?
- [ ] Is it directed or undirected?
- [ ] Is it weighted or unweighted?
- [ ] Can it have cycles?
- [ ] Is it connected or could it be disconnected?
- [ ] How is the input given? (edge list, adj list, matrix)
- [ ] What am I finding? (path, component, order, distance)
- [ ] BFS or DFS? (BFS for shortest, DFS for all paths/backtracking)

> **Remember**: When in doubt, start with BFS or DFS. Most graph problems boil down to these!

---

*Happy Coding! 🚀*
