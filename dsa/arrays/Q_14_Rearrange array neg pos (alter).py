def Rearrange(nums):
    n = len(nums)
    res = [0]*n
    pos, neg = 0, 1
    for i in range(0, n):
        if nums[i]>=0:
            res[pos]= nums[i]
            pos+=2
        else:
            res[neg]= nums[i]
            neg+=2
    return res

nums= [4,5,7,-3,-2,-8]
print(Rearrange(nums))
