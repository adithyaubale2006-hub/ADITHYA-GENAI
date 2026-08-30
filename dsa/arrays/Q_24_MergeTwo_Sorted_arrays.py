class Solution:
    def findUnion(self, a, b):
        n = len(a)
        m = len(b)
        result = []
        i, j = 0, 0
        
        
        while i < n and j < m:
            if a[i] <= b[j]:
                if len(result) == 0 or result[-1] != a[i]:
                    result.append(a[i])
                i+=1
            else:
                if len(result) == 0 or result[-1] != b[j]:
                    result.append(b[j])
                j+=1
                
        while i < n:
            if len(result) == 0 or result[-1] != a[i]:
                    result.append(a[i])
            i+=1
        while j < m:
            if len(result) == 0 or result[-1] != b[j]:
                    result.append(b[j])
            j+=1
                
        
        return result
            
                
if __name__ == '__main__':
    # Read the number of test cases
        a = [1, 2, 2, 3, 5]
        b = [2, 3, 4, 5]
        ob = Solution()
        ans = ob.findUnion(a, b)
        print(*ans)