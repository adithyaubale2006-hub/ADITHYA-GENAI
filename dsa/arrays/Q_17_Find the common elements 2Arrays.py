#BEST OPTIMAL SOLUTION(Return Indices)
def findIntersectionValues(nums1, nums2):
        set1 = set(nums1)
        set2 = set(nums2)

        answer1 = 0
        answer2 = 0

        for x in nums1:
            if x in set2:
                answer1 += 1

        for x in nums2:
            if x in set1:
                answer2 += 1

        return [answer1, answer2]

nums1 = [2,3,2]
nums2 = [1,2]
print(findIntersectionValues(nums1, nums2))


#This was my Solution 
def findIntersectionValues(nums1, nums2):
    hash1 = {}
    hash2 = {}

    count1, count2= 0, 0

    for i in nums1:
        hash1[i] = hash1.get(i, 0)+1
    for j in nums2:
        hash2[j] = hash2.get(j, 0)+1


    for i in nums1:
        if i in hash2:
            count1+=1
    for j in nums2:
        if j in hash1:
            count2+=1
    return [count1, count2]
nums1 = [2,3,2,4]
nums2 = [1,2,4]
print(findIntersectionValues(nums1, nums2))
        