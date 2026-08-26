#Longest Consequtive Sequence
#Brute force
def Lcs(nums):
    n = len(nums)
    max_count = 0
    for i in range(0, n):
        num = nums[i]
        count = 1
        while num+1 in nums:
            count+=1
            num = num+1
        max_count= max(max_count, count)
    return max_count

nums = [1, 99, 101, 98, 2, 5, 3, 100]
print(Lcs(nums))

#Better 
def lcs(nums):
    nums.sort()
    n = len(nums)
    count = 0
    last_small = float("-inf")
    longest = 0

    for i in range(0, n):
        num = nums[i]
        if num-1 == last_small:
            count+=1
            last_small = num
        elif num!=last_small:
            count=1
            last_small=num
        
        longest = max(longest, count)
    return longest

nums=[1,99,101,98,2,5,3,100]
print(lcs(nums))

#Optimal 
def lCs(nums):
    num_set = set(nums)
    longest = 0

    for num in num_set:
        # only start counting if num is the start of a sequence
        if num - 1 not in num_set:
            current = num
            count = 1

            while current + 1 in num_set:
                current += 1
                count += 1

                longest = max(longest, count)

    return longest

nums=[1,99,101,98,2,5,3,100]
print(lCs(nums))