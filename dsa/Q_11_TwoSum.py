#Brute Force Sol
nums = [5,9,1,2,4,15,6,3]
target = 13

for i in range(0, len(nums)):
  for j in range(i, len(nums)):
    if nums[i]+nums[j] == target:
      print([i, j])

#Better Sol
nums = [5,9,1,2,4,15,6,3]
target = 13

freq_map = {}

for i in range(len(nums)):
    remain = target - nums[i]

    if remain in freq_map:
        print(nums[i], remain) # values
        print([freq_map[remain], i])  # indices
        break

#IF 15 ITS NUMS[15] = 5
    freq_map[nums[i]] = i
