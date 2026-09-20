class Solution:
    def topKFrequent(self, nums, k):
        count = {}
        freq = [[] for i in range(len(nums) + 1)]

# Step 1: Count frequency
        for n in nums:
            count[n] = 1 + count.get(n, 0)

# Step 2: Put numbers into buckets based on frequency 
# n  is the Number, c is the Frequency
        for n, c in count.items():
            freq[c].append(n)

# Step 3: Collect top k frequent elements
        res = []
        for i in range(len(freq) - 1, 0, -1):
            for n in freq[i]:
                res.append(n)
                if len(res) == k:
                    return res
# Driver code
nums = [1, 1, 1, 2, 2, 3]
k = 2

sol = Solution()
result = sol.topKFrequent(nums, k)
print(result)
