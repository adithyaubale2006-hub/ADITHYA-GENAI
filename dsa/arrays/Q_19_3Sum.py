#Brute Force 
def Three_Sum(nums):
    n = len(nums)
    my_set = set()
    for i in range(0, n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if nums[i]+nums[j]+nums[k] == 0:
                    temp = [nums[i], nums[j], nums[k]]
                    temp.sort()
                    my_set.add(tuple(temp))

    return [list(ans) for ans in my_set]

nums = [-1, 0, 1, 2, -1, -4]
print(Three_Sum(nums))


#Better Solution
def Three_Sum(nums):
    res = set()
    for i in range(0, len(nums)):
        my_set = set()
        for j in range(i+1, len(nums)):
            third = -(nums[i]+nums[j])
            if third in my_set:
                temp =[nums[i], nums[j], third]
                temp.sort()
                res.add(tuple(temp))
            my_set.add(nums[j])
        
    return [list(ans) for ans in res]

nums = [-1, 0, 1, 2, -1, -4]
print(Three_Sum(nums))

#We Got tle Error


#Chat gpt best approach

def threeSum(nums):
        nums.sort()
        res = []
        n = len(nums)

        for i in range(n):
            if i > 0 and nums[i] == nums[i - 1]:
                continue  # skip duplicate first elements

            left, right = i + 1, n - 1

            while left < right:
                s = nums[i] + nums[left] + nums[right]

                if s == 0:
                    res.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1

                    # skip duplicates
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1

                elif s < 0:
                    left += 1
                else:
                    right -= 1

        return res
nums = [-1, 0, 1, 2, -1, -4]
print(threeSum(nums))