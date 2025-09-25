def longest_subarray_sum_leq_k(arr, k):
    l = 0
    cursum = 0
    max_len = 0

    for r in range(len(arr)):
        cursum += arr[r]

        # Shrink window while sum > k  it is not validated. while cursum<k: it is validated in sliding window

     # In sliding window, expand the right pointer and shrink the left pointer. not for every problem 
        while cursum > k and l <= r:
            cursum -= arr[l]
            l += 1

        # Update max length
        max_len = max(max_len, r - l + 1)

    return max_len


# Example
arr = [1, 2, 3, 4, 2]
k = 7
print(longest_subarray_sum_leq_k(arr, k))  # Output: 3 ([1,2,3] or [3,4])
