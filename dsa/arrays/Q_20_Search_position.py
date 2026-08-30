class Solution:
    def searchInsert(self, nums, target) -> int:
        for i in range(len(nums)):
            if nums[i] >= target:
                return i
                
        return len(nums)



# --- Driver Code ---
if __name__ == "__main__":
    # Initialize the solution class
    sol = Solution()
    
    # Test cases from the problem description
    test_cases = [
        {"nums": [1, 3, 5, 6], "target": 5, "expected": 2},
        {"nums": [1, 3, 5, 6], "target": 2, "expected": 1},
        {"nums": [1, 3, 5, 6], "target": 7, "expected": 4},
    ]
    
    # Run the test cases
    for i, tc in enumerate(test_cases, 1):
        nums = tc["nums"]
        target = tc["target"]
        expected = tc["expected"]
        
        result = sol.searchInsert(nums, target)
        
        print(f"Test Case {i}:")
        print(f"  Input: nums = {nums}, target = {target}")
        print(f"  Output: {result}")
        print(f"  Expected: {expected}")
        print(f"  Result: {'✅ Passed' if result == expected else '❌ Failed'}\n")