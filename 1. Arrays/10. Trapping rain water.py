class Solution:
    def trap(self, height: List[int]) -> int:
        left_max = right_max = total = 0
        l=0
        r=len(height)-1

        while l<r:
            if height[l]<=height[r]:
                if left_max > height[l]:
                    total +=left_max - height[l]
                else:
                    left_max = height[l]
                l+=1
            else:
                if right_max >= height[r]:
                    total+=right_max - height[r]
                else:
                    right_max = height[r]
                r-=1

        return total

                

