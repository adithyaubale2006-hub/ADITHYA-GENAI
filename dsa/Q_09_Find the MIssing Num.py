nums = [1, 0, 3, 4]
freq_map = {}

# Initialize all values from 0 to len(nums)
for i in range(len(nums) + 1):
    freq_map[i] = 0

# Mark present numbers
for num in nums:
    freq_map[num] = 1

# Find missing number
for k, v in freq_map.items():
    if v == 0:
        print(k)
