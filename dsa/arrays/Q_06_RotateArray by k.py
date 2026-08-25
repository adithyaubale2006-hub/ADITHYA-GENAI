#Rotate an array by K places
nums = [1, 2, 4, 5, 6]
x = int(input())
for i in range(0, x):
    e = nums.pop()
    nums.insert(0, e)

print(nums)

def Rev(nums, left, right):
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


nums = [3, 6, 7, 9, 4, 5]
k = 2
n = len(nums)

k = k % n   # handles cases when k > length

# Step 1: Reverse entire array
Rev(nums, 0, n-1)

# Step 2: Reverse first k elements
Rev(nums, 0, k-1)

# Step 3: Reverse remaining elements
Rev(nums, k, n-1)

print(nums)


#Method 3: Using slicing
nums = [3, 6, 7, 9, 4, 5]
k = 2
n = len(nums)
k = k % n
nums[:] = nums[-k:] + nums[:-k]
print(nums)
