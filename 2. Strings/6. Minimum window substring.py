class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t:
            return ""

        # Step 1: Build frequency map of t
        need = {}
        for c in t:
            need[c] = need.get(c, 0) + 1

        window = {}
        have, need_count = 0, len(need)
        min_len, index = float("inf"), [-1, -1]

        l = 0
        #"ADOBECODEBANC"
        for i in range(len(s)):
            # Step 2: expand window
            if s[i] in need:
                window[s[i]] = window.get(s[i], 0) + 1
                if window[s[i]] == need[s[i]]:
                    have += 1

            print(f"i={i}, s[i]={s[i]}, window={window}, have={have}")

            # Step 3: shrink window when valid
            while have == need_count:
                print(f"  Shrinking: l={l}, window={window}, min_len={min_len}")

                if (i - l + 1) < min_len:
                    min_len = i - l + 1
                    index = [l, i]
                    print(f"    Updated min_len={min_len}, index={index}")

                if s[l] in need:
                    window[s[l]] -= 1
                    if window[s[l]] < need[s[l]]:
                        have -= 1
                        print(f"    Decreased have={have} because {s[l]} count < need")
                l += 1

        l, r = index
        return s[l:r+1] if min_len != float("inf") else ""

# Create object
sol = Solution()

# Test example
s = "ADOBECODEBANC"
t = "ABC"
result = sol.minWindow(s, t)
print("\nFinal Result:", result)


