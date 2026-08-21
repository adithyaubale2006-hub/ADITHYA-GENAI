#Remove Duplicates from the arr
nums = [11, 11, 22, 11, 23, 12]
n = len(nums)
freq_map = {}
for i in range(0, n):
    freq_map[nums[i]] = 0

j = 0
for k in freq_map:
    nums[j] = k
    j+=1
print(j) 

#method 2
"""
if not nums:
    return 0
i = 0

for j in range(1, len(nums)):
    nums[j] != nums[i]
    i+=1
    nums[i] = nums[j]

return i+1
"""