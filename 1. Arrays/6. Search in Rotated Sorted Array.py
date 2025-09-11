class Solution:
    def search(self, nums: List[int], target: int) -> int:
       for i in range(len(nums)):
            if target not in nums:
                return -1
            if target == nums[i]:
                return i




class Solution:
    def search(self, nums: List[int], target: int) -> int:
        for i in range(len(nums)):
            if target == nums[i]:
                return i   
        return -1
            
