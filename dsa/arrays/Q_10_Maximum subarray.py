#Most Optimal solution (leetcode)
def maxSubArray(nums):
    cs=0
    gs=float ("-inf")
    for p in nums:
        cs=cs+p
        if(cs>gs):
            gs=cs
        if(cs<0):
            cs=0
    return gs
nums = [-2,1,-3,4,-1,2,1,-5,4]
maxSubArray(nums)
    

#2nd Most Optimal
def maxSubArray(nums):
    n = len(nums)
    maxi = float("-inf")
    total = 0
    for i in range(0, n):
        total = total+nums[i]
        maxi = max(maxi, total)

        if total < 0:
            total = 0
    return maxi

nums = [1, -1, 5, -2, 3]
print(maxSubArray(nums))