grid1 = [
        ['1', '1', '1', '1', '0'],
        ['1', '1', '0', '1', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '0', '0', '0']
    ]
print(grid1)
print(len(grid1))  
print(grid1[0])
print(len(grid1[0]))   
n = len(grid1)
m = len(grid1[0])
vis = [[0] * m for _ in range(n)]
print(vis)
count = 0


def dfs(row, col):
    print(f"  -> Visiting ({row}, {col})... Marking vis[{row}][{col}] = 1")
    vis[row][col] = 1 
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Names for clarity in output
    dir_names = {(-1,0):"UP", (1,0):"DOWN", (0,-1):"LEFT", (0,1):"RIGHT"}
    
    for dr, dc in directions: 
        nrow = row + dr  
        ncol = col + dc
        d_name = dir_names[(dr,dc)]
        
        print(f"    Checking {d_name} from ({row},{col}) -> Target: ({nrow},{ncol})")
        
        # Check bounds
        if 0 <= nrow < n and 0 <= ncol < m:
            if grid1[nrow][ncol] == '1' and not vis[nrow][ncol]:
                print(f"\n VALID LAND! Going deeper to ({nrow},{ncol})")
                dfs(nrow, ncol)
            elif vis[nrow][ncol]:
                 print(f" \n Already visited. Skipping.")
            else:
                 print(f"\n Water ('0'). Skipping.")
        else:
            print(f" \n Out of bounds. Skipping.")

print("\n--- STARTING MAIN LOOP ---")
for row in range(n):
    for col in range(m):
        if grid1[row][col] == '1' and not vis[row][col]:
            print(f"\n[NEW ISLAND FOUND] at ({row}, {col}). Starting DFS...")
            count += 1
            dfs(row, col)
        elif grid1[row][col] == '0':
            pass # print(f"Skipping water at ({row},{col})")
        else:
            pass # print(f"Skipping visited land at ({row},{col})")

print(f"\nTotal Islands: {count}")
