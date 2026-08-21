#Sort an Array
def SortArr(nums):
    n = len(nums)
    for i in range(0, n-1):
        if nums[i] >= nums[i+1]:
            return False
        return True 
        
nums = [10, 11, 23, 43, 12]
SortArr(nums)