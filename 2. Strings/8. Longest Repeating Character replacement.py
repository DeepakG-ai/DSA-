class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        l = 0
        max_freq = 0
        max_len = 0

        for r in range(len(s)):
            # 1. expand window
            count[s[r]] = count.get(s[r], 0) + 1
            max_freq = max(max_freq, count[s[r]])

            # 2. shrink window if invalid
            while (r - l + 1) - max_freq > k:
                count[s[l]] -= 1
                l += 1

            # 3. update result
            max_len = max(max_len, r - l + 1)

        return max_len
