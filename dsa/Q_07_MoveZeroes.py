def Move(nums):
    j = 0
    
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[j], nums[i] = nums[i], nums[j]
            j+=1
    return nums  
            
nums = [5, 2, 0, 0, 88, 0, 10]
print(Move(nums))