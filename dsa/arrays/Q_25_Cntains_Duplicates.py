from typing import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        hash_map = {}
        for i in nums:
            hash_map[i] = hash_map.get(i, 0)+1

        for i , v in hash_map.items():
            if v > 1:
                return True

        return False

        #ONE LINE CODE
        #return len(set(nums)) < len(nums)

# Driver code to test the solution
if __name__ == "__main__":
    solution = Solution()
    
    # Test case 1
    nums1 = [1, 2, 3, 1]
    print(f"Test case 1: {solution.containsDuplicate(nums1)}")  # Expected: True
    
    # Test case 2
    nums2 = [1, 2, 3, 4]
    print(f"Test case 2: {solution.containsDuplicate(nums2)}")  # Expected: False
    
    # Test case 3
    nums3 = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
    print(f"Test case 3: {solution.containsDuplicate(nums3)}")  # Expected: True