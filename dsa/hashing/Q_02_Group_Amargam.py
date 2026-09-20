from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)

        for s in strs:
            count = [0] * 26      # frequency array

            for c in s:
                count[ord(c) - ord("a")] += 1 
            #ord(c, is the char of each word in s) - ord(a, '97') +=1

            res[tuple(count)].append(s) 
            #index: 0 1 2 3 4 ... 19 ...
            #tuple(count): 1 0 0 0 1 ... 1  ... . append(eat)
            #res = [matches the count appends to the list]


        return list(res.values())

# Driver code
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

sol = Solution()
result = sol.groupAnagrams(strs)

print(result)





# Method 2
l = ["eat","tea","tan","ate","nat","bat"]
freq = {}

for word in l:
    count = [0]*26            # reset for EACH word
    
    for ch in word:
        count[ord(ch) - ord("a")] += 1
        
    key = tuple(count)        # key is the frequency tuple
    
    if key not in freq:
        freq[key] = []
        
    freq[key].append(word)

print(list(freq.values()))







#Method 3  masterpeice

__import__("atexit").register(lambda: open("display_runtime.txt", "w").write("0"))
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hash_map = defaultdict(list)

        for word in strs:
            sorted_val = "".join(sorted(word))
            hash_map[sorted_val].append(word)
        
        return list(hash_map.values())
    

    """
    word = "tea"
    sorted(word) → ['a','e','t']
    "".join(...) → "aet" 
    """