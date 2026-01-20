# Debug: Show how Alien Dictionary stores data

from collections import defaultdict

words = ["baa", "abcd", "abca", "cab", "cad"]

print("=" * 50)
print("STEP 1: Initialize")
print("=" * 50)

# Adjacency list
adj = defaultdict(set)
print(f"adj (empty): {dict(adj)}")

# In-degree dictionary
in_degree = {}
for word in words:
    for char in word:
        in_degree[char] = 0

print(f"in_degree: {in_degree}")

print("\n" + "=" * 50)
print("STEP 2: Build edges from word pairs")
print("=" * 50)

for i in range(len(words) - 1):
    s1 = words[i]
    s2 = words[i + 1]
    
    print(f"\nComparing: '{s1}' vs '{s2}'")
    
    min_len = min(len(s1), len(s2))
    
    for j in range(min_len):
        if s1[j] != s2[j]:
            print(f"  First difference at index {j}: '{s1[j]}' vs '{s2[j]}'")
            print(f"  -> Edge: '{s1[j]}' -> '{s2[j]}' (meaning '{s1[j]}' comes BEFORE '{s2[j]}')")
            
            if s2[j] not in adj[s1[j]]:
                adj[s1[j]].add(s2[j])
                in_degree[s2[j]] += 1
            break
        else:
            print(f"  Index {j}: '{s1[j]}' == '{s2[j]}' (same, continue...)")

print("\n" + "=" * 50)
print("FINAL DATA STRUCTURES")
print("=" * 50)

print("\nAdjacency List (who comes before whom):")
for char in adj:
    print(f"  '{char}' -> {list(adj[char])}")

print("\nIn-degree (how many chars come before this):")
for char in in_degree:
    print(f"  '{char}': {in_degree[char]}")

print("\n" + "=" * 50)
print("STEP 3: Topological Sort (Kahn's)")
print("=" * 50)

from collections import deque

queue = deque()
for char in in_degree:
    if in_degree[char] == 0:
        queue.append(char)

print(f"\nStarting queue (in-degree = 0): {list(queue)}")

result = []
while queue:
    char = queue.popleft()
    result.append(char)
    print(f"\nPopped '{char}' -> result so far: {result}")
    
    for neighbor in adj[char]:
        in_degree[neighbor] -= 1
        print(f"  Decreased in_degree['{neighbor}'] to {in_degree[neighbor]}")
        
        if in_degree[neighbor] == 0:
            queue.append(neighbor)
            print(f"  Added '{neighbor}' to queue")

print("\n" + "=" * 50)
print(f"FINAL ORDER: {''.join(result)}")
print("=" * 50)
