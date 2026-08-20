#Find the second largest
nums = [12, 13, 45, 32, 56]
largest = float("-inf")
second_large = float("-inf")
n = len(nums)
for i in range(0, n):
    #prints the largest element 56
    largest = max(largest, nums[i]) # max(-Inf, nums[0]12)

for i in range(0, n):
    #prints the second Largest element
    if nums[i]>second_large and nums[i]!=largest:
        second_large = nums[i]
print(second_large)
