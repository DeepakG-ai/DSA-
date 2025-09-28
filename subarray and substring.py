# generate_subarrays_substrings.py

def generate_subarrays_for_loop(arr):
    print("Subarrays using for loop:")
    for i in range(len(arr)):
        for j in range(i, len(arr)):
            subarray = arr[i:j+1]
            print(subarray)
    print("\n")
    # Expected Output:
    # [1]
    # [1, 2]
    # [1, 2, 3]
    # [2]
    # [2, 3]
    # [3]


def generate_subarrays_while_loop(arr):
    print("Subarrays using while loop:")
    i = 0
    while i < len(arr):
        j = i
        while j < len(arr):
            subarray = []
            k = i
            while k <= j:
                subarray.append(arr[k])
                k += 1
            print(subarray)
            j += 1
        i += 1
    print("\n")
    # Expected Output (same as for loop):
    # [1]
    # [1, 2]
    # [1, 2, 3]
    # [2]
    # [2, 3]
    # [3]


def generate_substrings_for_loop(s):
    print("Substrings using for loop:")
    for i in range(len(s)):
        for j in range(i, len(s)):
            substring = s[i:j+1]
            print(substring)
    print("\n")
    # Expected Output:
    # a
    # ab
    # abc
    # b
    # bc
    # c


def generate_substrings_while_loop(s):
    print("Substrings using while loop:")
    i = 0
    while i < len(s):
        j = i
        while j < len(s):
            substring = ""
            k = i
            while k <= j:
                substring += s[k]
                k += 1
            print(substring)
            j += 1
        i += 1
    print("\n")
    # Expected Output (same as for loop):
    # a
    # ab
    # abc
    # b
    # bc
    # c


if __name__ == "__main__":
    arr = [1, 2, 3]
    s = "abc"

    # Subarrays
    generate_subarrays_for_loop(arr)
    generate_subarrays_while_loop(arr)

    # Substrings
    generate_substrings_for_loop(s)
    generate_substrings_while_loop(s)
