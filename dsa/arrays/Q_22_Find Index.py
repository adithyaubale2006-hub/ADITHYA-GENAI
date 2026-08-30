#User function Template for python3

class Solution:
    def findIndex (self,arr, key ):
        first=-1
        last=-1
        
        for i in range(len(arr)):
            if arr[i] == key:
                if first == -1:
                    first = i
                last = i
                    
        return [first, last]