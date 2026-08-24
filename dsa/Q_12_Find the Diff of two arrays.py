class Solution:
    def findDifference(nums1, nums2):
        set1 = set(nums1)
        set2 = set(nums2)

        
        return [list(set1-set2), list(set2-set1)]
    
    nums1 = [1,2,2,3,3]
    nums2 = [1,2,2,2]
    print(findDifference(nums1, nums2))