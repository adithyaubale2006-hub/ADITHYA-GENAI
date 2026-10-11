l = [7,7,8,9,9]
freq = {}

for i in l:
  freq[i] = freq.get(i, 0)+1 
  
for i in l:
  if freq[i] == 1:
    print(i)
