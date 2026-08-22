#Rotate a array from right
nums = [12, 1, 11, 34, 2]
n = len(nums)
temp = nums[n-1]
for i in range(n-2, -1, -1):
    nums[i+1] = nums[i]


nums[0] = temp
print(nums)