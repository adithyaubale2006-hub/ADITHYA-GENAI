l = "leetcode"
freq = {}

for i in l:
  freq[i] = freq.get(i, 0)+1
  
for i in l:
  if freq[i] == 1:
    print(i)
    break


#if you wnat to print the index(Leetcode)
for idx in range(len(l)):
    if freq[l[idx]] == 1:
        print(idx)
        break