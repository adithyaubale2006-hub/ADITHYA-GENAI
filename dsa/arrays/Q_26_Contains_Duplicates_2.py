from typing import List

class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        hash_map = {}
        for i in range(len(nums)):
            # number in hash_map and index-hash_map_index less Than k
            if nums[i] in hash_map and (i - hash_map[nums[i]]) <= k:
                return True

            hash_map[nums[i]] = i
        return False

# Driver code to test the solution
if __name__ == "__main__":
    solution = Solution()
    
    # Test case 1
    nums1 = [1, 2, 3, 1]
    k1 = 3
    print(f"Test case 1: {solution.containsNearbyDuplicate(nums1, k1)}")  # Expected: True
    
    # Test case 2
    nums2 = [1, 0, 1, 1]
    k2 = 1
    print(f"Test case 2: {solution.containsNearbyDuplicate(nums2, k2)}")  # Expected: True
    
    # Test case 3
    nums3 = [1, 2, 3, 1, 2, 3]
    k3 = 2
    print(f"Test case 3: {solution.containsNearbyDuplicate(nums3, k3)}")  # Expected: False