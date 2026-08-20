#largest element in the arrays
nums = [10, 23, 45, 32, 69]
largest = nums[0]
n = len(nums)
for i in range(0, n):
    largest = max(largest, nums[i])

print(largest)

#PRATICE 2
num = [23, 45, 67, 89, 12]
large = num[0]
x = len(num)
for i in range(0, x):
    large = max(large, num[i])
print(large)

