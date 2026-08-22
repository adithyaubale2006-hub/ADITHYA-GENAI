#Method 1
def Move(nums):
    j = 0
    
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[j], nums[i] = nums[i], nums[j]
            j+=1
    return nums  
            
nums = [5, 2, 0, 0, 88, 0, 10]
print(Move(nums))

#Method 2
nums = [3, 0, 2, 5, 0, 0, 1]
if len(nums) == 1:
    return

i = 0
while i < len(nums):
    if nums[i] == 0:
        break
    i += 1

if i == len(nums):
    return

j = i + 1

while j < len(nums):
    if nums[j] != 0:
        nums[i], nums[j] = nums[j], nums[i]
        i += 1
    j += 1
