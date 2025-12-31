n=8
A =[[0,1],[1,2],[0,3],[3,4],[3,6],[3,7],[4,2],[4,5],[5,2]]

#Adjacency Matirx
M=[]
#M=[[0]*n for _ in range(n)]
for i in range(n):
    M.append([0]*n)


#M=[] it creates {list: 8} [[0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

for u,v in A:
    M[u][v]=1
"""    M[0][1] = 1
        ↑  ↑
        │  └── 1 = Column (destination node(to))
        └───── 0 = Row (source node (from))"""
"""A = [[0,1], [1,2], [0,3], ...]
M[0] = connections FROM node 0
M[1] = connections FROM node 1
M[2] = connections FROM node 2
...
M[7] = connections FROM node 7"""
# Edge [0, 1] → M[0][1] = 1
#   Row 0 (node 0), Column 1 → node 0 connects to node 1

# Edge [1, 2] → M[1][2] = 1  
#   Row 1 (node 1), Column 2 → node 1 connects to node 2

# Edge [0, 3] → M[0][3] = 1
#   Row 0 (node 0), Column 3 → node 0 connects to node 3
print(M)

"""
Visual Matrix Output:
         Column:  0  1  2  3  4  5  6  7
                  
Row 0 (Node 0):  [0, 1, 0, 1, 0, 0, 0, 0]  ← Node 0 → 1, 3
Row 1 (Node 1):  [0, 0, 1, 0, 0, 0, 0, 0]  ← Node 1 → 2
Row 2 (Node 2):  [0, 0, 0, 0, 0, 0, 0, 0]  ← Node 2 → nothing
Row 3 (Node 3):  [0, 0, 0, 0, 1, 0, 1, 1]  ← Node 3 → 4, 6, 7
Row 4 (Node 4):  [0, 0, 1, 0, 0, 1, 0, 0]  ← Node 4 → 2, 5
Row 5 (Node 5):  [0, 0, 1, 0, 0, 0, 0, 0]  ← Node 5 → 2
Row 6 (Node 6):  [0, 0, 0, 0, 0, 0, 0, 0]  ← Node 6 → nothing
Row 7 (Node 7):  [0, 0, 0, 0, 0, 0, 0, 0]  ← Node 7 → nothing

M[row][col] = 1 means: edge from row → col
"""

# ============================================
# ADJACENCY LIST - 3 Different Ways
# ============================================

# Method 1: Using defaultdict (cleanest)
from collections import defaultdict

graph1 = defaultdict(list)
for u, v in A:
    graph1[u].append(v)
    # graph1[v].append(u)  # Uncomment for undirected graph

print("\n--- Method 1: defaultdict ---")
print(dict(graph1))
# Output: {0: [1, 3], 1: [2], 3: [4, 6, 7], 4: [2, 5], 5: [2]}


# Method 2: Using regular dict (manual check)
graph2 = {}
for u, v in A:
    if u not in graph2:
        graph2[u] = []      # Must manually create empty list!
    graph2[u].append(v)

print("\n--- Method 2: regular dict ---")
print(graph2)
# Output: {0: [1, 3], 1: [2], 3: [4, 6, 7], 4: [2, 5], 5: [2]}


# Method 3: Without any library (using list of lists)
# Need to know number of nodes beforehand!
graph3 = [[] for _ in range(n)]  # Creates n empty lists
for u, v in A:
    graph3[u].append(v)

print("\n--- Method 3: list of lists (no library) ---")
print(graph3)
# Output: [[1, 3], [2], [], [4, 6, 7], [2, 5], [2], [], []]
#          node0  node1 node2  node3    node4  node5 node6 node7

"""
Comparison:
| Method          | Pros                      | Cons                           |
|-----------------|---------------------------|--------------------------------|
| defaultdict     | Clean, auto-creates list  | Needs import                   |
| regular dict    | No import needed          | Verbose (if check every time)  |
| list of lists   | No import, fast access    | Must know n beforehand         |

For interviews: defaultdict is preferred!
"""
