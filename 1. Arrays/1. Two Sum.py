# Two sum problem - 01

def TwoSum(arr, target):
    seen = {}
    for i, num in enumerate(arr):
        diff = target - num
        if diff in seen:
            return seen[diff], i
        seen[num] = i
    return -1

print(TwoSum([2, 5, 7, 9], 7))

"""def TwoSum(arr,target):
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            sum = arr[i]+arr[j]
            if sum==target:
                return i,j
        return -1

TwoSum([2,5,7,9],7)"""
